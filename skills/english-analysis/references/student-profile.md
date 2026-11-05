# Student profile (Word document)

## Contents
- Purpose and audience
- Content and order
- Rules
- Files and building

## Purpose and audience
A tutor-only Word document that pulls everything the record knows about one student into a few pages: who they are, how they have progressed, what is improving or stuck, and what to do next. The student record grows with every lesson and gets long; the profile is the current summary of it. Overwrite the previous version after each new analysis, keeping the updated date in the subtitle.

Build it right after the lesson report (workflow step 10), or on request ("overall analysis for <student>") from the record and the ledger, with no new recording needed.

## Content and order
Three to five pages. Numbers come from the record, `error_ledger.py history` and `error_ledger.py show`.

1. Title: `# <Name>: Student Profile`
2. Subtitle line (italic): current level and score, updated date, number of recordings, date range
3. **Who they are**: job or study, goal, interests, home language, session length, tutor preferences (from the profile section)
4. **Progress over time**: the Score History table printed by `error_ledger.py history`, then two or three sentences on what moved, using the student talk-time trend. Earlier sessions without a tagged transcript still appear here when their scores were saved with `error_ledger.py score`
5. **Error patterns over time**: the tracker table (top six codes, all sessions), the statuses (new, improving, fading, rising, stuck, steady, baseline) in plain words, and what each means for teaching. Say plainly when there are fewer than three tagged sessions and the statuses are first impressions. For a stuck code, name a different method (see `references/error-codes.md`)
6. **Strengths that hold across lessons**: three to five bullets with quoted examples from different dates
7. **Vocabulary**: what sticks and what fades (the pattern across lessons), plus a short list of words to re-teach
8. **Listening and pronunciation**: recurring targets, marked low confidence until checked by ear
9. **Learning path**: a table of lessons with their status (delivered, partly delivered, not yet) and what is carried over
10. **What to do next**: the three to five priorities, in order, and the standing strands every lesson should keep (for example reaction phrases, listening, fillers)
11. **How sure we are**: number of recordings and tagged sessions, what each estimate rests on

## Rules
- Black text only, no em dashes, the profile's pronouns (they/them if none stated)
- Names: the student by first name; third parties by role
- Do not change the profile level here; report whether the evidence supports it and leave the decision to the tutor
- Prefer a short table or a sentence over copying whole Analysis sections

## Files and building
Save the source as `~/eng-teaching-records/student-profiles/<slug>-profile.md` and the Word file next to it as `<slug>-profile.docx`. Build with `python3 scripts/report_docx.py <md> <docx>` (plain python3, not -I).
