# Exercise Types and Worksheet Anatomy

Contents: File format, Look and feel, Worksheet anatomy, The focus box, Designing for typing, Exercise catalog, Writing tasks, Answer key, Quality checks.

## File format

Write the whole pack as one markdown file. Separate worksheets with a line containing only `<!-- worksheet -->`. Start the file with the first marker and go straight into worksheet 1: **no cover or overview page** (a how-to-use note and a plan table state the obvious; the plan goes to the tutor in chat). The exporter still accepts text before the first marker as a front page, but do not write one. Use `<!-- pagebreak -->` to force a page break inside a worksheet.

- `##` is a worksheet title (a full-width blue banner). `###` is a part heading.
- `:::box` and `:::` is the focus box: light blue, with a blue border and title. `:::box bank` is a yellow word bank. `:::box watch` is a soft red watch out box.
- A `|` table gets a blue header row. If its last column is headed `Your answer`, the answer cells are light blue and the student types in them. A row numbered `0` is the worked example: its answer is already filled in and its cell is light green.
- `:::write 5` and `:::` is an empty tinted box about 5 lines tall for writing tasks.
- `> text` is a message or quote with a light blue background and a blue bar.
- `![alt](path){2.5}` is an image from a local file, centered, 2.5 inches wide. A missing file is skipped with a warning.

Skeleton:

```
<!-- worksheet -->
## Worksheet 1: Title in plain words

:::box
**Grammar Focus: the point in plain words**
The rule in one or two sentences.

**How to do it**
1. First step.
2. Second step.
3. When each form applies, with the exceptions.

| Form | Use | Example |
|---|---|---|
| ... | ... | ... |

**Examples**
- statement
- question
- negative
- a different work situation

:::

:::box watch
**Watch out**
- Don't use: ... Use: ... (short reason)
- Don't use: ... Use: ...
:::

<!-- pagebreak -->

### ✏️ Part A: Choose the right form
*Type the correct word in the light blue box.*

| # | Sentence | Your answer |
|---|---|---|
| 0 | worked example | the answer |
| 1 | item | |

### ✍️ Part B: Write
*Instruction.*

:::write 5
:::
```

## Look and feel

Color and images are welcome. Blue is the main color of every worksheet. Other elements use other light colors: yellow word banks, soft red Watch out boxes, green worked examples. Use emoji lightly in part headings (✏️ write, 🔤 choose, 💬 answer about you, 🔗 match, 🔍 find the mistake). Add an image only when a real file exists, and keep it small. Keep every fill light so typed text stays readable. The exporter sizes table columns so that no word is ever broken across lines; keep column headers short.

## Worksheet anatomy

- **Focus box first**, directly under the worksheet title, then the watch out box. Do not add an objective or purpose sentence: the title and the focus box already say what the worksheet is about.
- **15 to 20 minutes** unless the profile says otherwise. About 4 to 5 parts.
- **Order**: easier to freer. Recognize and choose, then repair, then answer questions or build sentences, then write.
- **At least one writing task** unless the worksheet is explicitly drill-only.
- **One short instruction** per part. Tell the student exactly what to type.
- **Titles in plain words**: "Do I need 'be'?" beats "Copula usage".

## The focus box

**Budget: the focus box and the watch out box together may fill one page, never more.** The page is a ceiling, not a target. The student should be able to do the worksheet from the box. It holds, in order:

1. **The rule**, in plain words, first. Do not add a "why it matters" line anywhere in the box. Then give either:
   - **How to do it** (a procedure, such as agreement or word order): short numbered steps, usually 3 to 6, each one action. Split a step that holds two ideas. Steps are things to do to a sentence. They never say "look at the table" and never refer to another step ("steps 1 to 3"): each says its idea directly. Include how to tell the cases apart and the exceptions.
   - **Key points** (a choice between forms, such as two tenses or prepositions): 2 to 4 short lines that each say when one form is used.

   Use steps only when there is something to do in order. Facts such as verb forms are not steps: put them in a short Verb forms or Key points list after the steps, introducing each item before any line says "other" or "the rest". The table columns follow the same order as that list. The rule and steps must work without the table, which only illustrates them. Use the real grammar terms (singular and plural, past and present) and explain each in brackets the first time ("singular (one)"), never vague labels like "one or more than one" on their own. Anything the rule or a step mentions ("words after of or in") must be shown in the examples, with the key words in bold (never brackets or other extra marks, which distract), and each word named gets its own example.
2. **One small provided table or pattern** (at most 6 rows, or all 7 subjects for a verb paradigm) that the activities use again. This replaces any "write all the forms" activity.
3. **Exactly 4 examples** that show dynamic use, not four versions of one sentence. Vary the sentence type (statement, question, negative), the subject, and the setting, in the student's work world. Bold the target. **If the rule tells the student to do something (replace the subject with a pronoun, find the main noun, add -s), every example must show that step and its result in the sentence, for example "The **number** of orders **was** low. → **It was** low." A label like "(it)" does not count.**

There is no dialogue in the focus box. Show one contrast side by side in a table with full example sentences (for example one vs more than one, or two tenses compared, three only if the point needs it), and nothing outside that contrast. Each How to do it step carries out the topic or is a tip for doing it well. The title, the box title, the rule, the table, the examples and the Watch out items all use the same words for the topic; a reader must be able to say the topic in one sentence after reading the box.

The watch out box follows, with **exactly 2 mistakes**, each written "Don't use: ... Use: ..." in the student's likely error form, then a brief *Why:* in italics. The Why is one short sentence that gives the reason for the change, not a restatement of the rule. Bad: "No word after call." Good: "Why: call already connects to the person, so nothing goes between." Never write "Not" and "Yes".

**Page 1 holds only the title, the focus box and the Watch out box.** Put `<!-- pagebreak -->` straight after the Watch out box so Part A starts on page 2. No second table or more examples. If the point needs them, narrow the focus or split it into two worksheets. A second point that does not fit goes into the instruction of the activity that uses it as one line ("Use 's for one owner and s' for many.").

**Write it clearly:**

- Each definition and rule starts on its own line, with a blank line between them. Blocks of text are harder to read. In word banks, put each definition, meaning, or option on its own line; a bank of single words can stay in one row.
- Every sentence is understandable on its own, and every term is explained in plain words the first time, or avoided. Name a group by what it does ("action verb: a word for something you do, like work or call"), never with a vague label like "normal verb". Define any grammar term the student has not met (such as past participle).
- When a word or pattern has more than one use, say exactly when each applies, and never state a pattern as always true if it has exceptions. Bad: "Some verbs need to or for before a person or thing." ("Please ask John" and "Please pay Cindy" need neither.) Good: "ask and pay need no word before a person, and for before a thing." A table is a guide for deciding, not only a formula: give the condition for each form and an example of each case.
- Title the box with the question the student is answering ("describing or doing?"), not a list of forms.
- Show contrasts in the table with full example sentences, not bare words. A table of verb forms gives every subject its own row (I, you, he, she, it, we, they). Never merge or skip subjects.
- If the table lists forms or words without sentences, label every example with its form and use: "Past simple, finished time: I **met** him last year." Where the cells already hold sentences, labeling by use is enough ("Describing:", "A habit:").

Name the box **Grammar Focus** on every worksheet, including verb patterns and word choice. Use **Language Focus** only if the whole pack is vocabulary. Never mix the two names in one pack.

## Designing for typing

Students open the file in Word or Google Docs and type in it. So:

- The item text stays in its own cell. The answer goes in the light blue cell next to it. The layout never moves.
- Ask for a word, a letter, or one sentence per cell. For anything longer, use a write box.
- Never ask for physical actions. Replace circle with "type the correct word," underline with "type the word," match with lines with "type the letter," tick with "type yes or no."
- Offer choices inside the sentence ("The sponsors **is / are** happy") and ask the student to type the one that fits.
- Gap-fills use plain blanks (`______`) with no numbers inside them. Say how many gaps there are, and have the student type the answers in order in a `# | Your answer` table. Do not add a column that repeats the gap. A third column is only for something useful, such as the base verb. Put a word bank in a `:::box bank` above it.
- Worked example: row `0` of every answer table, in the same format as the items, with the answer filled in. For a gap-fill text, fill the first gap in bold in the text and show it as row 0. Do not put the example in the instruction line.

## Exercise catalog

**Verb-form exercises (gap-fill where the student types a form of a given verb).** Always give the verb on its own in a bold "Verb" column with its meaning in brackets, never inside the sentence where it blends in or in brackets after a gap. Put the sentence with the gap in the tinted last column headed "Your sentence" (`| # | Verb | Your sentence |`) so the student types the answer inside the sentence, never in a separate cell floating outside it. The worked example shows the sentence complete. For multi-word verbs and expressions (go under, pave the way for, unlock value) the gap holds the whole expression, so the sentence must not repeat any part of it. The instruction says where they type ("In the blue box, replace the blank with...").

**Requirements are bullets.** Suggested words or structures in a writing task must fit the task's topic (suggest *underscore* for a report or conference, not a word that does not belong). When a writing task has two or more requirements (tense, a structure, a word from another part), write the task in one line ending "In your sentences, try to:" and list each requirement as a bullet, never in one block of text. Never use "must" in a student task. End with a one-line tip phrased as "Check to ensure ...", not a command step.

| Type | Use for | Items | Notes |
|---|---|---|---|
| Choose and type | Agreement, word choice, -ed/-ing, prepositions | 6 to 8 | Two or three options inside the sentence. Every wrong option is a real learner error |
| Fix the message | Errors the student makes | A 4 to 6 line email or chat with 4 to 6 errors | Put the whole message inside the write box already (`:::write 7` with the text between the fences) and ask the student to rewrite it with the mistakes fixed. Never ask them to type the whole message from scratch, and never put it in a quote block above an empty box. Say how many errors there are |
| Fix the sentence | Errors the student makes | 6 to 8 | Include 2 correct ones: "type OK if it is correct" |
| Fill the gaps in a text | Verbs, articles, prepositions, linking words | 6 to 10 gaps in one short text | Word bank or the focus table supplies the answers |
| Match and type | Vocabulary and meanings, situations and reactions | 6 to 8 | Student types the letter |
| Use the table | Anything from the focus table | 5 to 6 | Questions that need the table: "Which form fits this sentence?" |
| Answer about you | Real use of the point | 4 to 5 questions | Full-sentence answers about the student's own life, specific, with the target form as the natural answer. Never ask what a third person does, and never ask a vague question like "What does your manager check every day?" **Every question must have a natural answer of one short sentence, and the instruction says so ("Answer each question with one short sentence").** **Questions are specific, neutral and safe: never vague ("than before", "in general", a comparison with no clear base), and never sensitive or private (war, security, politics, religion, health, money or salary, family, relationships, exact location). Ask about work tasks, the city, food, hobbies, travel or ideas, and check each question against the student's real situation, for example a student in a country at war.**  Never ask about each or all of a group ("What does each person on your team do?") or for a list of people or things, unless the question says "name two". Never ask a "who" question whose answer is a name or a list of names: names are not sentence practice. Ask for a goal, a reason, a comparison, an opinion or a description instead, and prefer a topic the student would find interesting, not a plain fact about their surroundings (for example not "How is the electricity today?") |
| Join or transform | Rules, conditionals, reported speech | 4 to 5 | Give the first answer as a model |
| Build a sentence | Structure, questions | 4 to 5 | Give the words and ask for a sentence |
| Vocabulary review | Words from the student's own list | 6 plus a row 0 example | One part per worksheet, before the final write task. Rotate the type: gap-fill with a word bank, match word to meaning (type the letter), type the right form of the word, complete a phrase. Reuse the worksheet's grammar where possible |
| Write | Free production | 3 to 6 sentences | Name the target and a minimum, e.g. "use going to twice" |

Do not use: write every form of a verb, fill in a table of forms, copy sentences, or any task that only checks memory of a list.

Sizing: if an item takes longer than a minute, use fewer items.

## Writing tasks

Always give the topic, the length, the target structure, and one thing to check afterward. The topic must be a real, specific event in the right time frame, so the prompt cannot be answered in the wrong tense. Example: "Think of a tournament or a trip you went to recently. Write 5 sentences about what happened there. Use the past simple and two linking words. Check: is every verb in the past?" Use a `:::write` box sized to the answer (about one line per sentence plus one).

No recording tasks unless the profile says speaking tasks are fine. If it does, tell the student to bring the recording to the next lesson. Do not name the tutor.

## Answer key

Only when the tutor asks for one. A separate file with the same worksheet numbering. For each worksheet:

- A **Targets** line: which focus area from the profile it practices, and the evidence behind it.
- Answers by part, numbered to match.
- For open tasks: what to look for, and a sample answer.
- Notes where more than one answer is acceptable, or where a form is informal but fine.

Use `<!-- worksheet -->` markers here too, so the key splits the same way.

## Quality checks

Run these before exporting:

1. Every item has exactly one correct answer, or is labeled open. Test tense and article items for a second acceptable answer.
2. No wrong option in a choice or word bank can also be correct.
3. The worksheet has one point: the title, rule, table, examples, watch out items, and every activity are about the same thing. Read the focus box in order and check the table and examples match the rule.
4. The focus and watch out boxes fit one page together: one introduction and rule, a short how-to-do-it list, one table, exactly 4 examples, and exactly 2 "Don't use: ... Use: ..." items, each with a brief Why that gives the reason. Measure it, do not judge it: after export, render page 1 and check that the Watch out box ends above about 85% of the page height. If nothing can render it, build with at least 15% slack and say the layout was not verified. Re-render and re-measure after every later edit to a focus or watch out box.
5. The focus box is clear and true: nothing is stated as always true when it has exceptions, every form has a stated condition for when to use it, the box has the same name on every worksheet, each definition and rule on its own line, no vague labels, every term defined, full-sentence tables, every subject in verb tables, examples labeled when the table has no sentences.
6. The focus table is used in at least two activities, and no activity asks the student to write out forms from a list.
7. No item repeats a sentence from the focus box, or copies an error sentence from the student's own speech. Counts of mistakes and gaps are stated.
8. Questions and writing prompts are about the student's real life, specific, neutral (nothing vague, sensitive or private), in the right time frame, and make sense for how that life runs. Example sentences use the student's world. For every "Answer about you" question, write the shortest natural answer: if it needs more than one sentence, rewrite the question.
9. Instructions are short and clear, and every question names a specific thing.
10. Every worksheet has one vocabulary review part (unless the tutor opted out) with words from the student's list, a row 0 example, and an activity type that differs from the other worksheets.
11. Every answer table has a `Your answer` last column and a row 0 example, no gap has a number inside it, and every writing task has a `:::write` box.
12. No hit for tutor, teacher, instructor, or student, and none for circle, underline, cross out, tick, or draw, in student-facing text.
13. No em dashes. Dark text on light fills; white text only on the banner and header rows. Every image path exists.
14. The pack matches the approved plan: count, order, titles.
15. Walk through the rule as the student would. Apply it step by step to each of the 4 examples and to at least 3 items from the activities. If any step is not visible in the box, or the box gives a different answer from the answer key, rewrite the box.
16. **Learner-eye review passed.** The focus box and instructions were read as a lower-level learner who half-remembers the topic from earlier study (ideally by a subagent given only that text), with the topic stated in one sentence, no unexplained terms, nothing mentioned but not shown, the steps done by hand on one sentence, and every Part A item answerable from the box.
17. If no renderer is available, say the layout was not visually checked.
