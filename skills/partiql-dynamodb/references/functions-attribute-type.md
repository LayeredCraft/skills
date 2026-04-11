# ATTRIBUTE_TYPE

Checks whether an attribute is a specific DynamoDB type.

## Source

- https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/ql-functions.attribute_type.html

## Syntax

```sql
attribute_type(attributename, type)
```

## Arguments

- `attributename`: attribute to inspect.
- `type`: target attribute type token.

## Return type

- `bool`

## Example

```sql
SELECT * FROM "Music" WHERE attribute_type("Artist", 'S')
```

## Related references

- [Data Types](data-types.md)
- [SELECT](statements-select.md)
