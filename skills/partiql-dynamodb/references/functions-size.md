# SIZE

Returns a number representing an attribute size in bytes.

## Source

- https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/ql-functions.size.html

## Syntax

```sql
size(path)
```

## Arguments

- `path`: attribute name or document path.

## Return type

- `int`

## Where to use it

- Typically used in `WHERE` conditions to filter by attribute size.

## Limitations

- Valid only for DynamoDB-supported `size` operand types.
- Returns an integer byte size; use comparisons in conditions for filtering.

## Example

```sql
SELECT * FROM "Orders" WHERE "OrderID" = 1 AND size("Image") > 300
```

## Related references

- [SELECT](statements-select.md)
