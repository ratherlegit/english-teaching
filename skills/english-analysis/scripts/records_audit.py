#!/usr/bin/env python3
"""Audit the tutor's records folder: is every student complete, and is every file where it belongs?

Usage: records_audit.py [--records-dir DIR] [--student SLUG]
Default records folder: ~/eng-teaching-records. Run with `python3 -I`.

Layout it expects (see references/records-layout.md):
  <slug>.md and _tutor.md at the top level; everything else in a folder:
  handouts/<slug>/  lesson-docs/<slug>/  source-notes/<slug>/  transcripts/  error-ledgers/
  glossaries/  lesson-reports/  student-profiles/  one-pagers/  worksheets/
  Folders starting with an underscore (for example _review-before-deleting) are allowed.

Each finding is ERROR (fix it) or WARN (look at it). The exit code is 1 if there is any ERROR.
Checks per student: record exists and its Profile names pronouns and a level; every transcript
has an errors.tsv, a ledger session with scores and an Analysis section; the glossary, student profile and one-pager exist, are not older than the latest
transcript, and have a current .docx; no lesson has several handout versions.
At the top level: loose files other than records, and folders outside the layout.
"""
import datetime, json, os, re, sys

FOLDERS = {"handouts", "lesson-docs", "source-notes", "transcripts", "error-ledgers", "glossaries",
           "lesson-reports", "student-profiles", "one-pagers", "worksheets"}
DATE = r"\d{4}-\d{2}-\d{2}"


def read(path):
    try:
        return open(path, encoding="utf-8").read()
    except OSError:
        return ""


def students(root):
    return sorted(f[:-3] for f in os.listdir(root)
                  if f.endswith(".md") and not f.startswith("_") and os.path.isfile(os.path.join(root, f)))


def audit_layout(root, out):
    for name in sorted(os.listdir(root)):
        if name.startswith(".") or name.startswith("_"):
            continue
        path = os.path.join(root, name)
        if os.path.isdir(path):
            if name not in FOLDERS:
                out.append(("WARN", "", f"folder '{name}' is not part of the layout (move it or rename it with a leading underscore)"))
        elif not name.endswith(".md"):
            out.append(("ERROR", "", f"loose file '{name}' at the top level (handouts go in handouts/<student>/, dated lesson documents in lesson-docs/<student>/)"))


def profile_facts(text):
    prof = text.split("## Profile", 1)[-1].split("\n## ", 1)[0]
    pron = re.search(r"^- Pronouns:\s*(.+)$", prof, re.M)
    lvl = re.search(r"^- Level:\s*(.+)$", prof, re.M)
    return (pron.group(1).strip() if pron else ""), (lvl.group(1).strip() if lvl else "")


def updated(path):
    m = re.search(r"Updated (" + DATE + ")", read(path)[:600])
    return m.group(1) if m else ""


def mtime(path):
    return os.path.getmtime(path) if os.path.exists(path) else 0


def handout_versions(root, slug, out):
    folder = os.path.join(root, "handouts", slug)
    if not os.path.isdir(folder):
        return
    groups = {}
    for f in os.listdir(folder):
        m = re.match(re.escape(slug) + r"-(?:lesson-(\d+[a-z]?)|(" + DATE + r"))", f)
        if f.endswith(".docx") and m and "handout" in f:
            groups.setdefault(m.group(1) or m.group(2), []).append(f)
    for num, files in sorted(groups.items()):
        if len(files) > 1:
            dated = ", ".join(f"{f} ({datetime.date.fromtimestamp(mtime(os.path.join(folder, f))).isoformat()})" for f in sorted(files))
            out.append(("WARN", slug, f"{len(files)} handout files for lesson {num}: {dated}. They may be versions of one lesson or different lessons that share a number; ask which was taught and move the others to _review-before-deleting/"))


def audit_student(root, slug, out):
    rec = os.path.join(root, slug + ".md")
    text = read(rec)
    pron, lvl = profile_facts(text)
    if not pron or pron.lower().startswith(("none", "unknown", "not ", "tbd")):
        out.append(("ERROR", slug, "the Profile has no pronouns; ask the tutor, and use they/them until then"))
    if not lvl:
        out.append(("WARN", slug, "the Profile has no Level line"))
    tdir = os.path.join(root, "transcripts")
    dates = sorted(m.group(1) for f in (os.listdir(tdir) if os.path.isdir(tdir) else [])
                   for m in [re.fullmatch(re.escape(slug) + r"-(" + DATE + r")-transcript\.md", f)] if m)
    ledger = {}
    lp = os.path.join(root, "error-ledgers", slug + ".json")
    if os.path.exists(lp):
        try:
            data = json.load(open(lp, encoding="utf-8"))
            ledger = {s["date"]: s for s in data.get("sessions", [])}
            scores = {s["date"] for s in data.get("scores", [])} if isinstance(data.get("scores"), list) else set(data.get("scores", {}))
        except (ValueError, KeyError, TypeError, AttributeError):
            out.append(("ERROR", slug, "error-ledgers/%s.json cannot be read" % slug))
            scores = set()
    else:
        scores = set()
        if dates:
            out.append(("ERROR", slug, "has transcripts but no error ledger (run error_ledger.py add)"))
    analyses = re.findall(r"^## Analysis: (.+)$", text, re.M)
    for d in dates:
        if not os.path.exists(os.path.join(tdir, f"{slug}-{d}-errors.tsv")):
            out.append(("ERROR", slug, f"{d}: transcript has no errors.tsv (tag the errors)"))
        if ledger and d not in ledger:
            out.append(("ERROR", slug, f"{d}: transcript is not in the error ledger"))
        if d not in scores and d not in ledger:
            out.append(("WARN", slug, f"{d}: no scores saved"))
        if not any(d in a for a in analyses):
            out.append(("ERROR", slug, f"{d}: no '## Analysis' section in the record"))
        rp = os.path.join(root, "lesson-reports", f"{slug}-{d}-lesson-report")
        if os.path.exists(rp + ".md") and os.path.exists(rp + ".docx") and mtime(rp + ".docx") < mtime(rp + ".md") - 1:
            out.append(("WARN", slug, f"{d}: lesson report .docx is older than its .md (rebuild with report_docx.py)"))
    for d in sorted(set(ledger) - set(dates)):
        out.append(("WARN", slug, f"{d}: ledger session has no labeled transcript file"))
    if not os.path.exists(os.path.join(root, "glossaries", slug + ".txt")):
        out.append(("WARN", slug, "no glossary (glossaries/%s.txt)" % slug))
    latest = dates[-1] if dates else ""
    for label, folder, name in (("student profile", "student-profiles", f"{slug}-profile"),
                                ("one-pager", "one-pagers", f"{slug}-one-pager")):
        md = os.path.join(root, folder, name + ".md")
        dx = os.path.join(root, folder, name + ".docx")
        if not os.path.exists(md):
            if dates:
                out.append(("WARN", slug, f"no {label} ({folder}/{name}.md)"))
            continue
        if not os.path.exists(dx):
            out.append(("WARN", slug, f"{label} has no .docx"))
        elif mtime(dx) < mtime(md) - 1:
            out.append(("WARN", slug, f"{label} .docx is older than its .md (rebuild it)"))
        up = updated(md)
        if latest and up and up < latest:
            out.append(("WARN", slug, f"{label} says Updated {up} but the latest transcript is {latest}"))
    handout_versions(root, slug, out)
    return len(dates)


def main():
    a = sys.argv[1:]
    root, only = os.path.expanduser("~/eng-teaching-records"), None
    if "--records-dir" in a:
        i = a.index("--records-dir"); root = os.path.expanduser(a[i + 1]); del a[i:i + 2]
    if "--student" in a:
        i = a.index("--student"); only = a[i + 1]; del a[i:i + 2]
    if a:
        sys.exit(__doc__)
    if not os.path.isdir(root):
        sys.exit(f"No records folder at {root}")
    out = []
    audit_layout(root, out)
    names = students(root)
    if only:
        if only not in names:
            sys.exit(f"No record for '{only}' in {root}")
        names = [only]
    counts = {}
    for s in names:
        counts[s] = audit_student(root, s, out)
    if only:
        out = [o for o in out if o[1] in ("", only)]
    for s in names:
        mine = [o for o in out if o[1] == s]
        bad = sum(1 for o in mine if o[0] == "ERROR")
        print(f"{s}: {counts[s]} transcript(s), {bad} error(s), {len(mine) - bad} warning(s)")
    for o in out:
        print(f"{o[0]}: " + (f"[{o[1]}] " if o[1] else "") + o[2])
    errors = sum(1 for o in out if o[0] == "ERROR")
    print(f"\n{errors} error(s), {len(out) - errors} warning(s).")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
