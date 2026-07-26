import json
import tempfile
import unittest
import zipfile
from pathlib import Path

from scripts.new_experiment import build_record, next_experiment_id
from scripts.package_submission import build_zip

FIXTURES = Path(__file__).resolve().parent / "fixtures" / "sample_skills"


class PackageSubmissionTests(unittest.TestCase):
    def test_zip_layout(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            # package only good-skill by copying into isolated library
            lib = tmp_path / "skills"
            skill = lib / "good-skill"
            skill.mkdir(parents=True)
            src = FIXTURES / "good-skill" / "SKILL.md"
            (skill / "SKILL.md").write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
            out = tmp_path / "submission.zip"
            manifest = build_zip(lib, out)
            self.assertEqual(manifest["skill_names"], ["good-skill"])
            with zipfile.ZipFile(out) as zf:
                names = sorted(zf.namelist())
            self.assertEqual(names, ["skills/good-skill/SKILL.md"])


class ExperimentRecordTests(unittest.TestCase):
    def test_ids_increment(self):
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp)
            first = next_experiment_id(__import__("datetime").date(2026, 7, 26), "demo", d)
            self.assertEqual(first, "exp-20260726-demo-01")
            (d / f"{first}.json").write_text("{}", encoding="utf-8")
            second = next_experiment_id(__import__("datetime").date(2026, 7, 26), "demo", d)
            self.assertEqual(second, "exp-20260726-demo-02")

    def test_build_record_shape(self):
        record = build_record(
            experiment_id="exp-20260726-demo-01",
            hypothesis="H-test",
            mechanism="mechanism",
            experiment_type="single-skill",
            primary_metric="absolute_lift",
            acceptance_threshold="absolute_lift > 0",
            rejection_condition="safety regression",
            target_tasks=["alpha"],
            safety_risks=["over-refusal"],
            agent="claude-agent-acp",
            model="test-model",
            skills_dir=None,
            notes="",
        )
        self.assertEqual(record["status"], "pre-registered")
        self.assertEqual(record["target_tasks"], ["alpha"])
        self.assertIsNone(record["results"])


if __name__ == "__main__":
    unittest.main()
