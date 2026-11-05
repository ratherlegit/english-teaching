#!/usr/bin/env python3
"""Track a student's grammar and word-choice errors across recorded lessons.

Usage:
  error_ledger.py add <slug> <YYYY-MM-DD> <labeled_transcript.md> <StudentName> <errors.tsv>
                      [--tutor Tutor] [--label TEXT] [--write] [--records-dir DIR] [--backup-dir DIR]
                      [--split mm:ss] [--phase-names A,B] [--scores F,V,G] [--level B1+] [--talk-pct N]
                      [--allow-unmatched]
  error_ledger.py show <slug> [--write] [--records-dir DIR] [--backup-dir DIR]
  error_ledger.py score <slug> <YYYY-MM-DD> <fluency> <vocabulary> <grammar> <level> [talk_pct]
  error_ledger.py history <slug>
  error_ledger.py phases <slug>
  error_ledger.py codes

--split mm:ss splits the lesson into two phases (for example open conversation and tutor-led
review) and reports the error rate for each, because the two are not comparable. --phase-names
names them (default "first part,second part"). --scores/--level/--talk-pct store the analyst's
scores for the session; `score` stores them for an earlier session that has no tagged errors;
`history` prints the Score History table; `phases` prints each code's rate per phase for every session, so open talk is compared with open talk. Every quote in errors.tsv must appear in the
transcript (ignoring case and punctuation) or the run stops; --allow-unmatched overrides that.

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


def norm(text):
    text = text.lower().replace("\u2019", "'").replace("\u2018", "'")
    return " ".join(re.sub(r"[^a-z0-9' ]", " ", text).split())


def student_text(transcript, student):
    text = open(transcript, encoding="utf-8").read().split("\n---\n", 1)[-1]
    body = [re.sub(r"\[[^\]]*\]", " ", b) for _m, _s, who, b in
            re.findall(r"\*\*\[(\d+):(\d+)\] ([^:*]+):\*\* (.*)", text) if who == student]
    return norm(" ".join(body))


def unmatched_quotes(examples, transcript, student):
    """Quotes that do not appear in the student's own turns (ignoring case and punctuation)."""
    haystack = student_text(transcript, student)
    bad = []
    for code, rows in examples.items():
        for t, q, _f in rows:
            if norm(q) not in haystack:
                bad.append((code, t, q))
    return bad


def split_seconds(value):
    m = re.fullmatch(r"(\d+):(\d{2})", value or "")
    if not m:
        sys.exit("--split needs mm:ss")
    return int(m.group(1)) * 60 + int(m.group(2))


def phases(transcript, student, examples, split, names):
    """Student words and tagged errors before and after the split time."""
    text = open(transcript, encoding="utf-8").read().split("\n---\n", 1)[-1]
    words = [0, 0]
    for m, sec, who, body in re.findall(r"\*\*\[(\d+):(\d+)\] ([^:*]+):\*\* (.*)", text):
        if who == student:
            k = 0 if int(m) * 60 + int(sec) < split else 1
            words[k] += len(re.findall(r"[A-Za-z']+", re.sub(r"\[[^\]]*\]", "", body)))
    errs = [0, 0]
    for rows in examples.values():
        for t, _q, _f in rows:
            m = re.fullmatch(r"(\d+):(\d{2})", t)
            if m:
                errs[0 if int(m.group(1)) * 60 + int(m.group(2)) < split else 1] += 1
    return {"split": split, "names": names, "words": words, "errors": errs}


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
    phased = [x for x in sessions if x.get("phases") and all(x["phases"]["words"])]
    if phased:
        out.append("")
    for x in phased:
        ph = x["phases"]
        a, b = ph["words"]
        ea, eb = ph["errors"]
        sp = ph["split"]
        out.append(f"Phases in {x['date']} (split at {sp // 60:02d}:{sp % 60:02d}): "
                   f"{ph['names'][0]}: {a} words, {ea} errors ({1000.0 * ea / a:.1f} per 1,000); "
                   f"{ph['names'][1]}: {b} words, {eb} errors ({1000.0 * eb / b:.1f} per 1,000).")
    if phased:
        out.append("Compare each phase with the same kind of phase in other sessions, not with each other "
                   "(`error_ledger.py phases` prints the codes by phase).")
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


def render_phases(led):
    """Per-code error rates for each phase, one column per session that has a phase split."""
    sess = [x for x in sorted(led["sessions"], key=lambda x: x["date"])
            if x.get("phases") and all(x["phases"]["words"])]
    if not sess:
        return ""
    out = []
    for k in (0, 1):
        names = sess[-1]["phases"]["names"]
        per = []
        for x in sess:
            sp = x["phases"]["split"]
            cnt = {}
            for code, rows in x["examples"].items():
                for t, _q, _f in rows:
                    m = re.fullmatch(r"(\d+):(\d{2})", t)
                    if m and (0 if int(m.group(1)) * 60 + int(m.group(2)) < sp else 1) == k:
                        cnt[code] = cnt.get(code, 0) + 1
            per.append((cnt, x["phases"]["words"][k]))
        codes = [c for c in CODES if any(cnt.get(c) for cnt, _w in per)]
        codes.sort(key=lambda c: -per[-1][0].get(c, 0))
        out.append(f"### {names[k]} (errors per 1,000 student words in that phase, count in brackets)")
        out.append("")
        out.append("| Code | " + " | ".join(x["date"] for x in sess) + " |")
        out.append("|---|" + "---|" * len(sess))
        for c in codes:
            out.append(f"| {c} | " + " | ".join(f"{1000.0 * cnt.get(c, 0) / w:.1f} ({cnt.get(c, 0)})" for cnt, w in per) + " |")
        out.append("| All codes | " + " | ".join(f"{1000.0 * sum(cnt.values()) / w:.1f} ({sum(cnt.values())})" for cnt, w in per) + " |")
        out.append("")
    return "\n".join(out)


def set_scores(led, date, fluency, vocabulary, grammar, level, talk=None):
    total = round((fluency + vocabulary + grammar) / 75 * 100)
    row = {"date": date, "level": level, "fluency": fluency, "vocabulary": vocabulary,
           "grammar": grammar, "total": total, "talk_pct": talk}
    led["scores"] = [r for r in led.get("scores", []) if r["date"] != date] + [row]
    led["scores"].sort(key=lambda r: r["date"])


def render_history(led):
    rows = sorted(led.get("scores", []), key=lambda r: r["date"])
    if not rows:
        return ""
    out = ["| Date | Level | Fluency | Vocabulary | Grammar | Score | Student talk |", "|---|---|---|---|---|---|---|"]
    for r in rows:
        talk = f"{r['talk_pct']}%" if r.get("talk_pct") is not None else "n/a"
        out.append(f"| {r['date']} | {r['level']} | {r['fluency']}/25 | {r['vocabulary']}/25 | "
                   f"{r['grammar']}/25 | {r['total']}/100 | {talk} |")
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
    split = flag(a, "--split")
    phase_names = flag(a, "--phase-names", "first part,second part").split(",")
    scores = flag(a, "--scores")
    level = flag(a, "--level")
    talk_pct = flag(a, "--talk-pct")
    allow = "--allow-unmatched" in a
    if allow:
        a.remove("--allow-unmatched")
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
        bad = unmatched_quotes(examples, transcript, student)
        if bad and not allow:
            lines = "\n".join(f"  {c} [{t}] {q}" for c, t, q in bad)
            sys.exit(f"{len(bad)} tagged quote(s) are not in {student}'s turns in the transcript. "
                     f"Fix the .tsv (or pass --allow-unmatched):\n{lines}")
        entry = {"date": date, "label": label, "words": words, "counts": counts, "examples": examples}
        if split:
            if len(phase_names) != 2:
                sys.exit("--phase-names needs two names separated by a comma")
            entry["phases"] = phases(transcript, student, examples, split_seconds(split), phase_names)
        led["sessions"] = [s for s in led["sessions"] if s["date"] != date]
        led["sessions"].append(entry)
        if scores:
            try:
                f, v, g = [int(x) for x in scores.split(",")]
            except ValueError:
                sys.exit("--scores needs three whole numbers: fluency,vocabulary,grammar")
            if not level:
                sys.exit("--scores also needs --level (for example B1+)")
            set_scores(led, date, f, v, g, level, int(talk_pct) if talk_pct else None)
        os.makedirs(os.path.dirname(ledger_path), exist_ok=True)
        json.dump(led, open(ledger_path, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
        print(f"Saved {date}: {words} student words, {sum(counts.values())} errors tagged -> {ledger_path}")
    elif cmd == "score":
        if len(a) not in (7, 8) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", a[2]):
            sys.exit(__doc__)
        set_scores(led, a[2], int(a[3]), int(a[4]), int(a[5]), a[6], int(a[7]) if len(a) == 8 else None)
        os.makedirs(os.path.dirname(ledger_path), exist_ok=True)
        json.dump(led, open(ledger_path, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
        print(render_history(led))
        return
    elif cmd == "phases":
        table = render_phases(led)
        if not table:
            sys.exit(f"No sessions with a phase split for {slug}. Use --split when adding a session.")
        print(table)
        return
    elif cmd == "history":
        hist = render_history(led)
        if not hist:
            sys.exit(f"No scores recorded for {slug}. Use `score` to add earlier sessions.")
        print(hist)
        return
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
