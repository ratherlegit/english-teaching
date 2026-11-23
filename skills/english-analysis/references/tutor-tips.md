# Tips for the tutor

## Contents
- Purpose
- How to get the evidence
- Tip types
- How to word a tip
- Pace and clarity measures
- Clarity pass (opt-in)
- Rules

## Purpose
Every lesson report ends its findings with a short "Tips for you" section about the tutor's own teaching, based on the same transcript as the student analysis. The aim is a few specific, small things to try next lesson, not an evaluation. The tutor is the reader and the decision maker.

## How to get the evidence
Run `python3 -I scripts/tutor_stats.py <transcript.md> <StudentName> --split <mm:ss>` where `<mm:ss>` is the time the lesson changes mode (for example open conversation ends and tutor-led review begins; choose it by reading the transcript). It prints, for the whole lesson and each part:
- the student's share of words
- tutor turns of 100+ words (how many, the longest and when)
- tutor questions, and how many got a student answer of 15+ words
- the share of student turns that are 5 words or fewer
- tutor pace, tutor turns that stack two or more questions, and student requests for repetition (see Pace and clarity measures)

Then read the transcript for what counts cannot show: whether the tutor asked the student to guess or explain before explaining, whether a word the tutor supplied was used by the student soon after (uptake), whether corrections interrupted a story, and how much of the planned lesson was delivered.

## Tip types
Pick the two or three that the evidence supports most clearly. Include one thing the tutor did well, with its evidence, so the section is not only corrections.

| Type | Evidence that triggers it | What to suggest |
|---|---|---|
| Long explanations | Three or more tutor turns of 100+ words in a part where the student could be talking | Ask the student to guess or give their own sentence first, then explain in two or three sentences |
| Question yield | Questions followed by long answers in one part but not the other | Name the question types that worked and use them more; turn closed questions into "what would you do if..." or "what advice would you give..." |
| Guess first | The student guessed meanings correctly or nearly so when asked | Keep asking before explaining; it produces more student talk and shows what they already know |
| Uptake | A word the tutor supplied was used by the student within a few turns (strength), or never used | Praise and repeat the uptake routine; for words not used, ask for one sentence about the student's own work |
| Corrections | Corrections or word-supplying that cut off a story | Note the error, let the story finish, then give 2 or 3 patterns in the feedback step (fits the retell cycle) |
| Plan versus time | Large parts of the plan not delivered while open conversation ran long | Plan fewer activities, rank them, and let the best conversation run; keep the grammar point short and tied to what the student just said |
| Screen reading | Student turns are short or garbled when reading from the screen, longer when speaking freely | Move gap-fills to paper or the handout, or have the student say the answers without reading |
| Pace | Median tutor pace well above the guide for the student's level, plus repetition requests clustered in the same stretch | Slow down and pause after key words; give the instruction once, then wait |
| Stacked questions | Several tutor turns with two or more questions and a short or off-target student reply | Ask one question, then wait; rephrase only if there is silence |
| Lost time | A connection drop or other interruption | Note it and what was cut, so the next plan picks it up |

## How to word a tip
- One sentence of evidence with a number and a time ("5 tutor turns ran past 100 words, the longest 238 words at 21:59")
- One sentence of what to try, small enough for the next lesson
- A positive framing first when there is a strength; a colleague's tone, not a verdict

Example: "Your open questions worked: 11 of 13 got an answer of 15+ words before 20:20, against 4 of 10 after. Next lesson, turn the vocabulary review into the same kind of question, for example 'Where could you use this word at work this week?'"

## Pace and clarity measures
These come from `tutor_stats.py` and run every lesson. They are cheap counts, not judgments.
- **Pace** is words per minute over tutor turns of 30+ words, using the time to the next turn. Pauses inside a turn lower it, so treat it as a floor. Rough guide for tutor speech to a learner: A1-A2 about 100-130, B1 about 120-150, B2 and above about 140-170. Native conversation runs 150-190. A pace above the guide matters only when the student also asks for repetition or answers go short in the same stretch.
- **Stacked questions** are tutor turns with two or more question marks. One or two is normal; a pattern is worth a tip.
- **Repetition requests** are student turns like "sorry?", "pardon", "what do you mean". A cluster at one time (name the times) points at an unclear instruction or fast stretch, so look at the tutor turn just before each one.

## Clarity pass (opt-in)
Run only when the tutor asks ("how did I do?", "give me tutor feedback", "check my clarity") or asks for it in a lesson report. Do not run it by default. It uses the transcript already read, so it needs no second read; work from the turns around the repetition requests and the longest tutor turns first. Check:
- **Instruction check:** after a task was set, did the tutor confirm understanding in some way (the student restated it, tried an example), or did the student start wrong or ask again?
- **Unglossed language:** idioms, phrasal verbs or abstract words above the student's level that were not explained or rephrased.
- **Rephrasing:** when the student did not follow, did the tutor simplify or just repeat the same words louder or faster?
- **Modelling:** did the tutor give one clear example before asking the student to produce?
Report at most three findings, each with a timestamp and a quote of two to six words of the tutor's turn, plus one thing the tutor did clearly. Same tone and word rules as the tips. Save nothing to the student's record; it is feedback for the tutor only. The numbers behind it are already saved per lesson by `error_ledger.py add` (or `tutor-save` for older lessons); show the trend with `error_ledger.py tutor <slug>`.

**Tutor feedback only (no student scoring).** If the tutor wants just this, do steps 1 to 4 of the main workflow (skip error tagging), run `tutor_stats.py`, run `error_ledger.py tutor-save <slug> <date> <transcript.md> <StudentName> --split <mm:ss>` to store the numbers, do the clarity pass, and stop. Do not write an Analysis section, scores or a Learning Path update.

## Rules
- At most three tips, each with evidence from this transcript
- Counts are prompts for judgment, not scores; never rank the tutor or compare with other tutors
- A tip that depends on a number must name where the number came from
- Respect the profile: if the tutor wants light grammar or no grammar checks, do not suggest more correction
- No em dashes; no student names other than the student's own first name
