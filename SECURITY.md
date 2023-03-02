# Security Vulnerabilities

Our policy for security related issues is to fix related issues within our power on the most recent minor release.

## Versioning

Generally, we try to follow semantic versioning: `major.minor.patch`.

Versions | Description
-------- | -----------
Major    | This reserved for releases that introduce breaking features.
Minor    | This reserved for releases that introduce new functionality.
Patch    | This is reserved for releases that only include bug fixes.

Example

```
8.0
8.0.3
```

Occasionally, we may provide an alpha, beta, or release candidate introducing experimental features or fixes that are
not ready for a wide audience. This usually follows the the apporach of: `major.minor.patch(a | b | rc)(prerelease_number)`.

Example:

```
8.0b1
8.0.3rc2
```

Even more rare, we may fix a non functional change, maybe documentation builiding was broken in the release, or bad
metadata for PyPI. In these cases, we may release a postfix: `major.minor.patch.post(postfix_number)`.

```
8.0.post1
8.0.3.post2
```

## Create Security Vulnerability Report

If you have found a security vulnerability, you can create a draft "security advisory" on the GitHub repository,
[instructions here](https://docs.github.com/en/code-security/security-advisories/repository-security-advisories/creating-a-repository-security-advisory).
Such advisories are kept private as the issue is explored.

## Security Vulnerability Workflow

We will strive to acknowledge the report in about two business days.

Reports will be kept private until the issue is properly understood.

If the report is accepted, we will request a CVE from GitHub and work with the reporter to find a resolution. Work will
be done privately, and the final commit will not mention the security issue.

The fix, announcement, and release will be negotiated with the reporter.

Afterwards, a release will be made and the vulnerability will be made public as close to each other as possible.
