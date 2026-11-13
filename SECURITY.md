# Security notes

This project is a local development/demo application and has not undergone a production security review.

- Never commit `.env`, database files, or uploaded user content.
- Do not put real SMTP passwords or Django secret keys into source files.
- WebSocket chat needs server-side authorization for room access, message identity and message history before deployment to untrusted users.
- Review uses of dynamic evaluation and query/command handling in chat before exposing it publicly.
- Use a supported Django version and review deployment settings (`DEBUG`, HTTPS, allowed hosts, CSRF, static and media hosting) before deployment.
- Redis should not be exposed to the public Internet.
