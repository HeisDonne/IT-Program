# Employee API — Migration to PostgreSQL

## Setup
- Flask + `psycopg2` (no ORM)
- Database: PostgreSQL, hosted on a remote VM
- Local machine runs the Flask app only; it never talks to Postgres directly — it connects through an SSH tunnel forwarded to the VM
- Tables: `employees`, `departments` (one-to-many — an employee belongs to one department)

## Architecture

```
[ Local machine ]                 [ SSH tunnel ]                [ VM ]
  Flask app (prac.py)  ---- 127.0.0.1:5433 ---------------->  Postgres (port 5432)
  psycopg2 connection
```

The app's connection config points at `127.0.0.1:5433` — that's the local end of the tunnel, not the VM itself:

```python
def get_db_connection():
    return psycopg2.connect(
        host="127.0.0.1",
        port=5433,
        database="employee_db",
        user="employees_api",
        password="Password"
    )
```

## Process

1. Provision Postgres on the VM (installed and running on its default port, 5432).
2. Create the database, a dedicated role, and grant it access.
3. Open an SSH tunnel from the local machine, forwarding a local port to the VM's Postgres port.
4. Design and create the schema (`departments`, `employees`).
5. Install Python dependencies locally.
6. Write the Flask routes against the real database.
7. Test each route through the tunnel.

## Commands

### 1. Open the SSH tunnel
```bash
ssh -L 5433:localhost:5432 vm_user@vm_ip -N
```
- `-L 5433:localhost:5432` — forward local port `5433` to `localhost:5432` *as seen from the VM*, i.e. the VM's own Postgres. `localhost` here refers to the VM, not your machine.
- `vm_user@vm_ip` — the SSH login for the VM.
- `-N` — don't run a remote shell, just hold the port forward open.

Run this in its own terminal (or with `-f` to background it) and leave it running while you work — the app can't reach Postgres without it.

### 2. Create the database and role (on the VM, as a Postgres superuser)
```bash
sudo -u postgres psql
```
```sql
CREATE DATABASE employee_db;
CREATE USER employees_api WITH PASSWORD 'Password';
GRANT ALL PRIVILEGES ON DATABASE employee_db TO employees_api;
```
- `sudo -u postgres psql` — connect to Postgres as the `postgres` OS/DB superuser, which is created automatically on install.
- `GRANT ALL PRIVILEGES` — gives the new role full access to that one database (scoped to just this database, not the whole server).

### 3. Verify the tunnel works before touching any code
```bash
psql -h 127.0.0.1 -p 5433 -U employees_api -d employee_db
```
- `-h 127.0.0.1 -p 5433` — connect to the local end of the tunnel rather than the VM's address directly.
- `-U` / `-d` — the role and database created in step 2.

If this connects, the tunnel and credentials are both confirmed working, which rules them out as a source of errors once the app is running.

### 4. Create the schema
```sql
CREATE TABLE departments (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE employees (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    department_id INTEGER REFERENCES departments(id)
);
```
`employees.department_id` is the foreign key the `/employees` GET route joins on. Run this from the same `psql` session as step 3, or save it as `schema.sql` and run:
```bash
psql -h 127.0.0.1 -p 5433 -U employees_api -d employee_db -f schema.sql
```

### 5. Install dependencies locally
```bash
pip install flask psycopg2-binary --break-system-packages
```

### 6. Run the app
```bash
python3 prac.py
```
Requires the SSH tunnel from step 1 to still be open.

## Routes → SQL

**`GET /employees`** — joins across the relationship and returns one flat row per employee:
```sql
SELECT
    employees.id,
    employees.name,
    departments.name AS department
FROM employees
JOIN departments
    ON employees.department_id = departments.id
ORDER BY employees.id;
```
`cursor.fetchall()` pulls every matching row back at once; each row is a tuple accessed by position (`row[0]`, `row[1]`, `row[2]`), rebuilt into a dict per employee for the JSON response.

**`POST /employees`** — validates required fields, then inserts:
```sql
INSERT INTO employees (name, department_id)
VALUES (%s, %s)
RETURNING id, name, department_id;
```
`%s` placeholders are filled in by `psycopg2` from the tuple `(name, department_id)` passed as the second argument to `cursor.execute()` — never string-formatted into the query directly, which avoids SQL injection. `RETURNING` hands back the full inserted row in the same round trip, avoiding a second `SELECT`. `conn.commit()` is required after any write (`INSERT`/`UPDATE`/`DELETE`) — without it, the change stays uncommitted and isn't actually saved.

**`DELETE /employees/<id>`** — deletes and confirms in one statement:
```sql
DELETE FROM employees WHERE id = %s RETURNING id;
```
`cursor.fetchone()` returns `None` if no row matched that `id`, which is how the route distinguishes "deleted" (200) from "nothing to delete" (404) before deciding whether to commit.

## Every route, same connection pattern
Each route opens its own connection and cursor, and closes both when done:
```python
conn = get_db_connection()
cursor = conn.cursor()
# ... execute + fetch ...
cursor.close()
conn.close()
```
This is simple and correct for low traffic, but opens a new TCP connection through the SSH tunnel on every request. If this API needs to handle meaningfully more traffic later, a connection pool (e.g. `psycopg2.pool`) is the next step — it keeps a set of connections open and reuses them instead of reconnecting each time.

## Testing through the tunnel
```bash
curl http://127.0.0.1:5000/employees
curl -X POST http://127.0.0.1:5000/employees -H "Content-Type: application/json" -d '{"name": "Ada Obi", "department_id": 1}'
curl -X DELETE http://127.0.0.1:5000/employees/1
```
These hit the local Flask server (port 5000, Flask's default), which is a separate thing from the SSH-tunneled Postgres port (5433) — the tunnel only needs to be up in the background while these run.

## Command reference

| Task | Command |
|---|---|
| Open SSH tunnel to VM's Postgres | `ssh -L 5433:localhost:5432 vm_user@vm_ip -N` |
| Connect as Postgres superuser (on VM) | `sudo -u postgres psql` |
| Connect through the tunnel (from local) | `psql -h 127.0.0.1 -p 5433 -U employees_api -d employee_db` |
| Run a .sql file through the tunnel | `psql -h 127.0.0.1 -p 5433 -U employees_api -d employee_db -f schema.sql` |
| Install Python deps | `pip install flask psycopg2-binary --break-system-packages` |
| Run the app | `python3 prac.py` |
| List tables (inside psql) | `\dt` |
| Describe a table (inside psql) | `\d employees` |
