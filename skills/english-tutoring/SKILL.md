---
name: english-tutoring
description: Develops lesson plans for one-on-one English tutoring of a single ESL/EFL learner (non-native speaker, general English or exam prep). Use when the user asks to create, draft, or plan an English lesson or unit for one student — e.g. "write a lesson plan for present perfect for my student Maria", "I need a 45-minute ESL lesson on phrasal verbs for my tutee", or "help me teach conditionals to my intermediate student". Covers grammar, vocabulary, speaking, listening, reading, and writing lessons across CEFR levels A1-C2, and can build single lessons or multi-lesson units. For a class of several students (group classes, mixed levels), use english-classroom instead.
---

# ESL Lesson Plans

Build classroom-ready English lesson plans for ESL/EFL learners. Adapt structure, depth, and format to what the user asks for — don't force a template they didn't request.

**This skill covers one-on-one tutoring only.** Group classes need different personalization logic (shared themes instead of one student's interests, per-student differentiation, etc.) and are handled by the separate `english-classroom` skill — if the tutor describes a class of several students, point them to that skill rather than stretching this one to fit.

## Step 0: Check for a returning student

Before interviewing anyone, check whether the tutor is naming a student you already have a record for — e.g. "give me the next lesson for [student name]," or any request naming a student by name. Look for `~/eng-teaching-records/<name-slug>.md` (lowercase, hyphens for spaces).

**Records live outside the skill's own folder, at `~/eng-teaching-records/`, not inside `~/.claude/skills/english-tutoring/`.** This is deliberate: a student's profile, path, and vocab history are personal data that must survive skill updates, reinstalls, or repackaging — they must never be at risk of being wiped out along with the skill's own files. Create `~/eng-teaching-records/` if it doesn't exist yet.

- **If a record exists**: skip Step 1 entirely — do not re-run the interview. Load the student's profile, learning path (if any), and vocab log straight from that file. Ask only a brief check-in: whether anything's changed (interests, exclusions, session length, etc.). If the record has no English variety, treat it as American without asking.
  - **If there's an active learning path**: remind the tutor what's next (the next "Not yet delivered" row: lesson name, theme, grammar point) and confirm that's still what they want before generating it — don't just assume the path is unchanged. Give them the chance to request something different for this lesson (a different theme, a specific activity, skip ahead, etc.) instead of only offering yes/no.
  - **If there's no learning path** (the student has only ever had one-off lessons): offer to design one now, but make clear it's optional — a tutor who just wants another standalone lesson shouldn't feel pushed into planning a whole path. If they decline or don't respond to the offer, proceed with a single lesson as normal.
  - Then go straight to Step 3/4 to build that lesson (or Step 2 first, if a new path was just approved).
- **If no record exists** for that name, or this is the first time this student is mentioned: run the full Step 1 interview as normal, then create the record at the end of Step 1 (and update it after Step 2/4, per the Student Record File section below).

This is what makes "next lesson for [student name]" work in a brand-new session without re-asking their level, interests, goal, or path from scratch.

## Step 1: Interview the tutor

Before drafting, ask the tutor about the student — this is what turns a generic plan into one that actually fits the learner. Don't skip this for a one-off "just give me a lesson on X" request; ask briefly first, unless Step 0 found an existing record for this student.

**First, ask whether they want a detailed or light interview, with detailed as the default.** Detailed asks each item as its own question; light bundles the same information into a handful of open-ended prompts. Both gather the same information — light is just faster to answer, at the cost of the tutor doing more free-text writing per prompt instead of picking from options. If the tutor doesn't express a preference, proceed with detailed.

### Detailed mode
Ask for the following as **separate questions**, in this order — don't merge distinct pieces of information into one combined question, even when batching several questions into one round:
- **Student name**, asked first. This is always **free text entered by the tutor** — never offer suggested/example names as options; a name isn't a preference to pick from a list
- **Pronouns**, asked second — he/him, she/her, or they/them. Use this consistently in the plan rather than defaulting to "they" or guessing from the name
- **Current level** — CEFR estimate if known, or "not sure" (offer to help gauge it from a description of what they can/can't do)
- **Location/hometown or country** — ask for the specific place the student is from (city and/or country, e.g. "Barcelona" or "Naples"), not a language-family multiple choice. This is a free-text question like the student's name. Use the specific place as real personalization material (weave in local references, regional context, culturally relevant topics — a Barcelona student and a Naples student shouldn't get interchangeable "European" content). Silently infer the native language and likely L1-interference patterns from the location using `references/student-interview.md`'s cheat sheet — this informs your error-anticipation without needing to surface CEFR/linguistics jargon back to the tutor
- **Interests / profession / hobbies** — used to personalize example sentences and topics, which drives engagement far more than generic content
- **Goal for learning English** — exam, travel, work, immigration, general fluency — this should steer topic and skill choice as much as the level does
- **English variety** — American or British English. Offer **American (default)** first and British second. It controls spelling (color/colour, organize/organise), vocabulary (apartment/flat, elevator/lift), and example places and references. The tutor is American, so if they skip or don't answer, use American
- **Session length** — its own question, distinct from activity preferences. Offer concrete options such as 30 minutes, 60 minutes, or "something else" (let the tutor specify), and ask separately about frequency if relevant
- **Activity choice** — its own question. The tutor likely doesn't know what's in `references/teacher-activities.md`, so don't just ask "random or specific" cold. Offer three options: (a) **random** — you pick from the proven activities list each time, (b) the tutor **already has specific activities in mind** (their own, not necessarily from the list) and will name them, or (c) **show me the list first** — in which case display the activity names from `references/teacher-activities.md` (names alone are enough, not the full descriptions), then re-ask whether they want random selection or want to name specific ones now that they've seen it
- **Single lesson or learning path** — ask only whether it's one lesson or a multi-lesson path. **If a path is chosen, immediately ask how many lessons as the very next question**, before moving on to anything else — don't leave it implicit or bundle it with later questions, and never suggest or default to a specific number
- **Key skills to focus on** — if a path, which skills should get the most weight (e.g. speaking fluency, exam writing, listening comprehension) — this biases activity/theme selection across the whole path, not just one lesson
- **Anything else to incorporate or exclude** — e.g. topics to avoid (sensitive for this student), a coursebook/curriculum to align with, grammar points already mastered (skip re-teaching) or specifically requested
- **Prior work with this student (always the last question)** — ask whether the tutor has any documents from earlier work with this student (old lesson plans, handouts, vocab lists, notes, a coursebook unit) that they can share, by file path, folder, or pasted text. See "Importing prior work" below. "No, they're new to me" is a fine answer and ends the interview

### Light mode
Same information, bundled into four open-ended prompts instead of ~11 separate questions. Ask them one at a time, in order — each answer can be a short free-text paragraph covering multiple things at once:
1. "What's the student's name, pronouns, and current level (or describe what they can/can't do if you're not sure)?"
2. "Where are they from, and what are their interests, profession, or hobbies?"
3. "What's their goal for learning English, how long are your sessions (30 min, 60 min, other), and do you want American or British English (American is the default)?"
4. "Is this a single lesson or a learning path (if a path, how many lessons)? And any preferences for activities or things to include/exclude — or just say 'you choose' for defaults."

After the four prompts, ask the same closing question as detailed mode: "Do you have any documents from earlier work with this student (old lesson plans, handouts, vocab lists, notes) that I can look at so I don't repeat their vocabulary?"

Parse each free-text answer into the same underlying fields as detailed mode (name, pronouns, level, location, interests, goal, English variety, session length, single/path + count, activity choice, key skills, exclusions) before moving to Step 2 — light mode changes how the questions are asked, not what ends up stored in the record. If an answer leaves something out or is ambiguous, ask a quick one-off follow-up for just that item rather than guessing.

### Importing prior work
If the tutor shares prior documents, read them all (`.docx`, `.pdf`, `.md`, `.txt`, or pasted text) before building the record, and pull out:
- **Every vocabulary word or phrase previously taught or practiced.** Add them to the student's Vocabulary Log under a heading like `### Imported from prior work (<source file or description>)`, so Fresh Vocabulary never presents them as new (the existing "never repeat a word already taught" rule covers them). They remain eligible for Vocab Review, where recycling them is encouraged
- Grammar points already covered, so they're skipped or only recycled (note them in the profile's Exclusions or as "already covered")
- Anything useful for personalization the tutor didn't mention (interests, recurring errors, topics that landed well)

Show the tutor the extracted vocab list in one compact block and ask them to confirm or correct it before saving. If a document can't be read, say so plainly and ask for a pasted copy. If the tutor has nothing to share, move on; they can offer documents later and you import them the same way.

Either mode: **do not ask about vocab preferences or home assignments in this initial round.** Those only matter once an actual lesson is being written (see Step 4) — a tutor who's just asking for a learning path shouldn't have to answer questions about a single lesson's vocab section yet.

See `references/student-interview.md` for the full question set, why each matters, and an L1-interference cheat sheet to use once you know the student's location (map it to a likely native language yourself).

For a returning student with an existing record (see Step 0), don't run this interview at all beyond the brief check-in described there. If they've got new prior-work documents to add, import them the same way.

## Step 2: Design the learning path

Skip this step only when the tutor asked for a single standalone lesson. Whenever more than one lesson is requested, design the full path **before** writing any individual lesson plan, and share it with the tutor for approval/adjustment before drafting lesson content.

Output the path as a table:

| Lesson # | Lesson Name | Theme | Grammar Point | Activity Type(s) |
|---|---|---|---|---|
| 1 | ... | ... | ... | ... |

The Activity Type(s) column can list 2-3 activities per lesson, since Step 4 builds out that many for the Production stage — the path table is just the preview of what each lesson will offer.

Rules for building the path:
- **Grammar depth per lesson**: if the tutor wants no grammar focus for a lesson, write "None" in its Grammar Point column; for a light focus, still name the point but note "(light)". Ask the strong/light/none question (see Step 4) when designing the path if the tutor hasn't said, and let them vary it per lesson
- **Vary grammar points** across lessons, all appropriate to the student's level — don't drill one structure for the whole path unless the tutor specifically asked for that. Use `references/cefr-levels.md` to keep every grammar point within (or just at the edge of) the student's level, and sequence roughly from simpler to more complex where there's a natural order (e.g. present simple before present perfect before third conditional)
- **Vary activity types** across the path, pulling primarily from `references/teacher-activities.md`. Repetition of an activity is fine in longer paths, but space repeats out — don't repeat an activity within at least 3-4 lessons of its last use, and never back-to-back
- **Keep external-material activities rare across the path too** — default to the generated, self-contained activities (see "Choosing the activities" in Step 4) and don't schedule the found-article/media-clip activities back-to-back or in most lessons; one every few lessons at most, only where it clearly fits
- **Weight toward the tutor's stated key skills** — if speaking fluency was flagged as the focus, more lessons should land on speaking-heavy activities (Role Play, Mini Debates, Press conference, etc.) than on receptive-only ones, without abandoning variety entirely
- **Respect exclusions** — never schedule an excluded topic or a grammar point the tutor said is already mastered or off-limits
- Themes should track the student's interests and goal, varying enough that the path doesn't feel repetitive, while still building toward the stated overall goal

**Do not generate any lesson plans immediately after presenting the path.** After sharing the path table, ask the tutor whether they'd like any adjustments to it, or would like Lesson 1 generated. Only proceed to Step 3/4 for Lesson 1 once they say so — never generate the whole path's lessons in one go, and never generate even Lesson 1 before this check-in. Once Lesson 1 is delivered, ask before generating the next one, following Steps 3-4 for each using that lesson's row as the spec (theme, grammar point, activity type) rather than re-deciding those from scratch.

Once the tutor approves the path (even before any lesson is generated), save it into the student's record file (see Step 4's Student Record File section) with a Status column (all rows start "Not yet delivered"). This is what lets a future session pick up with "next lesson for [student name]" without the path having to be re-designed or re-approved.

Once the path is approved, also ask the tutor whether they'd like the path table exported as a `.docx` — it's a handy reference file to save outside the chat (e.g. to share with the student or a co-teacher, or to check off lessons as they're delivered). If yes, follow Step 6 to build it. This is separate from, and in addition to, the per-lesson export offer in Step 6.

## Step 3: Pick a framework

Default to **PPP (Presentation-Practice-Production)** for grammar/vocab lessons unless the user asks for something else or the goal is clearly task-based (e.g. exam prep, project work) or skills-focused (e.g. a reading/listening lesson, which fits better as pre-/during-/post-task).

See `references/lesson-frameworks.md` for framework options (PPP, TBL, ESA, receptive-skills pre/during/post) and when each fits.

## Step 4: Build the plan

If this lesson comes from an approved learning path, use that row's theme, grammar point, and activity type as given rather than re-choosing them — Step 4 is about fleshing them out into a full plan, not re-deciding the fundamentals.

### Lesson-specific questions (ask now, not during Step 1)
Before drafting, if not already answered for this student, ask:
- **Vocab constraint** — any preference for the fresh vocabulary section: phrasal verbs specifically, a certain part of speech (nouns, adjectives, etc.), or no constraint (default: mixed, chosen to fit the topic/interest)
- **Home assignment** — whether to include a take-home assignment section (default: include, unless the tutor opts out)
- **Grammar focus depth** — ask whether the lesson's grammar focus should be **strong** (detailed instruction, deeply integrated into the practice and activities), **light** (brief overview, with the grammar lightly woven into the other activities), or **none** (no grammar focus at all, just topical activities). Explain each option in one short line as you ask. If the lesson comes from a learning path, the tutor can pick per lesson; reuse the answer for later lessons unless they want to change it
- **Teacher's notes** — pedagogical rationale, timing/pacing tips, anticipated difficulties, and alternative approaches for the tutor's own reference (not shown to the student). Ask whether these should be **integrated** throughout the plan (a short note under each relevant stage), **end-only** (a single "Teacher's Notes" section after everything else), or **not included** at all. Default: **integrated** — plenty of tutors find inline notes useful, but let anyone who doesn't want them turn them off or push them to the end
- **Student handout** — only ask this if teacher's notes are set to integrated or end-only: whether the tutor also wants a second, notes-free version of the plan suitable for handing to the student. Default: **yes**, unless the tutor opts out

These only need answering once — for a single-lesson request, ask them right away as part of getting into Step 4; for a path, ask once before generating Lesson 1, then reuse the same answers for later lessons unless the tutor wants to change something for a specific one.

**Don't open the plan with a student-details or framework header** (e.g. a block restating the student's name/level/interests, or naming the PPP/TBL/ESA framework being used) — that's internal planning context, not something the tutor needs printed at the top of a document they'll use in front of a student. Start straight in with the lesson content.

Unless the user specifies their own format, include, **in this order**:
1. **Objective(s)** — a can-do statement written directly to the student in the second person ("You will be able to..."), never in the third person ("Students will...", "The student will...")
2. **Warm Up Conversation** — always comes immediately after the objective, before any vocab or content; see below for what goes in it
3. **Review of Prior Content** (every lesson that has anything to review, so from Lesson 2 of a path onward or any returning student) — see below
4. **Fresh Vocabulary** — always include this section (see below)
5. **Grammar Focus** — scaled to the depth the tutor chose (see "Grammar Focus section" below). **Strong**: presentation/input, controlled practice, and freer practice per the chosen framework (PPP's "Presentation" stage; use whatever this stage is called under a different framework — see `references/lesson-frameworks.md`), and the target grammar is built into the activities too. **Light**: a brief overview only (a short plain-language rule, a formula if there is one, 2-3 examples), with the target grammar woven into the activities' prompts rather than drilled separately. **None**: omit this section entirely and build the lesson around topical activities; don't sneak a grammar explanation back in
6. **Production/application activities** — students use the language with some autonomy, built from **several** activities per the chosen selection method (see below), not just one. This isn't a wrapping "Production" heading in the document itself, just the label for this stage in your own planning — go straight from Grammar Focus into the first activity's own heading (see "Choosing the activities" below)
7. **Wrap-up / assessment** — quick check of the objective (not necessarily formal testing)
8. **Home Assignment** — included by default; omit only if the tutor opted out during the interview
9. **Materials needed**
10. **Time Summary** — a single section, not per-stage headings (see below)
11. **Teacher's Notes** (if not turned off — see below) — either woven into the stages that have one, or collected in one closing section, per the tutor's preference
12. **Student Handout** (included by default whenever Teacher's Notes are on; omit only if the tutor opts out — not possible when Teacher's Notes are off) — a second, separate notes-free copy of the plan (see below)

### Time Summary
Timings are suggestions the tutor can flex on mid-lesson, not a rigid schedule — so don't put a time next to every stage/activity heading throughout the plan. Instead, collect all suggested timings into one **Time Summary** section (a short list or small table, e.g. "Warm Up Conversation — ~5 min"), placed near the end of the plan alongside Materials needed. Non-Production stages should sum close to the class length; the Production stage's activity options can add up to more than what's left (see "Choosing the activities" below) — that's intentional headroom, not an error.

### Warm Up Conversation section
Always placed immediately after the Objective, before Review of Prior Content or any lesson content. Not a lesson-topic teaser — a short, genuine check-in on the student's life, to build rapport before the lesson content starts. Include 2-3 open-ended questions about what's actually going on for them, in the spirit of "Any highlights from your week?" and "Anything you're looking forward to in the next couple of weeks?" — **write fresh questions for every lesson** (never repeat the same wording lesson to lesson) and **make them fun and varied in style, not just "how was your week"**. Rotate through different question types, and make at least one of the 2-3 playful: would-you-rather, a harmless hypothetical ("If you could have dinner with anyone..."), this-or-that, a quick favorites round, a silly scenario, a "best/worst" question, a one-minute story prompt, a two truths and a lie opener, or an imagination question tied to the student's interests. Mix in a real check-in (week just past, week ahead, a follow-up on something from a prior lesson) only as one of the questions, not the whole set. Check the record's Warm-Up Log and avoid the types used in the last few lessons, then add this lesson's types to it. Format the questions as a bulleted list, not a paragraph — this is the format to carry into the Student Handout too (see below).

### Review of Prior Content section (recycling)
**Every lesson includes this section whenever the student has any prior content on record** (vocabulary, grammar points, or a previous home assignment). New material that's never revisited doesn't stick, so spend a few minutes recycling before introducing anything new. Draw on whatever exists:
- **Vocabulary**: pull 2-4 items from the student's Vocabulary Log, including words imported from prior work, which are fair game for review even though they must never appear in Fresh Vocabulary as new. Prioritize items from lessons that are neither the most recent one (too fresh to need review yet) nor ones already reviewed multiple times, so review rotates through everything taught rather than only ever touching the last lesson's words
- **Grammar**: one quick retrieval task on a grammar point from an earlier lesson (a few prompts, a short error-correction, or "tell me about X using the structure"), rotating through earlier points
- **Last home assignment**: a brief follow-up on what the student produced (read a sentence aloud, share one answer, fix one error), if one was given
- Keep it to a few minutes, as short speaking prompts rather than worksheets: a sentence with the word blanked out, "use this word in a sentence about..." tied to the student's interests, or a one-minute retell using the old structure
- Skip this section only for a student's first-ever lesson with nothing imported (nothing to review yet)

### Home Assignment section
Included by default. Class time is for speaking, so **writing tasks belong here**, not in the in-class Production stage. Choose 1-2 tasks from the "Home assignment ideas" list in `references/activity-bank.md`, tied to the lesson's theme, vocabulary, and grammar. Keep it doable in 15-20 minutes, address it to the student, and note which one will be reviewed next lesson.

### Fresh Vocabulary section
Every lesson gets a standalone new-vocabulary section, not just vocab folded into the presentation stage:
- **Don't state or fix a number of items anywhere** (not in the heading, not in an intro line, not in the Time Summary, not in the objective). The tutor picks which words to teach and the number varies lesson to lesson, so offer a generous, varied pool of good candidates and let the tutor choose. There is no minimum unless the tutor gives one. Tie the words to the lesson's theme and therefore to the student's stated interests — every example sentence should read as if written for this specific student, not generic
- **Pitch vocab one CEFR level above the student's current level** (A2 student → A2/B1-boundary or B1 vocab; B1 → B2; B2 → C1; C1 → C2; a C2 student stays at C2 but pushes toward rarer/more nuanced items). This is a deliberate stretch to grow the student, not a comprehension check — use `references/cefr-levels.md` to judge what "one level up" looks like in practice
- Apply the vocab constraint from the interview: if phrasal verbs were requested, every item is a phrasal verb; if a part of speech was requested, every item matches it; otherwise mix naturally around the topic
- Make the word usable, not just recognizable: choose natural, collocation-rich example sentences (e.g. for "address" as a verb, an example like "We need to address the noise problem."). The collocations live in the Example line, never in parentheses in the definition
- **Never repeat a word/phrase already taught to this student.** Check the student's record file (below) before finalizing the list, and swap out any overlap

**Format** — every vocab item is written exactly as:
```
word – definition
Example: example sentence
```
Use an en dash (–) between word and definition. **Keep the definition clean: a plain-language meaning only, with no parentheses and no sample phrases or collocations inside it** (the Example line below it already shows the word in use). The example sentence must connect to the lesson's theme/the student's interests, not be a generic textbook sentence.

### Grammar Focus section
Applies to the **strong** and **light** depths (skip the whole section for **none**). A light focus keeps just the short rule, formula, and 2-3 examples from the list below and skips the separate controlled/freer practice; the grammar then shows up inside the activities (e.g. a prompt that invites the target structure). A strong focus is the lesson's main teaching point, and it needs to actually teach it, not just gesture at it with a couple of examples, and the activities should keep requiring the structure. For the presentation/input part of this stage, always include:
- **A clear, plain-language explanation of the rule** — what it means and when a speaker would reach for it, not just its name. Don't assume the name of the structure is self-explanatory.
- **A formula, if the structure has one, kept as short as possible** (e.g. *be* + past participle; *have/has* + past participle; *If* + past simple, *would* + base verb). Don't qualify it with parentheticals like "(in the correct tense)" or explain implementation details in the same line, that's implied and the tutor can explain it live if the student needs it. Skip the formula entirely for grammar points that aren't formulaic (e.g. article usage, word order preferences).
- **Several thematic examples**, tied to the lesson's topic and the student's interests, not generic textbook sentences. Two examples is too thin, aim for enough that the pattern is clearly visible.
- **If the grammar point has multiple distinct uses or forms, show examples for each one separately**, don't let one use stand in for all of them. For example: passive voice used across different tenses (present simple, past simple, present perfect, modal) if the lesson touches more than one; "used to" for past habits vs. "be used to" for familiarity; reported speech for statements vs. questions vs. commands. If the lesson is deliberately scoped to just one use or one tense, say so briefly so it's clear that's intentional, not an oversight.

Keep the whole presentation tight and skimmable. Don't add asides about edge cases or usage nuance (e.g. when to drop an agent/actor from a sentence, formality register, etc.) into the main explanation, formula, or examples, that kind of detail belongs in a Teacher's Note if it's worth flagging at all, not woven into the student-facing explanation where it disrupts the flow.

For a strong focus, controlled practice and freer practice follow the presentation as usual (per the chosen framework), building on the examples and formula already established rather than introducing the structure for the first time there.

### Teacher's Notes
These are for the tutor only — never phrase them as if speaking to the student. Keep each note short (1-2 sentences): pacing/timing guidance, why a stage or activity was chosen, a likely sticking point for this student specifically (e.g. an anticipated L1-interference error, a grammar point they've struggled with before), or a quick alternative if something isn't landing.

**Not every stage needs one.** A note only earns its place if it says something the tutor couldn't already infer from the heading — skip self-explanatory stages like Warm Up Conversation or Wrap-up unless there's genuinely something specific to flag for this student. Grammar Focus, Fresh Vocabulary, and the Production activity options are the stages most likely to have something worth noting (a rationale, an anticipated difficulty, a timing call); don't pad the rest just to have a note under every heading.
- **Integrated** (default): add a brief *Teacher's note:* line (italicized or otherwise visually distinct from the student-facing content) directly under the stages that have one — e.g. a note under Fresh Vocabulary about why this constraint was chosen, or under an activity option about which one to pick if time is short
- **End-only**: skip inline notes entirely and instead add a single "## Teacher's Notes" section as the last part of the plan, with one short bullet per stage that has something worth flagging — don't force a bullet for every stage if there's nothing useful to say
- **Not included**: omit teacher's notes entirely — don't sneak pedagogical asides into stage descriptions instead

### Student handout (optional)
If the tutor opted in, produce a second copy of the plan after the main one. **The handout is the same document — same content, same wording, same formatting — minus exactly three things:**
- All Teacher's Notes, wherever they appear (inline or in the closing section)
- **Materials needed**
- **Time Summary**

Nothing else changes (the objective, activity instructions, and every other student-facing line are already written to the student, so no rewording is needed). Every other section carries over as-is, in the same order: Warm Up Conversation (including its bulleted questions, unchanged), Review of Prior Content, Fresh Vocabulary, Grammar Focus, every Production activity's full instructions, Wrap-up, Home Assignment. Since activity instructions are already written addressed to the student (see "Choosing the activities" above), there's no rephrasing to do — copy the content over and delete only the three tutor-only sections.

Label it plainly with the same title as the main plan plus "Student Handout" (e.g. "# <Student Name> — <Date> — <Theme> — Student Handout") — **don't** add any parenthetical or caption describing what was stripped out (e.g. never write something like "(Teacher's notes and Materials removed)"); the student should never see a trace of what the tutor-only version contained.

If exporting to `.docx` (Step 6) and a handout was requested, export both as separate files rather than combining them into one document.

### Student Record File (profile, path progress, and vocab log)
Maintain one file per student at `~/eng-teaching-records/<student-name-slug>.md` (lowercase, hyphens for spaces, e.g. `maria-garcia.md`) — **not** inside the skill's own directory (see Step 0 for why). This is the single source of truth that lets a future session say "next lesson for [student name]" without re-running Step 1, and lets vocab stay genuinely new lesson over lesson. It has three parts:

```
# Student Record — <Name>

## Profile
- Pronouns: ...
- Level: ...
- Location: ...
- Interests: ...
- Goal: ...
- English variety: American/British (default American)
- Session length: ...
- Activity choice: ...
- Vocab constraint: ...
- Grammar focus depth: strong/light/none
- Home assignment: yes/no
- Teacher's notes: integrated/end-only/none
- Key skills weighting: ...
- Exclusions: ...

## Learning Path (omit if single-lesson only)
| Lesson # | Lesson Name | Theme | Grammar Point | Activity Type(s) | Status |
|---|---|---|---|---|---|
| 1 | ... | ... | ... | ... | Delivered 2026-09-24 |
| 2 | ... | ... | ... | ... | Not yet delivered |

## Activity Log
- 2026-09-24: Role Play, This or That

## Warm-Up Log
- 2026-09-24: would-you-rather, favorites round

## Vocabulary Log
### 2026-09-24 — Lesson 1: <name>
- word one
- word two
- Grammar: <point taught>
- Home assignment: <what was set>
```

- **Create/update the Profile** at the end of Step 1 (new student) or whenever the tutor changes something during a returning-student check-in (Step 0)
- **Create/update the Learning Path table** at the end of Step 2, and flip a lesson's Status to "Delivered <date>" immediately after generating it — this is what Step 0 reads to know which lesson is next, without asking the tutor
- **Before** drafting Fresh Vocabulary for any lesson: read the Vocabulary Log section to see everything already taught to this student
- **After** finalizing a lesson's activities: append the chosen Production activities to the Activity Log with the date
- **Before** choosing activities: read the Activity Log to apply the no-repeat rule
- **After** finalizing a lesson: append the new vocab items, the grammar point, and the home assignment under a new dated heading
- If the tutor mentions the student already knows certain words/phrases (from "anything to incorporate or exclude"), log those too so they're excluded from future lessons even though they weren't taught here

### Choosing the activities
Include **2-3 activities** in the Production/application stage, not a single fixed one — this fills the available time and gives the tutor real options to choose between, skip, or swap live in the lesson rather than being locked into one plan:
- **Random**: pick 2-3 that fit the level, topic, and available time from `references/teacher-activities.md`, using the weight tags there (High = 3, Medium = 2, Low = 1) after filtering. **Never reuse an activity from the student's Activity Log within the last 4 lessons**, and avoid repeating the same activity category (e.g. two debate-style activities) in one lesson. Pick varied enough that they're not redundant with each other (e.g. don't pair two debate-style activities back to back) — don't force a 5-item ranking scenario into a 20-minute slot
- **Specific**: use the named activity/activities as given (the no-repeat rule doesn't apply to requested activities); if the tutor only named one, add 1-2 more (random or judgment-based) so there are still options to fill the time
- **Tutor's judgment / unspecified**: default to `references/teacher-activities.md` first since these are proven-effective for this tutor; fall back to `references/activity-bank.md` only if nothing on the teacher's list fits the lesson's goal

**Generate almost all lesson content yourself, especially text.** The whole point is a realistic, usable lesson without the tutor having to go dig up materials. Dialogues, stories, scenarios, discussion questions, data tables — write all of it fresh, tied to the student's interests and level, rather than pointing the tutor at something to find. Only include **at most 1 activity per lesson** that requires the tutor to source real external material — in practice, that's an occasional real photo, video, or audio clip, or (rarely, for authentic-text needs like exam prep) a real article; the three ⚑-marked entries in `references/teacher-activities.md` — and only when it's clearly the best fit for the goal or the tutor specifically asked for one. Gallery tour and data/charts discussion are generated as vivid written descriptions or text-formatted data by default — see their entries in `references/teacher-activities.md` — so they don't count against this cap unless the tutor wants to supply real images/charts instead. **Describe a Picture is different: it genuinely needs a real photo to work as an activity** (a written description defeats the point, since the student is supposed to do the observing), so using it always counts against the cap — see its entry in `references/teacher-activities.md` for what to tell the tutor.

If Describe a Picture is used, list the photo in **Materials needed** as something the tutor still needs to bring (e.g. "A photo of a busy market or street scene, tutor to provide"), and add a Teacher's Note suggesting what kind of image would work well for this lesson's theme.

Present each option under its own heading named after the activity itself (e.g. "Role Play: Ordering at a Cafe"), **never lettered or numbered** ("Activity A", "Activity 2"), because the tutor may reorder, skip, or swap them live. **Every activity must work with no dependencies: if the tutor runs only this one, it must be complete.** Never refer to another activity by name or position ("as in Activity A", "after the debate", "use the words from the previous task"), and never rely on something produced in a different activity. Activities may share a story, setting, or theme (a nice touch when several are used), but each one must restate whatever it needs from that shared context (introduce the characters, the situation, the key facts) so it makes sense alone, and none may require another to have been done first. There is no separate stage heading wrapping them — go straight from the Grammar Focus content into the first activity heading. No time next to each heading; list a suggested time per activity in the Time Summary section instead. Don't write any framing sentence like "choose from these activities" or "you don't need to do all three" into the plan itself, that's implicit from the labeled options and belongs in your own planning, not in the document. **It's fine — expected, even — for the activities' combined time to run longer than the session length.** These are options to pick from live, not a mandatory sequence, so the tutor isn't meant to run all of them every time. Don't shrink or cut activities just to force this stage's total to fit the class length; a plan with more material than one session needs is more useful than one that runs out with time left over.

**Any list of items within an activity (images to describe in a Gallery Tour, sentences to rewrite in Sentence Upgrades, options in a ranking scenario, etc.) should be a bulleted list, not a numbered one.** Numbered lists are reserved for genuine sequential steps (e.g. Controlled Practice exercises the student works through in order); a set of items to choose from or work through in any order reads better as bullets and avoids numbering that can look like it's continuing from an earlier list in the document.

**Write every student-facing line addressed to the student, in the second person** (e.g. "Read the dialogue below and discuss...", "You will hear...", "You will see...", "You will be given...", "Rank these options from most to least important..."), not as stage directions to the tutor (e.g. not "Have the student read the dialogue and discuss..."). This applies throughout the plan (Warm Up Conversation questions, Grammar Focus practice, every Production activity) and above all in the Student Handout.

**Hard rule: no student-facing text may mention the tutor, teacher, instructor, or "the student" in any form.** That includes "your tutor", "your teacher", "the tutor", "the teacher", "your instructor", "your coach", "the student", and "the tutor will...". The tutor pastes this material into the lesson and is sitting right next to the student, so "your tutor will show you a photo" is awkward, and it makes a lesson built for this one learner read like generic worksheet text. Rewrite so nobody is named: "you will be given a photo", "you will hear a short story", "listen to the story", "look at the photo". If a human has to do something, use "we" or an imperative ("Let's role-play this dialogue", "Take turns reading"). Never say "ask your tutor"; say "ask me" only if the line truly needs a person, otherwise rephrase. Tutor-only content (Teacher's Notes, Materials needed, Time Summary) is the only place the tutor is mentioned, and it never appears in the handout.

**Before delivering the main plan or the handout, scan the student-facing text for the words tutor, teacher, instructor, and student (case-insensitive) and rewrite every hit.** Do this check every time, not just when you remember to.

Calibrate example sentences, instructions, and reading/listening text complexity to the stated CEFR level — don't write B2-complexity examples for an A2 class.

Personalize using what the interview surfaced: swap generic example sentences/topics for ones tied to the student's stated interests, profession, and specific location/hometown (real place names, regional references — not generic "Europe"/"Asia" framing), and pick discussion/reading topics that fit their goal (e.g. workplace scenarios for a business-goal student, campus/exam scenarios for an academic one). Using their location, silently check `references/student-interview.md`'s L1-interference notes and pre-empt the most likely error rather than waiting for it to surface — this stays a background input to your planning, not something stated back to the tutor.

### Wrap-up section
Give the student one concrete, specific task or question to do right now, in the room, not a vague prompt like "summarize what you learned" or "tell me what you learned today." Tie it directly to the lesson's actual content: a specific scenario to respond to, a specific question that requires using the target grammar/vocab to answer, or a short concrete task (e.g. "Tell me about a film you'd recommend to a friend, using at least two passive constructions and one new vocab word" rather than "summarize what you learned about the passive voice"). This should double as a real check of the objective, not just a ritual close to the lesson.

## Step 5: Differentiation and common pitfalls

- If the student's level assessment feels uncertain, or they're clearly having a stronger/weaker day than expected, keep one extension idea and one simplification in your back pocket for the main activity rather than rewriting the whole plan mid-lesson
- Avoid overloading a single lesson with more than one new grammar point or a pile of unrelated new vocabulary (the tutor trims the vocab pool as needed)
- For exam-prep lessons, tie every activity back to the specific exam skill being tested (e.g. IELTS Task 2 essay structure, not just "writing practice")

## Output format

Write the plan as clean markdown with headers per stage — no timing in the headers themselves; all suggested timings live together in the Time Summary section (see Step 4). Don't pad with generic teaching theory the teacher already knows — keep it concrete and usable at the front of a classroom.

**Use the chosen English variety consistently, American by default.** Every word in every output (lesson text, dialogues, vocab words and definitions, example sentences, instructions, handouts, teacher's notes) follows American spelling and usage unless the tutor chose British in Step 1: color, favorite, organize, realize, center, traveling, program, gray, practice (noun and verb), check (not cheque), plus American vocabulary (apartment, elevator, truck, vacation, soccer, cell phone) and American date and measurement conventions. If British was chosen, use it just as consistently. Never mix the two in one document, and match spelling inside quoted student-facing texts as well. Run a quick scan for common British spellings (-our, -ise, -re, -ll- doubling) before delivering.

**Never use an em dash (—) in narrative/body text, in any output this skill produces** (lesson plans, handouts, learning paths, teacher's notes, interview questions, record files, chat responses — everything). Em dashes read as a giveaway of AI-generated writing, and this skill's whole point is realistic, human-feeling content. Use a period, comma, colon, or parentheses instead, or just rephrase as two sentences. The only place an em dash is acceptable is as a formatting separator in a heading or label (e.g. "# Maria — 2026-10-19 — Weekend Plans," "# Maria — 2026-10-19 — Weekend Plans — Student Handout") or in a vocab item's `word – definition` line — and that vocab-item dash should be an en dash (–), not an em dash, per the Fresh Vocabulary format below. When in doubt, don't use one.

## Step 6: Export as a .docx (optional)

A finished lesson plan — or an approved learning path table (see Step 2) — is a document the tutor will print, edit, or hand to a co-teacher, or file away for reference, not something that only lives as chat text. After presenting either one, offer to export it as a `.docx` file the tutor can open in Word/Google Docs and edit further. Don't export automatically — only build the file once the tutor says yes (or asks for a doc/Word file/download up front).

**Many tutors using this skill aren't technical, so exporting a file must not be a place they can get stuck.** Don't assume file delivery will just work — verify it, in this order:

1. **Check whether this environment actually has a place to write files that the tutor can get to.** Some chat-based harnesses only reliably hand a file to the tutor when it's created through the harness's own native file/attachment mechanism, or when a specific folder has been explicitly connected for this session — a file written by a background script isn't guaranteed to reach the tutor even if the script itself runs without error. If you're unsure whether this environment has a working, connected location for this session, don't guess and don't assume last session's connection carried over — check first (e.g. by trying to access the intended folder, or by checking whatever the harness uses to indicate a connected workspace).
2. **If there's a working connected location**, ask where to save (unless the tutor already told you a folder for this student or session), reuse that answer for the rest of the session, and write the file there.
3. **If there's no connected location, or you can't confirm one, say so in plain language** (e.g. "I don't have a folder connected in this session, so I'll share the file directly here in the chat instead") rather than silently failing or leaving the tutor to guess why nothing showed up. If the harness supports requesting folder access for future sessions, offer that too, but don't block delivery on it — get the tutor their file now, through whatever channel (direct chat attachment, output panel, etc.) actually works in this environment.
4. **After creating the file, confirm it actually exists and is reachable by the tutor before saying it's done** — a script exiting with no error is not proof the tutor can open the file.

**If this environment has a dedicated Outputs/Files panel separate from the chat itself** (e.g. Claude's Cowork-style task view, which shows "Outputs" and "Context" panels alongside the conversation): confirmed root cause from real testing — a file the assistant writes directly (its own file-write action) surfaces in that panel automatically, but a file produced by *running a script* (like the bundled `md_to_docx.py` converter) does not; it lands in the working directory but needs an explicit send/attach step afterward to actually reach the tutor. **After running the conversion script, always follow up with an explicit send/attach action for each generated file — don't treat a clean script exit as the end of the job.** Then, in the same message:
- Name every file sent, exactly as written (e.g. "maria-lesson-1.docx" and "maria-lesson-1-handout.docx")
- Tell the tutor by name where to find them in the interface (e.g. "click **Outputs** in the panel on the right to open or download them")
- Don't assume the panel being visible is enough — a tutor skimming chat text needs the file names and the click target spelled out, not left implicit

**If this environment has no way to run code or a shell at all** (a plain chat assistant with no tools enabled, e.g. Claude.ai or ChatGPT without code execution turned on): there's no way to produce an actual `.docx` file — don't claim to have created one. Instead, tell the tutor plainly that this environment can't generate a Word file directly, then output the plan as clean, well-structured markdown (proper `#`/`##` headings, `**bold**`, bullet/numbered lists) and tell them to copy it and paste it straight into Word or Google Docs — pasted markdown formatting carries over reasonably well in both. If the tutor's platform does have code execution available (e.g. a "Python" or "Code Interpreter" tool), you can instead try running an equivalent conversion so they get a real file.

**Default, works on any harness with shell access** (Codex, Cursor, Aider, Claude Code, etc.): write the finished plan to a markdown file, then run the bundled converter:

```bash
python3 skills/english-tutoring/scripts/md_to_docx.py <plan>.md <output>.docx
```

If `python-docx` isn't installed, install it first (`pip install python-docx`) and retry — it's a small, standard library, not a platform-specific plugin. The script (tested end-to-end) handles `#`/`##`/`###` headings, `**bold**`/`*italic*` inline markup, `-`/numbered lists, `> ` blockquote lines (rendered indented, black, and italic — use this for Teacher's Notes so they read as clearly separate from student-facing content), and standard markdown tables (rendered as a real Word table with a bold header row and gridlines — use this for the learning-path table). Write the source markdown accordingly:
- Lesson title as `#`, always in the form `<Student Name> — <Date of the lesson> — <Title/Theme>` (e.g. `# Jayden — 2026-10-19 — Planning a Road Trip`). **Never put the lesson number in the title**, and use the lesson date (ask if you don't know it; default to today's date), each stage (Warm Up Conversation, Review of Prior Content, Fresh Vocabulary, etc.) as `##`
- Bold the vocab word in each `word – definition` line, italicize the example sentence
- Prefix each Teacher's Note line with `> ` so the script styles it distinctly, whether integrated per-stage or collected at the end
- For a learning path, write the path exactly as the `| Lesson # | ... |` markdown table already used to present it — no reformatting needed

**Always use the bundled converter for lesson plans, handouts, and path tables, on every harness, including Claude Code.** Do not use the `docx` skill, docx-js, or hand-built Word files for these exports: their default heading and title styles are blue, which is the most common way color sneaks back in.

**Exports are black text only, with no exceptions.** This means no blue headings, no blue title or rule under the title, no colored text, no colored table shading, and no hyperlinks (Word renders them blue and underlined). The converter forces every style to black, turns `[label](url)` into plain label text, and checks the saved file, exiting with an error if any color or hyperlink remains. Never add color formatting to the source markdown or post-process the file. If the converter reports non-black formatting, fix the cause and re-export instead of delivering the file. Do not report an export as done until the converter has printed `Wrote <file>` without an error.

Name the file `<student-name>-lesson-<n>.docx` (or `<student-name>-<lesson-name>.docx` for a single lesson) and save it in the location the tutor gave you (see above). If a student handout was also requested, name it `<student-name>-lesson-<n>-handout.docx` as a separate file. For a learning path table, name it `<student-name>-learning-path.docx`.

**After creating any file, tell the tutor exactly where it landed** — the full path if it was saved to a connected folder, or a plain statement that it's attached/available directly in the chat if that's how it was delivered. This applies to every file this skill writes: a `.docx` export, a student handout, or a record file. A tutor who doesn't know where something went can't find or share it.
