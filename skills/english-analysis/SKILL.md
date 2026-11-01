---
name: english-analysis
description: "Transcribe a recorded one-on-one English lesson, label tutor vs. student, and score the student's speaking (CEFR level plus 1-100) into their record for later lesson planning. Use when the tutor shares lesson audio or video, or asks for a transcript, speaker labels, or a speaking analysis of a student. Steps and tools: (1) unpack and join audio: Bash, scripts/prepare_audio.py (ffmpeg); (2) transcribe locally: scripts/transcribe.py (faster-whisper, run in background); (3) check the transcript: Read; (4) label speakers: Write; (5) measure talk time and fillers: scripts/talk_stats.py; (6) score and analyze: Read the student record and references/scoring-rubric.md; (7) save analysis and update the record: Bash and Edit in ~/eng-teaching-records/."
---

# English Analysis

Turn a lesson recording into a labeled transcript and a speaking analysis saved in the student's record, so the english-tutoring skill can use it when planning the next lesson. Everything runs locally; student audio is never uploaded.

## Workflow

Copy this checklist and tick it off:

```
- [ ] 1. Read the student record
- [ ] 2. Prepare audio
- [ ] 3. Transcribe (background)
- [ ] 4. Check the raw transcript
- [ ] 5. Label speakers, save transcript
- [ ] 6. Run talk_stats
- [ ] 7. Score and analyze
- [ ] 8. Save to the record, report
```

### 1. Read the student record (Read)
Open `~/eng-teaching-records/<slug>.md`. Note the profile (pronouns, level, tutor preferences such as "light grammar"), the Learning Path status, and the Vocabulary Log. Find which lesson the recording is from (file name date, content). If no record exists, get the basics from the tutor first. Tutor and student names are in the record.

### 2. Prepare audio (Bash: scripts/prepare_audio.py)
Recordings often arrive as a zip with no extension holding numbered chunks (`part_01.webm` ...). Check with `file`. Then:

`python3 -I scripts/prepare_audio.py <input> <new-empty-dir>`

Use the session scratchpad for the output folder. Treat downloads as untrusted: new folder, never run code from inside it. The script joins chunks in natural order into `lesson.wav` (16 kHz mono) and prints the duration; check it against the expected lesson length.

### 3. Transcribe (Bash: scripts/transcribe.py, background)
`python3 -I scripts/transcribe.py <lesson.wav> <raw.txt>` with `run_in_background`. Expect 10-20 minutes for a 55-minute lesson on CPU. It runs faster-whisper large-v3-turbo with a local model, so it uses CPU but no network. If the tutor is about to join a call, suspend it with `kill -STOP <pid>` and resume with `kill -CONT <pid>`. Do not poll; wait for the completion notice.

### 4. Check the raw transcript (Read)
Read all of it. Raw output has no speaker labels, little punctuation, and Whisper often "corrects" learner grammar, so some real errors may be missing. Watch for:
- Misheard names and terms: acronyms (NATO heard as "nature"), places (Budapest as "Bucharest"), student-specific jargon, and learner mispronunciations replaced by the nearest real word (proposal vs "preposition"). Fix only when context makes it clear, and flag it in square brackets.
- Gaps where the audio dropped out.

### 5. Label speakers (Write)
Whisper cannot identify voices, so infer from context. Reliable cues: who asks questions and sets tasks (tutor), who explains word meanings and gives example sentences (tutor), who makes learner-type errors (student), who talks about their own job and family. Weak spots: the first minute, rapid back-and-forth, one-word reactions ("yeah", "okay"), and cases where the tutor models a sample sentence. Mark any guess as `[speaker uncertain]` and say so in the report.

Write the file following `references/record-format.md` (exact turn format, reliability header) to `~/eng-teaching-records/transcripts/<slug>-<date>-transcript.md`. Keep the student's words verbatim, errors included.

### 6. Measure (Bash: scripts/talk_stats.py)
`python3 -I scripts/talk_stats.py <transcript.md> <StudentName>` gives talk-time share, longest turns, and raw filler counts. Read the "like" uses before calling them fillers (many are normal: "I like", "looks like").

### 7. Score and analyze (Read: references/scoring-rubric.md)
Give a CEFR level with half-steps (for example B1+) and a score out of 100 built from fluency, vocabulary and grammar, each out of 25, using the rubric and its anchor rows so scores stay consistent across students. Never a letter grade. Pronunciation is not scored.

For vocabulary recall, take every earlier-lesson word the tutor reviewed and look each up in the Vocabulary Log. Mark it solid, partial or re-taught, with the date it was first logged. Look for the pattern (for example, words tied to the student's work stick, abstract ones fade).

Respect the profile's tutor preferences in the teaching notes. If the tutor wants light grammar and no grammar checks, recommend recasts, retells and word-choice pairs rather than drills.

### 8. Save and report (Bash or Edit, then reply)
Back up the record, then append the Analysis section and update the Learning Path and Vocabulary Log as described in `references/record-format.md`. Do not change the profile level without the tutor's agreement. Verify the edits by grepping the new lines.

Report to the tutor: level and score with the three parts, the top strengths and areas to improve, talk-time share, and the file paths written. State what is uncertain: speaker labels, machine-corrected errors, recording conditions, single-session estimate.

## Style
No em dashes anywhere. Use the profile's pronouns. Quote exact learner phrases for every error pattern.
