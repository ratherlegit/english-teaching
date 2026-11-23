# english-teaching

**Planning, homework and lesson-review assistants for English teachers, in one install.** Five skills cover the full teaching loop: plan the lesson, teach it, analyze what the student actually said, write homework that targets what they got wrong, and see every student's progress on one dashboard.

| Skill | Use it when | You get |
|---|---|---|
| **english-tutoring** | You teach one student | A personalized lesson or a whole approved learning path |
| **english-classroom** | You teach a group | Lesson plans with Support, Core and Stretch versions of every activity |
| **english-worksheet** | A student needs homework | Worksheets and an answer key built from that student's real errors |
| **english-analysis** | You recorded a lesson | A transcript, a CEFR level and score, a record update, and Word reports |
| **english-dashboard** | You want to see how your students are doing | One interactive page: every student at a glance, or one student in detail, with score and error trends |

All five are fast first drafts, not replacements for your judgment. Every activity, question, score and note is meant to be reviewed, edited, or swapped. Each skill points to the others when a request fits one better.

## english-tutoring: lessons for one student

**The problem.** A one-on-one lesson only works if it fits the person in front of you: their level, job, hobbies, hometown and goal. Writing that from scratch every week takes time, and it is easy to teach the same words twice or lose track of where a multi-week course is heading.

**What it does**
- Keeps a tutor profile (`_tutor.md`) with your name and standing preferences: vocab candidate and final counts, grammar depth and types, outputs, activity choice and session length. Your name is used for the tutor's side of roleplays and dialogues. Student needs still come first, and a student's own settings or your answer in the session override the profile
- Starts with a teacher interview (detailed or light), or imports old lesson plans and vocabulary lists so earlier work is not repeated
- Designs a multi-lesson learning path as a table you approve or adjust before any lesson is written
- Writes each lesson in a fixed order: objective, a fresh warm-up, review of earlier vocabulary, new vocabulary, grammar focus, a short controlled practice (6 to 8 items in the student's own world), 2 to 3 activities, wrap-up and optional home assignment
- Shows a list of candidate words (about 20 by default, or your profile's number, with definitions and examples) before anything else is written, lets you narrow them fast by number ("cut 2, 5, 7-9"), and builds the whole lesson around those words, each used at least twice
- Picks new vocabulary about one CEFR level above the student, tied to their interests, and never repeats a word already taught. Only the words you keep are logged
- Uses the latest speaking analysis in the student's record to aim the lesson at their real errors and to review the words they were shakiest on
- Lets you choose grammar depth (strong, light or none) and where teacher's notes go (inline, at the end, or not at all)
- Builds activities from a weighted list so staples come up often and intense ones rarely, with an activity log to avoid repeats
- Produces a separate student handout with your private notes removed, and exports editable `.docx` files

**Why it helps**
- "Next lesson for [name]" works in a new session, because the student's profile, path progress and vocabulary log are remembered
- Examples feel written for that student, which keeps lessons engaging
- Lessons build on each other instead of drifting, and old vocabulary keeps coming back for review

## english-classroom: lessons for a group

**The problem.** In a class, one lesson has to work for students at different levels with different backgrounds. Stronger students finish early and weaker ones get lost, and there is no single person whose interests you can build around.

**What it does**
- Interviews you about the class and keeps a class record (profile, optional roster, learning path, activity, warm-up and vocabulary logs)
- Reads the same teacher profile (`_tutor.md`) as english-tutoring, so your name, vocab counts and preferred outputs carry over
- Shows about 20 candidate words first, numbered so you can narrow them by number, and builds the lesson around the ones you keep, each used at least twice
- Follows every grammar focus with a short controlled practice (6 to 8 items in the class's own world) before the activities, and checks that the grammar rule, formula and examples agree
- Plans around themes the whole class shares instead of one student's interests
- Gives every activity three versions: Support (scaffolds such as sentence frames or a word bank), Core, and Stretch (an extra constraint or longer output)
- Suggests groupings for each activity, naming pairs and groups when you have a roster
- Adds a short quick level check to the first lesson while the class levels are only estimated
- Ends with an exit task that is quick to check across the room, and exports a student handout and `.docx` files

**Why it helps**
- One plan serves the whole room, so you spend less time improvising differentiation during class
- Activities are not reused within the last 4 lessons, so a course does not feel repetitive
- The class record lets you pick the course back up in a later session without starting over

## english-worksheet: homework built from real errors

**The problem.** Generic worksheets drill things the student already knows. Targeted homework needs evidence of what this student keeps getting wrong, and gathering that evidence and formatting the sheets by hand takes a long time.

**What it does**
- Builds a student profile from data you already have (a tutoring record, transcripts, a written analysis, old handouts, notes), from a short interview, or from both
- Extracts recurring error patterns with quoted evidence and asks you to confirm the profile
- Proposes a plan table (title, focus, vocabulary review, exercise types, minutes) and waits for your approval before writing
- Writes the number of worksheets you ask for, each on one point only, opening with a clear Grammar Focus box and a Watch out box
- Includes a vocabulary review part of 6 words with a worked example, taken from the student's own list
- Exports typing-friendly `.docx` files (one combined file or one per worksheet) with the answer key as a separate file the student never sees
- Uses the latest speaking Analysis in the student's record as its main evidence: the error patterns become the focus areas, and words marked partial or re-taught decide the vocabulary review
- Plans each Grammar Focus box before drafting it: one topic, steps for a procedure or key points for a choice between forms, every term explained, everything mentioned shown in an example, and the table introducing nothing new
- Checks its own work before export: the focus and Watch out boxes are measured to fit page 1, the steps are walked through on real items, and a learner-eye review (ideally by a fresh subagent that sees only the box and instructions) catches unexplained terms and unclear lines
- Chooses focus points that are worth the learner's time: reliable evidence (machine transcripts invent and hide errors), not too basic for the level, and explained by the learner's first language where possible
- Keeps tasks short and friendly: "Answer about you" questions are neutral and need one short sentence, messages to correct come already inside the answer box, and requirements are bullets
- Reads the student's tutoring record but never changes it

**Why it helps**
- Practice goes where the student's mistakes actually are, in priority order
- Sheets are ready to type into in Word or Google Docs, with a worked example in every exercise
- After english-analysis scores a recorded lesson, the homework starts from that analysis, with no copying and pasting

## english-analysis: turn a recorded lesson into evidence

**The problem.** After a lesson you remember a few mistakes, but not how much the student spoke, which errors repeat, or which old words they still know. Without evidence, the next lesson plan is built on a guess.

**What it does**
- Joins recording chunks (including a zip of numbered parts) into one audio file and transcribes it on your own computer with a local model, so no student audio is uploaded. A per-student glossary of names and terms (clients, teams, acronyms) is given to the model, so they are misheard less often
- Labels tutor and student from context, keeping the student's words word for word and marking any uncertain lines. The model writes only a short list of who speaks when, and a script builds the labeled transcript from it, which keeps the cost per lesson down and flags the turns most worth a second look
- Measures talk-time share, longest turns and filler counts, and shows the student's share and error rate separately for open conversation and tutor-led review, since the two are not comparable
- Scores speaking with a CEFR level (with half-steps such as B1+) and a score out of 100 built from fluency, vocabulary and grammar, each out of 25 in half points, using calibration anchors, a grammar anchor from the error rate, a three-recording average and a plus or minus 3 noise band so scores stay consistent and small changes are not over-read
- Checks which earlier vocabulary the student recalled, needed a hint for, or had to be re-taught
- Tags every grammar and word-choice error with one of 15 codes and keeps an Error Tracker in the student's record: errors per 1,000 words for each lesson, and a status for each code (new, improving, fading, rising, stuck). Counting is done by a script, so trends are comparable from lesson to lesson, and every tagged quote is checked against the transcript so a typo cannot slip into the numbers. After each lesson it also shows five tagged errors next to the student's own turn, so you can confirm the tagging in a minute without reading the transcript
- Saves the transcript to `~/eng-teaching-records/transcripts/` and adds an Analysis section to the student's tutoring record, with strengths, error patterns in priority order and teaching notes that follow your preferences. When you catch up on many past lessons, only the most recent two per student get the full Analysis; older ones are scored and tagged for the tracker and dashboard with a two-line note
- Builds an overall student profile as a Word document (score history, error trends, strengths, what sticks, learning-path progress, what to do next), and, only when you ask, a lesson report for one lesson (what was planned versus delivered, talk time by phase, error table, vocabulary recall, next steps, and a few tips about your own teaching such as long explanations and which questions got long answers)
- Builds a tutor-only one-page summary per student as an editable `.docx` (level, score, strengths, top three things to work on with quoted examples, vocabulary check, talk time, next-lesson focus), on request at any time from the saved analysis. A length limit keeps it to one page

**Why it helps**
- The next lesson plan, and the homework from english-worksheet, start from what the student really said
- You can see progress between recordings and how much of the talking the student does
- A one-page summary you can read in a minute before planning, instead of rereading a long record
- english-tutoring and english-worksheet pick the next grammar point from the tracker, and switch to a different method when a code is stuck
- Student sentences stay in your private record: lessons and worksheets get new sentences with the same kind of error
- Level changes are your decision: the skill reports whether a recording supports the current level and leaves the profile alone until you agree

## english-dashboard: see every student's progress in one page

**The problem.** english-analysis saves scores and error counts lesson after lesson, but they sit in separate files. To see whether a student is improving, or which student needs attention, you would have to reread each record and compare the numbers by hand.

**What it does**
- Reads the ledgers english-analysis already saved (`~/eng-teaching-records/error-ledgers/`) and builds one self-contained HTML file, `~/eng-teaching-records/dashboard/dashboard.html`, that you open in any browser
- **All students view**: total score over time for every student, error rate over time, and a table with level, latest score, last-3 average, change since the last lesson, talk share, errors per 1,000 words and last lesson date. Click a row to focus on that student
- **One student view**, chosen from a list at the top: level, latest score and last-3 average, a total-score chart with a shaded plus or minus 3 band, fluency, vocabulary and grammar lines, error rate per lesson with open conversation and tutor-led review shown separately, the top error codes of the latest lesson, and a code picker that shows one code's trend with recent examples
- Hover over any point or bar for the exact value and date
- Follows the same cautions as english-analysis: every score is plus or minus 3, so judge movement from the last-3 average
- Read-only: it never changes a record, ledger or transcript, and you refresh it by building it again after new lessons

**Why it helps**
- You see at a glance who is improving, who has stalled and where each student's errors are concentrated, instead of reading each record in turn
- The charts show trends that single lesson reports cannot, such as a code that keeps coming back
- Student data stays private: the page makes no network requests (a Content-Security-Policy blocks them), loads no outside library or font, and shows student text as plain text only. It is a local file with owner-only permissions, in the records folder that git does not track
- It needs no recording and no extra install: standard-library Python only

## Shared by all five skills

- American English by default, British on request
- Word banks and matching columns are never in the same order as the items
- Editable `.docx` exports: black text only for lesson plans and handouts (your private notes are removed from the student handout), colorful and typing-friendly for worksheets
- Per-student and per-class records kept outside the repo, so they survive updates
- No em dashes in anything the skills write, so the text reads like a person wrote it

## Setting it up

### Claude.ai or the Claude Desktop app

**On claude.ai (web):**
1. Click your account name in the bottom left, then **Settings**.
2. Open the **Plugins** tab.
3. Click **Add**, then **Add a marketplace**.
4. Enter `ratherlegit/english-teaching` and confirm. This adds the marketplace. It does not install the plugin yet.
5. Still on the **Plugins** tab, search for `english-teaching` and click **Add** to install all the skills.

**On the Claude Desktop app:**
1. Click **Customize** in the left sidebar, then open the **Plugins** tab.
2. Click **Add**, then **Add marketplace**.
3. Choose **Add from a repository**, enter `ratherlegit/english-teaching`, and confirm.
4. Search for `english-teaching` and click **Add** to install it.

Then type `/english-tutoring`, `/english-classroom`, `/english-worksheet`, or `/english-analysis` to get started.

### Claude Code

```
claude plugin marketplace add ratherlegit/english-teaching
claude plugin install english-teaching@english-teaching
```

Then ask in plain English, for example *"Plan a B1 speaking lesson for my student Maria"* or *"Plan a lesson for my class of 12 B1 teens."* To invoke a skill explicitly: `/english-teaching:english-tutoring`, `/english-teaching:english-classroom`, `/english-teaching:english-worksheet`, or `/english-teaching:english-analysis`, or `/english-teaching:english-dashboard`.

If you installed the older standalone `english-tutoring` or `english-classroom` plugins, uninstall them first so you do not get duplicates.

### ChatGPT

Use ChatGPT's **Projects** feature, once per skill:
1. Open the skill's `SKILL.md` (`skills/english-tutoring/SKILL.md`, `skills/english-classroom/SKILL.md`, or `skills/english-worksheet/SKILL.md`), skip the short block between the two `---` lines at the top, and copy everything below it.
2. Download this repository as a ZIP from the green **Code** button and unzip it. Upload that skill's `references/` files to the project.
3. Create a new Project, paste the copied text into its instructions, and ask for lessons as normal.

`english-analysis` is not available this way: it needs a computer that can run `ffmpeg` and `faster-whisper`, so use it in Claude Code or another tool with a shell.

### OpenAI Codex, Cursor, Aider, Windsurf, Gemini CLI, and others

These read `AGENTS.md` automatically. Clone the repo, open it in your tool, and ask for a lesson plan:

```
git clone https://github.com/ratherlegit/english-teaching.git
```

## Exporting to Word

Every lesson plan, handout, path table, and the tutor-only one-page summary can be exported as a `.docx` in black text only. Worksheets are the exception: they use light colors and typed-answer cells. This needs an environment that can run code. Without one, you get clean markdown to paste into Word or Google Docs.

## Where your information is kept

Student profiles and the tutor profile (`_tutor.md`) live in `~/eng-teaching-records/`, class records in `~/eng-teaching-records/classes/`, and worksheet profiles and logs in `~/eng-teaching-records/worksheets/`, outside the skill folders so they survive updates. The worksheet skill reads a student's tutoring record, including its latest Analysis section, but never changes it. One-page student summaries live in `~/eng-teaching-records/one-pagers/`. Lesson transcripts live in `~/eng-teaching-records/transcripts/`, and the analysis skill adds an Analysis section to the student's tutoring record. Analysis needs Python 3 with `faster-whisper` and `ffmpeg` installed (`pip install faster-whisper`). The dashboard skill needs only Python 3 and writes `~/eng-teaching-records/dashboard/dashboard.html`.

## For developers

Run the checks with `python3 tests/validate_skill.py`.

The worksheet skill began as the standalone `english-worksheet` repo, now archived. All updates go here.

## License

MIT. The tools the skills call (`python-docx`, `faster-whisper`, `ffmpeg`) are not bundled: you install them separately, and each keeps its own license.
