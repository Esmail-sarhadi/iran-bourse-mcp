# Security

`iran-bourse-mcp` is a read-only client of public endpoints. It stores no credentials, places no orders and opens no inbound ports unless you start an HTTP transport yourself.

- **HTTP transport has no authentication.** `iran-bourse-mcp serve --transport streamable-http` binds to `127.0.0.1` by default. If you expose it, put it behind an SSH tunnel or an authenticating reverse proxy.
- **Proxy.** `IRAN_BOURSE_PROXY` is used for all outbound requests; only set it to a proxy you trust.
- **Untrusted text.** Supervisor messages and Codal titles are third-party text returned to your model. Treat them as data, not instructions.

To report a vulnerability, please use GitHub's private vulnerability reporting on this repository (Security tab) rather than a public issue.
