# Performance Learnings

- Avoid redundant list creations when calling `sorted()` on a `set()`. `sorted(set(...))` is faster and uses less memory than `sorted(list(set(...)))`.
