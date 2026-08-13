import csv
import tempfile
import unittest
from pathlib import Path

from src.validate_migration import validate_migration


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SOURCE_FILE = REPOSITORY_ROOT / "data" / "hana_orders.csv"
TARGET_FILE = REPOSITORY_ROOT / "data" / "fabric_orders.csv"


class MigrationValidationTests(unittest.TestCase):
    def test_correct_migration_passes(self) -> None:
        report = validate_migration(SOURCE_FILE, TARGET_FILE)

        self.assertTrue(report["passed"])
        self.assertEqual(report["source_row_count"], 6)
        self.assertEqual(report["target_row_count"], 6)
        self.assertEqual(report["field_level_mismatches"], [])

    def test_changed_target_value_fails_and_identifies_order(self) -> None:
        with TARGET_FILE.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            fieldnames = reader.fieldnames
            rows = list(reader)

        rows[2]["quantity"] = "999"
        with tempfile.TemporaryDirectory() as temporary_directory:
            changed_target = Path(temporary_directory) / "fabric_orders_changed.csv"
            with changed_target.open("w", newline="", encoding="utf-8") as handle:
                writer = csv.DictWriter(handle, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rows)

            report = validate_migration(SOURCE_FILE, changed_target)

        self.assertFalse(report["passed"])
        self.assertEqual(
            report["field_level_mismatches"],
            [
                {
                    "order_id": "ORD-1003",
                    "field": "quantity",
                    "source_value": "200",
                    "target_value": "999",
                }
            ],
        )


if __name__ == "__main__":
    unittest.main()
