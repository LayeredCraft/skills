# Getting Started

Use this page for first-run DynamoDB PartiQL workflows in console, NoSQL Workbench, CLI, and API code paths.

## Source

- https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/ql-gettingstarted.html

## Main usage paths

- Console: use the DynamoDB PartiQL editor and generated query flow.
- NoSQL Workbench: build statements and supply typed parameters.
- AWS CLI: run `aws dynamodb execute-statement --statement "..."`.
- SDK/API: run `ExecuteStatement` style operations with parameterized values.

## Prerequisites

- Have a DynamoDB table with known partition key (and sort key if applicable).
- For AWS examples that use `Music`, adapt key names and values to your table schema.

## Useful starter sequence

- Insert one item with `INSERT`.
- Retrieve with `SELECT`.
- Modify with `UPDATE`.
- Remove with `DELETE`.

## Caveats

- Keep examples DynamoDB-specific and table-key aware.
- Prefer parameterized statements for safety and clarity in API workflows.

## Related references

- [Overview](overview.md)
- [SELECT](statements-select.md)
- [INSERT](statements-insert.md)
- [UPDATE](statements-update.md)
- [DELETE](statements-delete.md)
