# Validation Output Training Guide

This guide explains the report for an analyst or business stakeholder. The sample data is entirely synthetic.

## Reading the result

The last field, `passed`, is the overall outcome:

- `true` means all implemented controls agree;
- `false` means at least one difference needs review.

A pass supports migration assurance, but it does not by itself prove that every business rule or production requirement has been tested.

## Report sections

- **`source_row_count` / `target_row_count`:** how many rows were supplied from each side. Equal counts are useful but can still hide offsetting missing and extra records.
- **`duplicate_business_keys`:** repeated order IDs. Each order should be uniquely identifiable for this sample.
- **`missing_required_fields`:** blank mandatory values, with the CSV row and order ID where available.
- **`records_missing_from_target`:** source orders that did not arrive in the target extract.
- **`unexpected_extra_target_records`:** target orders that are outside the supplied source scope.
- **`field_level_mismatches`:** shared order IDs whose customer, product, quantity, price, date or status differs. The report shows both values.

## What to do when validation fails

1. Do not alter the retained source or target evidence.
2. Note the affected order ID and report section.
3. Ask the relevant owner whether the difference is expected, a mapping issue, a load issue or a data-quality issue.
4. Record the decision and correction.
5. Rerun with newly versioned files and retain both reports.

## Handover check

Before accepting responsibility, the receiving analyst should be able to run the command, explain each report section, reproduce the controlled-failure test and follow the escalation steps in the runbook.
