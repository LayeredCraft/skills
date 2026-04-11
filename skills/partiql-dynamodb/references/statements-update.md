# UPDATE

Use `UPDATE` to modify attributes in a single DynamoDB item.

## Source

- https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/ql-reference.update.html

## Syntax

```sql
UPDATE table
[SET | REMOVE] path [= data] [...]
WHERE condition [RETURNING returnvalues]
```

## Key DynamoDB behavior

- One item per statement.
- `WHERE` must resolve to a single primary key value.
- Supports `LIST_APPEND`, `SET_ADD`, and `SET_DELETE` in `SET` operations.
- Optional `RETURNING` controls whether old/new attributes are returned.

## Minimal examples

```sql
UPDATE "Music"
SET AwardsWon = 1
SET AwardDetail = {'Grammys': [2020, 2018]}
WHERE Artist = 'Acme Band' AND SongTitle = 'PartiQL Rocks'
```

```sql
UPDATE "Music"
SET BandMembers = set_add(BandMembers, <<'newbandmember'>>)
WHERE Artist = 'Acme Band' AND SongTitle = 'PartiQL Rocks'
```

## Related references

- [Data Types](data-types.md)
- [Functions](functions.md)
- [Transactions](transactions.md)
- [Batch Operations](batch-operations.md)
