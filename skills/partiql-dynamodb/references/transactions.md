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

## Parts explained

- `Statement`: required PartiQL statement string.
- `Parameters`: optional typed values used in positional placeholders.
- `parametertype`: DynamoDB type wrapper (for example `S`, `N`, `BOOL`).
- `parametervalue`: value for that typed parameter.

## Return behavior

- Write transactions do not return item content.
- Read transactions return items based on the `SELECT` statements and conditions.

## Operational caveats

- On per-statement failures, transaction cancellation behavior is surfaced as `TransactionCanceledException`.
- Keep statements and conditions deterministic to avoid partial-intent retries.
- If any statement fails, DynamoDB cancels the transaction.

## Related references

- [EXISTS](functions-exists.md)
- [Statements](statements.md)
- [IAM](iam.md)
