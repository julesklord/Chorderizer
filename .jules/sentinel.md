## Security Issue: Insecure PRNG Usage

**Issue:** The `random` module was used for generating note velocities. `random` is a pseudorandom number generator (PRNG) and is not cryptographically secure. While velocity generation might not be highly sensitive, using PRNGs where a secure alternative exists is a poor security practice that could establish bad patterns.

**Fix:** Replaced `import random` with `import secrets` and updated `random.randint(...)` to `secrets.SystemRandom().randint(...)`. This uses the operating system's strongest available randomness source, ensuring that randomness remains cryptographically secure.
