# Records folder layout

## Contents
- The layout
- Rules
- The audit
- Records first

## The layout
Everything lives in `~/eng-teaching-records/`, outside the skill folders, so updates and reinstalls never touch it.

```
~/eng-teaching-records/
  <slug>.md                     one record per student (profile, learning path, logs, tracker, analyses)
  _tutor.md                     the tutor's own profile
  handouts/<slug>/              lesson plans and student handouts (.docx) from the english-tutoring skill
  lesson-docs/<slug>/           the tutor's final version of each dated lesson document (often the Drive copy with their tweaks), named <Name> <date>.docx; this is the real record of what was taught
  source-notes/<slug>/          summaries and notes that fed an analysis but are not recordings
  transcripts/                  <slug>-<date>-transcript.md and <slug>-<date>-errors.tsv
  error-ledgers/                <slug>.json (written by error_ledger.py, never by hand)
  glossaries/                   <slug>.txt (names and terms for the transcriber)
  lesson-reports/               <slug>-<date>-lesson-report.md and .docx (only when the tutor asks for one)
  student-profiles/             <slug>-profile.md and .docx
  one-pagers/                   <slug>-one-pager.md and .docx
  worksheets/                   <slug>.md worksheet profiles
  _review-before-deleting/      anything uncertain; the tutor decides, nothing is deleted without asking
```

## Rules
- Only `<slug>.md` records and `_tutor.md` sit at the top level. Every other file goes in a folder above.
- A new file type needs a folder, not the top level. Folders starting with an underscore are allowed for holding areas.
- `<slug>` is the student's first name, lowercase, hyphens for spaces. Dates are `YYYY-MM-DD`, using the date on the recording or the lesson, and if the tutor's own file is dated differently, keep both dates in the record and name files by the recording.
- Name versions plainly. Keep one handout per lesson; move older versions to `_review-before-deleting/` once the tutor says which was used. Tutors name their plans by lesson date, so handouts are named `<slug>-<YYYY-MM-DD>.docx` and `<slug>-<YYYY-MM-DD>-handout.docx`; this also keeps two lessons that share a number apart. Never save a second copy of a record or transcript next to the first.
- Never move or delete a tutor's file without telling them, and keep an undo list when moving more than a few.
- Every Word file is built from a markdown file kept beside it, so a change is made in the markdown and the Word file rebuilt.

## The audit
`python3 -I scripts/records_audit.py` checks the whole folder (add `--student <slug>` for one student). It reports each finding as ERROR or WARN and exits with 1 if there is any ERROR:
- the top level holds only records and known folders
- every record has pronouns and a level in its Profile
- every transcript has an errors file, a ledger session and an Analysis section in the record (lesson reports are optional and are not required)
- the glossary, student profile and one-pager exist, are not older than the latest transcript, and have a current .docx
- no lesson has several handout versions

Run it at the end of every analysis (workflow step 11) and whenever the tutor asks if the folder is in order. Fix ERRORs before reporting; tell the tutor about WARNs.

## Records first
Before saying anything about a student, including pronouns, level, location, job, family or what was taught, read their record. Never infer pronouns from a name or carry them over from another student. If the record states none, use they/them and ask the tutor. If a fact is not in the record, say it is not recorded. If the tutor says the record is wrong or incomplete, look in the other folders and the tutor's own files before agreeing or disagreeing, and say what you checked.
