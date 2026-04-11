# MISSING

Checks whether an item does not include a specified attribute.

## Source

- https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/ql-functions.missing.html

## Syntax

```sql
attributename IS MISSING
attributename IS NOT MISSING
```

## Key DynamoDB behavior

- Only equality and inequality style checks are supported with this function pattern.

## Return type

- `bool`

## Example

```sql
SELECT * FROM Music WHERE "Awards" IS MISSING
```

## Related references

- [SELECT](statements-select.md)
