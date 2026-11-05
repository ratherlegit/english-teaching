# english-teaching

ESL/EFL lesson-planning and worksheet agents in one repo. This file follows the [AGENTS.md](https://agents.md) convention, read automatically by OpenAI Codex, Cursor, Aider, Windsurf, Gemini CLI, and other coding-agent harnesses.

Pick the skill that matches the request and follow its instructions in full:

- **One student**: `skills/english-tutoring/SKILL.md`. Records live in `~/eng-teaching-records/`.
- **A class of several students**: `skills/english-classroom/SKILL.md`. Records live in `~/eng-teaching-records/classes/`. Never read or modify the one-on-one files from this skill.
- **Homework worksheets for one student**: `skills/english-worksheet/SKILL.md`. Records live in `~/eng-teaching-records/worksheets/`. It may read the student's english-tutoring record, including its latest `## Analysis` section, never write to it. Before drafting each Grammar Focus box it writes a 14-line spec, and before export it runs a measured page check, a walk-through, and a learner-eye review (a fresh subagent given only the box and instructions, if the harness has one).
- **A recorded lesson to transcribe and score**: `skills/english-analysis/SKILL.md`. Writes transcripts to `~/eng-teaching-records/transcripts/` appends an Analysis section to the student's english-tutoring record, builds tutor-only one-page summaries in `~/eng-teaching-records/one-pagers/`, and writes a Word lesson report to `~/eng-teaching-records/lesson-reports/` and an overall student profile to `~/eng-teaching-records/student-profiles/`; a per-student glossary lives in `~/eng-teaching-records/glossaries/`. Needs Python 3 with `faster-whisper`, `python-docx` and `ffmpeg`, so it works only in a harness with a shell.

Each skill reads its own `references/` folder from this repo. Record folders live outside the repo on purpose so they survive updates (create them if missing).

**Exporting to .docx** works on any harness with shell access: run the bundled `scripts/md_to_docx.py` inside the skill's folder (english-worksheet has its own version with typed answer cells, and english-analysis has `one_pager_docx.py` for its one-page summary and `report_docx.py` for its lesson report and student profile) (requires `pip install python-docx`). In a chat-only harness with no code execution, say so plainly and give clean, paste-ready markdown instead.

**Platform notes:**
- **Codex, Aider, Cursor, Windsurf, RooCode/Cline, Gemini CLI**: no setup, just have this repo open.
- **Claude Code**: install as a plugin (see `README.md`).
- **Anything else**: paste the body of the chosen `SKILL.md` (below its YAML frontmatter) into your system prompt along with that skill's `references/` files.
