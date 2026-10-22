# english-teaching

ESL/EFL lesson-planning agents in one repo. This file follows the [AGENTS.md](https://agents.md) convention, read automatically by OpenAI Codex, Cursor, Aider, Windsurf, Gemini CLI, and other coding-agent harnesses.

Pick the skill that matches the request and follow its instructions in full:

- **One student**: `skills/english-tutoring/SKILL.md`. Records live in `~/eng-teaching-records/`.
- **A class of several students**: `skills/english-classroom/SKILL.md`. Records live in `~/eng-teaching-records/classes/`. Never read or modify the one-on-one files from this skill.

Each skill reads its own `references/` folder from this repo. Record folders live outside the repo on purpose so they survive updates (create them if missing).

**Exporting to .docx** works on any harness with shell access: run the bundled `scripts/md_to_docx.py` inside the skill's folder (requires `pip install python-docx`). In a chat-only harness with no code execution, say so plainly and give clean, paste-ready markdown instead.

**Platform notes:**
- **Codex, Aider, Cursor, Windsurf, RooCode/Cline, Gemini CLI**: no setup, just have this repo open.
- **Claude Code**: install as a plugin (see `README.md`).
- **Anything else**: paste the body of the chosen `SKILL.md` (below its YAML frontmatter) into your system prompt along with that skill's `references/` files.
