# User Acceptance Test Cases

These cases use synthetic sustainable-packaging orders. They demonstrate how an analyst or business owner could assess migration evidence; they are not evidence from a production migration.

| ID | Business objective | Procedure | Expected result | Evidence / owner |
|---|---|---|---|---|
| UAT-01 | Confirm all orders migrated | Run the validator against the baseline source and target extracts. | Source and target counts are both 6; no missing or extra order IDs; `passed` is `true`. | JSON report / data analyst |
| UAT-02 | Confirm key uniqueness | Review duplicate-key results for both extracts. | No duplicate `order_id` values are reported. | JSON report / data analyst |
| UAT-03 | Confirm mandatory information | Review missing-required-field results. | No blank order, customer, product, quantity, price, date or status values are reported. | JSON report / business analyst |
| UAT-04 | Confirm financial and quantity accuracy | Compare quantities and unit prices by order and review aggregate SQL outputs. | No field mismatch; total quantities and calculated order values reconcile. | JSON and SQL results / finance or operations owner |
| UAT-05 | Confirm status integrity | Compare the status distribution between source and target. | Counts for `PENDING`, `CONFIRMED`, `PROCESSING` and `SHIPPED` agree. | SQL result / operations owner |
| UAT-06 | Prove exception detection | Change one quantity in a working copy of the target extract and rerun. | `passed` is `false`; the report identifies the affected `order_id`, field and both values. | Failure report / test lead |
| UAT-07 | Confirm rerun readiness | Correct the working-copy exception and rerun the same command. | The corrected run passes and is retained as the latest evidence. | JSON report / test lead |

## Acceptance decision

Business acceptance requires all agreed controls to pass, any accepted exceptions to have an owner and rationale, and the final evidence to be stored with the migration test record. A technical pass does not replace business-owner sign-off.
