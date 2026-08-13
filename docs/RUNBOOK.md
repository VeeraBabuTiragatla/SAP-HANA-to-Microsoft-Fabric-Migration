# Migration Validation Runbook

## Purpose

Provide a repeatable procedure for reconciling a controlled SAP HANA source extract with a Microsoft Fabric target extract. The included files are synthetic and the tool makes no platform connection.

## Prerequisites

- Python 3.9 or later;
- read access to the two approved CSV extracts;
- identical required columns as documented in the README;
- a repository working directory; and
- an agreed evidence location and named validation owner.

## Validation procedure

1. Confirm the source and target filenames, extraction window and business scope.
2. Preserve the supplied files as read-only evidence; use copies for experiments.
3. From the repository root, run:
   `python -m src.validate_migration <source.csv> <target.csv> --output validation_report.json`
4. Check the process exit status: `0` means passed, `1` means validation differences, and `2` means an input or execution error.
5. Review every report section, even when `passed` is `true`.
6. Run the SQL control checks in approved source and target query tools when validating a real migration.
7. Record the command, file versions or checksums, run time, reviewer and result.
8. Obtain analyst and business-owner approval against the agreed UAT cases.

## Exception handling

Classify each exception before changing anything:

- **Duplicate key:** confirm the business-key definition and whether the source itself contains duplicates.
- **Missing required value:** verify extraction filters, transformations and target constraints.
- **Missing or extra record:** compare load scope, rejection logs and incremental-load boundaries.
- **Field mismatch:** review mapping, type conversion, precision, date formatting and business rules.
- **Execution error:** confirm paths, permissions, encoding and required CSV headers.

Record the affected order IDs, likely cause, owner and disposition. Never conceal a difference by editing retained evidence.

## Rerun and escalation

1. Correct the transformation, loading issue or test input through the governed change process.
2. Generate new, versioned extracts for the same agreed scope.
3. Rerun the validator and retain both failed and corrected reports.
4. If the same exception recurs, escalate to the migration lead and relevant source, target or business-data owner.
5. Do not recommend UAT approval while unexplained material differences remain.

## Handover

Provide the final report, SQL evidence, accepted-exception register, UAT decision and this runbook to the operational owner. Confirm that the owner can execute a rerun and identify where to escalate a failed result.
