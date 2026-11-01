# english-teaching

**Lesson-planning and homework assistants for English teachers, in one install.** Four skills come together:

- **english-tutoring**: one student at a time. Interviews you, drafts a personalized lesson or a whole multi-lesson course, and remembers the student for next time.
- **english-classroom**: a class of several students. Plans lessons that work for everyone in the room at once, with Support, Core, and Stretch versions of every activity and suggested groupings.
- **english-worksheet**: homework for one student. Builds a profile from data you already have (or a short interview), then writes the number of worksheets you ask for, each opening with a clear grammar or language focus and built for typing in Word or Google Docs.
- **english-analysis**: a recorded lesson in, a student record update out. Transcribes the audio on your own computer (nothing is uploaded), labels tutor and student, measures talk time, then scores the student's speaking with a CEFR level and a score out of 100 and saves the strengths, error patterns and next steps to their record for the next lesson plan.

Both are fast first drafts, not replacements for your judgment. Every activity, question, and note is meant to be reviewed, edited, or swapped. Each skill points to the other when a request fits it better.

## What you get

- A teacher interview, then a full learning path you approve before any lesson is written
- Personalized vocabulary that never repeats what was already taught, with a review of prior content in every lesson
- A weighted activity list (staples come up often, intense activities come up rarely) plus an activity log so activities do not repeat
- American English by default, British on request
- Editable `.docx` exports, black text only for lesson plans and handouts (your private notes are removed from the student handout), and colorful, typing-friendly worksheets
- Per-student and per-class memory, so "next lesson for [name]" just works

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
