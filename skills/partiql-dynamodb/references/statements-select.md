# SELECT

Use `SELECT` to retrieve items from DynamoDB tables or indexes through PartiQL.

## Source

- https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/ql-reference.select.html

## Syntax

```sql
SELECT expression [, ...]
FROM table[.index]
[WHERE condition]
[ORDER BY key [DESC|ASC], ...]
```

## Key DynamoDB behavior

- `WHERE` design determines whether the operation is query-like or scan-like.
- To avoid full table scans, include partition-key equality or `IN` conditions.
- Missing or non-key-only filters can force full scans.

## Practical guardrails

- Prefer `WHERE PartitionKey = value` or `WHERE PartitionKey IN [...]`.
- Be careful with `OR` combinations that include non-key predicates.
- Use IAM policy controls when you must block scan-causing PartiQL patterns.

## Minimal examples

```sql
SELECT OrderID, Total
FROM "Orders"
WHERE OrderID = 1
```

```sql
SELECT OrderID, Total
FROM "Orders"
WHERE OrderID IN [1, 2, 3] ORDER BY OrderID DESC
```

## Related references

- [Operators](operators.md)
- [Functions](functions.md)
- [IAM](iam.md)
