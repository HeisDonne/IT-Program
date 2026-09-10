# Password Hashing

## Definition
Password hashing is the process of converting a plaintext password into a fixed-format string that can be used to *verify* a password later, without ever storing the original password itself. If a database is ever compromised, properly hashed passwords cannot be directly reversed back into the originals.

## Why a general-purpose hash (e.g. SHA256) is unsuitable for passwords
```python
import hashlib
hashlib.sha256(password.encode()).hexdigest()   # do not use this for passwords
```
Two specific problems:
- **It's fast.** SHA256 was designed for speed — useful for checksums/integrity verification, but exactly the wrong property for password storage. Modern hardware can compute billions of SHA256 hashes per second, making brute-force guessing of common passwords computationally trivial.
- **It's unsalted by default.** Identical passwords produce identical hashes. This enables **rainbow tables** — precomputed lookup tables mapping common passwords to their hash — turning "cracking" into a simple lookup.

## What bcrypt does differently
- **Deliberately slow, and adjustably so** — controlled by a "work factor" (also called cost/rounds), which sets how many internal iterations the algorithm runs. As hardware gets faster over time, the work factor can be increased to keep pace, which a fixed-speed algorithm like SHA256 cannot do.
- **Automatic random salting** — a random salt is generated per password and embedded directly into the resulting hash string, so identical passwords produce different stored hashes, defeating rainbow tables outright.

## Installing and using it

```bash
pip install flask-bcrypt
```

```python
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)   # or bcrypt.init_app(app) if created separately, see Project Structure
```

**Hashing a password (on register):**
```python
hashed = bcrypt.generate_password_hash(password).decode("utf-8")
```
- `generate_password_hash(password)` — generates a random salt, runs the slow hashing algorithm using it, and returns the salt + resulting hash + work factor packed into one value.
- Returns **bytes** by default (`b'$2b$12$...'`), not a string — `.decode("utf-8")` converts it to a plain string for storage in a `String`/`VARCHAR` database column.

**Verifying a password (on login):**
```python
bcrypt.check_password_hash(stored_hash, entered_password)
```
- Reads the salt back out of `stored_hash`, re-hashes `entered_password` using that same salt, and compares the result to the hash portion of `stored_hash`. Returns `True`/`False`.

## Anatomy of a stored hash
```
$2b$12$KIXQeE9y8QmY3vN.OZ1u1eV5C9Xz6yqzX9L9zGqLxKz7VwHqXeWzO
```
| Segment | Meaning |
|---|---|
| `$2b$` | bcrypt algorithm version identifier |
| `12$` | work factor (cost) used |
| next 22 characters | the salt |
| remainder | the hash of (password + salt) |

The salt is **embedded in this single string** — no separate `salt` column is needed in your table. One `password_hash` column, one string, everything required to verify it later.

## Naming convention worth following
Name the column `password_hash`, not `password`. The column never holds a plaintext password; naming it accordingly makes that unambiguous to anyone reading the schema or code later, reducing the chance of it being mistakenly logged, displayed, or handled as if it were retrievable plaintext.

## Related notes
- **Flask** — where `generate_password_hash`/`check_password_hash` are called, inside route functions
- **JWT** — the next step after a password check succeeds: issuing a token
- **Authentication API** — this pattern applied in a working register/login flow
