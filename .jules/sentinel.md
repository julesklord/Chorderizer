## 2024-05-18 - [Error Message Leakage]
**Vulnerability:** Raw exception messages were printed to user output, potentially leaking sensitive system information such as paths or OS details.
**Learning:** It is crucial to hide raw exception messages from users, providing only generic feedback, while logging the actual exception details securely for maintainers.
**Prevention:** Always use a logging module to track exact errors, and display sanitized messages to end users.
