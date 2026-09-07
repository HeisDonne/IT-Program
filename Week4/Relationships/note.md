# Relationships

## Placeholders used
`parent_table` = the table on the "one" side of a one-to-many relationship. `child_table` = the table on the "many" side. `table_a` / `table_b` = two tables in a many-to-many relationship. Which real table plays which role is decided when designing the schema.

## Definition
A relationship links a row in one table to a row (or rows) in another, instead of duplicating that data inline. This is enforced through a **foreign key**: a column in one table whose value is required to match a primary key value in another table.

## Why relationships exist
Repeating related details (e.g. a customer's full name/address) on every row that references them duplicates data and risks it going out of sync when the original changes. Splitting related data into its own table, and linking to it, is called **normalization**.

## Foreign keys

```sql
CREATE TABLE parent_table (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE child_table (
    id SERIAL PRIMARY KEY,
    parent_id INTEGER REFERENCES parent_table(id),
    detail VARCHAR(100)
);
```
- `parent_id INTEGER` — the foreign key column itself; holds a whole number.
- `REFERENCES parent_table(id)` — constrains that number to match an existing `id` in `parent_table`, or be `NULL`. An insert/update supplying a `parent_id` that doesn't exist in `parent_table` is rejected.

## Relationship types

### One-to-many
One row in `parent_table` can be linked to many rows in `child_table`; each `child_table` row belongs to exactly one parent. The foreign key is placed on the "many" side (`child_table.parent_id`), since a single column can only hold one value.

### Many-to-many
Rows on both sides can link to multiple rows on the other side. Requires a third table — a **junction table** — holding one foreign key to each side:

```sql
CREATE TABLE table_a (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE table_b (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE table_a_table_b (
    table_a_id INTEGER REFERENCES table_a(id),
    table_b_id INTEGER REFERENCES table_b(id),
    PRIMARY KEY (table_a_id, table_b_id)
);
```
- `table_a_id` / `table_b_id` — one foreign key column per side.
- `PRIMARY KEY (table_a_id, table_b_id)` — a **composite primary key**: uniqueness applies to the combination of both columns, so the same pairing can't be inserted twice, but each individual value can appear in many different pairings.

### One-to-one
Each row in one table relates to at most one row in another. Enforced with `UNIQUE` on the foreign key column:

```sql
CREATE TABLE related_table (
    parent_id INTEGER UNIQUE REFERENCES parent_table(id),
    extra_detail TEXT
);
```
- `UNIQUE` here stops the same `parent_id` from being linked to more than one row in `related_table`.

## ON DELETE behavior
Specified as part of the foreign key definition; determines what happens to child rows when the referenced parent row is deleted.

```sql
parent_id INTEGER REFERENCES parent_table(id) ON DELETE CASCADE
```
- `CASCADE` — deleting the parent row automatically deletes every child row referencing it.

```sql
parent_id INTEGER REFERENCES parent_table(id) ON DELETE SET NULL
```
- `SET NULL` — deleting the parent row sets `parent_id` to `NULL` on child rows instead of deleting them (requires the column to allow `NULL`).

```sql
parent_id INTEGER REFERENCES parent_table(id) ON DELETE RESTRICT
```
- `RESTRICT` — blocks the delete entirely while any child row still references the parent.

## JOIN
Combines rows from two tables into single result rows based on a matching condition.

```sql
SELECT child_table.detail, parent_table.name
FROM child_table
JOIN parent_table ON child_table.parent_id = parent_table.id;
```
- `JOIN parent_table` — the table being joined in.
- `ON child_table.parent_id = parent_table.id` — the matching condition; for each `child_table` row, find the `parent_table` row where `id` equals that row's `parent_id`.
- This is an `INNER JOIN` (`JOIN` alone defaults to it) — rows with no match on either side are excluded from the result.

```sql
SELECT parent_table.name, child_table.detail
FROM parent_table
LEFT JOIN child_table ON parent_table.id = child_table.parent_id;
```
- `LEFT JOIN` — keeps every row from `parent_table` (the "left" table, named first) regardless of a match, filling `NULL` into `child_table.detail` when none exists.

| JOIN type | Returns |
|---|---|
| `INNER JOIN` / `JOIN` | Only rows with a match on both sides |
| `LEFT JOIN` | All rows from the left table; `NULL` from the right where unmatched |
| `RIGHT JOIN` | All rows from the right table; `NULL` from the left where unmatched |
| `FULL JOIN` | All rows from both tables, matched where possible |
