---
name: english-analysis
description: "Transcribe a recorded one-on-one English lesson, label tutor vs. student, and score the student's speaking (CEFR level plus 1-100) into their record for later lesson planning. Use when the tutor shares lesson audio or video, or asks for a transcript, speaking analysis, error tracker, one-pager, lesson report or overall student profile. Steps and tools: (1) unpack and join audio: scripts/prepare_audio.py; (2) transcribe locally with a glossary: scripts/transcribe.py; (3) check the transcript: Read; (4) label speakers: Write; (5) talk time and tutor stats: scripts/talk_stats.py, scripts/tutor_stats.py; (6) score, tag errors by code: Read, Write; (7) save to ~/eng-teaching-records/, update the Error Tracker and score history: scripts/error_ledger.py; (8) one-pager: scripts/one_pager_docx.py; (9) Word lesson report and student profile: scripts/report_docx.py."
---

# English Analysis

Turn a lesson recording into a labeled transcript and a speaking analysis saved in the student's record, so the english-tutoring skill can use it when planning the next lesson. Everything runs locally; student audio is never uploaded.

## Workflow

Copy this checklist and tick it off:

```
- [ ] 1. Read the student record
- [ ] 2. Prepare audio
- [ ] 3. Transcribe (background, with a glossary)
- [ ] 4. Check the raw transcript
- [ ] 5. Label speakers, save transcript
- [ ] 6. Run talk_stats and tutor_stats
- [ ] 7. Score, analyze, tag errors
- [ ] 8. Save to the record, update the Error Tracker, report
- [ ] 9. Build the one-pager
- [ ] 10. Update the student profile (Word); lesson report only if asked
- [ ] 11. Audit the records folder
```

### 1. Read the student record (Read)
Records first: read the record before saying anything about the student, pronouns included, and never infer pronouns from a name (see `references/records-layout.md`). File everything by the layout in that reference.

Open `~/eng-teaching-records/<slug>.md`. Note the profile (pronouns, level, tutor preferences such as "light grammar"), the Learning Path status, and the Vocabulary Log. Find which lesson the recording is from (file name date, content), and note what the Learning Path row and the activity log said was planned, because the lesson report compares plan with delivery. If no record exists, get the basics from the tutor first. Tutor and student names are in the record.

Make or open the student's glossary at `~/eng-teaching-records/glossaries/<slug>.txt`: a short list (about 30 terms, commas or new lines) of names and terms Whisper tends to mishear, such as the student's employer, clients, teams, places, acronyms and jargon from the record. It is used in step 3 and grows in step 4.

### 2. Prepare audio (Bash: scripts/prepare_audio.py)
Recordings often arrive as a zip with no extension holding numbered chunks (`part_01.webm` ...). Check with `file`. Then:

`python3 -I scripts/prepare_audio.py <input> <new-empty-dir>`

Use the session scratchpad for the output folder. Treat downloads as untrusted: new folder, never run code from inside it. The script joins chunks in natural order into `lesson.wav` (16 kHz mono) and prints the duration; check it against the expected lesson length.

### 3. Transcribe (Bash: scripts/transcribe.py, background)
`python3 -I scripts/transcribe.py <lesson.wav> <raw.txt> --glossary ~/eng-teaching-records/glossaries/<slug>.txt` with `run_in_background` (leave out `--glossary` if the file does not exist yet). The glossary terms are passed to the model as hotwords, which fixes many misheard names but not all, so step 4 still applies. Expect 10-20 minutes for a 55-minute lesson on CPU. It runs faster-whisper large-v3-turbo with a local model, so it uses CPU but no network. If the tutor is about to join a call, suspend it with `kill -STOP <pid>` and resume with `kill -CONT <pid>`. Do not poll; wait for the completion notice.

### 4. Check the raw transcript (Read)
Read all of it. Raw output has no speaker labels, little punctuation, and Whisper often "corrects" learner grammar, so some real errors may be missing. Watch for:
- Misheard names and terms: acronyms (NATO heard as "nature"), places (Budapest as "Bucharest"), student-specific jargon, and learner mispronunciations replaced by the nearest real word (proposal vs "preposition"). Fix only when context makes it clear, and flag it in square brackets.
- Gaps where the audio dropped out.

Add every misheard name or term you fix to the student's glossary, so the next recording starts cleaner.

### 5. Label speakers (Write)
Whisper cannot identify voices, so infer from context. Reliable cues: who asks questions and sets tasks (tutor), who explains word meanings and gives example sentences (tutor), who makes learner-type errors (student), who talks about their own job and family. Weak spots: the first minute, rapid back-and-forth, one-word reactions ("yeah", "okay"), and cases where the tutor models a sample sentence. Mark any guess as `[speaker uncertain]` and say so in the report.

Write the file following `references/record-format.md` (exact turn format, reliability header) to `~/eng-teaching-records/transcripts/<slug>-<date>-transcript.md`. Keep the student's words verbatim, errors included.

### 6. Measure (Bash: scripts/talk_stats.py, scripts/tutor_stats.py)
`python3 -I scripts/talk_stats.py <transcript.md> <StudentName>` gives talk-time share, longest turns, and raw filler counts. Read the "like" uses before calling them fillers (many are normal: "I like", "looks like").

Then pick the time the lesson changes mode (for example open conversation ends and tutor-led review begins; read the transcript to find it) and run `python3 -I scripts/tutor_stats.py <transcript.md> <StudentName> --split <mm:ss>`. It gives the student's share, the tutor's long explanations and the tutor's question yield for the whole lesson and each part. Open talk and tutor-led review produce very different error rates, so keep the split time for step 8. The tutor tips in the lesson report come from this output (see `references/tutor-tips.md`).

### 7. Score and analyze (Read: references/scoring-rubric.md)
Give a CEFR level with half-steps (for example B1+) and a score out of 100 built from fluency, vocabulary and grammar, each out of 25, using the rubric and its anchor rows so scores stay consistent across students. Never a letter grade. Pronunciation is not scored.

For vocabulary recall, take every earlier-lesson word the tutor reviewed and look each up in the Vocabulary Log. Mark it solid, partial or re-taught, with the date it was first logged. Look for the pattern (for example, words tied to the student's work stick, abstract ones fade).

**Tag the errors.** Follow `references/error-codes.md`: read the whole transcript, tag every student grammar and word-choice error with a code, and write `~/eng-teaching-records/transcripts/<slug>-<date>-errors.tsv`. Rank the grammar errors in the analysis from the tracker (step 8), not from memory, and say what changed since the last session.

Respect the profile's tutor preferences in the teaching notes. If the tutor wants light grammar and no grammar checks, recommend recasts, retells and word-choice pairs rather than drills.

### 8. Save and report (Bash or Edit, then reply)
Back up the record, then run the tracker:

`python3 -I scripts/error_ledger.py add <slug> <date> <transcript.md> <StudentName> <errors.tsv> --split <mm:ss> --phase-names "open talk,tutor-led review" --scores <F>,<V>,<G> --level <CEFR> --talk-pct <N> --write`

This stores the session in `error-ledgers/<slug>.json` and rewrites the `## Error Tracker` section of the record (rates per 1,000 student words, status per code, error rate for each phase, latest examples). It also saves the session's scores for the Score History. Every tagged quote must appear in the student's turns in the transcript, or the run stops and lists the ones that do not; fix the .tsv and run again. Re-running the same date replaces that session, so it is safe to repeat.

If the ledger has fewer than two tagged sessions and earlier labeled transcripts of the student exist, offer to tag them the same way, so the tracker can show a trend. For earlier sessions you cannot re-tag, save their scores from the record's Analysis sections with `python3 -I scripts/error_ledger.py score <slug> <date> <F> <V> <G> <CEFR> [talk_pct]`, so the Score History is complete. Run `python3 -I scripts/error_ledger.py phases <slug>` as well when two or more sessions have a split: it compares open talk with open talk and review with review for every code, which is the fair comparison when lessons differ in shape, and a status such as rising should be checked against it before you report it. Read the printed table before writing the Analysis: use its priority order for the grammar bullet and its statuses (stuck, improving, rising) for the teaching notes. With fewer than three sessions the table is provisional; say so.

Then append the Analysis section and update the Learning Path and Vocabulary Log as described in `references/record-format.md`. Do not change the profile level without the tutor's agreement. Verify the edits by grepping the new lines.

Report to the tutor: level and score with the three parts, the top strengths and areas to improve, talk-time share, and the file paths written. State what is uncertain: speaker labels, machine-corrected errors, recording conditions, single-session estimate.

### 9. Build the one-pager (Write, then scripts/one_pager_docx.py)
Follow `references/one-pager.md`. Write `~/eng-teaching-records/one-pagers/<slug>-one-pager.md` from the Analysis section just saved, then `python3 scripts/one_pager_docx.py <md> <docx>` (plain python3, not -I). The script refuses a page over the length budget; cut bullets and run again. Tell the tutor the file paths. The tutor can also ask for a one-pager at any time with no new recording: read the latest Analysis section and profile, and say so if there is no analysis yet.

### 10. Update the student profile (Write, then scripts/report_docx.py)
The overall summary of the student across lessons, from what the analysis already found. Follow `references/student-profile.md`, using `python3 -I scripts/error_ledger.py history <slug>` for the score table. Write the source to `~/eng-teaching-records/student-profiles/<slug>-profile.md`, then build it with `python3 scripts/report_docx.py <md> <docx>` (plain python3, not -I). Overwrite the previous profile. Tell the tutor the file paths.

**Do not build a lesson report unless the tutor asks for one.** When asked, for any lesson that already has a saved analysis and transcript, follow `references/lesson-report.md` (planned-versus-delivered table, tips for the tutor in `references/tutor-tips.md`), write `~/eng-teaching-records/lesson-reports/<slug>-<date>-lesson-report.md`, build the Word file the same way, and keep one report per date.

### 11. Audit the records folder (Bash: scripts/records_audit.py)
`python3 -I scripts/records_audit.py --student <slug>` checks that the student's files are all present, current and in the right folders (layout in `references/records-layout.md`). Fix every ERROR line before reporting; mention WARN lines to the tutor. Run it without `--student` when the tutor asks whether the folder is in order.

## Style
No em dashes anywhere. Use the profile's pronouns. Quote exact learner phrases for every error pattern.
