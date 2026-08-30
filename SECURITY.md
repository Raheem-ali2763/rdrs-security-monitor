# Security Policy

## About RDRS

RDRS is a security monitoring and incident detection platform designed to monitor filesystem activity, identify suspicious behavior, calculate threat scores, and generate security incidents.

## Supported Version

The current supported release is:

- RDRS v0.1.0

## Reporting a Security Issue

If you discover a security vulnerability or security-related issue in RDRS, please do not disclose sensitive details publicly through GitHub Issues.

Instead, contact the repository maintainer privately through the contact method associated with this GitHub account.

When reporting an issue, please provide:

- A clear description of the vulnerability
- Steps to reproduce the issue
- The affected component or file
- Potential security impact
- Any relevant logs or screenshots that do not contain sensitive information

## Responsible Disclosure

Please allow reasonable time for the issue to be reviewed before publicly disclosing security-sensitive details.

## Security Considerations

RDRS is intended for authorized security monitoring and defensive security research.

Users should:

- Run RDRS only on systems they are authorized to monitor.
- Protect access to the RDRS dashboard and API.
- Review configuration before enabling filesystem monitoring.
- Avoid committing credentials, secrets, private keys, databases, or other sensitive runtime data.
- Keep project dependencies updated.

## Sensitive Data

Do not commit the following to the repository:

- Passwords
- API keys
- Authentication tokens
- Private keys
- `.env` files containing secrets
- Production databases
- Sensitive logs
- Confidential incident evidence

The repository `.gitignore` excludes common runtime and sensitive files.

## Scope

This security policy applies to the RDRS source code and its documented components in this repository.
