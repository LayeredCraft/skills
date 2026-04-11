# Batch Operations

Use this page for batch PartiQL execution in DynamoDB.

## Source

- https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/ql-reference.multiplestatements.batching.html

## Core limits and rules

- A batch must be all reads or all writes.
- Maximum 25 statements per batch.

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

- Keep batches small and predictable for retry safety.
- Batch behavior is still bounded by DynamoDB throughput and request limits.

## Related references

- [Statements](statements.md)
- [Transactions](transactions.md)
