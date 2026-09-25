from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

from scripts import validate


ROOT = Path(__file__).resolve().parents[1]
CASES = json.loads((ROOT / "tests" / "fixtures" / "cases.json").read_text(encoding="utf-8"))


class ContractTests(unittest.TestCase):
    def case(self, case_id: str) -> dict:
        return next(case for case in CASES if case["id"] == case_id)

    def test_repository_validator_passes(self) -> None:
        result = subprocess.run([sys.executable, "scripts/validate.py"], cwd=ROOT, text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_going_concern_runway_case(self) -> None:
        case = self.case("going-concern-runway")
        self.assertEqual(case["expected_categories"], ["liquidity", "going concern"])
        self.assertIn("4.0 months", case["output"])
        self.assertIn("**Unknown:**", case["output"])

    def test_dilution_case(self) -> None:
        case = self.case("dilution")
        self.assertIn("dilution", case["expected_categories"])
        self.assertIn("overhang/current shares", case["output"])
        self.assertIn("40.0%", case["output"])
        self.assertIn("**Citation:**", case["output"])

    def test_related_party_control_weakness_case(self) -> None:
        case = self.case("related-party-control-weakness")
        self.assertIn("related party", case["expected_categories"])
        self.assertIn("do not establish misconduct", case["output"])

    def test_clean_negative_control(self) -> None:
        case = self.case("clean-negative-control")
        self.assertEqual(case["expected_categories"], [])
        self.assertIn("No material concern established", case["output"])
        self.assertIn("full filings are needed", case["output"])

    def test_validator_rejects_unsafe_conclusions(self) -> None:
        base = self.case("clean-negative-control")["output"]
        for unsafe in ("Buy the stock.", "This is a scam.", "Composite risk score: 9/10."):
            errors: list[str] = []
            validate.check_output(errors, "mutation", base + "\n" + unsafe)
            self.assertTrue(errors, unsafe)

    def test_validator_rejects_missing_as_of_date(self) -> None:
        output = self.case("clean-negative-control")["output"].replace(
            "**As of:** 2026-05-01", "**As of:** unknown"
        )
        errors: list[str] = []
        validate.check_output(errors, "mutation", output)
        self.assertTrue(errors)


if __name__ == "__main__":
    unittest.main()
