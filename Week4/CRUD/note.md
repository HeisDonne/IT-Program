# CRUD

## Placeholders used
`table_name`, `column1`, `column2`, `'value1'`, `'value2'` represent your actual table name, column names, and data. `id` is left as-is (primary key convention). `%s`, seen in application code, is a driver-level parameter placeholder — not SQL syntax — filled in safely by the driver from a value passed separately, which avoids SQL injection.

## Definition
CRUD stands for Create, Read, Update, Delete — the four operations performed on stored data. Each maps to one SQL statement: `INSERT` (Create), `SELECT` (Read), `UPDATE` (Update), `DELETE` (Delete).

## Create — INSERT

```sql
INSERT INTO table_name (column1, column2)
VALUES ('value1', 'value2');
```
- `INSERT INTO table_name` — the table receiving the new row.
- `(column1, column2)` — which columns are being supplied values for; any column left out gets its `DEFAULT`, or `NULL` if allowed, or the statement fails if it's `NOT NULL` with no default.
- `VALUES ('value1', 'value2')` — the actual data, matched positionally to the column list.

```sql
INSERT INTO table_name (column1, column2)
VALUES
    ('value1', 'value2'),
    ('value3', 'value4');
```
- Multiple `(...)` groups after `VALUES`, comma-separated — inserts several rows in one statement.

```sql
INSERT INTO table_name (column1, column2)
VALUES ('value1', 'value2')
RETURNING id, column1, created_at;
```
- `RETURNING` — lists columns from the row as it now exists in the database, handed back immediately without a separate `SELECT`. Useful for reading back auto-generated values like `id` or a `DEFAULT`-filled timestamp.

## Read — SELECT

```sql
SELECT * FROM table_name;
```
- `*` — every column.

```sql
SELECT column1, column2 FROM table_name;
```
- Naming columns explicitly instead of `*` limits the result to just those fields.

```sql
SELECT * FROM table_name WHERE column1 = 'value1';
```
- `WHERE` — condition restricting which rows are returned (full syntax in **SQL Basics**).

```sql
SELECT * FROM table_name ORDER BY column2 DESC LIMIT 5;
```
- `ORDER BY column2 DESC` — sorts results by `column2`, highest to lowest.
- `LIMIT 5` — caps the result to the first 5 rows after sorting.

```sql
SELECT * FROM table_name WHERE id = 3;
```
- Lookup by primary key — the typical shape of a "get one item" API route.

## Update — UPDATE

```sql
UPDATE table_name
SET column1 = 'new_value'
WHERE id = 3;
```
- `SET column1 = 'new_value'` — the column(s) being changed and their new value(s).
- `WHERE id = 3` — restricts the change to matching rows. Omitting `WHERE` applies the `SET` to every row in the table.

```sql
UPDATE table_name
SET column1 = 'new_value', column2 = 'another_value'
WHERE id = 3
RETURNING *;
```
- Multiple `SET` assignments, comma-separated.
- `RETURNING *` — returns the row as it looks after the update.

## Delete — DELETE

```sql
DELETE FROM table_name WHERE id = 3;
```
- `WHERE id = 3` — restricts which rows are removed. Omitting it deletes every row in the table.

```sql
DELETE FROM table_name WHERE id = 3 RETURNING *;
```
- `RETURNING *` — returns the row(s) as they were just before deletion.

## Upsert — INSERT ... ON CONFLICT

```sql
INSERT INTO table_name (id, column1, column2)
VALUES (3, 'value1', 'value2')
ON CONFLICT (id)
DO UPDATE SET column1 = EXCLUDED.column1, column2 = EXCLUDED.column2;
```
- `ON CONFLICT (id)` — the constraint (here, the primary key) to watch for a clash on.
- `DO UPDATE SET ...` — runs instead of failing, when a row with that `id` already exists.
- `EXCLUDED` — refers to the row values that were originally proposed for insertion, reusable in the update clause.

## Transactions

```sql
BEGIN;

UPDATE table_name SET column1 = column1 - 100 WHERE id = 1;
UPDATE table_name SET column1 = column1 + 100 WHERE id = 2;

COMMIT;
```
- `BEGIN` — starts a transaction; statements after it are provisional.
- `COMMIT` — confirms every statement since `BEGIN` at once, making the changes permanent.
- `ROLLBACK` (in place of `COMMIT`) — discards every change since `BEGIN`, as if none of it happened.

## Mapping to an API

| HTTP verb | Route example | SQL |
|---|---|---|
| POST | `/resource` | `INSERT ... RETURNING *` |
| GET | `/resource` | `SELECT * FROM table_name` |
| GET | `/resource/<id>` | `SELECT * FROM table_name WHERE id = %s` |
| PUT/PATCH | `/resource/<id>` | `UPDATE ... WHERE id = %s RETURNING *` |
| DELETE | `/resource/<id>` | `DELETE FROM table_name WHERE id = %s` |

See **Employee-API-Migration** for this pattern applied to a working API.
