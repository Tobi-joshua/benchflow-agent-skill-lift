import json
import unittest
from pathlib import Path

from scripts.lib.metrics import compute_paired_metrics, trials_from_records

FIXTURE = Path(__file__).resolve().parent / "fixtures" / "sample_trials.json"


class ComputeLiftTests(unittest.TestCase):
    def test_paired_metrics(self):
        data = json.loads(FIXTURE.read_text(encoding="utf-8"))
        metrics = compute_paired_metrics(trials_from_records(data["trials"]))
        self.assertEqual(metrics.n_tasks, 3)
        # alpha +1.0, beta -1.0, gamma 0.0 -> mean lift 0.0
        self.assertAlmostEqual(metrics.absolute_lift, 0.0)
        self.assertAlmostEqual(metrics.baseline_success_rate, 1.0 / 3.0)
        self.assertAlmostEqual(metrics.treatment_success_rate, 1.0 / 3.0)
        self.assertEqual(len(metrics.regressions), 1)
        self.assertEqual(metrics.regressions[0]["task"], "beta")
        self.assertAlmostEqual(metrics.regression_rate, 1.0 / 3.0)


if __name__ == "__main__":
    unittest.main()
