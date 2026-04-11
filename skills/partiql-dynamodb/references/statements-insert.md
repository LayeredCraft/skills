# INSERT

Use `INSERT` to add one new item to a DynamoDB table.

## Source

- https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/ql-reference.insert.html

## Syntax

```sql
INSERT INTO table VALUE item
```

## Key DynamoDB behavior

- One item per statement.
- If an item with the same primary key exists, DynamoDB returns `DuplicateItemException`.

## Minimal example

```sql
INSERT INTO "Music" VALUE {'Artist': 'Acme Band', 'SongTitle': 'PartiQL Rocks'}
```

## Related references

- [Data Types](data-types.md)
- [Transactions](transactions.md)
- [Batch Operations](batch-operations.md)
