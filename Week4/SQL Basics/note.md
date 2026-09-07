# SQL Basics

## Placeholders used
`table_name`, `column1`, `column2`, quoted `'value'`s represent your actual table name, column names, and data. `table_a` / `table_b` in the JOIN example represent any two related tables.

## Definition
SQL (Structured Query Language) is the language used to read and write data in a relational database. It's declarative — a statement describes *what* result is wanted, and the database's query planner determines *how* to retrieve it.

## SELECT statement structure

```sql
SELECT column1, column2       -- columns to return
FROM table_name                -- source table
WHERE condition                -- row filter
ORDER BY column1 ASC          -- sort order
LIMIT 10 OFFSET 0;             -- pagination
```
- `SELECT` — the columns to include in the result.
- `FROM` — the table being queried.
- `WHERE` — an optional condition filtering which rows qualify.
- `ORDER BY` — optional sort instruction.
- `LIMIT` / `OFFSET` — optional row-count cap and skip count.

Logical execution order (differs from the order you write it): `FROM` → `WHERE` → `GROUP BY` → `HAVING` → `SELECT` → `ORDER BY` → `LIMIT`.

## WHERE — filtering rows

```sql
SELECT * FROM table_name WHERE column1 > 100;
```
- Standard comparisons: `=`, `!=` (or `<>`), `>`, `<`, `>=`, `<=`.

```sql
SELECT * FROM table_name WHERE column1 BETWEEN 10 AND 50;
```
- `BETWEEN a AND b` — inclusive range check, equivalent to `column1 >= a AND column1 <= b`.

```sql
SELECT * FROM table_name WHERE column1 IN ('value1', 'value2');
```
- `IN (...)` — matches any value in the given list.

```sql
SELECT * FROM table_name WHERE column1 LIKE '%partial%';
```
- `LIKE` — pattern match on text. `%` matches any sequence of characters (including none); `_` matches exactly one character. `'%partial%'` matches values containing "partial" anywhere.

```sql
SELECT * FROM table_name WHERE column1 IS NULL;
```
- `IS NULL` / `IS NOT NULL` — tests for absence of a value. `= NULL` never matches anything, including null values themselves, so this special syntax is required.

```sql
SELECT * FROM table_name WHERE column1 > 100 AND column2 = 'value';
SELECT * FROM table_name WHERE column1 = 'value1' OR column1 = 'value2';
```
- `AND` — both conditions must be true. `OR` — at least one must be true. Parentheses can group conditions, e.g. `WHERE (a OR b) AND c`.

## ORDER BY and LIMIT

```sql
SELECT * FROM table_name ORDER BY column1 DESC;
```
- `DESC` — descending order (highest/most-recent first). `ASC` (ascending) is the default if omitted.

```sql
SELECT * FROM table_name ORDER BY column1 ASC, column2 DESC;
```
- Multiple columns — rows are sorted by the first; ties are then sorted by the second.

```sql
SELECT * FROM table_name ORDER BY id LIMIT 10 OFFSET 20;
```
- `LIMIT 10` — return at most 10 rows.
- `OFFSET 20` — skip the first 20 matching rows before collecting those 10. Standard pagination pattern (`OFFSET 20 LIMIT 10` = "page 3" at 10 rows/page).

## DISTINCT

```sql
SELECT DISTINCT column1 FROM table_name;
```
- Returns each unique value in `column1`, with duplicates collapsed to one entry.

## Aggregate functions

```sql
SELECT COUNT(*) FROM table_name;
SELECT AVG(column1) FROM table_name;
SELECT MIN(column1), MAX(column1) FROM table_name;
SELECT SUM(column1) FROM table_name WHERE column2 = 'value';
```
- `COUNT(*)` — number of rows. `AVG` — mean value. `MIN`/`MAX` — smallest/largest value. `SUM` — total. `WHERE` still applies before the aggregate runs.

## GROUP BY

```sql
SELECT column2, COUNT(*) AS total, AVG(column1) AS average
FROM table_name
GROUP BY column2;
```
- `GROUP BY column2` — buckets rows sharing the same `column2` value; aggregate functions run separately per bucket.
- `AS total`, `AS average` — aliases, renaming the output columns for readability.
- Rule: every non-aggregated column in `SELECT` must also appear in `GROUP BY`.

## HAVING

```sql
SELECT column2, COUNT(*) AS total
FROM table_name
GROUP BY column2
HAVING COUNT(*) > 5;
```
- `HAVING` — filters groups after aggregation (`WHERE` filters individual rows before grouping; it can't reference an aggregate result since that value doesn't exist yet at that stage).

## JOIN
(full detail in **Relationships**)
```sql
SELECT table_a.column1, table_b.column1
FROM table_a
JOIN table_b ON table_a.table_b_id = table_b.id;
```
- `ON` — the condition matching rows between the two tables.

## Subqueries

```sql
SELECT * FROM table_name
WHERE column1 > (SELECT AVG(column1) FROM table_name);
```
- `(SELECT AVG(column1) FROM table_name)` — a nested query evaluated first, producing a single value used by the outer `WHERE`.

## Comments

```sql
-- text after two dashes, to end of line, is ignored

/* text between these markers,
   across multiple lines,
   is also ignored */
```

## Case sensitivity
- Keywords (`SELECT`, `WHERE`, etc.) — not case-sensitive; uppercase is convention only.
- Unquoted table/column names — automatically lowercased by Postgres, so `TableName` and `tablename` refer to the same object.
- String values in `'single quotes'` — case-sensitive: `'Value'` and `'value'` are different strings.
