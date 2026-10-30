---
name: english-worksheet
description: Creates personalized English homework worksheets and answer keys for a single ESL/EFL learner, built from a student profile. The profile comes from existing data (an english-tutoring record, lesson transcripts, a written analysis, old handouts, tutor notes) or from a short interview with the tutor. The tutor chooses how many worksheets, and gets either one combined .docx or one .docx per worksheet. Use when the user asks for worksheets, homework, practice exercises, drills, or a practice pack for an English learner, e.g. "make homework for Maria based on this analysis" or "I need 5 worksheets on articles and past tense for my student". For lesson plans use english-tutoring (one student) or english-classroom (a group).
---

# English Worksheets

Build homework worksheets that target what one learner actually gets wrong, then export them as Word files. The profile is the product: a worksheet pack is only as good as the evidence about the student behind it. Adapt to what the tutor asks for. Do not force steps they have already answered.

## Step 0: Find the student

Look for the student by name before asking anything.

1. `~/eng-teaching-records/worksheets/<name-slug>.md` (lowercase, hyphens). This skill's own file: profile, focus areas, worksheet log. If it exists, load it, skip Step 1, and ask only whether anything changed since last time.
2. `~/eng-teaching-records/<name-slug>.md`, the english-tutoring record. Read-only. Import level, interests, goal, location, English variety, vocabulary log, and grammar already covered. Never write to this file.

Create `~/eng-teaching-records/worksheets/` if it does not exist. Records live outside the skill folder on purpose, so they survive updates.

## Step 1: Build the student profile

Ask how the tutor wants to build it, offering these as options:

- **Ingest existing data**: a student record, transcripts, a written analysis, old worksheets or handouts, notes, a folder. Accept file paths, folders, or pasted text.
- **Answer interview questions**.
- **Both**: ingest first, then interview only for the gaps.

**Ingesting.** Read every file fully, then follow `references/student-profile.md` ("Ingesting data") to extract: profile fields, recurring error patterns with quoted evidence, strengths, vocabulary and grammar already taught, and the student's own stated goals and weaknesses. Show the extracted profile in one compact block, then ask the tutor to confirm or correct it. Interview only for missing fields.

**Interviewing.** Offer a **detailed** interview (one question at a time, the default) or a **light** one (four bundled prompts). Use the question set in `references/student-profile.md` ("Interview"). The most important answer is the focus areas: what this student keeps getting wrong, in the tutor's own words. If the tutor cannot say, offer to look at a sample of the student's writing or speech and analyze it.

Save or update the profile file (format in `references/student-profile.md`) once the tutor confirms it.

## Step 2: Plan the worksheets

Ask these, one at a time, never suggesting a default number:

1. **How many worksheets do you want?** The tutor suggests the number.
2. **One combined file, or one file per worksheet?** Both can include an overview page.
3. **Answer key?** Default yes, as a separate file the student never sees.
4. Only if not already known: minutes per worksheet (default 15 to 20) and whether speaking or recording tasks are welcome.

Then propose a plan as a table and wait for approval before writing anything:

| # | Title | Focus (from the profile) | Exercise types | Minutes |
|---|---|---|---|---|

Rules for the plan:
- Order by priority: the most frequent and most noticeable errors first, then the less frequent ones. Within a pack, move from simple to complex where there is a natural order.
- If the tutor wants more worksheets than there are distinct focus areas, split by skill (grammar, vocabulary, speaking, pronunciation, writing, listening) and add review worksheets. If fewer, cover the top priorities and say plainly what was left out.
- One main focus per worksheet. Two small related points can share one only if the focus box still fits half a page.
- Vary exercise types across the pack (see `references/exercise-types.md`).
- Never schedule a point the profile marks as mastered or excluded. Treat a point with only one weak piece of evidence as "check first" and say so.

## Step 3: Write the worksheets

Write the whole pack as one markdown file following `references/exercise-types.md` (worksheet anatomy, exercise catalog, answer key format). Apply these rules to every worksheet:

- **Open with a short focus box** (Grammar Focus on grammar worksheets, Language Focus on vocabulary and phrase worksheets). **Budget: about half a page, never more than one page.** It holds the rule in one or two plain sentences, one small provided table or pattern (at most 6 rows), exactly 4 examples that show the point used in different ways (for example a statement, a question, a negative, and a different work situation), and a brief dialogue of 3 lines ("In real use") with the target in bold. **Say it clearly:** every term in the box is explained in plain words the first time it appears, with an example, and no vague category word is used (never "normal," "regular," "special," or "basic" verbs). Name a group by what it does ("action verb: a word for something you do"), and do not use grammar terms the student has not met, or define them on the spot. Show the contrast in the table with full example sentences, not isolated words. Follow it with a separate Watch out box holding exactly 2 common mistakes, each written "Don't use: ... Use: ..." with an optional few-word reason in brackets. Never write "Not" and "Yes". No extra sections. If the point needs more room, narrow the focus or suggest another worksheet. A second point that does not fit gets one line of hint in the instructions of the activity that uses it.
- **Provide the forms, never ask the student to produce them in a list.** Do not ask the student to write out every form of a verb or fill in a table of forms. Put the table in the focus box, then make the student use it in different ways across the activities: choose the right form in a message, repair a short text, answer questions about their own work, build a sentence from a prompt, write a short paragraph.
- **Make it look good.** Color and images are welcome. Blue is the main color for every worksheet (banner, headings, table headers, focus box). Other elements use other light colors: yellow word banks, soft red Watch out boxes, green worked examples. Keep all fills light so typed text stays readable. Light icons or emoji in part headings are fine (for example a pencil for writing). Use an image only when there is a real file for it (a tutor-provided photo, or one an image tool in your harness produced). Never invent a path. Keep text easy to read: dark text on light tints, white text only on the dark banner and header colors.
- **Design for typing.** Students work on a computer in the same Word or Google Docs file. They will not circle, underline, cross out, tick, or draw. Give each item a "Your answer" cell to type in (a table whose last column is headed `Your answer`) and use a `:::write` box for writing tasks. Ask the student to type a word, a letter, or a sentence. Never write "circle," "underline," or "draw a line."
- **Gap-fills: no numbers inside the gaps.** Write each gap as a plain blank (`______`), say how many gaps there are, and have the student type the answers in order in a two-column table headed `#` and `Your answer`. Do not add a column that repeats the gap. A third column is only for something useful, like the base verb to change.
- **Worked example as row 0.** In every answer table, put the example as row `0`, in the same format as the real items, with the answer filled in. The exporter shades it green. For a gap-fill text, fill the first gap in bold in the text and show it as row 0. Do not put the example in the instruction line.

Apply these rules to every student-facing line:

- Address the student in the second person. Write in simple English matched to the CEFR level, and simpler than the exercise content. Short instructions beat clever ones.
- **Never mention the tutor, teacher, instructor, or "the student".** For recordings, write "bring it to your next lesson", not "send it to your tutor".
- Personalize: use the student's work, interests, location, and real situations in the example sentences. Do not copy the student's own error sentences verbatim as exercise items. Write fresh sentences with the same error type.
- Every exercise item has exactly one correct answer, unless it is labeled open. Check gap-fills and multiple choice so a distractor cannot also truthfully complete the sentence.
- **Questions must make sense in the student's real life.** Check each question against how their work and week really run. Do not ask about something that is not constant or regular as if it were (for example, tournaments are occasional, so do not ask "Are your tournaments busy this month?"). Use their schedule, a recent trip, or a regular event instead.
- **A writing prompt names something real and specific, in the right time frame.** If the target is the past, point to an event the student really went to ("a tournament or trip you went to recently") and ask what happened, so the prompt cannot be answered in the wrong tense. Do the same for future plans ("next week") and habits ("every week").
- Do not mark acceptable informal English as wrong. If a form is understandable but less usual, say so in the answer key.
- Never reuse a vocabulary word the profile lists as taught, unless the worksheet is reviewing it.
- No em dashes anywhere. No small label lines above headings (the part headings and box titles are fine).

Before building, scan the student-facing text for the words *tutor*, *teacher*, *instructor*, and *student* (case-insensitive), and for *circle*, *underline*, *cross out*, *tick*, and *draw*, and rewrite every hit. Do this every time.

## Step 4: Build the files

Ask where to save if the tutor has not said; default to `~/Downloads/<student-slug>-worksheets/`. Run the bundled exporter from the skill folder (needs `pip install python-docx`):

- **Combined file**: `python3 scripts/md_to_docx.py pack.md out/pack.docx`
- **One file per worksheet**: `python3 scripts/md_to_docx.py pack.md out/ --split`
- The answer key is a separate markdown file exported the same way, never merged into the student's file.

If there is no shell access, say so plainly and give clean markdown to paste instead. If rendering is available (LibreOffice), look at the pages. On macOS without it, `qlmanage -t -s 1400 -o <dir> file.docx` makes a first-page preview, but it ignores table widths and page breaks, so it only confirms fonts, borders, and shading. If nothing can render the file, tell the tutor the layout was not visually checked.

## Step 5: Update the record

Append to the Worksheet Log in the student's worksheet profile: date, titles, focus areas covered, and the vocabulary used. Add new "already practiced" vocabulary. Offer to adjust the plan after the tutor has seen how the student did, and fold any new errors back into the Focus Areas table.

## Reference files

- `references/student-profile.md`: how to ingest data, the interview question set, and the profile file format. Read in Step 1.
- `references/exercise-types.md`: worksheet anatomy, exercise catalog with sizing, speaking tasks, answer key format, and quality checks. Read in Steps 2 and 3.
