#!/usr/bin/env python3
"""Tutor-side measures from a labeled transcript, for the tutor tips in the lesson report.

Usage: tutor_stats.py <labeled_transcript.md> <StudentName> [--tutor Tutor] [--split mm:ss]
Expects turn lines like:  **[12:34] Maria:** text   (default tutor label: Tutor)
Text in [square brackets] (analyst notes) is ignored. Run with `python3 -I`.

Prints, for the whole lesson and, with --split, for the part before and after that time
(for example where open conversation ends and tutor-led review begins):
  - student share of words
  - tutor turns of 100+ words (long explanations): how many, and the longest
  - tutor questions, and how many were followed by a student answer of 15+ words
  - the share of student turns that are 5 words or fewer
These are counts to read, not scores. Judge the teaching by reading the transcript too.
"""
import re, sys

LONG_TURN = 100      # tutor words in one turn that count as a long explanation
OPEN_ANSWER = 15     # student words that make an answer a real answer
SHORT_REPLY = 5      # student words or fewer is a one-line reply


def parse(path):
    text = open(path, encoding="utf-8").read().split("\n---\n", 1)[-1]
    turns = []
    for m, s, who, body in re.findall(r"\*\*\[(\d+):(\d+)\] ([^:*]+):\*\* (.*)", text):
        clean = re.sub(r"\[[^\]]*\]", "", body)
        turns.append({"t": int(m) * 60 + int(s), "who": who.strip(), "body": clean,
                      "n": len(re.findall(r"[A-Za-z']+", clean))})
    return turns


def stamp(sec):
    return f"{sec // 60:02d}:{sec % 60:02d}"


def measure(turns, student, tutor):
    sw = sum(t["n"] for t in turns if t["who"] == student)
    tw = sum(t["n"] for t in turns if t["who"] == tutor)
    tt = [t for t in turns if t["who"] == tutor]
    long_turns = sorted(((t["n"], stamp(t["t"])) for t in tt if t["n"] >= LONG_TURN), reverse=True)
    questions = answered = 0
    for i, t in enumerate(turns):
        if t["who"] != tutor or "?" not in t["body"]:
            continue
        questions += 1
        nxt = next((u for u in turns[i + 1:] if u["who"] != tutor), None)
        if nxt is not None and nxt["who"] == student and nxt["n"] >= OPEN_ANSWER:
            answered += 1
    st = [t for t in turns if t["who"] == student]
    short = sum(1 for t in st if t["n"] <= SHORT_REPLY)
    return {"student_words": sw, "tutor_words": tw, "tutor_turns": len(tt), "long": long_turns,
            "questions": questions, "answered": answered, "student_turns": len(st), "short": short}


def show(label, m):
    total = (m["student_words"] + m["tutor_words"]) or 1
    sp = 100 * m["student_words"] / total
    print(f"{label}: student {m['student_words']} words ({sp:.0f}%), tutor {m['tutor_words']} words ({100 - sp:.0f}%)")
    longest = ", ".join(f"{n} words at {t}" for n, t in m["long"][:3]) or "none"
    print(f"  tutor turns of {LONG_TURN}+ words: {len(m['long'])} of {m['tutor_turns']} (longest: {longest})")
    print(f"  tutor questions: {m['questions']}; followed by a student answer of {OPEN_ANSWER}+ words: {m['answered']}")
    pct = 100 * m["short"] / (m["student_turns"] or 1)
    print(f"  student turns of {SHORT_REPLY} words or fewer: {m['short']} of {m['student_turns']} ({pct:.0f}%)")


def main():
    a = sys.argv[1:]
    if len(a) < 2:
        sys.exit(__doc__)
    tutor, split = "Tutor", None
    if "--tutor" in a:
        i = a.index("--tutor"); tutor = a[i + 1]; del a[i:i + 2]
    if "--split" in a:
        i = a.index("--split")
        mm = re.fullmatch(r"(\d+):(\d{2})", a[i + 1])
        if not mm:
            sys.exit("--split needs mm:ss")
        split = int(mm.group(1)) * 60 + int(mm.group(2)); del a[i:i + 2]
    path, student = a[0], a[1]
    turns = parse(path)
    if not any(t["who"] == student for t in turns):
        sys.exit(f"No turns found for speaker label '{student}' in {path}")
    show("Whole lesson", measure(turns, student, tutor))
    if split is not None:
        show(f"Before {stamp(split)}", measure([t for t in turns if t["t"] < split], student, tutor))
        show(f"From {stamp(split)}", measure([t for t in turns if t["t"] >= split], student, tutor))


if __name__ == "__main__":
    main()
