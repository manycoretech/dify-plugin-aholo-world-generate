# Security Policy

## Supported Versions

Security fixes are provided for the latest released version on the [Dify Marketplace](https://marketplace.dify.ai/) and the latest tag on the source repository.

| Version | Supported |
| --- | --- |
| 1.0.x | Yes |
| < 1.0.0 | No |

## Reporting a Vulnerability

If you discover a security issue in this plugin, please report it responsibly:

1. **Preferred:** Open a private security advisory on GitHub  
   https://github.com/manycoretech/dify-plugin-aholo-world-generate/security/advisories/new
2. **Alternative:** Open a GitHub issue and clearly mark it as a security report. Avoid posting exploit details publicly until a fix is available.

Please include:

- Affected version
- Steps to reproduce
- Impact assessment
- Suggested fix (if any)

We aim to acknowledge reports within **5 business days** and share an initial assessment within **10 business days**.

## Scope

This policy covers the `dify-plugin-aholo-world-generate` plugin source code and packaged `.difypkg` releases.

Out of scope:

- Vulnerabilities in Dify itself (report to [langgenius/dify](https://github.com/langgenius/dify/security))
- Vulnerabilities in Aholo API services (report to Aholo / Manycore through your official support channel)
- Misconfiguration such as exposing an Aholo API key in workflow logs or shared credentials

## Security Practices

- API keys are accepted only as Dify provider credentials and are not returned in tool outputs.
- Optional `cover` URLs are validated to reject localhost and private network hosts before requests are sent.
- Do not commit `.env` files or real API keys to the repository.

## Dify Marketplace Disclosure

For issues that affect the Marketplace distribution channel, you may also follow Dify's security disclosure process:

https://github.com/langgenius/dify-plugins#security-disclosure
