import unittest
from pathlib import Path

from scripts.lib.validate import validate_library

FIXTURES = Path(__file__).resolve().parent / "fixtures" / "sample_skills"
ROOT_SKILLS = Path(__file__).resolve().parents[1] / "skills"


class ValidateSkillsTests(unittest.TestCase):
    def test_good_skill_ok(self):
        # validate only the good-skill directory via a temp-like single-child view
        report = validate_library(FIXTURES)
        codes = {(i.skill, i.code, i.severity) for i in report.issues}
        self.assertIn(("leaky-skill", "leak:oracle_path", "error"), codes)
        self.assertIn(("leaky-skill", "leak:tasks_tree", "error"), codes)
        good_errors = [i for i in report.errors if i.skill == "good-skill"]
        self.assertEqual(good_errors, [])

    def test_empty_skills_dir_ok_by_default(self):
        report = validate_library(ROOT_SKILLS, allow_empty=True)
        self.assertTrue(report.ok)
        self.assertEqual(report.skill_count, 0)


if __name__ == "__main__":
    unittest.main()
