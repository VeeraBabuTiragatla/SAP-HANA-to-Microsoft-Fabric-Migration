"""Reconcile synthetic SAP HANA and Microsoft Fabric order extracts."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path
from typing import Any, Iterable


BUSINESS_KEY = "order_id"
REQUIRED_FIELDS = (
    "order_id",
    "customer_id",
    "product",
    "quantity",
    "unit_price",
    "order_date",
    "status",
)


def read_csv(path: str | Path) -> list[dict[str, str]]:
    """Read a UTF-8 CSV extract and verify its expected columns."""
    source_path = Path(path)
    with source_path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        columns = set(reader.fieldnames or [])
        missing_columns = [field for field in REQUIRED_FIELDS if field not in columns]
        if missing_columns:
            raise ValueError(
                f"{source_path} is missing required columns: {', '.join(missing_columns)}"
            )
        return [
            {field: (value or "").strip() for field, value in row.items()}
            for row in reader
        ]


def duplicate_keys(rows: Iterable[dict[str, str]]) -> list[str]:
    counts = Counter(row[BUSINESS_KEY] for row in rows if row[BUSINESS_KEY])
    return sorted(key for key, count in counts.items() if count > 1)


def missing_required_fields(rows: Iterable[dict[str, str]]) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    for row_number, row in enumerate(rows, start=2):
        missing = [field for field in REQUIRED_FIELDS if not row[field]]
        if missing:
            issues.append(
                {
                    "row_number": row_number,
                    "order_id": row.get(BUSINESS_KEY, ""),
                    "fields": missing,
                }
            )
    return issues


def rows_by_key(rows: Iterable[dict[str, str]]) -> dict[str, dict[str, str]]:
    """Index non-empty keys; duplicate keys are reported separately."""
    return {row[BUSINESS_KEY]: row for row in rows if row[BUSINESS_KEY]}


def validate_migration(source_path: str | Path, target_path: str | Path) -> dict[str, Any]:
    """Return a JSON-serialisable reconciliation report."""
    source_rows = read_csv(source_path)
    target_rows = read_csv(target_path)
    source_duplicates = duplicate_keys(source_rows)
    target_duplicates = duplicate_keys(target_rows)
    source_missing_fields = missing_required_fields(source_rows)
    target_missing_fields = missing_required_fields(target_rows)

    source_by_key = rows_by_key(source_rows)
    target_by_key = rows_by_key(target_rows)
    source_keys = set(source_by_key)
    target_keys = set(target_by_key)

    missing_from_target = sorted(source_keys - target_keys)
    unexpected_in_target = sorted(target_keys - source_keys)
    mismatches: list[dict[str, str]] = []
    comparison_fields = [field for field in REQUIRED_FIELDS if field != BUSINESS_KEY]

    for order_id in sorted(source_keys & target_keys):
        for field in comparison_fields:
            source_value = source_by_key[order_id][field]
            target_value = target_by_key[order_id][field]
            if source_value != target_value:
                mismatches.append(
                    {
                        "order_id": order_id,
                        "field": field,
                        "source_value": source_value,
                        "target_value": target_value,
                    }
                )

    report: dict[str, Any] = {
        "source_row_count": len(source_rows),
        "target_row_count": len(target_rows),
        "duplicate_business_keys": {
            "source": source_duplicates,
            "target": target_duplicates,
        },
        "missing_required_fields": {
            "source": source_missing_fields,
            "target": target_missing_fields,
        },
        "records_missing_from_target": missing_from_target,
        "unexpected_extra_target_records": unexpected_in_target,
        "field_level_mismatches": mismatches,
    }
    report["passed"] = (
        len(source_rows) == len(target_rows)
        and not source_duplicates
        and not target_duplicates
        and not source_missing_fields
        and not target_missing_fields
        and not missing_from_target
        and not unexpected_in_target
        and not mismatches
    )
    return report


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate synthetic SAP HANA and Microsoft Fabric order extracts."
    )
    parser.add_argument("source", type=Path, help="Path to the HANA source CSV extract")
    parser.add_argument("target", type=Path, help="Path to the Fabric target CSV extract")
    parser.add_argument("--output", type=Path, help="Optional path for the JSON report")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        report = validate_migration(args.source, args.target)
    except (OSError, ValueError, csv.Error) as exc:
        print(json.dumps({"passed": False, "error": str(exc)}, indent=2))
        return 2

    rendered = json.dumps(report, indent=2)
    print(rendered)
    if args.output:
        args.output.write_text(rendered + "\n", encoding="utf-8")
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
