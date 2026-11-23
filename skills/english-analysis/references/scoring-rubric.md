# Scoring rubric

## Contents
- Level (CEFR)
- Score (1-100)
- Grammar anchor from the error rate
- Task mix
- Category guide
- Calibration anchors
- Caveats to state in every analysis

## Level (CEFR)
Report a CEFR level with half-steps: A2, A2+, B1, B1+, B2, B2+, C1, C1+, C2. Never a letter grade (A/B/C alone is not used in the records). Judge the level from CEFR descriptors for spoken production and interaction, not from the number. Compare with the Level line in the student's profile: say whether the recording supports it, and let the tutor decide before changing the profile.

## Score (1-100)
Three categories, each out of 25: fluency, vocabulary, grammar. Use whole or half points (18.5 is allowed), because one whole point moves the total by 1.3 and real changes can be smaller. Score = (sum / 75) x 100, rounded. Show the three parts and the sum, as in the anchors below. Pronunciation is not scored (text only) and is not shown in score tables; list pronunciation targets separately at low confidence.

Treat every score as plus or minus 3 (provisional, from one speaker whose recordings varied by 3 points with no clear change). A difference smaller than 3 between two recordings is noise. Report movement from the average of the last three recordings, which `error_ledger.py history` prints, and say "no measurable change" when the average stays within 3.

The number is for tracking one student across recordings, not for comparing students. Two students with the same level can score differently.

## Grammar anchor from the error rate
Do not set the grammar score by feel alone. After tagging errors, take the session's errors per 1,000 student words (the number of lines in the errors.tsv divided by the student's word count from talk_stats.py, times 1,000) and start from this band, then move the score by at most 2 points for range of structures attempted and severity (impact-3 codes such as tense or word choice count more), and write the reason in the Analysis.

| Errors per 1,000 words | Grammar anchor (of 25) |
|---|---|
| under 5 | 23 |
| 5 to 9.9 | 21 |
| 10 to 14.9 | 19 |
| 15 to 19.9 | 16.5 |
| 20 to 24.9 | 14.5 |
| 25 to 29.9 | 13 |
| 30 to 39.9 | 11 |
| 40 or more | 9 |

These bands are provisional. They were fitted to one B2 speaker (six recordings, 17 to 24 errors per 1,000 words, grammar scored 14 to 15) and have not been tested at other levels. Revisit them after three or four students, and compare only counts tagged with the same standard (tag all of a student's recordings in one pass, as in `references/error-codes.md`). `error_ledger.py history` prints the anchor next to the score you gave.

## Task mix
The same score on a harder task is stronger evidence than on an easy one, so name what the session asked of the student. In every Analysis, list the share of her speech by task: open conversation, a prepared monologue, tutor-led review (words read with examples), reading aloud, and role play or debate. Prepared monologues on the student's own work show her best case; role plays, debates and unprepared answers are harder; reading aloud shows pronunciation and little else, so leave it out of fluency and vocabulary. When two recordings have the same score but a different mix, say which was harder and do not call the change flat without that comment.

## Category guide
- **Fluency (25)**: length of uninterrupted turns, organization of ideas, pauses and restarts, filler load (count raw, then read the "like" uses to see which are real fillers), self-repair, ability to keep going when a word is missing (circumlocution), reaction and small-talk phrases.
- **Vocabulary (25)**: range and precision, collocations, word form (energy/energetic), domain vocabulary for the student's job or interests, use of words from earlier lessons, and recall of previously taught items (see the vocabulary recall check in SKILL.md).
- **Grammar (25)**: accuracy and range. Rank error patterns by how often they occur and how much they hurt understanding. Quote the student's exact words. Note patterns that match the likely L1 transfer already noted in the profile.

Score what the student produced, not what the tutor said. Prompted review answers (explain this old word) show less than open answers; say which dominated the session.

## Calibration anchors
| Student | Level | Score | Fluency | Vocabulary | Grammar |
|---|---|---|---|---|---|
| Student A (two sessions) | B1+ | 63 | 18 | 15 | 14 |
| Student B (one session) | B2 | 71 | 20 | 18 | 15 |
| Student C (six recordings over six months) | B2 | 69 | 20 | 18 | 14 |

Keep new scores consistent with these: a B1+ speaker with frequent basic errors lands near 60-65; a B2 speaker with long coherent turns but steady errors lands near 70-75. Add each new student as an anchor row once analyzed, labeled Student C, D and so on. Never put real student names in this file.

## Caveats to state in every analysis
- One or two recordings is an estimate, not a validated test; confirm patterns in later lessons.
- Recording conditions (car, weak connection, phone) and what the session was (review vs open conversation).
- Speaker labels are inferred from context; the machine transcript may have corrected some learner errors.
- Scores are plus or minus 3, so say whether a change is inside that band.
- The task mix (see above), because a prepared monologue and a role play are not equally hard.
