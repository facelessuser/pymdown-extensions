"""Populate GitHub labels for issue tracker."""
from github import Github
from collections import namedtuple
import sys
import os

# Repository name
REPO_NAME = 'pymdown-extensions'

# Options
DELETE_UNSPECIFIED = True

# Colors
BUG = 'c45b46'
FEATURE = '7b17d8'
SUPPORT = 'efbe62'
MAINTENANCE = 'b2ffeb'

CATEGORY = '709ad8'
SUBCATEGORY = 'bfd4f2'

PENDING = 'f0f49a'
REJECTED = 'f7c7be'
APPROVED = 'beed6d'

LOW = 'dddddd'

# Labels.
# To rename a label, use ('old_name', 'new_name') as the key.
label_list = {
    # Issue type
    'bug': (BUG, "Bug report."),
    'feature': (FEATURE, "Feature request."),
    'maintenance': (MAINTENANCE, "Maintenance chore."),
    'support': (SUPPORT, "Support request."),

    # Category
    'extension': (CATEGORY, "Related to extension code."),
    'integration': (CATEGORY, "Related to packaging and/or testing."),
    'docs': (CATEGORY, "Related to documentation."),

    # Sub categories
    'arithmatex': (SUBCATEGORY, "Related to the arithmatex extension."),
    'b64': (SUBCATEGORY, "Related to the b64 extension."),
    'betterem': (SUBCATEGORY, "Related to the betterem extension."),
    'caret': (SUBCATEGORY, "Related to the caret extension."),
    'critic': (SUBCATEGORY, "Related to the critic extension."),
    'details': (SUBCATEGORY, "Related to the details extension."),
    'emoji': (SUBCATEGORY, "Related to the emoji extension."),
    'escapeall': (SUBCATEGORY, "Related to the escapeall extension."),
    'extra': (SUBCATEGORY, "Related to the extra extension."),
    'extrarawhtml': (SUBCATEGORY, "Related to the extrarawhtml extension."),
    'highlight': (SUBCATEGORY, "Related to the highlight extension."),
    'inlinehilite': (SUBCATEGORY, "Related to the inlinehilite extension."),
    'keys': (SUBCATEGORY, "Related to the keys extension."),
    'magiclink': (SUBCATEGORY, "Related to the magiclink extension."),
    'mark': (SUBCATEGORY, "Related to the mark extension."),
    'pathconverter': (SUBCATEGORY, "Related to the paythconverter extension."),
    'progressbar': (SUBCATEGORY, "Related to the progressbar extension."),
    'slugs': (SUBCATEGORY, "Related to the slugs extension."),
    'smartsymbols': (SUBCATEGORY, "Related to the smartsymbols extension."),
    'snippets': (SUBCATEGORY, "Related to the snippets extension."),
    'striphtml': (SUBCATEGORY, "Related to the striphtml extension."),
    'superfences': (SUBCATEGORY, "Related to the superfences extension."),
    'tasklist': (SUBCATEGORY, "Related to the tasklist extension."),
    'tilde': (SUBCATEGORY, "Related to the tilde extension."),

    # Issue status
    'more-info-needed': (PENDING, "More information is required."),
    'needs-confirmation': (PENDING, "The alleged behavior needs to be confirmed."),
    'needs-decision': (PENDING, "A decision needs to be made regarding request."),
    'confirmed': (APPROVED, "Confirmed bug report or approved feature request."),
    'maybe': (LOW, "Pending approval of low priority request."),
    'duplicate': (REJECTED, "The issue has been previously reported."),
    'wontfix': (REJECTED, "The issue will not be fixed for the stated reasons."),
    'invalid': (REJECTED, "Invalid report (user error, upstream issue, etc)."),

    # Pull request status
    'work-in-progress': (PENDING, "A partial solution. More changes will be coming."),
    'needs-review': (PENDING, "Needs to be reviewed and/or approved."),
    'requires-changes': (PENDING, "Awaiting updates after a review."),
    'approved': (APPROVED, "The pull request is ready to be merged."),
    'rejected': (REJECTED, "The pull request is rejected for the stated reasons.")
}


# Label handling
class LabelEdit(namedtuple('LabelEdit', ['old', 'new', 'color', 'description'])):
    """Label Edit tuple."""


def find_label(label, label_color, label_description):
    """Find label."""
    edit = None
    for name, values in label_list.items():
        color, description = values
        if isinstance(name, tuple):
            old_name = name[0]
            new_name = name[1]
        else:
            old_name = name
            new_name = name
        if label.lower() == old_name.lower():
            edit = LabelEdit(old_name, new_name, color, description)
            break
    return edit


def update_labels(repo):
    """Update labels."""
    updated = set()
    for label in repo.get_labels():
        edit = find_label(label.name, label.color, label.description)
        if edit is not None:
            print('    Updating {}: #{} "{}"'.format(edit.new, edit.color, edit.description))
            label.edit(edit.new, edit.color, edit.description)
            updated.add(edit.old)
            updated.add(edit.new)
        else:
            if DELETE_UNSPECIFIED:
                print('    Deleting {}: #{} "{}"'.format(label.name, label.color, label.description))
                label.delete()
            else:
                print('    Skipping {}: #{} "{}"'.format(label.name, label.color, label.description))
            updated.add(label.name)
    for name, values in label_list.items():
        color, description = values
        if isinstance(name, tuple):
            new_name = name[1]
        else:
            new_name = name
        if new_name not in updated:
            print('    Creating {}: #{} "{}"'.format(new_name, color, description))
            repo.create_label(new_name, color, description)


# Authentication
def get_auth():
    """Get authentication."""
    import getpass
    user = input("User Name: ")  # noqa
    pswd = getpass.getpass('Password: ')
    return Github(user, pswd)


def main():
    """Main."""

    if len(sys.argv) > 1 and os.path.exists(sys.argv[1]):
        try:
            with open(sys.argv[1], 'r') as f:
                user_name, password = f.read().strip().split(':')
            git = Github(user_name, password)
            password = None
        except Exception:
            git = get_auth()
    else:
        git = get_auth()

    user = git.get_user()

    print('Finding repo...')
    for repo in user.get_repos():
        if repo.owner.name == user.name:
            if repo.name == REPO_NAME:
                print(repo.name)
                update_labels(repo)
                break


if __name__ == "__main__":
    main()
