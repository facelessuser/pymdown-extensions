# Security Vulnerabilities

Our policy for security related issues is to fix related issues within our power on the most recent major release.

## Versioning

Versioning follows [PEP440](https://peps.python.org/pep-0440/): `major.minior.patch`.

Versions | Description
-------- | -----------
Major    | This reserved for releases that introduce breaking features.
Minor    | This reserved for releases that introduce new functionality.
Patch    | This is reserved for releases that only include bug fixes.

Example

```
8.0
8.1
8.1.3
```

## Create Security Vulnerability Report

If you have found a security vulnerability, you can create a draft "security advisory" on the GitHub repository,
[instructions here](https://docs.github.com/en/code-security/security-advisories/repository-security-advisories/creating-a-repository-security-advisory).
Such advisories are kept private as the issue is explored.

## Security Vulnerability Workflow

We will strive to acknowledge the report in about two business days.

Reports will be kept private until the issue is properly understood.

If the report is accepted we will notify Tidelift (who we've partnered with), request a CVE from GitHub, and work with
the reporter to find a resolution. Work will be done privately, and the final commit will not mention the security
issue.

The fix, announcement, and release will be negotiated with the reporter.

Afterwards, a release will be made and the vulnerability will be made public as close to each other as possible.
