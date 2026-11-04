# Error codes and tagging rules

## Contents
- How to tag
- The codes
- Choosing between codes
- Reading the tracker

## How to tag
Tag errors after step 5 (speaker labels are final), while writing the analysis in step 7. The tags feed `scripts/error_ledger.py`, which counts them, divides by the student's word count and draws the trend. The counting is mechanical; the judgment is yours, so be consistent.

- **Read the whole transcript, not a sample.** A tracker built on the first half of a lesson is not comparable with one built on the whole.
- **One tag per error.** Do not tag the same phrase twice. Several different errors in one sentence get one tag each.
- **Student speech only.** Skip the tutor's model sentences, repeats of a phrase the tutor just said, and lines marked `[speaker uncertain]`.
- **Skip self-repairs.** If the student fixes it in the same breath ("they are not they are barely speaking"), do not tag it. Mention it as a strength in the analysis.
- **Skip pronunciation and transcription noise.** Only tag what the written transcript shows. If Whisper may have smoothed a line, leave it.
- **Quote exactly**, errors included, with the `mm:ss` of the turn and a short correction.
- Save the tags as `~/eng-teaching-records/transcripts/<slug>-<YYYY-MM-DD>-errors.tsv`, one error per line, tab separated: `CODE`, `mm:ss`, quote, correction. Lines starting with `#` are ignored.

## The codes
Run `python3 -I scripts/error_ledger.py codes` for the live list. The number is how much the error usually hurts understanding (3 = often blocks meaning); the tracker multiplies it by the latest rate to rank priorities.

| Code | Impact | What counts | Example |
|---|---|---|---|
| BE | 3 | Missing or wrong *be*, including auxiliary *be* | "if you interested" |
| SVA | 2 | Verb does not agree with its subject | "his competitors was older" |
| TENSE | 3 | Wrong tense, or drifting between tenses in a story | "when we just get the reception" (got) |
| FEEL | 1 | Feeling adjectives (-ed/-ing) and get/be with feelings | "we were so exciting" |
| ART | 1 | Missing, extra or wrong article or determiner | "it's lack of electricity" |
| PLUR | 1 | Plurals, countable vs. uncountable, possessive 's | "business in Ukraine have to pay" |
| VPREP | 2 | Wrong or missing preposition or object after a verb | "replied me", "agreed in something" |
| COMP | 2 | Comparatives, superlatives, "the same as" | "the best better scenario" |
| WFORM | 2 | Right word, wrong form | "without navigate", "confidence" for *confident* |
| QFORM | 3 | Question and indirect-question word order and auxiliaries | "why you told me why you got written down" |
| ORDER | 2 | Word order outside questions | "to give to our people jobs" |
| LINK | 1 | Missing or misused linking words (*however*, *although*) | "and then, and then" for a contrast |
| WCHOICE | 3 | Wrong word or wrong register; false friends | "absolutely actual topic" (current) |
| COLLOC | 2 | Words that do not go together | "did a lot of mistakes" (made) |
| OTHER | 1 | A real grammar error that fits nowhere else | use sparingly |

Add a code only when OTHER holds at least five errors of the same kind across sessions, and add it to both this file and `CODES` in the script.

## Choosing between codes
- Pick the code that explains the error, not the one that describes the surface. "I got shocked" is FEEL, not VPREP.
- WFORM is the right root with the wrong ending (confidence/confident). WCHOICE is a different word altogether.
- VPREP is a preposition or object problem after a verb (*agree in*). COLLOC is a fixed pair that sounds wrong (*do a mistake*). If a verb + noun pair is wrong, use COLLOC.
- Question errors always go to QFORM, even if they also involve tense or *be*.
- Likely first-language transfer goes in the analysis text, not in the tag. Example: "actual" for *current* from Ukrainian and Russian.

## Reading the tracker
- Rates are errors per 1,000 student words. A 60-minute session with a talkative student is around 2,000 words, so three errors is about 1.5.
- A code is **present** at 1.5 or above. Statuses: baseline (one session), new, improving, fading, stuck (three sessions, flat), rising, steady, minor (under 3 tagged in total).
- The machine transcript can smooth errors out, so compare a student with themselves, never with another student.
- Counts under about 5 move a lot by chance. Say "first impression" in the analysis until a pattern has held for two sessions.
- Stuck means the current teaching approach is not working for that code. Suggest a different approach in the teaching notes (retell cycle, chunks instead of rules, noticing tasks), not more of the same drill.
