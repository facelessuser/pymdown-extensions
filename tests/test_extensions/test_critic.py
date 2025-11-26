"""Test caret."""
from .. import util
import pytest


class TestCriticViewMode(util.MdCase):
    """Test view mode."""

    extension = [
        'pymdownx.critic'
    ]
    extension_configs = {
        "pymdownx.critic": {
            "mode": 'view'
        }
    }

    @pytest.mark.filterwarnings("ignore")
    def test_view(self):
        """Test view mode."""

        self.check_markdown(
            R"""
            Here is some {--*incorrect*--} Markdown.  I am adding this{++ here.++}.  Here is some more {--text
            that I am removing--}text.  And here is even more {++text that I
            am ++}adding.{~~

            ~>  ~~}Paragraph was deleted and replaced with some spaces.{~~  ~>

            ~~}Spaces were removed and a paragraph was added.

            And here is a comment on {==some
             ==text== ==}{>>This works quite well. I just wanted to comment on it.<<}. Substitutions {~~is~>are~~} great!

            General block handling.

            {--

            * test
            * test
            * test
                * test
            * test

            --}

            {++

            * test
                * test
            * test
            * test
            * test

            ++}
            """,
            """
            <p>Here is some <del class="critic"><em>incorrect</em></del> Markdown.  I am adding this<ins class="critic"> here.</ins>.  Here is some more <del class="critic">text
            that I am removing</del>text.  And here is even more <ins class="critic">text that I
            am </ins>adding.<del class="critic break">&nbsp;</del><ins class="critic">  </ins>Paragraph was deleted and replaced with some spaces.<del class="critic">  </del></p>
            <ins class="critic break">&nbsp;</ins>
            <p>Spaces were removed and a paragraph was added.</p>
            <p>And here is a comment on <mark class="critic">some
             ==text== </mark><span class="critic comment">This works quite well. I just wanted to comment on it.</span>. Substitutions <del class="critic">is</del><ins class="critic">are</ins> great!</p>
            <p>General block handling.</p>
            <del class="critic block">
            <ul>
            <li>test</li>
            <li>test</li>
            <li>test<ul>
            <li>test</li>
            </ul>
            </li>
            <li>test</li>
            </ul>
            </del>
            <ins class="critic block">
            <ul>
            <li>test<ul>
            <li>test</li>
            </ul>
            </li>
            <li>test</li>
            <li>test</li>
            <li>test</li>
            </ul>
            </ins>
            """,
            True
        )


class TestCriticAcceptMode(util.MdCase):
    """Test accept mode."""

    extension = [
        'pymdownx.critic'
    ]
    extension_configs = {
        "pymdownx.critic": {
            "mode": 'accept'
        }
    }

    def test_accept(self):
        """Test accept mode."""

        self.check_markdown(
            R"""
            Here is some {--*incorrect*--} Markdown.  I am adding this{++ here.++}.  Here is some more {--text
            that I am removing--}text.  And here is even more {++text that I
            am ++}adding.{~~

            ~>  ~~}Paragraph was deleted and replaced with some spaces.{~~  ~>

            ~~}Spaces were removed and a paragraph was added.

            And here is a comment on {==some
             ==text== ==}{>>This works quite well. I just wanted to comment on it.<<}. Substitutions {~~is~>are~~} great!

            General block handling.

            {--

            * test
            * test
            * test
                * test
            * test

            --}

            {++

            * test
                * test
            * test
            * test
            * test

            ++}
            """,
            """
            <p>Here is some  Markdown.  I am adding this here..  Here is some more text.  And here is even more text that I
            am adding.  Paragraph was deleted and replaced with some spaces.</p>
            <p>Spaces were removed and a paragraph was added.</p>
            <p>And here is a comment on some
             ==text== . Substitutions are great!</p>
            <p>General block handling.</p>
            <ul>
            <li>test<ul>
            <li>test</li>
            </ul>
            </li>
            <li>test</li>
            <li>test</li>
            <li>test</li>
            </ul>
            """,
            True
        )


class TestCriticRejectMode(util.MdCase):
    """Test reject mode."""

    extension = [
        'pymdownx.critic'
    ]
    extension_configs = {
        "pymdownx.critic": {
            "mode": 'reject'
        }
    }

    def test_reject(self):
        """Test reject mode."""

        self.check_markdown(
            R"""
            Here is some {--*incorrect*--} Markdown.  I am adding this{++ here.++}.  Here is some more {--text
            that I am removing--}text.  And here is even more {++text that I
            am ++}adding.{~~

            ~>  ~~}Paragraph was deleted and replaced with some spaces.{~~  ~>

            ~~}Spaces were removed and a paragraph was added.

            And here is a comment on {==some
             ==text== ==}{>>This works quite well. I just wanted to comment on it.<<}. Substitutions {~~is~>are~~} great!

            General block handling.

            {--

            * test
            * test
            * test
                * test
            * test

            --}

            {++

            * test
                * test
            * test
            * test
            * test

            ++}
            """,
            """
            <p>Here is some <em>incorrect</em> Markdown.  I am adding this.  Here is some more text
            that I am removingtext.  And here is even more adding.</p>
            <p>Paragraph was deleted and replaced with some spaces.  Spaces were removed and a paragraph was added.</p>
            <p>And here is a comment on some
             ==text== . Substitutions is great!</p>
            <p>General block handling.</p>
            <ul>
            <li>test</li>
            <li>test</li>
            <li>test<ul>
            <li>test</li>
            </ul>
            </li>
            <li>test</li>
            </ul>
            """,
            True
        )


class TestCriticEscapeAll(util.MdCase):
    """Test critic with escaping."""

    extension = [
        'pymdownx.critic',
        'pymdownx.escapeall'
    ]
    extension_configs = {
        "pymdownx.critic": {
            "mode": 'view'
        }
    }

    @pytest.mark.filterwarnings("ignore")
    def test_escape(self):
        """Test with escapes."""

        self.check_markdown(
            R"""
            We shouldn't escape STX and ETX characters:

            Don't escape crtiic placeholder: \{>>comment<<}
            """,
            """
            <p>We shouldn't escape STX and ETX characters:</p>
            <p>Don't escape crtiic placeholder: <span class="critic comment">comment</span></p>
            """,
            True
        )
