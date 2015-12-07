# ProgressBar {: .doctitle}
Syntax for progress bars.

---

## Overview
ProgressBar is an extension that adds support for progress/status bars.  It can take percentages or fractions, and it can optionally generate classes for percentages at 20% levels.  It also works with Python Markdown's built in `attr_list` extension.  Though progress bars are rendered as block items, it accepts attr_list's inline format.

The basic syntax for progress bars is: `[= <percentage or fraction> "optional single or double quoted title"]`.  The opening `[` can be followed by one or more `=` characters. After the `=` char(s) the percentage is specified as either a fraction or percentage and can optionally be followed by a title surrounded in either double quotes or single quotes.

## Options
| Option    | Type | Default | Description |
|-----------|------|---------|-------------|
|level_class| bool | True | Enables or disables the level class feature.  The level class feature adds level classes in increments of 20. |
|add_classes| string | '' | This option accepts a string of classes separated by spaces. |

## Examples

```
| Test               | Result                                         |
|--------------------|------------------------------------------------|
|Animated: 0%        |[=0% "0%"]{: .candystripe-animate}              |
|Animated: 5%        |[=5% "5%"]{: .candystripe-animate}              |
|Animated: 25%       |[=25% "25%"]{: .candystripe-animate}            |
|Animated: 45%       |[=45% "45%"]{: .candystripe-animate}            |
|Animated: 65%       |[=65% "65%"]{: .candystripe-animate}            |
|Animated: 85%       |[=85% "85%"]{: .candystripe-animate}            |
|Animated: 100%      |[=100% "100%"]{: .candystripe-animate}          |
|Division Percentage |[= 212.2/537 "212.2/537 Testing division"]      |
|No Label            |[=== 50%]                                       |
|Inline              |Before[= 50% "I'm a block!"]After               |
|Animated with Gloss |[= 50% "Glossy"]{: .candystripe-animate .gloss} |
```

| Test               | Result                                         |
|--------------------|------------------------------------------------|
|Animated: 0%        |[=0% "0%"]{: .candystripe-animate}              |
|Animated: 5%        |[=5% "5%"]{: .candystripe-animate}              |
|Animated: 25%       |[=25% "25%"]{: .candystripe-animate}            |
|Animated: 45%       |[=45% "45%"]{: .candystripe-animate}            |
|Animated: 65%       |[=65% "65%"]{: .candystripe-animate}            |
|Animated: 85%       |[=85% "85%"]{: .candystripe-animate}            |
|Animated: 100%      |[=100% "100%"]{: .candystripe-animate}          |
|Division Percentage |[= 212.2/537 "212.2/537 Testing division"]      |
|No Label            |[=== 50%]                                       |
|Inline              |Before[= 50% "I'm a block!"]After               |
|Animated with Gloss |[= 50% "Glossy"]{: .candystripe-animate .gloss} |

# CSS
The general HTML structure of the progress bar is as follows:

```html
<div class="progress progress-100plus">
    <div class="progress-bar" style="width:100.00%">
        <p class="progress-label">100%</p>
    </div>
</div>
```

| Classes | Description |
|---------|-------------|
| progress | This is attached to the outer `div` container of the progress bar. |
| progress-bar | This is attached to the inner `div` whose width is adjusted to give the visual appearance of a bar at the desired percentage. |
| progress-label | This is attached to the `p` element that will contain the desired label. |
| progress-<integer\>plus | This is an optional class that indicates the percentage of the progress bar by increments of 20. |

```css
/* Progress Bars */
.markdown-body .progress {
  display: block;
  width: 300px;
  margin: 10px 0;
  height: 24px;
  -webkit-border-radius: 3px;
  -moz-border-radius: 3px;
  border-radius: 3px;
  background-color: #ededed;
  position: relative;
  box-shadow: inset -1px 1px 3px rgba(0, 0, 0, .1);
}

.markdown-body .progress-label {
  position: absolute;
  text-align: center;
  font-weight: bold;
  width: 100%; margin: 0;
  line-height: 24px !important;
  color: #333;
  text-shadow: 1px 1px 0 #fefefe, -1px -1px 0 #fefefe, -1px 1px 0 #fefefe, 1px -1px 0 #fefefe, 0 1px 0 #fefefe, 0 -1px 0 #fefefe, 1px 0 0 #fefefe, -1px 0 0 #fefefe, 1px 1px 2px #000;
  -webkit-font-smoothing: antialiased !important;
  white-space: nowrap;
  overflow: hidden;
}

.markdown-body .progress-bar {
  height: 24px;
  float: left;
  -webkit-border-radius: 3px;
  -moz-border-radius: 3px;
  border-radius: 3px;
  background-color: #96c6d7;
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, .5), inset 0 -1px 0 rgba(0, 0, 0, .1);
  background-size: 30px 30px;
  background-image: -webkit-linear-gradient(
    135deg, rgba(255, 255, 255, .4) 27%,
    transparent 27%,
    transparent 52%, rgba(255, 255, 255, .4) 52%,
    rgba(255, 255, 255, .4) 77%,
    transparent 77%, transparent
  );
  background-image: -moz-linear-gradient(
    135deg,
    rgba(255, 255, 255, .4) 27%, transparent 27%,
    transparent 52%, rgba(255, 255, 255, .4) 52%,
    rgba(255, 255, 255, .4) 77%, transparent 77%,
    transparent
  );
  background-image: -ms-linear-gradient(
    135deg,
    rgba(255, 255, 255, .4) 27%, transparent 27%,
    transparent 52%, rgba(255, 255, 255, .4) 52%,
    rgba(255, 255, 255, .4) 77%, transparent 77%,
    transparent
  );
  background-image: -o-linear-gradient(
    135deg,
    rgba(255, 255, 255, .4) 27%, transparent 27%,
    transparent 52%, rgba(255, 255, 255, .4) 52%,
    rgba(255, 255, 255, .4) 77%, transparent 77%,
    transparent
  );
  background-image: linear-gradient(
    135deg,
    rgba(255, 255, 255, .4) 27%, transparent 27%,
    transparent 52%, rgba(255, 255, 255, .4) 52%,
    rgba(255, 255, 255, .4) 77%, transparent 77%,
    transparent
  );
}

.markdown-body .progress-100plus .progress-bar {
  background-color: #a6d796;
}

.markdown-body .progress-80plus .progress-bar {
  background-color: #c6d796;
}

.markdown-body .progress-60plus .progress-bar {
  background-color: #d7c896;
}

.markdown-body .progress-40plus .progress-bar {
  background-color: #d7a796;
}

.markdown-body .progress-20plus .progress-bar {
  background-color: #d796a6;
}

.markdown-body .progress-0plus .progress-bar {
  background-color: #c25f77;
}

.markdown-body .candystripe-animate .progress-bar{
  -webkit-animation: animate-stripes 3s linear infinite;
  -moz-animation: animate-stripes 3s linear infinite;
  animation: animate-stripes 3s linear infinite;
}

@-webkit-keyframes animate-stripes {
  0% {
    background-position: 0 0;
  }

  100% {
    background-position: 60px 0;
  }
}

@-moz-keyframes animate-stripes {
  0% {
    background-position: 0 0;
  }

  100% {
    background-position: 60px 0;
  }
}

@keyframes animate-stripes {
  0% {
    background-position: 0 0;
  }

  100% {
    background-position: 60px 0;
  }
}

.markdown-body .gloss .progress-bar {
  box-shadow:
    inset 0 4px 12px rgba(255, 255, 255, .7),
    inset 0 -12px 0 rgba(0, 0, 0, .05);
}
```
