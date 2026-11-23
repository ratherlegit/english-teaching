#!/usr/bin/env python3
"""Build the labeled transcript from the raw Whisper output and a short speaker map.

Usage: label_transcript.py <raw.txt> <map.txt> <header.md> <out.md> --student NAME [--tutor Tutor]

<raw.txt> is the transcribe.py output, lines like "[12:34] text". Line numbers are the
physical line numbers (the Read tool shows them). <map.txt> is the only thing the analyst
writes about speakers, one entry per line:

  1 T                      from the start of line 1, the tutor is speaking (until the next entry)
  4 S                      from the start of line 4, the student is speaking
  9 T?                     tutor, but uncertain (the turn gets [speaker uncertain])
  14 "so today you" T      the speaker changes in the MIDDLE of line 14, where the quoted
                           words begin (Whisper often puts both speakers in one line)
  fix 12 Bucharest => Budapest [heard as "Bucharest"]    exact text replacement on one line
  # comments and blank lines are ignored

Only the switches are listed, so the map is a few hundred short lines instead of the whole
lesson. A speaker stays in force until the next entry. Entries go in order. Several entries may
share a line if all but the first carry a quoted anchor; an anchor is a few words exactly as they
appear in the raw line (case ignored), and finds the first match after the previous entry on
that line. A fix must sit inside one speaker's words. <header.md> holds the "# title" and the
reliability block; the script adds the "---" line and the turns. Consecutive pieces from one
speaker (same certainty) are merged into one turn, timed at its first piece (a mid-line piece
gets a time estimated between its line and the next one). Run with `python3 -I`.

The script prints each speaker's share of words and a short list of turns worth a second look
(uncertain turns, one-to-three-word turns between two turns of the other speaker, and words
labeled as the student that read like tutor prompts). It exits with an error, and writes
nothing, if the map is inconsistent, so a bad map can never produce a quietly wrong transcript.
"""
import os
import re
import sys

RAW_RE = re.compile(r"\[(\d+):(\d{2})\] (.*)")
ENTRY_RE = re.compile(r'(\d+)(?:\s+"([^"]+)")?\s+([TS])(\?)?')
FIX_RE = re.compile(r"fix\s+(\d+)\s+(.+?)\s+=>\s+(.*)")
NAME_RE = re.compile(r"[A-Za-z][A-Za-z '\-]{0,40}")
PROMPT_RE = re.compile(r"^(can you|could you|let's|lets|please|tell me|what do you think|how do you say|"
                       r"do you want|what about|try to|read|repeat|now)\b", re.I)
SHOW = 10


def fail(msg):
    sys.exit(f"label_transcript: {msg}")


def read_raw(path):
    lines = {}
    for n, line in enumerate(open(path, encoding="utf-8"), 1):
        line = line.rstrip("\n")
        if not line.strip():
            continue
        m = RAW_RE.fullmatch(line)
        if not m:
            fail(f"{path} line {n} is not '[mm:ss] text': {line[:60]!r}")
        lines[n] = (int(m.group(1)) * 60 + int(m.group(2)), m.group(3).strip())
    if not lines:
        fail(f"{path} has no transcript lines")
    return lines


def read_map(path, lines):
    entries, fixes = [], {}
    last = 0
    last_line = max(lines)
    for n, raw in enumerate(open(path, encoding="utf-8"), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        fx = FIX_RE.fullmatch(line)
        if fx:
            ln, old, new = int(fx.group(1)), fx.group(2), fx.group(3)
            if ln not in lines:
                fail(f"map line {n}: fix refers to line {ln}, which is not in the raw file")
            if old not in lines[ln][1]:
                fail(f"map line {n}: {old!r} is not in raw line {ln}")
            fixes.setdefault(ln, []).append((old, new))
            continue
        m = ENTRY_RE.fullmatch(line)
        if not m:
            fail(f"map line {n} is not 'LINE [\"words\"] T|S[?]' or 'fix LINE old => new': {line[:60]!r}")
        ln, anchor = int(m.group(1)), m.group(2)
        if ln < last or (ln == last and not anchor):
            fail(f"map line {n}: entries must go in increasing line order (got {ln} after {last})")
        if ln > last_line:
            fail(f"map line {n}: line {ln} is past the end of the raw file ({last_line})")
        if anchor and ln not in lines:
            fail(f"map line {n}: line {ln} is not in the raw file")
        entries.append({"line": ln, "anchor": anchor, "who": m.group(3), "unc": bool(m.group(4)), "n": n})
        last = ln
    if not entries:
        fail("the map has no speaker entries")
    return entries, fixes


def clock(secs):
    return f"{int(secs) // 60:02d}:{int(secs) % 60:02d}"


def build_pieces(lines, entries, fixes):
    """Cut every raw line into pieces, one per speaker stretch: dicts with line, secs, who, unc, text."""
    order = sorted(lines)
    pieces, k, cur = [], 0, None
    for i, ln in enumerate(order):
        secs, text = lines[ln]
        nxt = lines[order[i + 1]][0] if i + 1 < len(order) else None
        while k < len(entries) and entries[k]["line"] < ln:
            cur = (entries[k]["who"], entries[k]["unc"])
            k += 1
        cuts, last_pos = [], -1
        while k < len(entries) and entries[k]["line"] == ln:
            e = entries[k]
            k += 1
            if e["anchor"]:
                pos = text.lower().find(e["anchor"].lower(), last_pos + 1)
                if pos < 0:
                    fail(f"map line {e['n']}: {e['anchor']!r} not found in raw line {ln}"
                         + (" after the previous entry on that line" if last_pos >= 0 else ""))
            else:
                pos = 0
            cuts.append((pos, (e["who"], e["unc"])))
            last_pos = pos
        segs = [] if cuts and cuts[0][0] == 0 else [(0, cur)]
        segs += cuts
        if segs[0][1] is None:
            fail(f"raw line {ln} has no speaker: the first entry must start at line {order[0]}"
                 " (or quote where the first speaker starts)")
        cur = segs[-1][1]
        parts = []
        for j, (pos, sp) in enumerate(segs):
            end = segs[j + 1][0] if j + 1 < len(segs) else len(text)
            parts.append({"line": ln, "start": pos, "end": end, "who": sp[0], "unc": sp[1]})
        for old, new in fixes.get(ln, []):
            at = text.find(old)
            home = [p for p in parts if p["start"] <= at and at + len(old) <= p["end"]]
            if not home:
                fail(f"fix {old!r} on raw line {ln} runs across a speaker change; make the fix text sit inside one speaker's words")
            home[0].setdefault("fixes", []).append((at, old, new))
        for p in parts:
            body = text[p["start"]:p["end"]]
            for at, old, new in sorted(p.get("fixes", []), reverse=True):
                body = body[:at - p["start"]] + new + body[at - p["start"] + len(old):]
            body = body.strip()
            if not body:
                continue
            frac = p["start"] / max(len(text), 1)
            p["secs"] = secs + (nxt - secs) * frac if nxt and nxt > secs and p["start"] else secs
            p["text"] = body
            pieces.append(p)
    return pieces


def build_turns(pieces):
    turns = []
    for p in pieces:
        last = turns[-1] if turns else None
        if last and last["who"] == p["who"] and last["unc"] == p["unc"]:
            last["text"] += " " + p["text"]
        else:
            turns.append({"line": p["line"], "secs": p["secs"], "who": p["who"], "unc": p["unc"], "text": p["text"]})
    return turns


def words(text):
    return len(re.findall(r"[A-Za-z']+", re.sub(r"\[[^\]]*\]", "", text)))


def report(turns, pieces, name, tutor):
    wc = {"S": 0, "T": 0}
    for t in turns:
        wc[t["who"]] += words(t["text"])
    total = sum(wc.values()) or 1
    print(f"{len(turns)} turns. {tutor}: {wc['T']} words ({100 * wc['T'] / total:.0f}%), "
          f"{name}: {wc['S']} words ({100 * wc['S'] / total:.0f}%).")
    problems = []
    share = wc["S"] / total
    if share < 0.15 or share > 0.85:
        problems.append(f"WARN: {name} has {100 * share:.0f}% of the words, which is unusual for a lesson; "
                        "check that T and S are not swapped.")
    if len(turns) < 20:
        problems.append(f"WARN: only {len(turns)} turns; the map may be missing speaker changes.")
    unc = [t for t in turns if t["unc"]]
    short = [turns[i] for i in range(1, len(turns) - 1)
             if words(turns[i]["text"]) <= 3 and turns[i - 1]["who"] == turns[i + 1]["who"] != turns[i]["who"]
             and not turns[i]["unc"]]
    prompts = [p for p in pieces if p["who"] == "S" and not p["unc"] and PROMPT_RE.match(p["text"])]
    for label, items in (("Uncertain turns (kept marked; not tagged for errors)", unc),
                         ("Short turns between two turns of the other speaker (usually fine: yeah, okay)", short),
                         (f"Words labeled as {name} that read like tutor prompts (check the labels)", prompts)):
        if items:
            print(f"{label}: {len(items)}")
            for t in items[:SHOW]:
                who = name if t["who"] == "S" else tutor
                print(f"  raw line {t['line']} [{clock(t['secs'])}] {who}: {t['text'][:70]}")
            if len(items) > SHOW:
                print(f"  ... and {len(items) - SHOW} more")
    for p in problems:
        print(p)


def main():
    a = sys.argv[1:]
    name, tutor = None, "Tutor"
    for flag in ("--student", "--tutor"):
        if flag in a:
            i = a.index(flag)
            if i + 1 >= len(a):
                fail(f"{flag} needs a value")
            if flag == "--student":
                name = a[i + 1]
            else:
                tutor = a[i + 1]
            del a[i:i + 2]
    if len(a) != 4 or not name:
        sys.exit(__doc__)
    raw_path, map_path, header_path, out_path = [os.path.expanduser(x) for x in a]
    for label in (name, tutor):
        if not NAME_RE.fullmatch(label):
            fail(f"bad speaker label {label!r}: letters, spaces, apostrophes and hyphens only")
    if name == tutor:
        fail("student and tutor labels must differ")
    header = open(header_path, encoding="utf-8").read().rstrip()
    if not header.startswith("# "):
        fail("the header must start with a '# title' line")
    if re.search(r"^---\s*$", header, re.M):
        fail("the header must not contain a '---' line (the script adds it)")
    if chr(0x2014) in header:
        fail("the header contains an em dash; use a period, comma, colon or parentheses")
    lines = read_raw(raw_path)
    entries, fixes = read_map(map_path, lines)
    pieces = build_pieces(lines, entries, fixes)
    turns = build_turns(pieces)
    label = {"S": name, "T": tutor}
    body = []
    for t in turns:
        text = t["text"] + (" [speaker uncertain]" if t["unc"] else "")
        body.append(f"**[{clock(t['secs'])}] {label[t['who']]}:** {text}")
    out = header + "\n\n---\n\n" + "\n\n".join(body) + "\n"
    fd = os.open(out_path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write(out)
    os.chmod(out_path, 0o600)
    print(f"Wrote {out_path}")
    report(turns, pieces, name, tutor)


if __name__ == "__main__":
    main()
