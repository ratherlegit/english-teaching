#!/usr/bin/env python3
"""Build a self-contained student performance dashboard (one HTML file).

Usage: build_dashboard.py [--records-dir DIR] [--out FILE]
Reads <records-dir>/error-ledgers/<slug>.json (written by english-analysis) and the
student's record <records-dir>/<slug>.md (display name only). Writes
<records-dir>/dashboard/dashboard.html (owner-only) and prints its path.
The page needs no network: charts are inline SVG drawn by the script embedded in it.
Student text goes into the page as JSON and is shown with textContent only.
Read-only for everything except the output file. Run with `python3 -I`.
"""
import json, os, re, sys
from datetime import date as _date
from pathlib import Path

SLUG_RE = re.compile(r"[a-z0-9][a-z0-9_-]{0,63}")
DATE_RE = re.compile(r"\d{4}-\d{2}-\d{2}")
MAX_SESSIONS = 400
MAX_EXAMPLES = 6

# Mirrors CODES in english-analysis/scripts/error_ledger.py (tests/validate_skill.py checks they match).
CODES = {
    "BE": "missing or wrong 'be'", "SVA": "subject-verb agreement", "TENSE": "tense choice or drift",
    "FEEL": "feeling adjectives and get/be", "ART": "articles and determiners",
    "PLUR": "plurals, countable/uncountable, possessive 's", "VPREP": "verb + preposition or object",
    "COMP": "comparatives and superlatives", "WFORM": "word form", "QFORM": "question forms",
    "ORDER": "word order", "LINK": "linking words", "WCHOICE": "wrong word or register",
    "COLLOC": "collocation", "OTHER": "other grammar error",
}


def num(x, default=None):
    if isinstance(x, bool) or not isinstance(x, (int, float)):
        return default
    return float(x)


def text(x, limit=300):
    return x[:limit] if isinstance(x, str) else ""


def good_date(d):
    if not isinstance(d, str) or not DATE_RE.fullmatch(d):
        return False
    try:
        _date.fromisoformat(d)
        return True
    except ValueError:
        return False


def display_name(records, slug):
    try:
        head = (records / f"{slug}.md").read_text(encoding="utf-8")[:400]
    except OSError:
        return slug
    m = re.match(r"#\s*Student Record\s*[^\w\s]\s*(.+)", head)
    return text(m.group(1).strip(), 60) if m else slug


def profile_level(records, slug):
    try:
        t = (records / f"{slug}.md").read_text(encoding="utf-8")
    except OSError:
        return ""
    m = re.search(r"^- Level:\s*(.+)$", t, re.M)
    return text(m.group(1).strip(), 20) if m else ""


def load_student(records, path, warn):
    slug = path.stem
    if not SLUG_RE.fullmatch(slug):
        warn(f"skipped {path.name}: file name is not a valid student slug")
        return None
    try:
        led = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        warn(f"skipped {path.name}: {e}")
        return None
    if not isinstance(led, dict):
        warn(f"skipped {path.name}: unexpected format")
        return None
    sessions = []
    for s in (led.get("sessions") or [])[:MAX_SESSIONS]:
        if not isinstance(s, dict) or not good_date(s.get("date")):
            warn(f"{slug}: skipped a session with a bad date")
            continue
        words = num(s.get("words"), 0)
        counts = {k: int(v) for k, v in (s.get("counts") or {}).items()
                  if k in CODES and num(v) is not None and v >= 0}
        total = sum(counts.values())
        rate = lambda n: round(n * 1000 / words, 2) if words else None
        ex = {}
        for k, items in (s.get("examples") or {}).items():
            if k not in CODES or not isinstance(items, list):
                continue
            ex[k] = [[text(i[0], 10), text(i[1]), text(i[2])] for i in items[:MAX_EXAMPLES]
                     if isinstance(i, list) and len(i) >= 3]
        ph = s.get("phases") if isinstance(s.get("phases"), dict) else None
        phases = None
        if ph and isinstance(ph.get("words"), list) and isinstance(ph.get("errors"), list) \
                and len(ph["words"]) == 2 and len(ph["errors"]) == 2:
            names = ph.get("names") if isinstance(ph.get("names"), list) and len(ph["names"]) == 2 else ["first part", "second part"]
            w = [num(v, 0) for v in ph["words"]]
            e = [num(v, 0) for v in ph["errors"]]
            phases = {"names": [text(n, 40) for n in names], "words": w, "errors": e,
                      "rates": [round(e[i] * 1000 / w[i], 2) if w[i] else None for i in (0, 1)]}
        sessions.append({
            "date": s["date"], "label": text(s.get("label"), 80), "words": words, "errors": total,
            "rate": rate(total), "rates": {k: rate(v) for k, v in counts.items()},
            "examples": ex, "phases": phases})
    sessions.sort(key=lambda s: s["date"])
    scores = []
    for s in led.get("scores") or []:
        if not isinstance(s, dict) or not good_date(s.get("date")):
            continue
        f, v, g = (num(s.get(k)) for k in ("fluency", "vocabulary", "grammar"))
        if None in (f, v, g):
            continue
        scores.append({"date": s["date"], "level": text(s.get("level"), 10), "fluency": f, "vocabulary": v,
                       "grammar": g, "total": num(s.get("total"), f + v + g), "talk_pct": num(s.get("talk_pct"))})
    scores.sort(key=lambda s: s["date"])
    return {"slug": slug, "name": display_name(records, slug), "profile_level": profile_level(records, slug),
            "sessions": sessions, "scores": scores}


TEMPLATE = (Path(__file__).resolve().parent / "dashboard_template.html")


def safe_json(obj):
    s = json.dumps(obj, ensure_ascii=False, separators=(",", ":"))
    return (s.replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")
             .replace("\u2028", "\\u2028").replace("\u2029", "\\u2029"))


def main():
    args = sys.argv[1:]
    def flag(name, default):
        return args[args.index(name) + 1] if name in args and args.index(name) + 1 < len(args) else default
    if "-h" in args or "--help" in args:
        sys.exit(__doc__)
    records = Path(flag("--records-dir", "~/eng-teaching-records")).expanduser().resolve()
    out = Path(flag("--out", str(records / "dashboard" / "dashboard.html"))).expanduser()
    ledger_dir = records / "error-ledgers"
    if not ledger_dir.is_dir():
        sys.exit(f"no error-ledgers folder in {records}; run english-analysis on a lesson first")
    warns = []
    students = [s for s in (load_student(records, p, warns.append) for p in sorted(ledger_dir.glob("*.json"))) if s]
    for w in warns:
        print("warning:", w, file=sys.stderr)
    if not students:
        sys.exit("no student ledgers found")
    data = {"generated": _date.today().isoformat(), "codes": CODES, "students": students}
    html = TEMPLATE.read_text(encoding="utf-8").replace("/*__DATA__*/null", safe_json(data))
    out.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    fd = os.open(out, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"wrote {out} ({len(students)} student(s))")


if __name__ == "__main__":
    main()
