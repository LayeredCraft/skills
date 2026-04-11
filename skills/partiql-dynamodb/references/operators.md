# Operators

Use this page for supported arithmetic, comparison, and logical operators in DynamoDB PartiQL.

## Source

- https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/ql-operators.html

## Arithmetic operators

- `+`
- `-`

## Comparison operators

- `=`
- `<>`
- `!=`
- `>`
- `<`
- `>=`
- `<=`

## Logical operators

- `AND`
- `BETWEEN`
- `IN`
- `IS`
- `NOT`
- `OR`

## DynamoDB caveats

- Only listed operators are supported.
- `IN` has practical limits called out in docs (value count and paginated retrieval behavior).

## Related references

- [SELECT](statements-select.md)
- [Functions](functions.md)
