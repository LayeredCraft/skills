# Data Types

Use this page to map DynamoDB types to PartiQL representations and write valid literals.

## Source

- https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/ql-reference.data-types.html

## Core mappings

- `String` -> `'value'`
- `Number` -> `1`, `1.0`, `1e0`
- `Boolean` -> `TRUE` / `FALSE`
- `Null` -> `NULL`
- `List` -> `[value1, value2]`
- `Map` -> `{'name': value}`
- `Number Set` -> `<<1,2,3>>`
- `String Set` -> `<<'a','b'>>`

## Caveats

- String values require single quotes.
- Number precision follows DynamoDB numeric limits.
- Binary handling is not represented as inline literal syntax in this reference context.

## Minimal examples

```sql
INSERT INTO TypesTable VALUE {
  'primarykey':'1',
  'NumberType':1,
  'MapType': {'entryname1': 'value', 'entryname2': 4},
  'ListType': [1, 'stringval'],
  'NumberSetType': <<1,34,32,4.5>>,
  'StringSetType': <<'stringval','stringval2'>>
}
```

## Related references

- [UPDATE](statements-update.md)
- [Functions](functions.md)
