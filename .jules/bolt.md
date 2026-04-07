## 2026-04-04 - Caching Chord Generation and Note Indices
**Learning:** Generating all diatonic chords for all scales and displaying them involves repeatedly calling `MusicTheoryUtils.get_note_index` and `ChordGenerator.generate_scale_chords` with identical inputs. Calculating intervals and processing string structures redundantly takes considerable time.
**Action:** Implemented caching (memoization) on these frequent pure-function-like calls, which dropped the time to generate chords for all 12 keys 1000 times from ~1.00s down to ~0.007s.
## Performance Learnings

- Identifying redundant calculations within tight loops (like iterating over chords/notes) and hoisting them to an outer scope can have measurable positive impacts.
- For example, when calculating strum delay ticks based on BPM, the math does not change per inner chord iteration. Hoisting this variable pre-computation can save constant CPU work.
