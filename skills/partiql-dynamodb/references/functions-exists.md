# EXISTS

Use `EXISTS` for transactional existence checks similar to `ConditionCheck` behavior.

## Source

- https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/ql-functions.exists.html

## Syntax

```sql
EXISTS(statement)
```

## Arguments

- `statement`: required `SELECT` statement to evaluate.

## Key DynamoDB behavior

- Only valid in transactional operations.
- The `SELECT` inside `EXISTS` must specify a full primary key and one additional condition.

## Return type

- `bool`

## Example

```sql
EXISTS(
  SELECT * FROM "Music"
  WHERE "Artist" = 'Acme Band' AND "SongTitle" = 'PartiQL Rocks'
)
```

## Related references

- [Transactions](transactions.md)
