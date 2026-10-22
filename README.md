# english-teaching

**Lesson-planning assistants for English teachers, in one install.** Two skills come together:

- **english-tutoring**: one student at a time. Interviews you, drafts a personalized lesson or a whole multi-lesson course, and remembers the student for next time.
- **english-classroom**: a class of several students. Plans lessons that work for everyone in the room at once, with Support, Core, and Stretch versions of every activity and suggested groupings.

Both are fast first drafts, not replacements for your judgment. Every activity, question, and note is meant to be reviewed, edited, or swapped. Each skill points to the other when a request fits it better.

## What you get

- A teacher interview, then a full learning path you approve before any lesson is written
- Personalized vocabulary that never repeats what was already taught, with a review of prior content in every lesson
- A weighted activity list (staples come up often, intense activities come up rarely) plus an activity log so activities do not repeat
- American English by default, British on request
- Editable `.docx` exports in black text only, plus a clean student handout with your private notes removed
- Per-student and per-class memory, so "next lesson for [name]" just works

## Setting it up

### Claude.ai or the Claude Desktop app

**On claude.ai (web):**
1. Click your account name in the bottom left, then **Settings**.
2. Open the **Plugins** tab.
3. Click **Add**, then **Add a marketplace**.
4. Enter `ratherlegit/english-teaching` and confirm. This adds the marketplace. It does not install the plugin yet.
5. Still on the **Plugins** tab, search for `english-teaching` and click **Add** to install both skills.

**On the Claude Desktop app:**
1. Click **Customize** in the left sidebar, then open the **Plugins** tab.
2. Click **Add**, then **Add marketplace**.
3. Choose **Add from a repository**, enter `ratherlegit/english-teaching`, and confirm.
4. Search for `english-teaching` and click **Add** to install it.

Then type `/english-tutoring` or `/english-classroom` to get started.

### Claude Code

```
claude plugin marketplace add ratherlegit/english-teaching
claude plugin install english-teaching@english-teaching
```

Then ask in plain English, for example *"Plan a B1 speaking lesson for my student Maria"* or *"Plan a lesson for my class of 12 B1 teens."* To invoke a skill explicitly: `/english-teaching:english-tutoring` or `/english-teaching:english-classroom`.

If you installed the older standalone `english-tutoring` or `english-classroom` plugins, uninstall them first so you do not get duplicates.

### ChatGPT

Use ChatGPT's **Projects** feature, once per skill:
1. Open the skill's `SKILL.md` (`skills/english-tutoring/SKILL.md` or `skills/english-classroom/SKILL.md`), skip the short block between the two `---` lines at the top, and copy everything below it.
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

Student profiles live in `~/eng-teaching-records/` and class records in `~/eng-teaching-records/classes/`, outside the skill folders so they survive updates.

## For developers

Run the checks with `python3 tests/validate_skill.py`.

## License

MIT
