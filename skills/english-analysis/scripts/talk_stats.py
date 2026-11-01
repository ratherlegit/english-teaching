#!/usr/bin/env python3
"""Talk-time share, longest turns and filler counts from a labeled transcript.

Usage: talk_stats.py <labeled_transcript.md> <StudentName> [TutorLabel]
Expects turn lines like:  **[12:34] Maria:** text   (default tutor label: Tutor)
Text in [square brackets] (analyst notes) is ignored. Run with `python3 -I`.
Report fillers as raw counts; judge which "like" uses are real fillers by reading.
"""
import re, sys

FILLERS = ["like", "i don't know", "uh", "um", "you know", "yeah", "so", "maybe",
           "i suppose", "i think", "i believe", "actually", "basically"]

def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    path, student = sys.argv[1], sys.argv[2]
    tutor = sys.argv[3] if len(sys.argv) > 3 else "Tutor"
    text = open(path).read().split("\n---\n", 1)[-1]
    turns = re.findall(r"\*\*\[(\d+):(\d+)\] ([^:*]+):\*\* (.*)", text)
    words = {student: 0, tutor: 0}
    mine, longest = [], []
    for m, s, who, body in turns:
        body = re.sub(r"\[[^\]]*\]", "", body)
        n = len(re.findall(r"[A-Za-z']+", body))
        if who in words:
            words[who] += n
        if who == student:
            mine.append(body)
            longest.append((n, f"{m}:{s}"))
    total = sum(words.values()) or 1
    print("words:", words, {k: f"{100*v/total:.0f}%" for k, v in words.items()})
    print(f"{student} turns: {len(longest)}; longest (words, time): {sorted(longest, reverse=True)[:5]}")
    low = " ".join(mine).lower()
    n = max(len(re.findall(r"[a-z']+", low)), 1)
    for f in FILLERS:
        c = len(re.findall(r"\b" + re.escape(f) + r"\b", low))
        print(f"  {f!r}: {c} ({100*c/n:.1f}% of {student}'s {n} words)")

if __name__ == "__main__":
    main()
