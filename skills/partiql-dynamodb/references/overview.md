# Overview

PartiQL in DynamoDB provides SQL-compatible statements for reading and modifying items, while keeping DynamoDB data-plane behavior.

## Source

- https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/ql-reference.html

## What DynamoDB PartiQL is

- Supports SQL-like `SELECT`, `INSERT`, `UPDATE`, and `DELETE` against DynamoDB tables.
- Works through DynamoDB console, NoSQL Workbench, AWS CLI, and DynamoDB APIs.
- Uses DynamoDB service semantics for performance and availability.

## Important boundaries

- DynamoDB supports a subset of PartiQL.
- DynamoDB docs explicitly call out that Amazon Ion format and literals are not supported.

## Related references

- [Getting Started](getting-started.md)
- [Statements](statements.md)
- [Functions](functions.md)
- [Operators](operators.md)
- [Transactions](transactions.md)
- [Batch Operations](batch-operations.md)
- [IAM](iam.md)
