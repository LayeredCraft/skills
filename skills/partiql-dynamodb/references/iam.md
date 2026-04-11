# IAM

Use this page for permission requirements and policy patterns for DynamoDB PartiQL.

## Source

- https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/ql-iam.html

## Required actions by statement type

- `dynamodb:PartiQLSelect`
- `dynamodb:PartiQLInsert`
- `dynamodb:PartiQLUpdate`
- `dynamodb:PartiQLDelete`

## Practical policy patterns

- allow all PartiQL actions on a table
- allow only `PartiQLSelect`
- allow action scope on a table index ARN
- allow only transactional PartiQL via `dynamodb:EnclosingOperation`
- deny transactional PartiQL while allowing non-transactional usage
- deny full-table-scan style `SELECT` using `dynamodb:FullTableScan`

## Caveats

- Scope permissions to exact table/index ARNs whenever possible.
- Use explicit deny rules for scan-risk controls when needed.

## Related references

- [SELECT](statements-select.md)
- [Transactions](transactions.md)
- [Batch Operations](batch-operations.md)
