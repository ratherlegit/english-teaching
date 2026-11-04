#!/usr/bin/env python3
"""Track a student's grammar and word-choice errors across recorded lessons.

Usage:
  error_ledger.py add <slug> <YYYY-MM-DD> <labeled_transcript.md> <StudentName> <errors.tsv>
                      [--tutor Tutor] [--label TEXT] [--write] [--records-dir DIR] [--backup-dir DIR]
  error_ledger.py show <slug> [--write] [--records-dir DIR] [--backup-dir DIR]
  error_ledger.py codes

errors.tsv has one error per line, tab separated:  CODE <TAB> mm:ss <TAB> quote <TAB> correction
Lines starting with # and blank lines are skipped. Codes are listed by `codes` and in
references/error-codes.md. The analyst (Claude) tags the errors by reading the transcript;
this script only does the counting, trend rules and table rendering.

The ledger lives in <records-dir>/error-ledgers/<slug>.json (one entry per session date;
adding the same date again replaces it). With --write the rendered "## Error Tracker" section
is put into <records-dir>/<slug>.md (replaced if present, otherwise inserted before the first
"## Analysis" heading, otherwise appended), after copying the record to --backup-dir.
Run with `python3 -I`.
"""
import json, os, re, shutil, sys, tempfile

# code: (short name, impact on understanding 1-3)
CODES = {
    "BE":      ("missing or wrong 'be'", 3),
    "SVA":     ("subject-verb agreement", 2),
    "TENSE":   ("tense choice or drift", 3),
    "FEEL":    ("feeling adjectives and get/be (excited/exciting)", 1),
    "ART":     ("articles and determiners", 1),
    "PLUR":    ("plurals, countable/uncountable, possessive 's", 1),
    "VPREP":   ("verb + preposition or object", 2),
    "COMP":    ("comparatives and superlatives", 2),
    "WFORM":   ("word form (confidence/confident)", 2),
    "QFORM":   ("question and indirect-question forms", 3),
    "ORDER":   ("word order", 2),
    "LINK":    ("linking and connecting words", 1),
    "WCHOICE": ("wrong word or register", 3),
    "COLLOC":  ("collocation (make/do, strong/heavy)", 2),
    "OTHER":   ("other grammar error", 1),
}
PRESENT = 1.5      # errors per 1,000 words at or above this counts as "present" (about 3 in a 2,000-word session)
MIN_TOTAL = 3      # fewer tagged instances than this across all sessions is noise, not a pattern
CHANGE = 0.30      # relative change that counts as a real move


def paths(records, slug):
    return (os.path.join(records, "error-ledgers", slug + ".json"),
            os.path.join(records, slug + ".md"))


def student_words(transcript, student, tutor):
    text = open(transcript, encoding="utf-8").read().split("\n---\n", 1)[-1]
    n = 0
    for _m, _s, who, body in re.findall(r"\*\*\[(\d+):(\d+)\] ([^:*]+):\*\* (.*)", text):
        if who == student:
            n += len(re.findall(r"[A-Za-z']+", re.sub(r"\[[^\]]*\]", "", body)))
    if n == 0:
        sys.exit(f"No turns found for speaker label '{student}' in {transcript}")
    return n


def read_errors(path):
    counts, examples = {}, {}
    for i, line in enumerate(open(path, encoding="utf-8"), 1):
        if not line.strip() or line.startswith("#"):
            continue
        parts = line.rstrip("\n").split("\t")
        code = parts[0].strip().upper()
        if code not in CODES:
            sys.exit(f"{path}:{i}: unknown code '{code}'. Run `codes` to list them.")
        if len(parts) < 3:
            sys.exit(f"{path}:{i}: need CODE, time, quote (and optionally correction), tab separated")
        counts[code] = counts.get(code, 0) + 1
        quote = parts[2].strip()
        fix = parts[3].strip() if len(parts) > 3 else ""
        examples.setdefault(code, []).append([parts[1].strip(), quote, fix])
    return counts, examples


def status(rates, total=99):
    """rates: errors per 1,000 words per session, oldest first (zeros included)."""
    if len(rates) < 2:
        return "baseline"
    if total < MIN_TOTAL:
        return "minor"
    last, prev = rates[-1], rates[-2]
    if max(last, prev) < PRESENT:
        return "minor"
    if last < PRESENT and prev < PRESENT:
        return "fading"
    if last >= PRESENT and all(r < PRESENT for r in rates[:-1]):
        return "new"
    if last < PRESENT and prev >= PRESENT:
        return "improving"
    if len(rates) >= 3:
        tail = rates[-3:]
        mean = sum(tail) / 3
        if min(tail) >= PRESENT and (max(tail) - min(tail)) <= CHANGE * mean * 2:
            if last >= prev * (1 - CHANGE):
                return "stuck"
    if prev >= PRESENT and last <= prev * (1 - CHANGE):
        return "improving"
    if prev >= PRESENT and last >= prev * (1 + CHANGE):
        return "rising"
    return "steady"


def render(slug, led):
    sessions = sorted(led["sessions"], key=lambda s: s["date"])
    if not sessions:
        return ""
    codes = [c for c in CODES if any(s["counts"].get(c) for s in sessions)]
    rows = []
    for c in codes:
        rates = [1000.0 * s["counts"].get(c, 0) / s["words"] for s in sessions]
        total = sum(s["counts"].get(c, 0) for s in sessions)
        rows.append((rates[-1] * CODES[c][1], c, rates, status(rates, total)))
    rows.sort(key=lambda r: (-r[0], r[1]))
    n = len(sessions)
    out = ["## Error Tracker",
           f"Generated by scripts/error_ledger.py from error-ledgers/{slug}.json (last session {sessions[-1]['date']}). "
           "Cells show errors per 1,000 student words, with the raw count in brackets. A code with under 3 instances in total is shown as minor, because so few cases are noise. The machine transcript "
           "may smooth over some errors, so treat rates as relative to this student's earlier sessions, not as absolute scores. "
           "Priority is the latest rate times how much the error hurts understanding."]
    if n < 3:
        out.append(f"Provisional: {n} session{'s' if n != 1 else ''} so far, so statuses are first impressions. "
                   "A status of stuck needs three sessions.")
    head = "| Priority | Code | Pattern | " + " | ".join(s["date"] for s in sessions) + " | Status |"
    out += ["", head, "|" + "---|" * (4 + n)]
    for k, (_p, c, rates, st) in enumerate(rows, 1):
        cells = []
        for s, r in zip(sessions, rates):
            cells.append(f"{r:.1f} ({s['counts'].get(c, 0)})")
        out.append(f"| {k} | {c} | {CODES[c][0]} | " + " | ".join(cells) + f" | {st} |")
    out.append("")
    out.append("Student words per session: " + ", ".join(f"{s['date']}: {s['words']}" for s in sessions)
               + ". Errors tagged: " + ", ".join(f"{s['date']}: {sum(s['counts'].values())}" for s in sessions) + ".")
    last = sessions[-1]
    out.append("")
    out.append(f"Examples from {last['date']} (top codes):")
    shown = 0
    for _p, c, _r, _st in rows:
        ex = last["examples"].get(c)
        if not ex:
            continue
        for t, q, f in ex[:2]:
            out.append(f"- {c} [{t}] \"{q}\"" + (f" -> \"{f}\"" if f else ""))
        shown += 1
        if shown == 5:
            break
    return "\n".join(out) + "\n"


def write_section(rec, section, backup_dir):
    text = open(rec, encoding="utf-8").read()
    os.makedirs(backup_dir, exist_ok=True)
    shutil.copy2(rec, os.path.join(backup_dir, os.path.basename(rec) + ".before-error-tracker"))
    pat = re.compile(r"^## Error Tracker\n.*?(?=^## |\Z)", re.S | re.M)
    if pat.search(text):
        text = pat.sub(lambda m: section + "\n", text, count=1)
    else:
        m = re.search(r"^## Analysis", text, re.M)
        if m:
            text = text[:m.start()] + section + "\n" + text[m.start():]
        else:
            text = text.rstrip("\n") + "\n\n" + section
    open(rec, "w", encoding="utf-8").write(text)


def flag(args, name, default=None):
    if name in args:
        i = args.index(name)
        val = args[i + 1]
        del args[i:i + 2]
        return val
    return default


def main():
    a = sys.argv[1:]
    if not a:
        sys.exit(__doc__)
    write = "--write" in a
    if write:
        a.remove("--write")
    records = os.path.expanduser(flag(a, "--records-dir", "~/eng-teaching-records"))
    backup = os.path.expanduser(flag(a, "--backup-dir", tempfile.gettempdir()))
    tutor = flag(a, "--tutor", "Tutor")
    label = flag(a, "--label", "")
    cmd = a[0]
    if cmd == "codes":
        for c, (name, imp) in CODES.items():
            print(f"{c:8} impact {imp}  {name}")
        return
    if len(a) < 2:
        sys.exit(__doc__)
    slug = a[1]
    ledger_path, rec = paths(records, slug)
    led = {"student": slug, "sessions": []}
    if os.path.exists(ledger_path):
        led = json.load(open(ledger_path, encoding="utf-8"))
    if cmd == "add":
        if len(a) != 6:
            sys.exit(__doc__)
        date, transcript, student, errors = a[2:6]
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", date):
            sys.exit("date must be YYYY-MM-DD")
        words = student_words(transcript, student, tutor)
        counts, examples = read_errors(errors)
        led["sessions"] = [s for s in led["sessions"] if s["date"] != date]
        led["sessions"].append({"date": date, "label": label, "words": words,
                                "counts": counts, "examples": examples})
        os.makedirs(os.path.dirname(ledger_path), exist_ok=True)
        json.dump(led, open(ledger_path, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
        print(f"Saved {date}: {words} student words, {sum(counts.values())} errors tagged -> {ledger_path}")
    elif cmd != "show":
        sys.exit(__doc__)
    section = render(slug, led)
    if not section:
        sys.exit(f"No sessions recorded for {slug}")
    print(section)
    if write:
        if not os.path.exists(rec):
            sys.exit(f"No student record at {rec}")
        write_section(rec, section, backup)
        print(f"Wrote the Error Tracker section into {rec} (backup in {backup})")


if __name__ == "__main__":
    main()
