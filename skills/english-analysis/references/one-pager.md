# Student one-pager

## Contents
- Purpose and audience
- Content and order
- Template
- Rules
- Files and updating

## Purpose and audience
A single page for the tutor to read before planning the next lesson. Tutor-only: it may quote errors and include teaching notes. Show CEFR level and the 1-100 score only; no other rating systems.

Build it right after an analysis (workflow step 8), or on request ("one-pager for <student>") from the latest Analysis section in the student's record, with no new recording needed. If the record has no Analysis section, say so and offer to analyze a recording.

## Content and order
1. Title: `# <Name>: One-Page Summary`
2. Subtitle line: level, score /100, date of the latest analysis, and how many recordings it rests on
3. Score table: Fluency, Vocabulary, Grammar (each /25), Pronunciation (not scored)
4. **Snapshot**: one or two lines from the profile (job or study, goal, interests, home language patterns, session length, tutor preferences such as light grammar)
5. **Strengths**: 3 bullets, each with a quoted example or a concrete observation
6. **Work on next**: top 3 error patterns, each with a quoted example and the fix in plain words
7. **Vocabulary check**: one line each for solid, needs a hint, re-teach (omit if the lesson did no review)
8. **Talk time**: one line with a bar, for example `Student ■■■■■■■□□□□□□□□□□□□□ 38% | Tutor 62%` (20 squares in total, filled squares = student percentage rounded to the nearest 5%)
9. **Next lesson focus**: 3 bullets that follow the profile's tutor preferences
10. **Confidence**: one line (single recording, recording conditions, labels inferred)

## Template
```
# Maria: One-Page Summary
*Level B1+ | Score 63/100 | Updated 2026-10-28 | Based on 2 recordings*

| Fluency | Vocabulary | Grammar | Pronunciation |
|---|---|---|---|
| 18/25 | 15/25 | 14/25 | Not scored |

## Snapshot
Works in logistics, goal is meetings in English. Prefers light grammar.

## Strengths
- Tells clear stories in order ("First I called them, then...")

## Work on next
- Missing be: "if you interested" (say: if you are interested)
```

## Rules
- Hard budget: at most 450 words and about 55 lines. scripts/one_pager_docx.py refuses a longer page. Cut the least useful bullets rather than shrinking the font.
- Black text only, no colors, no em dashes, no real names of anyone but the student.
- Use the profile's pronouns; they/them if none.
- Every number must come from the Analysis section or talk_stats.py. Never invent scores for a page.

## Files and updating
- Save the source as `~/eng-teaching-records/one-pagers/<slug>-one-pager.md` and the Word file next to it as `<slug>-one-pager.docx`. Create the folder if missing.
- Build with `python3 scripts/one_pager_docx.py <md> <docx>` (no -I flag, so python-docx is found; install with `pip install python-docx` if missing).
- Overwrite the previous version when a new analysis arrives, and keep the updated date in the subtitle.
