# Operators

Use this page for supported arithmetic, comparison, and logical operators in DynamoDB PartiQL.

## Source

- https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/ql-operators.html

## Arithmetic operators

- `+` add numeric values
- `-` subtract numeric values

## Comparison operators

- `=` equal to
- `<>` not equal to
- `!=` not equal to
- `>` greater than
- `<` less than
- `>=` greater than or equal to
- `<=` less than or equal to

## Logical operators

- `AND` all conditions must be true
- `BETWEEN` inclusive range check
- `IN` membership check in a list of values
- `IS` type/null/missing style checks
- `NOT` negates a condition
- `OR` at least one condition must be true

## DynamoDB caveats

- Only listed operators are supported.
- `IN` has practical limits called out in docs (value count and paginated retrieval behavior).

## Related references

- [SELECT](statements-select.md)
- [Functions](functions.md)
