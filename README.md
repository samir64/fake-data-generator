# Python Fake Data Generator v1.0

## Getting Started

Python `fake-data-generator`'s project use to `JSON` object to define `sample data` and `table definitions`.

These files are `samples.json` and `tables.json`.

### `Sample Data` Structore

You can use one level to n-level nested data.
to get an item you must call children recursively by "`.`" operand like this:

`group1.subgroup1.subgroup1_child1.subgroup1_child1_item1`

```json
{
  "group1": {
    "subgroup1": {
      "child1": [
        "item1",
        "item2",
        ...
      ],
      "child2": [
        "item1",
        "item2",
        ...
      ]
    },
    "subgroup2": [
      "item1",
      "item2",
      ...
    ]
    ...
  },
  "group2": [
    "item1",
    "item2",
    ...
  ],
  ...
}
```

### `Table Definitions` Structore

```json
{
  "table_name": {
    "count": 20, // For generate 20 record. Default value is 10.
    "relations": { // If this table related to another by a field, if not leave this section
      "related_field": { // This table related field
        "table": "target_table_name",
        "field": "detination_field"
      },
      ...
    },
    "fields": {
      "field_name": {
        "type": "string|number",
        "format": "FORMAT_STRING" // See `Format String` section
      },
      ...
    }
  }
}
```

### Format String

`<from,to>` To define a random number between `from` and `to`

`[a-f2-6:count_from,count_to]` To return a string by defined characters before "`:`" repeated some times between `count_from` and `count_to`.
Default value of `count_from` is 10 and if dont use `count_to` it use `count_from` value as `count_to`.


`@sample_name;` For use a random sample value from your samples list. for accessing to nested values you have to use "`.`" like this: `@group1.subgroup2.child2;`, this means you need an item in `group1 -> subgroup2 -> child2` (`child2` should defines as an array)
