# SAP HANA to Microsoft Fabric Migration Validation Lab

A small, runnable portfolio lab showing how a migration team can validate a structured order extract as it moves from an SAP HANA source context to a Microsoft Fabric target context.

This is a technical demonstration, not a production or client implementation. **All order data is synthetic.** The CSV files represent controlled extracts; the project does not connect to, emulate, or claim access to a real SAP HANA or Microsoft Fabric environment.

## What the project demonstrates

The validator reconciles a synthetic source extract and target extract using `order_id` as the business key. It reports:

- source and target row counts;
- duplicate business keys;
- missing required fields;
- records missing from the target;
- unexpected target records;
- field-level mismatches for shared business keys; and
- a final `passed: true` or `passed: false` result.

The supporting SQL, UAT cases, runbook and training guide show how the same checks fit into a controlled migration-validation and business-handover process.

## Conceptual architecture

![Conceptual SAP HANA and Microsoft Fabric architecture](architecture_diagram.jpg)

The diagram is retained from the original repository as conceptual context. It does not represent connectivity implemented by this lab. The original architectural discussion is preserved in [Architecture Context](docs/ARCHITECTURE_CONTEXT.md).

## Repository structure

```text
data/
  hana_orders.csv                  Synthetic source extract
  fabric_orders.csv                Synthetic target extract
src/
  __init__.py
  validate_migration.py            Standard-library reconciliation tool
tests/
  test_validate_migration.py       Automated pass and controlled-failure tests
sql/
  reconciliation_checks.sql        Example platform-neutral reconciliation SQL
docs/
  UAT_TEST_CASES.md                Analyst and business acceptance cases
  RUNBOOK.md                       Operating and exception-handling procedure
  TRAINING_GUIDE.md                Plain-language guide to the output
  ARCHITECTURE_CONTEXT.md          Preserved conceptual discussion
```

## Run the validator

Prerequisite: Python 3.10 or later. No third-party packages are required.

From the repository root:

```bash
python -m src.validate_migration data/hana_orders.csv data/fabric_orders.csv
```

The command prints a JSON report and exits with status `0` when validation passes or `1` when it fails. To save evidence for review:

```bash
python -m src.validate_migration data/hana_orders.csv data/fabric_orders.csv --output validation_report.json
```

## Run the tests

```bash
python -m unittest discover -s tests -v
```

The tests verify that a matching migration passes and that changing one target value fails with the affected order ID and field in the report.

## Create a controlled failure

Work on a copy of `data/fabric_orders.csv`, change the `quantity` or `unit_price` for one order, and pass that copy as the second argument. Do not change the baseline sample if you want the standard run to remain green.

Example:

```bash
python -m src.validate_migration data/hana_orders.csv path/to/fabric_orders_changed.csv
```

The report will set `passed` to `false` and list the order under `field_level_mismatches`.

## Why migration validation matters

A successful load is not proof that the right data arrived. Row-count, key, completeness, aggregate and field-level checks reduce the risk of silent data loss, duplication or transformation errors. Clear evidence also gives analysts and business owners a practical basis for UAT approval, reruns and escalation.

## SAP HANA and Microsoft Fabric context

In a real programme, extraction, security, network configuration, data types, transformation rules and Fabric ingestion would be implemented with approved enterprise services. This lab deliberately begins after extraction: `hana_orders.csv` stands in for a governed HANA source extract, while `fabric_orders.csv` stands in for the resulting Fabric table extract. This keeps the example honest, quick to run and focused on reconciliation.

## Skills demonstrated

- migration analysis and reconciliation design;
- Python data validation with minimal dependencies;
- SQL control checks and exception analysis;
- automated testing and repeatable evidence;
- business-oriented UAT planning;
- operational runbook, analyst training and user handover; and
- clear separation between a portfolio demonstration and production architecture.

## Author

- **Veera Babu Tiragatla**
- Melbourne, Australia
- [LinkedIn](https://www.linkedin.com/in/veerababutiragatla)
- [Website](https://www.veerababutiragatla.com)
