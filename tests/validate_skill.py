"""Structure and rule checks for the english-teaching plugin (tutoring and classroom skills). Stdlib only."""
import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL_DIR = ROOT / "skills" / "english-classroom"
TUTOR_DIR = ROOT / "skills" / "english-tutoring"
SKILL_MD = SKILL_DIR / "SKILL.md"
REFS = SKILL_DIR / "references"
EM_DASH = "\u2014"


def read(path):
    return Path(path).read_text(encoding="utf-8")


def frontmatter(text):
    match = re.match(r"---\n(.*?)\n---\n", text, re.S)
    if not match:
        return {}
    fields = {}
    for line in match.group(1).splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            fields[key.strip()] = value.strip()
    return fields


def non_heading_lines(text):
    body = re.sub(r"\A---\n.*?\n---\n", "", text, flags=re.S)
    return [ln for ln in body.splitlines() if not ln.lstrip().startswith("#")]


def em_dash_lines(path):
    return [ln for ln in non_heading_lines(read(path)) if EM_DASH in ln]


class TestScaffold(unittest.TestCase):
    def test_required_files_exist(self):
        required = [
            ".claude-plugin/plugin.json",
            ".claude-plugin/marketplace.json",
            ".gitignore",
            "LICENSE",
            "skills/english-classroom/scripts/md_to_docx.py",
            "skills/english-classroom/references/cefr-levels.md",
            "skills/english-classroom/references/lesson-frameworks.md",
            "skills/english-classroom/references/activity-bank.md",
            "skills/english-classroom/references/teacher-activities.md",
            "skills/english-tutoring/SKILL.md",
            "skills/english-tutoring/scripts/md_to_docx.py",
            "skills/english-tutoring/references/teacher-activities.md",
            "skills/english-tutoring/references/activity-bank.md",
            "skills/english-tutoring/references/student-interview.md",
            "AGENTS.md",
            "README.md",
        ]
        for rel in required:
            self.assertTrue((ROOT / rel).is_file(), rel)

    def test_plugin_json(self):
        data = json.loads(read(ROOT / ".claude-plugin/plugin.json"))
        self.assertEqual(data["name"], "english-teaching")
        self.assertEqual(data["version"], "2.14.0")
        self.assertEqual(data["license"], "MIT")
        self.assertIn("ratherlegit/english-teaching", data["repository"])

    def test_marketplace_json_matches_plugin(self):
        plugin = json.loads(read(ROOT / ".claude-plugin/plugin.json"))
        market = json.loads(read(ROOT / ".claude-plugin/marketplace.json"))
        self.assertEqual(market["name"], "english-teaching")
        self.assertEqual(market["version"], plugin["version"])
        self.assertEqual(market["plugins"][0]["name"], "english-teaching")
        self.assertEqual(market["plugins"][0]["source"], "./")

    def test_gitignore(self):
        self.assertIn(".DS_Store", read(ROOT / ".gitignore"))

    def test_converter_identical_to_english_tutoring_copy(self):
        self.assertEqual(
            (SKILL_DIR / "scripts/md_to_docx.py").read_bytes(),
            (TUTOR_DIR / "scripts/md_to_docx.py").read_bytes(),
        )

    def test_tutoring_skill_rules(self):
        text = read(TUTOR_DIR / "SKILL.md")
        self.assertEqual(frontmatter(text).get("name"), "english-tutoring")
        for phrase in [
            "Review of Prior Content",
            "Activity Log",
            "American by default",
            "no student-facing text may mention the tutor",
            "Exports are black text only",
            "never lettered or numbered",
        ]:
            self.assertIn(phrase, text, phrase)
        for rel in re.findall(r"`((?:references|scripts)/[\w./-]+)`", text):
            self.assertTrue((TUTOR_DIR / rel).is_file(), rel)

    def test_tutoring_final_check_before_delivering(self):
        text = read(TUTOR_DIR / "SKILL.md")
        self.assertIn("Final check before delivering", text)
        block = text.split("Final check before delivering", 1)[1][:2500]
        for phrase in ["Word-bank order", "Role, not name", "No privacy language", "No tutor words", "Grammar consistency", "Decision Meeting", "secret"]:
            self.assertIn(phrase, block, phrase)

    def test_tutoring_grammar_must_follow_its_own_rule(self):
        text = read(TUTOR_DIR / "SKILL.md")
        self.assertIn("must follow its own rule", text)
        self.assertIn("Never leave an unexplained exception", text)

    def test_classroom_final_check_before_delivering(self):
        text = read(SKILL_MD)
        self.assertIn("Final check before delivering", text)
        block = text.split("Final check before delivering", 1)[1][:2500]
        for phrase in ["Word-bank order", "Grammar consistency", "Controlled Practice", "No teacher words"]:
            self.assertIn(phrase, block, phrase)

    def test_classroom_controlled_practice_and_grammar_consistency(self):
        text = read(SKILL_MD)
        self.assertIn("must follow its own rule", text)
        self.assertIn("### Controlled Practice", text)
        block = text.split("### Controlled Practice", 1)[1].split("###", 1)[0]
        for phrase in ["right after the Grammar Focus", "before any role play", "does not count", "6 to 8 items", "class's own world", "Recycle the fresh vocabulary", "read the finished sentences aloud", "one sentence of their own"]:
            self.assertIn(phrase, block, phrase)
        self.assertIn("Controlled Practice (<format>)", text)
        self.assertLess(text.index("6. **Grammar Focus**"), text.index("7. **Controlled Practice**"))

    def test_tutoring_controlled_practice_stage(self):
        text = read(TUTOR_DIR / "SKILL.md")
        self.assertIn("### Controlled Practice section", text)
        block = text.split("### Controlled Practice section", 1)[1].split("###", 1)[0]
        for phrase in ["strong", "light", "right after the Grammar Focus", "before any role play", "does not count", "6 to 8 items", "student's own world", "Recycle the new vocabulary", "read the finished sentences aloud", "one sentence of their own"]:
            self.assertIn(phrase, block, phrase)
        self.assertIn("Controlled Practice (<format>)", text)
        self.assertLess(text.index("6. **Controlled Practice**"), text.index("7. **Production/application activities**"))

    def test_vocab_candidates_are_numbered_chat_text(self):
        for skill in ["english-tutoring", "english-classroom"]:
            text = read(ROOT / "skills" / skill / "SKILL.md")
            for phrase in ["never inside a question, option or form box", "Number the candidates", "cut 2, 5, 7-9", "never appear in the lesson"]:
                self.assertIn(phrase, text, f"{skill}: {phrase}")

    def test_tutoring_card_activities_point_to_role_card_rules(self):
        text = read(TUTOR_DIR / "references" / "teacher-activities.md")
        for name in ["Role Play", "Phone Call Simulation", "Decision Meeting"]:
            line = next(ln for ln in text.splitlines() if f"**{name}**" in ln)
            self.assertIn("role card rules", line, name)

    def test_activity_weights_present(self):
        for d in (TUTOR_DIR, SKILL_DIR):
            text = read(d / "references/teacher-activities.md")
            for tag in ("[High]", "[Medium]", "[Low]"):
                self.assertIn(tag, text, f"{d.name} {tag}")


class TestExport(unittest.TestCase):
    def test_converter_builds_docx_with_heading_and_table(self):
        try:
            import docx
        except ImportError:
            self.skipTest("python-docx not installed")
        md = (
            "# Test Lesson\n\n## Warm Up Conversation\n\n- One\n- Two\n\n"
            "| Lesson # | Lesson Name | Grouping | Status |\n|---|---|---|---|\n"
            "| 1 | Intro | Mixed pairs | Not yet delivered |\n"
        )
        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp) / "plan.md"
            out = Path(tmp) / "plan.docx"
            src.write_text(md, encoding="utf-8")
            subprocess.run(
                [sys.executable, str(SKILL_DIR / "scripts/md_to_docx.py"), str(src), str(out)],
                check=True,
            )
            self.assertTrue(out.is_file())
            document = docx.Document(str(out))
            self.assertEqual(len(document.tables), 1)
            texts = [p.text for p in document.paragraphs]
            self.assertIn("Test Lesson", texts)


class TestNewReferences(unittest.TestCase):
    def test_class_interview_content(self):
        text = read(REFS / "class-interview.md")
        for phrase in [
            "Number of students",
            "Backgrounds",
            "mono-lingual",
            "mixed",
            "Light mode",
            "Roster",
            "L1 interference cheat sheet",
            "age-appropriate",
            "can do",
            "headcount",
            "first name",
            "last initial",
            "diagnoses",
        ]:
            self.assertIn(phrase, text, phrase)

    def test_differentiation_content(self):
        text = read(REFS / "differentiation.md")
        for phrase in [
            "Support",
            "Core",
            "Stretch",
            "two CEFR bands",
            "parallel",
            "Small",
            "Medium",
            "Large",
            "mixed-level pairs",
            "early finishers",
            "single level",
            "never a shorter",
            "bimodal",
            "headcount",
            "lower of the two",
            "Quick Level Check",
        ]:
            self.assertIn(phrase, text, phrase)

    def test_no_em_dashes_in_new_references(self):
        for name in ["class-interview.md", "differentiation.md"]:
            self.assertEqual(em_dash_lines(REFS / name), [], name)


def group_section(name):
    text = read(REFS / name)
    marker = "## Group classroom notes"
    return text[text.index(marker):]


class TestGroupNotes(unittest.TestCase):
    def test_group_notes_appended(self):
        for name in ["teacher-activities.md", "activity-bank.md", "lesson-frameworks.md"]:
            self.assertIn("## Group classroom notes", read(REFS / name), name)

    def test_teacher_activities_group_rules(self):
        text = group_section("teacher-activities.md")
        for phrase in ["Support", "Stretch", "rotate", "Press conference", "Found article"]:
            self.assertIn(phrase, text, phrase)

    def test_group_sections_no_em_dashes(self):
        for name in ["teacher-activities.md", "activity-bank.md", "lesson-frameworks.md"]:
            self.assertNotIn(EM_DASH, group_section(name), name)


class TestSkillMd(unittest.TestCase):
    def setUp(self):
        self.text = read(SKILL_MD)

    def test_frontmatter(self):
        fm = frontmatter(self.text)
        self.assertEqual(fm.get("name"), "english-classroom")
        desc = fm.get("description", "")
        self.assertIn("english-tutoring", desc)
        self.assertIn("class", desc)
        self.assertLess(len(desc), 1024)

    def test_steps_present_in_order(self):
        headings = [
            "## Step 0: Check for a returning class",
            "## Step 1: Interview the teacher about the class",
            "## Step 2: Design the class learning path",
            "## Step 3: Pick a framework",
            "## Step 4: Build the plan",
            "## Step 5: Differentiation and common pitfalls",
            "## Output format",
            "## Step 6: Export as a .docx (optional)",
        ]
        positions = [self.text.find(h) for h in headings]
        self.assertTrue(all(p >= 0 for p in positions), positions)
        self.assertEqual(positions, sorted(positions))

    def test_required_rules(self):
        for phrase in [
            "~/eng-teaching-records/classes/",
            "median",
            "Support",
            "Core",
            "Stretch",
            "Grouping",
            "two CEFR bands",
            "parallel",
            "never a shorter",
            "exit task",
            "bimodal",
            "headcount",
            "new term",
            "path is complete",
            "Quick Level Check",
            "last initial",
            "estimated",
            "Never overwrite a record",
            "Previous Paths",
            "whole roster",
            "never inferred",
            "culture-sharing prompt",
            "Differentiation",
            "Review of Prior Content",
            "Activity Log",
            "American by default",
            "no student-facing text may mention the teacher",
            "Exports are black text only",
            "never lettered or numbered",
            "first lesson",
            "Never save exports inside",
        ]:
            self.assertIn(phrase, self.text, phrase)

    def test_review_focus_rules(self):
        for phrase in [
            "class of one",
            "already exists",
            "age-appropriate",
            "single level",
            "can do",
            "cannot generate a Word file",
            "diagnoses",
        ]:
            self.assertIn(phrase, self.text, phrase)

    def test_referenced_files_exist(self):
        for rel in re.findall(r"`((?:references|scripts)/[\w./-]+)`", self.text):
            self.assertTrue((SKILL_DIR / rel).is_file(), rel)

    def test_no_em_dashes(self):
        self.assertEqual(em_dash_lines(SKILL_MD), [])


class TestDocs(unittest.TestCase):
    def test_readme(self):
        text = read(ROOT / "README.md")
        self.assertIn("ratherlegit/english-teaching", text)
        self.assertIn("english-tutoring", text)
        self.assertIn("english-classroom", text)
        self.assertIn("english-worksheet", text)
        self.assertIn("english-analysis", text)
        self.assertIn("claude plugin install english-teaching@english-teaching", text)
        self.assertEqual(em_dash_lines(ROOT / "README.md"), [])

    def test_agents(self):
        text = read(ROOT / "AGENTS.md")
        self.assertIn("skills/english-classroom/SKILL.md", text)
        self.assertIn("skills/english-tutoring/SKILL.md", text)
        self.assertIn("skills/english-worksheet/SKILL.md", text)
        self.assertIn("skills/english-analysis/SKILL.md", text)
        self.assertIn("~/eng-teaching-records/classes/", text)
        self.assertIn("~/eng-teaching-records/worksheets/", text)
        self.assertEqual(em_dash_lines(ROOT / "AGENTS.md"), [])


class TestPublishHygiene(unittest.TestCase):
    def test_no_local_paths_or_log_em_dashes(self):
        files = [ROOT / "README.md", ROOT / "AGENTS.md", SKILL_MD, TUTOR_DIR / "SKILL.md",
                 REFS / "class-interview.md", REFS / "differentiation.md"]
        for path in files:
            self.assertNotIn("/Users/", read(path), str(path))


WS_DIR = ROOT / "skills" / "english-worksheet"
WS_MD = WS_DIR / "SKILL.md"
WS_SCRIPT = WS_DIR / "scripts" / "md_to_docx.py"
WS_SAMPLE = """# Sample Pack

Overview text.

<!-- worksheet -->
## Worksheet 1: Do I need be?

:::box
**Grammar Focus: be**
- I am busy.

| Subject | be |
|---|---|
| I | am |
:::

:::box watch
**Watch out**
- Don't use: She working. Use: She is working.
:::

:::box bank
am    is    are
:::

![a picture](pic.png){1.5}

### Part A: Fix it
*Type the correct sentence in the colored box.*

| # | Sentence | Your answer |
|---|---|---|
| 0 | She working now. | She is working now. |
| 1 | I working now. |  |

:::write 4
:::

<!-- worksheet -->
## Worksheet 2: Past tense

1. went
"""

# a 1x1 PNG so the image test needs no imaging library
WS_PNG = bytes.fromhex(
    "89504e470d0a1a0a0000000d49484452000000010000000108060000001f15c489"
    "0000000d49444154789c6360f8cfc000000301010018dd8db00000000049454e44ae426082"
)


class TestWorksheetSkill(unittest.TestCase):
    def test_frontmatter(self):
        fm = frontmatter(read(WS_MD))
        self.assertEqual(fm.get("name"), "english-worksheet")
        self.assertGreater(len(fm.get("description", "")), 100)
        self.assertEqual(set(fm), {"name", "description"})

    def test_referenced_files_exist_and_are_linked(self):
        for ref in re.findall(r"`(references/[\w.-]+)`", read(WS_MD)):
            self.assertTrue((WS_DIR / ref).exists(), ref)
        for ref in (WS_DIR / "references").glob("*.md"):
            self.assertIn(f"references/{ref.name}", read(WS_MD), ref.name)

    def test_design_rules_present(self):
        text = read(WS_MD)
        for phrase in ["Grammar Focus", "Design for typing", "Your answer", "`:::write`",
                       "Never mention the tutor", "Never write \"circle,\"",
                       "Don't use: ... Use: ...", "no numbers inside the gaps", "worked example as row 0",
                       "every subject its own row", "Say it clearly", "vocabulary review part",
                       "second acceptable answer", "new sentences", "right time frame", "One point per worksheet", "say exactly when each applies", "brief *Why:*", "no cover or overview page"]:
            self.assertIn(phrase, text, phrase)

    def test_no_em_dashes_and_no_student_data(self):
        for path in [WS_MD, *(WS_DIR / "references").glob("*.md")]:
            self.assertNotIn(EM_DASH, read(path), str(path))
        for path in WS_DIR.rglob("*"):
            if path.is_file() and path.suffix in {".md", ".py"}:
                self.assertNotIn("jay" + "den", read(path).lower(), str(path))

    def test_worksheet_converter_is_its_own_file(self):
        # english-tutoring and english-classroom share one converter; the worksheet skill's adds typed answer cells
        self.assertIn("Your answer", read(WS_SCRIPT))
        self.assertNotEqual(WS_SCRIPT.read_bytes(), (TUTOR_DIR / "scripts/md_to_docx.py").read_bytes())


def _have_docx():
    try:
        import docx  # noqa: F401
        return True
    except ImportError:
        return False


@unittest.skipUnless(_have_docx(), "python-docx not installed")
class TestWorksheetExporter(unittest.TestCase):
    def run_script(self, *args):
        return subprocess.run([sys.executable, str(WS_SCRIPT), *args], capture_output=True, text=True)

    def test_single_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp) / "pack.md"
            src.write_text(WS_SAMPLE, encoding="utf-8")
            (Path(tmp) / "pic.png").write_bytes(WS_PNG)
            out = Path(tmp) / "pack.docx"
            result = self.run_script(str(src), str(out))
            self.assertEqual(result.returncode, 0, result.stderr)
            import zipfile
            z = zipfile.ZipFile(out)
            xml = z.read("word/document.xml").decode()
            self.assertEqual(xml.count("w:pageBreakBefore"), 2)
            self.assertIn("1F4E9A", xml)  # blue banner and table headers
            self.assertNotIn("2E7D32", xml)  # every worksheet stays blue
            self.assertIn("F3F7FD", xml)  # focus box tint
            self.assertIn("E6EFFB", xml)  # answer cells and write box
            self.assertIn("E3F3E6", xml)  # worked example (row 0)
            self.assertIn("FFF6D6", xml)  # word bank
            self.assertIn("FDECEA", xml)  # watch out box
            self.assertIn("w:trHeight", xml)  # answer rows have a minimum height
            self.assertGreaterEqual(xml.count("<w:tbl>"), 6)
            self.assertTrue(any(name.startswith("word/media/") for name in z.namelist()))  # image embedded

    def test_missing_image_is_skipped(self):
        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp) / "pack.md"
            src.write_text(WS_SAMPLE, encoding="utf-8")  # pic.png is not created
            out = Path(tmp) / "pack.docx"
            result = self.run_script(str(src), str(out))
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("image not found", result.stderr)

    def test_split(self):
        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp) / "pack.md"
            src.write_text(WS_SAMPLE, encoding="utf-8")
            out = Path(tmp) / "out"
            result = self.run_script(str(src), str(out), "--split")
            self.assertEqual(result.returncode, 0, result.stderr)
            names = sorted(p.name for p in out.glob("*.docx"))
            self.assertEqual(names, ["00-overview.docx", "01-worksheet-1-do-i-need-be.docx", "02-worksheet-2-past-tense.docx"])


SA_DIR = ROOT / "skills" / "english-analysis"
SA_MD = SA_DIR / "SKILL.md"


class TestStudentAnalysisSkill(unittest.TestCase):
    def test_frontmatter(self):
        fm = frontmatter(read(SA_MD))
        self.assertEqual(fm.get("name"), "english-analysis")
        self.assertEqual(set(fm), {"name", "description"})
        self.assertLessEqual(len(fm["description"]), 1026)

    def test_referenced_files_exist_and_are_linked(self):
        text = read(SA_MD)
        for ref in re.findall(r"`((?:references|scripts)/[\w.-]+)`", text):
            self.assertTrue((SA_DIR / ref).exists(), ref)
        for ref in (SA_DIR / "references").glob("*.md"):
            self.assertIn(f"references/{ref.name}", text, ref.name)
        for script in (SA_DIR / "scripts").glob("*.py"):
            self.assertIn(f"scripts/{script.name}", text, script.name)

    def test_scripts_compile(self):
        for script in (SA_DIR / "scripts").glob("*.py"):
            compile(read(script), str(script), "exec")

    def test_no_em_dashes_no_student_data_no_local_paths(self):
        for path in SA_DIR.rglob("*"):
            if path.is_file() and path.suffix in {".md", ".py"}:
                text = read(path)
                self.assertNotIn(EM_DASH, text, str(path))
                self.assertNotIn("/Users/", text, str(path))
                for name in ("jay" + "den", "ole" + "na"):
                    self.assertNotIn(name, text.lower(), str(path))

    def test_talk_stats_runs(self):
        sample = "# T\n\n---\n\n**[00:01] Tutor:** How was your week?\n\n**[00:05] Maria:** It was good, uh, I like it.\n"
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "t.md"
            path.write_text(sample, encoding="utf-8")
            out = subprocess.run([sys.executable, "-I", str(SA_DIR / "scripts" / "talk_stats.py"), str(path), "Maria"],
                                 capture_output=True, text=True)
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertIn("Maria", out.stdout)

    def test_one_pager_builder(self):
        try:
            import docx  # noqa: F401
        except ImportError:
            self.skipTest("python-docx not installed")
        script = SA_DIR / "scripts" / "one_pager_docx.py"
        short = "# Maria: One-Page Summary\n*Level B1+ | Score 63/100*\n\n| Fluency | Grammar |\n|---|---|\n| 18/25 | 14/25 |\n\n## Strengths\n- Clear stories\n"
        with tempfile.TemporaryDirectory() as tmp:
            md, out = Path(tmp) / "p.md", Path(tmp) / "p.docx"
            md.write_text(short, encoding="utf-8")
            ok = subprocess.run([sys.executable, str(script), str(md), str(out)], capture_output=True, text=True)
            self.assertEqual(ok.returncode, 0, ok.stderr)
            self.assertTrue(out.exists())
            md.write_text("# T\n\n" + ("word " * 500) + "\n", encoding="utf-8")
            bad = subprocess.run([sys.executable, str(script), str(md), str(out)], capture_output=True, text=True)
            self.assertNotEqual(bad.returncode, 0)
            self.assertIn("Too long for one page", bad.stderr)

    def test_tutor_stats_runs(self):
        sample = ("# T\n\n---\n\n**[00:01] Tutor:** How was your week?\n\n"
                  "**[00:05] Maria:** It was good, I went to the market with my sister and we bought a lot of fruit.\n\n"
                  "**[01:10] Tutor:** " + ("explain " * 120) + "\n\n**[02:00] Maria:** Okay.\n")
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "t.md"
            path.write_text(sample, encoding="utf-8")
            out = subprocess.run([sys.executable, "-I", str(SA_DIR / "scripts" / "tutor_stats.py"), str(path), "Maria",
                                  "--split", "01:00"], capture_output=True, text=True)
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertIn("tutor turns of 100+ words: 1 of 2", out.stdout)
        self.assertIn("followed by a student answer of 15+ words: 1", out.stdout)
        self.assertIn("Before 01:00", out.stdout)
        self.assertIn("From 01:00", out.stdout)

    def _ledger(self, tmp, tsv, extra=()):
        transcript = Path(tmp) / "t.md"
        transcript.write_text("# T\n\n---\n\n**[00:01] Tutor:** How was your week?\n\n"
                              "**[00:05] Maria:** Yesterday I go to the market, and my sister she are happy.\n\n"
                              "**[01:30] Maria:** We was tired after that.\n", encoding="utf-8")
        errors = Path(tmp) / "e.tsv"
        errors.write_text(tsv, encoding="utf-8")
        return subprocess.run([sys.executable, "-I", str(SA_DIR / "scripts" / "error_ledger.py"), "add", "maria",
                               "2026-01-01", str(transcript), "Maria", str(errors), "--records-dir", tmp, *extra],
                              capture_output=True, text=True)

    def test_ledger_quote_check_phases_and_scores(self):
        with tempfile.TemporaryDirectory() as tmp:
            bad = self._ledger(tmp, "TENSE\t00:05\tYesterday I went to the market\tgo -> went\n")
            self.assertNotEqual(bad.returncode, 0)
            self.assertIn("not in Maria's turns", bad.stderr + bad.stdout)
            self.assertFalse((Path(tmp) / "error-ledgers" / "maria.json").exists())
            tsv = ("TENSE\t00:05\tYesterday I go to the market\twent\n"
                   "SVA\t00:05\tmy sister she are happy\tis\n"
                   "SVA\t01:30\tWe was tired\twere\n")
            ok = self._ledger(tmp, tsv, ["--split", "01:00", "--phase-names", "open,review",
                                         "--scores", "18,15,14", "--level", "B1+", "--talk-pct", "45"])
            self.assertEqual(ok.returncode, 0, ok.stderr)
            self.assertIn("Phases in 2026-01-01 (split at 01:00): open:", ok.stdout)
            hist = subprocess.run([sys.executable, "-I", str(SA_DIR / "scripts" / "error_ledger.py"), "history", "maria",
                                   "--records-dir", tmp], capture_output=True, text=True)
            self.assertEqual(hist.returncode, 0, hist.stderr)
            self.assertIn("| 2026-01-01 | B1+ | 18/25 | 15/25 | 14/25 | 63/100 | 45% |", hist.stdout)
            sc = subprocess.run([sys.executable, "-I", str(SA_DIR / "scripts" / "error_ledger.py"), "score", "maria",
                                 "2025-12-01", "17", "14", "13", "B1", "--records-dir", tmp],
                                capture_output=True, text=True)
            self.assertEqual(sc.returncode, 0, sc.stderr)
            self.assertLess(sc.stdout.index("2025-12-01"), sc.stdout.index("2026-01-01"))
            ph = subprocess.run([sys.executable, "-I", str(SA_DIR / "scripts" / "error_ledger.py"), "phases", "maria",
                                 "--records-dir", tmp], capture_output=True, text=True)
            self.assertEqual(ph.returncode, 0, ph.stderr)
            self.assertIn("### open", ph.stdout)
            self.assertIn("| All codes |", ph.stdout)

    def test_report_builder(self):
        try:
            import docx  # noqa: F401
        except ImportError:
            self.skipTest("python-docx not installed")
        script = SA_DIR / "scripts" / "report_docx.py"
        text = ("# Maria: Lesson Report, 2026-01-01\n*Level B1+*\n\n## At a glance\n| Fluency | Grammar |\n|---|---|\n| 18/25 | 14/25 |\n\n"
                "### Tips\n- One\n1. First\n> a quote\n\n" + ("word " * 800) + "\n")
        with tempfile.TemporaryDirectory() as tmp:
            md, out = Path(tmp) / "r.md", Path(tmp) / "r.docx"
            md.write_text(text, encoding="utf-8")
            res = subprocess.run([sys.executable, str(script), str(md), str(out)], capture_output=True, text=True)
            self.assertEqual(res.returncode, 0, res.stderr)
            self.assertTrue(out.exists())

    def test_report_references_cover_required_sections(self):
        report = read(SA_DIR / "references" / "lesson-report.md")
        for heading in ("At a glance", "What the lesson covered", "Tips for you", "How sure we are"):
            self.assertIn(heading, report)
        profile = read(SA_DIR / "references" / "student-profile.md")
        for heading in ("Progress over time", "Error patterns over time", "What to do next"):
            self.assertIn(heading, profile)
        tips = read(SA_DIR / "references" / "tutor-tips.md")
        self.assertIn("At most three tips", tips)

    def _audit(self, root, *args):
        return subprocess.run([sys.executable, "-I", str(SA_DIR / "scripts" / "records_audit.py"),
                               "--records-dir", str(root), *args], capture_output=True, text=True)

    def _make_records(self, root, pronouns="she/her"):
        for d in ("transcripts", "error-ledgers", "glossaries", "lesson-reports", "student-profiles", "one-pagers"):
            (root / d).mkdir(parents=True, exist_ok=True)
        prof = "- Pronouns: " + pronouns + "\n" if pronouns else ""
        (root / "ana.md").write_text("# Student Record: Ana\n\n## Profile\n" + prof + "- Level: B1\n\n## Analysis: transcript of 2026-01-05 (x)\ntext\n")
        (root / "transcripts" / "ana-2026-01-05-transcript.md").write_text("# t\n---\n**[00:01] Ana:** hi\n")
        (root / "transcripts" / "ana-2026-01-05-errors.tsv").write_text("")
        (root / "error-ledgers" / "ana.json").write_text('{"student": "ana", "sessions": [{"date": "2026-01-05"}], "scores": []}')
        (root / "glossaries" / "ana.txt").write_text("Ana")
        for folder, name in (("lesson-reports", "ana-2026-01-05-lesson-report"), ("student-profiles", "ana-profile"), ("one-pagers", "ana-one-pager")):
            (root / folder / (name + ".md")).write_text("# x\n*Updated 2026-01-06*\n")
            (root / folder / (name + ".docx")).write_text("x")

    def test_records_audit_clean_and_findings(self):
        import tempfile
        from pathlib import Path
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._make_records(root)
            ok = self._audit(root)
            self.assertEqual(ok.returncode, 0, ok.stdout)
            (root / "ana-lesson-1.docx").write_text("x")
            bad = self._audit(root)
            self.assertEqual(bad.returncode, 1)
            self.assertIn("loose file 'ana-lesson-1.docx'", bad.stdout)
            (root / "ana-lesson-1.docx").unlink()
            (root / "transcripts" / "ana-2026-01-05-errors.tsv").unlink()
            self.assertIn("no errors.tsv", self._audit(root).stdout)

    def test_records_audit_pronouns_and_handout_versions(self):
        import tempfile
        from pathlib import Path
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._make_records(root, pronouns="")
            out = self._audit(root)
            self.assertEqual(out.returncode, 1)
            self.assertIn("no pronouns", out.stdout)
            self._make_records(root)
            folder = root / "handouts" / "ana"
            folder.mkdir(parents=True)
            for name in ("ana-lesson-2-handout.docx", "ana-lesson-2-handout-v2.docx"):
                (folder / name).write_text("x")
            self.assertIn("2 handout files for lesson 2", self._audit(root).stdout)
            for name in ("ana-2026-01-05-handout.docx", "ana-2026-01-05-handout-v2.docx"):
                (folder / name).write_text("x")
            self.assertIn("2 handout files for lesson 2026-01-05", self._audit(root).stdout)

    def test_records_rules_in_skills(self):
        layout = read(SA_DIR / "references" / "records-layout.md")
        self.assertIn("Records first", layout)
        self.assertIn("Never infer pronouns", layout)
        self.assertIn("records_audit.py", read(SA_MD))
        self.assertIn("references/records-layout.md", read(SA_MD))
        tutoring = read(TUTOR_DIR / "SKILL.md")
        self.assertIn("Records first", tutoring)
        self.assertIn("eng-teaching-records/handouts/<student-name>/", tutoring)

    def test_transcribe_accepts_glossary(self):
        self.assertIn("--glossary", read(SA_DIR / "scripts" / "transcribe.py"))
        self.assertIn("--glossary", read(SA_MD))


if __name__ == "__main__":
    unittest.main()
