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

## Example

```sql
SELECT * FROM "Orders" WHERE "OrderID" = 1 AND size("Image") > 300
```

## Related references

- [SELECT](statements-select.md)
