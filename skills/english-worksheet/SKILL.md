---
name: english-worksheet
description: Creates personalized English homework worksheets and answer keys for a single ESL/EFL learner, built from a student profile. The profile comes from existing data (an english-tutoring record, lesson transcripts, a written analysis, old handouts, tutor notes) or from a short interview with the tutor. The tutor chooses how many worksheets, and gets either one combined .docx or one .docx per worksheet. Use when the user asks for worksheets, homework, practice exercises, drills, or a practice pack for an English learner, e.g. "make homework for Maria based on this analysis" or "I need 5 worksheets on articles and past tense for my student". For lesson plans use english-tutoring (one student) or english-classroom (a group).
---

# English Worksheets

Build homework worksheets that target what one learner actually gets wrong, then export them as Word files. The profile is the product: a worksheet pack is only as good as the evidence about the student behind it. Adapt to what the tutor asks for. Do not force steps they have already answered.

## Step 0: Find the student

Look for the student by name before asking anything.

1. `~/eng-teaching-records/worksheets/<name-slug>.md` (lowercase, hyphens). This skill's own file: profile, focus areas, worksheet log. If it exists, load it, skip Step 1, and ask only whether anything changed since last time.
2. `~/eng-teaching-records/<name-slug>.md`, the english-tutoring record. Read-only. Import level, interests, goal, location, English variety, vocabulary log, and grammar already covered. Never write to this file. **If it has an `## Analysis` section** (written by english-analysis from a recorded lesson), read the most recent one and use it as the main evidence for focus areas, as described in `references/student-profile.md` ("Using a saved Analysis").

Create `~/eng-teaching-records/worksheets/` if it does not exist. Records live outside the skill folder on purpose, so they survive updates.

## Step 1: Build the student profile

Ask how the tutor wants to build it, offering these as options:

- **Ingest existing data**: a student record, transcripts, a written analysis, old worksheets or handouts, notes, a folder. Accept file paths, folders, or pasted text.
- **Answer interview questions**.
- **Both**: ingest first, then interview only for the gaps.

**Ingesting.** Read every file fully, then follow `references/student-profile.md` ("Ingesting data") to extract: profile fields, recurring error patterns with quoted evidence, strengths, vocabulary and grammar already taught, and the student's own stated goals and weaknesses. Show the extracted profile in one compact block, then ask the tutor to confirm or correct it. The block must include a vocabulary line that names the source and its size, for example "Vocabulary log: olena.md, about 150 items, last taught 10/25", so the tutor can see the full log is the source and not only recent words. Interview only for missing fields.

**Interviewing.** Offer a **detailed** interview (one question at a time, the default) or a **light** one (four bundled prompts). Use the question set in `references/student-profile.md` ("Interview"). The most important answer is the focus areas: what this student keeps getting wrong, in the tutor's own words. If the tutor cannot say, offer to look at a sample of the student's writing or speech and analyze it.

Save or update the profile file (format in `references/student-profile.md`) once the tutor confirms it.

## Step 2: Plan the worksheets

Ask these, one at a time, never suggesting a default number:

1. **How many worksheets do you want?** The tutor suggests the number.
2. **One combined file, or one file per worksheet?** The file opens straight on worksheet 1: **no cover or overview page**. The worksheets explain themselves, and the plan table goes to the tutor in chat.
3. **Answer key?** Default yes, as a separate file the student never sees.
4. **Vocabulary review?** Ask whenever the student has a vocabulary list or log. Default yes: one vocabulary review part in every worksheet, 6 words plus 1 worked example, taken from the student's own list.
5. Only if not already known: minutes per worksheet (default 15 to 20) and whether speaking or recording tasks are welcome.

Then propose a plan as a table and wait for approval before writing anything:

| # | Title | Focus (from the profile) | Vocabulary review (words and activity) | Exercise types | Minutes |
|---|---|---|---|---|---|

Rules for the plan:
- Order by priority: the most frequent and most noticeable errors first, then the less frequent ones. Within a pack, move from simple to complex where there is a natural order.
- If the tutor wants more worksheets than there are distinct focus areas, split by skill (grammar, vocabulary, speaking, pronunciation, writing, listening) and add review worksheets. If fewer, cover the top priorities and say plainly what was left out.
- **One point per worksheet.** Never combine two separate topics, even if both are on the profile (for example conditionals and future forms). If there are more topics than worksheets, leave one out and say so, or add a worksheet. The title, rule, table, examples, Watch out box, and activities must all be about the same point.
- Vary exercise types across the pack (see `references/exercise-types.md`).
- Never schedule a point the profile marks as mastered or excluded. Treat a point with only one weak piece of evidence as "check first" and say so.

## Step 3: Write the worksheets

Write the whole pack as one markdown file following `references/exercise-types.md` (file format, focus box, exercise catalog, answer key, quality checks). The rules that matter most:

**Focus box and Watch out**
- Open each worksheet with a focus box (called Grammar Focus on every worksheet, including verb patterns and word choice; use Language Focus instead only if the whole pack is vocabulary, and never mix the two names in one pack), then a separate Watch out box. Together they fit one page at most. The page is a ceiling, not a target. Contents and order: "The focus box" in the reference.
- **One point only.** The title, rule, table, examples, and Watch out items are all about the same point. Read them in order before moving on: if the table or examples do not match the rule, the box has two topics, so split it.
- **When a word or pattern has more than one use, say exactly when each applies.** Never state a pattern as always true if it has exceptions ("ask and pay need no word before a person, and for before a thing", not "verbs need to or for"). A table must be a guide for deciding, not only a formula: include a column or line that says when to use each form, with an example for each case.
- **Say it clearly.** Plain words, every term explained or avoided, no vague labels ("normal verb"), and every sentence understandable on its own. Each definition and rule starts on its own line. Use your judgment.
- A table of verb forms gives every subject its own row (I, you, he, she, it, we, they) with its own example sentence. If a table has no complete sentences, label every example with the form it shows ("Past simple, finished time: ...").
- The Watch out box has exactly 2 mistakes, each written "Don't use: ... Use: ..." and followed by a brief *Why:* in italics: one short sentence that gives the reason, not a repeat of the rule ("Why: yesterday is a finished time, and the present perfect cannot go with a finished time"). Never leave a correction without its reason.

**Activities**
- Provide the forms; never ask the student to write out forms in a list. Put the table in the focus box, then have the student use it in several activities, including writing.
- **Add a vocabulary review part** to every worksheet (unless the tutor said no): 6 words plus a worked example, from the student's own list, before the final writing task, with a different activity type in each worksheet. Prefer words not yet reviewed, skip niche or vulgar words, and reuse the worksheet's grammar where you can.
- Every item has exactly one correct answer unless it is labeled open. Test each item for a second acceptable answer (tense and article items especially) and add a detail that rules it out. Items use new sentences, never ones from the focus box or dialogue. State how many mistakes or gaps there are.
- Questions and writing prompts are about the student's real life, specific, in the right time frame, and make sense for how their life really runs (occasional events are not treated as regular). The natural answer uses the target form.
- **Design for typing.** Students type in the same Word or Google Docs file. Give each item a "Your answer" cell and use a `:::write` box for writing tasks. Never write "circle," "underline," or "draw a line." Gap-fills use plain blanks with no numbers inside the gaps, and the answers go in order in a `#` and `Your answer` table. Put a worked example as row 0 of every answer table.

**Student-facing language**
- Address the student in the second person. Be concise and clear: match the wording to the CEFR level, but never let simple wording make an item vague. Name the specific thing.
- **Never mention the tutor, teacher, instructor, or "the student".** For recordings, write "bring it to your next lesson".
- Personalize with the student's work, interests, and real situations. Do not copy the student's own error sentences. Write fresh sentences with the same error type.
- Do not mark acceptable informal English as wrong. Never reuse a word the profile lists as taught, unless the worksheet is reviewing it.
- No em dashes. No small label lines above headings.

**Look**
- Blue is the main color of every worksheet. Other elements use other light colors (yellow word banks, soft red Watch out boxes, green examples). Keep fills light so typed text is readable. Emoji icons in part headings are fine. Use an image only when a real file exists; never invent a path.

Before building, read every focus box and instruction as the student would, and rewrite anything vague. Then scan the student-facing text for the words *tutor*, *teacher*, *instructor*, and *student* (case-insensitive), and for *circle*, *underline*, *cross out*, *tick*, and *draw*, and rewrite every hit. Do this every time. Then run the walk-through check and the measured page-budget check from Quality checks in `references/exercise-types.md`, and write down the steps for at least one item per part. A box that tells the student to do something must show it done in its examples.

## Step 4: Build the files

Ask where to save if the tutor has not said; default to `~/Downloads/<student-slug>-worksheets/`. Run the bundled exporter from the skill folder (needs `pip install python-docx`):

- **Combined file**: `python3 scripts/md_to_docx.py pack.md out/pack.docx`
- **One file per worksheet**: `python3 scripts/md_to_docx.py pack.md out/ --split`
- The answer key is a separate markdown file exported the same way, never merged into the student's file.

If there is no shell access, say so plainly and give clean markdown to paste instead. If rendering is available (LibreOffice), look at the pages. On macOS without it, `qlmanage -t -s 1400 -o <dir> file.docx` makes a first-page preview, but it ignores table widths and page breaks, so it only confirms fonts, borders, and shading. If nothing can render the file, tell the tutor the layout was not visually checked.

## Step 5: Update the record

Append to the Worksheet Log in the student's worksheet profile: date, titles, focus areas covered, and the vocabulary words reviewed in each worksheet, so the next pack rotates to other words. Add new "already practiced" vocabulary. Offer to adjust the plan after the tutor has seen how the student did, and fold any new errors back into the Focus Areas table.

## Reference files

- `references/student-profile.md`: how to ingest data, the interview question set, and the profile file format. Read in Step 1.
- `references/exercise-types.md`: worksheet anatomy, exercise catalog with sizing, speaking tasks, answer key format, and quality checks. Read in Steps 2 and 3.
