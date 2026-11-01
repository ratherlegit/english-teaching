# english-teaching

**Planning, homework and lesson-review assistants for English teachers, in one install.** Four skills cover the full teaching loop: plan the lesson, teach it, analyze what the student actually said, then write homework that targets what they got wrong.

| Skill | Use it when | You get |
|---|---|---|
| **english-tutoring** | You teach one student | A personalized lesson or a whole approved learning path |
| **english-classroom** | You teach a group | Lesson plans with Support, Core and Stretch versions of every activity |
| **english-worksheet** | A student needs homework | Worksheets and an answer key built from that student's real errors |
| **english-analysis** | You recorded a lesson | A transcript, a CEFR level and score, and a record update |

All four are fast first drafts, not replacements for your judgment. Every activity, question, score and note is meant to be reviewed, edited, or swapped. Each skill points to the others when a request fits one better.

## english-tutoring: lessons for one student

**The problem.** A one-on-one lesson only works if it fits the person in front of you: their level, job, hobbies, hometown and goal. Writing that from scratch every week takes time, and it is easy to teach the same words twice or lose track of where a multi-week course is heading.

**What it does**
- Starts with a teacher interview (detailed or light), or imports old lesson plans and vocabulary lists so earlier work is not repeated
- Designs a multi-lesson learning path as a table you approve or adjust before any lesson is written
- Writes each lesson in a fixed order: objective, a fresh warm-up, review of earlier vocabulary, new vocabulary, grammar focus, 2 to 3 activities, wrap-up and optional home assignment
- Picks new vocabulary about one CEFR level above the student, tied to their interests, and never repeats a word already taught
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
- Interviews you about the class and keeps a class record (profile, optional roster, learning path, activity and vocabulary logs)
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
- Reads the student's tutoring record but never changes it

**Why it helps**
- Practice goes where the student's mistakes actually are, in priority order
- Sheets are ready to type into in Word or Google Docs, with a worked example in every exercise
- You can paste in an analysis from a recorded lesson and get homework from it in one step

## english-analysis: turn a recorded lesson into evidence

**The problem.** After a lesson you remember a few mistakes, but not how much the student spoke, which errors repeat, or which old words they still know. Without evidence, the next lesson plan is built on a guess.

**What it does**
- Joins recording chunks (including a zip of numbered parts) into one audio file and transcribes it on your own computer with a local model, so no student audio is uploaded
- Labels tutor and student from context, keeping the student's words word for word and marking any uncertain lines
- Measures talk-time share, longest turns and filler counts
- Scores speaking with a CEFR level (with half-steps such as B1+) and a score out of 100 built from fluency, vocabulary and grammar, each out of 25, using calibration anchors so scores stay consistent
- Checks which earlier vocabulary the student recalled, needed a hint for, or had to be re-taught
- Saves the transcript to `~/eng-teaching-records/transcripts/` and adds an Analysis section to the student's tutoring record, with strengths, error patterns in priority order and teaching notes that follow your preferences
- Builds a tutor-only one-page summary per student as an editable `.docx` (level, score, strengths, top three things to work on with quoted examples, vocabulary check, talk time, next-lesson focus), on request at any time from the saved analysis. A length limit keeps it to one page

**Why it helps**
- The next lesson plan, and the homework from english-worksheet, start from what the student really said
- You can see progress between recordings and how much of the talking the student does
- A one-page summary you can read in a minute before planning, instead of rereading a long record
- Level changes are your decision: the skill reports whether a recording supports the current level and leaves the profile alone until you agree

## Shared by all four skills

- American English by default, British on request
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

Then ask in plain English, for example *"Plan a B1 speaking lesson for my student Maria"* or *"Plan a lesson for my class of 12 B1 teens."* To invoke a skill explicitly: `/english-teaching:english-tutoring`, `/english-teaching:english-classroom`, `/english-teaching:english-worksheet`, or `/english-teaching:english-analysis`.

If you installed the older standalone `english-tutoring` or `english-classroom` plugins, uninstall them first so you do not get duplicates.

### ChatGPT

Use ChatGPT's **Projects** feature, once per skill:
1. Open the skill's `SKILL.md` (`skills/english-tutoring/SKILL.md`, `skills/english-classroom/SKILL.md`, or `skills/english-worksheet/SKILL.md`), skip the short block between the two `---` lines at the top, and copy everything below it.
2. Download this repository as a ZIP from the green **Code** button and unzip it. Upload that skill's `references/` files to the project.
3. Create a new Project, paste the copied text into its instructions, and ask for lessons as normal.

### OpenAI Codex, Cursor, Aider, Windsurf, Gemini CLI, and others

These read `AGENTS.md` automatically. Clone the repo, open it in your tool, and ask for a lesson plan:

```
git clone https://github.com/ratherlegit/english-teaching.git
```

## Exporting to Word

Every lesson plan, handout, and path table can be exported as a `.docx` in black text only. This needs an environment that can run code. Without one, you get clean markdown to paste into Word or Google Docs.

## Where your information is kept

Student profiles live in `~/eng-teaching-records/`, class records in `~/eng-teaching-records/classes/`, and worksheet profiles and logs in `~/eng-teaching-records/worksheets/`, outside the skill folders so they survive updates. The worksheet skill reads a student's tutoring record but never changes it. Lesson transcripts live in `~/eng-teaching-records/transcripts/`, and the analysis skill adds an Analysis section to the student's tutoring record. Analysis needs Python 3 with `faster-whisper` and `ffmpeg` installed (`pip install faster-whisper`).

## For developers

Run the checks with `python3 tests/validate_skill.py`.

The worksheet skill began as the standalone `english-worksheet` repo, now archived. All updates go here.

## License

MIT
