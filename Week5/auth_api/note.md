# Authentication API — Build Process

## Setup
- Flask + `flask-sqlalchemy` (ORM) + `flask-bcrypt` + `flask-jwt-extended`
- Database: PostgreSQL, on the same remote VM used for the Employee API, reached through an SSH tunnel
- Features: Register, Login, a JWT-protected route, Logout (token revocation)

## Process overview
1. Scaffold the project structure (app factory + blueprint pattern)
2. Set up a virtual environment and install dependencies
3. Reuse the existing SSH tunnel to the VM's Postgres; create a new database and role
4. Define the `User` model
5. Wire up the app factory and entry point
6. Build the routes: register, login, protected route, logout
7. Debug real issues hit during setup (documented below, in the order encountered)
8. Test end-to-end with curl and a Postman collection

## 1–2. Scaffold and environment

```bash
mkdir -p auth_api/app/routes
cd auth_api
touch app/__init__.py app/config.py app/extensions.py app/models.py
touch app/routes/__init__.py app/routes/auth.py
touch run.py requirements.txt

python3 -m venv venv
source venv/bin/activate
pip install flask flask-sqlalchemy flask-bcrypt flask-jwt-extended psycopg2-binary
pip freeze > requirements.txt
```

## 3. Database — reusing the existing tunnel

The SSH tunnel from the Employee API project already forwards to the VM's Postgres server, so it didn't need to be recreated — only a new database and role, scoped to this project:

```bash
ssh -L 5433:localhost:5432 vm_user@vm_ip -N
```
Then, connected to the VM directly (not through the tunnel) as the Postgres superuser:
```bash
sudo -u postgres psql
```
```sql
CREATE DATABASE auth_api_db;
CREATE USER auth_api WITH PASSWORD 'yourpassword';
GRANT ALL PRIVILEGES ON DATABASE auth_api_db TO auth_api;
```

## 4. The model — `app/models.py`

```python
from app.extensions import db

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
```
`password_hash`, not `password` — the column holds a bcrypt hash, never plaintext, and the name makes that unambiguous.

## 5. Extensions and app factory

```python
# app/extensions.py
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()


```

```python
# app/config.py
import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", "postgresql://auth_api:yourpassword@127.0.0.1:5433/auth_api_db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "dev-jwt-secret")
```

```python
# app/__init__.py
from flask import Flask
from app.config import Config
from app.extensions import db, bcrypt, jwt

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp)

    return app
```

```python
# run.py
from app import create_app
from app.extensions import db

app = create_app()

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
```
`db.create_all()` runs `CREATE TABLE` for any model that doesn't yet have a matching table — the ORM equivalent of writing `CREATE TABLE users (...)` by hand. `app.app_context()` is required because `db.create_all()` needs access to `app.config`'s database URL, which isn't automatically available outside of a request or an explicit context.

## 6. Routes — `app/routes/auth.py`

```python
from flask import Blueprint, request, jsonify
from app.extensions import db, bcrypt, BLOCKLIST
from app.models import User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Request body must be valid JSON"}), 400

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not name or not email or not password:
        return jsonify({"error": "name, email, and password are required"}), 400

    if len(password) < 8:
        return jsonify({"error": "Password must be at least 8 characters"}), 400

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"error": "Email already registered"}), 409

    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
    new_user = User(name=name, email=email, password_hash=hashed_password)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"id": new_user.id, "name": new_user.name, "email": new_user.email}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Request body must be valid JSON"}), 400

    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()

    if not user or not bcrypt.check_password_hash(user.password_hash, password):
        return jsonify({"error": "Invalid email or password"}), 401

    access_token = create_access_token(identity=str(user.id))
    return jsonify({"access_token": access_token}), 200


@auth_bp.route("/profile", methods=["GET"])
@jwt_required()
def profile():
    user_id = get_jwt_identity()
    user = User.query.get(int(user_id))

    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({"id": user.id, "name": user.name, "email": user.email}), 200


@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    BLOCKLIST.add(jti)
    return jsonify({"message": "Successfully logged out"}), 200
```

## 7. Issues actually hit while building this, and their fixes

**`ModuleNotFoundError: No module named 'app.routes'`**
Cause: `app/routes/__init__.py` didn't exist on disk (the `mkdir -p`/`touch` sequence hadn't fully run for that folder). Python won't treat a plain folder as an importable package without it.
Fix: `mkdir -p app/routes && touch app/routes/__init__.py`, then recreate `auth.py`'s content.

**`psycopg2.errors.InsufficientPrivilege: permission denied for schema public`**
Cause: since Postgres 15, `GRANT ALL PRIVILEGES ON DATABASE ... TO role` no longer implicitly grants `CREATE` on that database's `public` schema — database-level and schema-level grants are separate. `db.create_all()` needs `CREATE` on the schema specifically.
Fix (connected as the Postgres superuser, on the target database): `ALTER SCHEMA public OWNER TO auth_api;` — makes the app's role the schema owner outright, avoiding partial-grant ambiguity. (Plain `GRANT ALL ON SCHEMA public TO auth_api;` was tried first and silently granted nothing — worth knowing this can happen rather than assuming the grant succeeded.)
Note: this is scoped per-database — altering `auth_api_db`'s `public` schema owner has no effect on any other database's `public` schema (e.g. `employee_db`), even though they share the same schema name.

**`must be owner of schema public`, when trying to run the `ALTER SCHEMA` above**
Cause: the `psql` session was still connected as the app's own role (`auth_api`), not the superuser — `\c postgres` switches *database*, not role.
Fix: connect directly on the VM (not through the SSH tunnel, since the superuser role commonly only allows peer/local authentication, not password auth over TCP): `sudo -u postgres psql -d auth_api_db`.

**`TypeError: 'password' is an invalid keyword argument for User`**
Cause: `User(..., password=hashed_password)` used a keyword that didn't match any column on the model — the actual column is `password_hash`. SQLAlchemy rejects unrecognized keyword arguments outright rather than ignoring them.
Fix: match the keyword to the real column name — `User(..., password_hash=hashed_password)`.

**`{"msg": "Subject must be a string"}`**
Cause: `create_access_token(identity=user.id)` passed a raw integer; current `flask-jwt-extended` requires the identity/subject claim to be a string.
Fix: `create_access_token(identity=str(user.id))`, and cast back on read: `User.query.get(int(get_jwt_identity()))`.

**Fix didn't seem to take effect on the next request**
Cause: a JWT is a fixed signed string once issued — restarting/fixing the server code does nothing to tokens issued *before* the fix. The old token still carried the broken (integer) identity.
Fix: log in again after any change to token creation logic, to get a freshly issued token, and use that for testing — not a token obtained before the fix.

**`InsecureKeyLengthWarning: The HMAC key is 14 bytes long...`**
Cause: the dev `JWT_SECRET_KEY` (`"dev-jwt-secret"`) is below the 32-byte minimum recommended for the default signing algorithm. Non-blocking for local development, but should be addressed before any real deployment.
Fix (for real use): `python3 -c "import secrets; print(secrets.token_hex(32))"` — generate a proper random key and load it via an environment variable, not hardcoded in `config.py`.

## 8. Testing

```bash
curl -X POST http://127.0.0.1:5000/register \
  -H "Content-Type: application/json" \
  -d '{"name": "Dev", "email": "dev@example.com", "password": "testpass123"}'

curl -X POST http://127.0.0.1:5000/login \
  -H "Content-Type: application/json" \
  -d '{"email": "dev@example.com", "password": "testpass123"}'

curl http://127.0.0.1:5000/profile \
  -H "Authorization: Bearer <token from login>"

curl -X POST http://127.0.0.1:5000/logout \
  -H "Authorization: Bearer <token>"

curl http://127.0.0.1:5000/profile \
  -H "Authorization: Bearer <same token — should now fail>"
```

A full Postman collection (`Authentication-API.postman_collection.json`) covering these plus the failure cases — missing fields, weak password, duplicate email, wrong password, missing/invalid token — accompanies this documentation, with automated pass/fail assertions on status codes.

## Command reference

| Task | Command |
|---|---|
| Scaffold folders | `mkdir -p app/routes` |
| Create virtual environment | `python3 -m venv venv` |
| Activate it | `source venv/bin/activate` |
| Install dependencies | `pip install flask flask-sqlalchemy flask-bcrypt flask-jwt-extended psycopg2-binary` |
| Freeze dependencies | `pip freeze > requirements.txt` |
| Open SSH tunnel to VM's Postgres | `ssh -L 5433:localhost:5432 vm_user@vm_ip -N` |
| Connect as Postgres superuser (on the VM) | `sudo -u postgres psql -d auth_api_db` |
| Connect through the tunnel (from local) | `psql -h 127.0.0.1 -p 5433 -U auth_api -d auth_api_db` |
| Check running processes on a port | `lsof -i :5000` |
| Run the app | `python run.py` |
| Generate a secure secret key | `python3 -c "import secrets; print(secrets.token_hex(32))"` |
