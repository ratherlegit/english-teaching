# Lesson report (Word document)

## Contents
- Purpose and audience
- Content and order
- Rules
- Files and building

## Purpose and audience
A tutor-only Word document for one recorded lesson: the evidence behind the analysis, in a form you can read in five minutes and keep. The one-pager is a single page to skim before planning; the lesson report is the full picture of one lesson (what was covered, how much the student spoke, which errors appeared, what stuck, what to try next). It may quote errors and includes tips about the tutor's own teaching. It is not for the student.

Build it right after the analysis (workflow step 10), or on request for any lesson that already has a saved analysis and transcript.

## Content and order
Aim for two to four pages. Use real numbers from the Analysis section, `talk_stats.py`, `tutor_stats.py` and the Error Tracker; never invent one.

1. Title: `# <Name>: Lesson Report, <date>`
2. Subtitle line (italic): lesson label, recording length, level and score, and how many recordings the record now rests on
3. **At a glance**: a table with Fluency, Vocabulary, Grammar (each /25), Score /100 and Level, with a second row "Last time" when an earlier score exists. One sentence on what moved and why
4. **What the lesson covered**: a table with columns Planned, Done, Notes, built from the Learning Path row, the logs and the transcript (Done is Yes, Partly or No). Add a line for anything that happened but was not planned. Then **Carry into next lesson**: one bullet per unfinished item
5. **How much they talked**: whole-lesson share, then the share before and after the phase split from `tutor_stats.py`, with a text bar (20 squares, filled squares = student percentage rounded to the nearest 5%). Say which prompts produced the longest turns and which the shortest
6. **Strengths**: three to five bullets, each with a quoted example
7. **Error patterns**: a table with columns Priority, Code, Pattern, Rate (count), Status, Example and fix, taken from the Error Tracker (top five or six codes, with a column for each tagged session), then a sentence on the like-for-like comparison from `error_ledger.py phases`. One plain-words fix per row. Say whether statuses are provisional (fewer than three sessions)
8. **Vocabulary**: a table with Word, First logged, Result (solid, partial, re-taught), then one line on new words and how they landed, and one line on the pattern. Omit the table if no earlier word was reviewed
9. **Listening and pronunciation**: what was missed or needed repeating; pronunciation targets marked low confidence
10. **Tips for you**: the tutor tips, following `references/tutor-tips.md`
11. **Next lesson**: three to five concrete steps that follow the profile's tutor preferences, including an opening question drawn from what the student said
12. **How sure we are**: single-recording estimate, recording conditions, inferred speaker labels, anything the machine transcript may have smoothed

## Rules
- Black text only, no em dashes, the profile's pronouns (they/them if none stated)
- Names: the student by first name; refer to clients, colleagues and family by role ("a client", "the boss")
- Quote the student exactly, errors included; every error pattern gets a quote
- Report what is uncertain; do not round a provisional status up to a trend

## Files and building
Save the source as `~/eng-teaching-records/lesson-reports/<slug>-<date>-lesson-report.md` and the Word file next to it as `.docx`. Build with `python3 scripts/report_docx.py <md> <docx>` (plain python3, not -I, so python-docx is found). Tell the tutor both paths.
