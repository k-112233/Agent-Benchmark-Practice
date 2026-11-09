import sys
import tempfile
import unittest
from pathlib import Path

TOOL_DIR = Path(__file__).resolve().parents[1]
if str(TOOL_DIR) not in sys.path:
    sys.path.insert(0, str(TOOL_DIR))

from summary import load_results, summarize_results


class EvaluationSummaryTests(unittest.TestCase):
    def make_csv(self, content):
        temp = tempfile.TemporaryDirectory()
        path = Path(temp.name) / "results.csv"
        path.write_text(content, encoding="utf-8")
        return temp, path

    def test_metric_denominator(self):
        temp, path = self.make_csv(
            "task_id,agent,trial,status,runtime_seconds,failure_type\n"
            "a,x,1,passed,1.0,\n"
            "a,x,2,failed,2.0,wrong_output\n"
            "b,x,1,error,3.0,environment_error\n"
            "c,x,1,timeout,4.0,timeout\n"
        )
        try:
            result = summarize_results(load_results(path))
            self.assertEqual(result["total_trials"], 4)
            self.assertEqual(result["passed_trials"], 1)
            self.assertAlmostEqual(result["pass_rate"], 0.25)
        finally:
            temp.cleanup()

    def test_missing_column(self):
        temp, path = self.make_csv(
            "task_id,agent,trial,status,runtime_seconds\n"
            "a,x,1,passed,1.0\n"
        )
        try:
            with self.assertRaises(ValueError):
                load_results(path)
        finally:
            temp.cleanup()

    def test_unknown_status(self):
        temp, path = self.make_csv(
            "task_id,agent,trial,status,runtime_seconds,failure_type\n"
            "a,x,1,unknown,1.0,\n"
        )
        try:
            with self.assertRaises(ValueError):
                load_results(path)
        finally:
            temp.cleanup()

    def test_negative_runtime(self):
        temp, path = self.make_csv(
            "task_id,agent,trial,status,runtime_seconds,failure_type\n"
            "a,x,1,passed,-1.0,\n"
        )
        try:
            with self.assertRaises(ValueError):
                load_results(path)
        finally:
            temp.cleanup()


if __name__ == "__main__":
    unittest.main()
