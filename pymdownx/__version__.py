"""Version."""

version_info = (1, 0, 1, 'final', 0)


def _version():
    """
    Get the version.

    Printed versions format:

    main = '1.0' | '1.0.1'
    prerel = 'a1' | 'b1' | 'c1' | ''
    dev = '.dev' | ''
    """

    releases = {"alpha": 'a', "beta": 'b', "rc": 'c', "final": ''}
    assert len(version_info) == 5
    assert version_info[3] in releases

    main = '.'.join(str(x)for x in (version_info[0:2] if version_info[2] == 0 else version_info[0:3]))
    prerel = releases[version_info[3]]
    prerel += str(version_info[4]) if prerel else ''
    dev = '.dev' if version_info[3] == 'alpha' else ''

    return ''.join((main, prerel, dev))

version = _version()
