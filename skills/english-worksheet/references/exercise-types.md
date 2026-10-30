# Exercise Types and Worksheet Anatomy

Contents: File format, Look and feel, Worksheet anatomy, The focus box, Designing for typing, Exercise catalog, Writing tasks, Answer key, Quality checks.

## File format

Write the whole pack as one markdown file. Separate worksheets with a line containing only `<!-- worksheet -->`. Anything before the first marker is an overview (how to use the pack, a plan table). Use `<!-- pagebreak -->` to force a page break inside a worksheet.

- `#` is the pack title. `##` is a worksheet title (a full-width blue banner). `###` is a part heading.
- `:::box` and `:::` is the focus box: light blue, with a blue border and title. `:::box bank` is a yellow word bank. `:::box watch` is a soft red watch out box.
- A `|` table gets a blue header row. If its last column is headed `Your answer`, the answer cells are light blue and the student types in them. A row numbered `0` is the worked example: its answer is already filled in and its cell is light green.
- `:::write 5` and `:::` is an empty tinted box about 5 lines tall for writing tasks.
- `> text` is a message or quote with a light blue background and a blue bar.
- `![alt](path){2.5}` is an image from a local file, centered, 2.5 inches wide. A missing file is skipped with a warning.

Skeleton:

```
# Pack Title

One short paragraph on how to use the pack. Say: type your answers in the light blue boxes. A green box is an example.

<!-- worksheet -->
## Worksheet 1: Title in plain words

:::box
**Grammar Focus: the point in plain words**
The rule in one or two sentences.

| Form | Use | Example |
|---|---|---|
| ... | ... | ... |

**Examples**
- statement
- question
- negative
- a different work situation

**In real use**
Anna: ...
Ken: ...
Anna: ...
:::

:::box watch
**Watch out**
- Don't use: ... Use: ... (short reason)
- Don't use: ... Use: ...
:::

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

Color and images are welcome. Blue is the main color of every worksheet. Other elements use other light colors: yellow word banks, soft red Watch out boxes, green worked examples. Use emoji lightly in part headings (✏️ write, 🔤 choose, 💬 answer about you, 🔗 match, 🔍 find the mistake). Add an image only when a real file exists, and keep it small. Keep every fill light so typed text stays readable.

## Worksheet anatomy

- **Focus box first**, directly under the worksheet title, then the watch out box. Do not add an objective or purpose sentence: the title and the focus box already say what the worksheet is about.
- **15 to 20 minutes** unless the profile says otherwise. About 4 to 5 parts.
- **Order**: easier to freer. Recognize and choose, then repair, then answer questions or build sentences, then write.
- **At least one writing task** unless the worksheet is explicitly drill-only.
- **One short instruction** per part. Tell the student exactly what to type.
- **Titles in plain words**: "Do I need 'be'?" beats "Copula usage".

## The focus box

**Budget: half a page, never more than one page.** The student should still be able to do the worksheet from it. It holds, in order:

1. **A plain rule in one or two sentences**, with no jargon. Say what the point does for the speaker ("use this to talk about plans").
2. **One small provided table or pattern** (at most 6 rows) that the activities use again: forms, uses, quantifiers, prepositions, word families, or reactions. This replaces any "write all the forms" activity.
3. **Exactly 4 examples that show dynamic use**, not four versions of one sentence. Vary the sentence type (statement, question, negative), the subject, and the setting, in the student's own work world. Bold the target.
4. **A brief dialogue of 3 lines** under the label "In real use", in a real work situation, with the target in bold.

The watch out box follows it with **exactly 2 mistakes**, written "Don't use: ... Use: ..." in the student's likely error form, with an optional reason of a few words in brackets. Never write "Not" and "Yes".

Do not add a second table, more examples, or a longer dialogue.

**Be clear, not vague.** Explain every term the first time it appears, in plain words with an example. Name a group by what its members do, not with a vague label: "action verb (a word for something you do, like work or call)" works, "normal verb" does not, because the student cannot tell what makes the others abnormal. Do not use a grammar term the student has not met (such as past participle) without defining it in the box. In a contrast table, show full example sentences in each cell, not bare words, so the difference is visible. Title the box with the question the student is answering ("describing or doing?"), not a list of forms. If a worksheet seems to need them, the focus is too wide: narrow it or split it into two worksheets. A second point that does not fit goes into the instruction of the activity that uses it as a single line, such as "Use 's for one owner and s' for many."

Name the box **Grammar Focus** for grammar points and **Language Focus** for vocabulary, phrases, and word choice. Keep the name consistent across a pack.

## Designing for typing

Students open the file in Word or Google Docs and type in it. So:

- The item text stays in its own cell. The answer goes in the light blue cell next to it. The layout never moves.
- Ask for a word, a letter, or one sentence per cell. For anything longer, use a write box.
- Never ask for physical actions. Replace circle with "type the correct word," underline with "type the word," match with lines with "type the letter," tick with "type yes or no."
- Offer choices inside the sentence, like "The sponsors **is / are** happy," and ask the student to type the one that fits.
- Gap-fills use plain blanks (`______`) in the text, with no numbers inside them. Say how many gaps there are and have the student type the answers in order in a `# | Your answer` table. Do not add a column that repeats the gap. A third column is only for something useful, such as the base verb. Put a word bank in a `:::box bank` above it.
- Worked example: show it as row `0` in the answer table, in the same format as the items, with the answer filled in. For a gap-fill text, fill the first gap in bold in the text and show it as row 0. Do not put the example in the instruction line.

## Exercise catalog

| Type | Use for | Items | Notes |
|---|---|---|---|
| Choose and type | Agreement, word choice, -ed/-ing, prepositions | 6 to 8 | Two or three options inside the sentence. Every wrong option is a real learner error |
| Fix the message | Errors the student makes | A 4 to 6 line email or chat with 4 to 6 errors | Student retypes it correctly in a write box. Say how many errors there are |
| Fix the sentence | Errors the student makes | 6 to 8 | Include 2 correct ones: "type OK if it is correct" |
| Fill the gaps in a text | Verbs, articles, prepositions, linking words | 6 to 10 gaps in one short text | Word bank or the focus table supplies the answers |
| Match and type | Vocabulary and meanings, situations and reactions | 6 to 8 | Student types the letter |
| Use the table | Anything from the focus table | 5 to 6 | Questions that need the table: "Which form fits this sentence?" |
| Answer about you | Real use of the point | 4 to 5 questions | Full-sentence answers about the student's own work and week |
| Join or transform | Rules, conditionals, reported speech | 4 to 5 | Give the first answer as a model |
| Build a sentence | Structure, questions | 4 to 5 | Give the words and ask for a sentence |
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

1. Every item has exactly one correct answer, or is labeled open.
2. In choices and word banks, no wrong option can also be correct in the sentence.
3. The focus box fits one page at most: one rule, one table of at most 6 rows, exactly 4 examples, a 3-line dialogue. The watch out box has exactly 2 mistakes, written "Don't use: ... Use: ...".
4. The focus table is used in at least two different activities.
5. No activity asks the student to write out forms from a list.
5b. Every term in the focus box is defined in plain words, and no label is vague (no "normal," "regular," or "special" verbs). Contrast tables use full example sentences.
6. Example sentences use the student's world (work, places, interests), not generic "John goes to the shop". Every question makes sense in how the student's life really runs (nothing occasional is treated as constant).
7. Instructions are simpler than the exercise content.
8. No sentence copies an error sentence from the student's own speech. Same error type, new sentence.
9. No hit for tutor, teacher, instructor, or student, and none for circle, underline, cross out, tick, or draw, in student-facing text.
10. No em dashes. Dark text on light fills; white text only on the banner and header rows.
11. Every answer table has a `Your answer` last column and a row 0 example, no gap has a number inside it, and every writing task has a `:::write` box.
12. Every image path exists. Never invent one.
13. The pack matches the approved plan: count, order, titles.
14. If no renderer is available, say the layout was not visually checked.
