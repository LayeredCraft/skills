# CONTAINS

Checks whether a string contains a substring or whether a set includes a member.

## Source

- https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/ql-functions.contains.html

## Syntax

```sql
contains(path, substring)
```

## Arguments

- `path`: attribute name or document path.
- `substring`: target substring or set member.

## Return type

- `bool`

## Where to use it

- Typically used in `WHERE` conditions for substring or set-member checks.

## Limitations

- `contains` is documented for string substring checks and set membership checks.
- Input/value compatibility depends on the underlying attribute type.

## Example

```sql
SELECT * FROM "Orders" WHERE "OrderID" = 1 AND contains("Address", 'Kirkland')
```

## Related references

- [SELECT](statements-select.md)
- [Data Types](data-types.md)
