# Transactions

Use this page for multi-statement transactional PartiQL execution in DynamoDB.

## Source

- https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/ql-reference.multiplestatements.transactions.html

## Core limits and rules

- Up to 100 total statements per transaction.
- A transaction must be all reads or all writes.
- `EXISTS` is the documented exception used for conditional-style checks within transaction workflows.

## Statement shape

```json
[
  {
    "Statement": "statement",
    "Parameters": [
      { "S": "value" }
    ]
  }
]
```

## Operational caveats

- On per-statement failures, transaction cancellation behavior is surfaced as `TransactionCanceledException`.
- Keep statements and conditions deterministic to avoid partial-intent retries.

## Related references

- [EXISTS](functions-exists.md)
- [Statements](statements.md)
- [IAM](iam.md)
