# PostgreSQL

## Definition
PostgreSQL ("Postgres") is an open-source relational database management system (RDBMS). Data is organized into tables (rows of typed columns), tables can reference one another, and all reading and writing is done through SQL (Structured Query Language). Postgres runs as a server process; applications connect to it as clients over a network connection (even if that network is `localhost`).

**Relational** means data lives in separate tables linked by shared key values, rather than one unstructured collection — this avoids duplicating the same information across many records and lets the database enforce rules about how records relate to each other.

## Key properties

| Property | What it means |
|---|---|
| ACID transactions | A group of statements either all succeed or all fail together — no partial/corrupted writes |
| Enforced constraints | Rules like `NOT NULL`, `UNIQUE`, `FOREIGN KEY`, `CHECK` are enforced by the database engine itself, not left to application code |
| Rich data types | Native support for arrays, `JSON`/`JSONB`, `UUID`, and more, beyond plain numbers/text |
| Standards-compliant | Closely follows the SQL standard, so skills transfer to other relational databases |
| Free, open-source | No license cost, runs on all major OSes and cloud providers |

## Comparison to alternatives

| vs | Difference |
|---|---|
| SQLite | Single local file, no server process — fits small/single-user apps. Postgres runs as a dedicated server built for many concurrent clients |
| MySQL | Both are mature open-source RDBMSs; Postgres is generally stricter on SQL standards and has richer data types |
| NoSQL (e.g. MongoDB) | NoSQL stores are schema-flexible, often storing loose JSON-like documents; Postgres requires a defined schema and enforces relational integrity |

## Core vocabulary

| Term | Definition |
|---|---|
| Database | A named container holding a related set of tables |
| Table | A structured collection of rows sharing the same typed columns |
| Row (record) | One entry in a table |
| Column (field) | A named, typed slot every row in a table has |
| Primary key | The column (or columns) that uniquely identifies each row |
| Foreign key | A column whose values must match a primary key in another table |
| Index | An auxiliary structure that speeds up lookups on a column |
| Transaction | A group of statements executed as a single all-or-nothing unit |

## Connecting to a database

### `psql` — interactive command-line client
```bash
psql -U postgres -d your_database
```
- `psql` — the client program, installed alongside the Postgres server.
- `-U postgres` — connect using the role (user) named `postgres`.
- `-d your_database` — the specific database to connect to.

Once connected, you're at an interactive prompt where you type SQL statements (terminated with `;`) or `psql`-specific meta-commands (prefixed with `\`, e.g. `\dt`).

### From application code
```bash
pip install psycopg2-binary --break-system-packages   # raw SQL driver — you write the SQL directly
pip install flask-sqlalchemy --break-system-packages  # ORM — you write Python classes, it generates SQL
```
- `psycopg2-binary` — a Python driver that opens a connection to Postgres and lets you execute SQL strings directly.
- `flask-sqlalchemy` — an ORM (Object-Relational Mapper) integrated with Flask; you define Python classes representing tables, and it translates method calls into SQL for you.
- `--break-system-packages` — required on distributions (e.g. recent Debian/Ubuntu) that block `pip` from installing outside a virtual environment by default.

## Related notes
- **Tables** — defining structure
- **SQL Basics** — the query language
- **Relationships** — linking tables together
- **CRUD** — the four core read/write operations
- **Employee-API-Migration** — all of the above applied to a real API
