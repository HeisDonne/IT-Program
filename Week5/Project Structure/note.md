# Project Structure

## Placeholders used
`<feature>` stands for a real domain area of your app (e.g. `auth`, `orders`). Folder/file names shown (`app/`, `routes/`, `models.py`, `extensions.py`, `config.py`, `run.py`) are the actual conventional names used — not placeholders — since project layout names are a convention worth following as-is, not something you invent per project.

## Definition
Project structure is how a codebase's files and folders are organized to separate distinct responsibilities, so the codebase stays navigable and testable as it grows beyond a single file. A small Flask app can live entirely in one file; once it has multiple resources, authentication, and real business logic, a single file becomes hard to read, hard to test in isolation, and prone to merge conflicts if more than one person works on it.

## The five responsibilities being separated
| Responsibility | Contains | Typical file |
|---|---|---|
| Talking to the database | Connection/session objects | `extensions.py` |
| Defining what data *is* | Table/column definitions (models) | `models.py` |
| Deciding what happens per URL | Route functions | `routes/<feature>.py` |
| App-wide settings | DB URL, secret keys, environment values | `config.py` |
| Wiring everything together and starting the server | App creation, extension init, blueprint registration | `__init__.py`, `run.py` |

## A standard layout

```
project-name/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── extensions.py
│   ├── models.py
│   └── routes/
│       ├── __init__.py
│       └── <feature>.py
├── run.py
└── requirements.txt
```
- `app/routes/__init__.py` — must exist (can be empty). Its presence is what makes Python treat `routes/` as an importable package rather than an ordinary folder; without it, `from app.routes.<feature> import <feature>_bp` fails with `ModuleNotFoundError`.

## The app factory pattern

```python
# app/__init__.py
from flask import Flask
from app.config import Config
from app.extensions import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    from app.routes.<feature> import <feature>_bp
    app.register_blueprint(<feature>_bp)

    return app
```
- The Flask app is built inside a function (`create_app()`) rather than as a bare `app = Flask(__name__)` at module level. This allows building a fresh, independently configured app instance on demand — useful for running automated tests against a separate test database, or supporting multiple environments (dev/staging/prod) without duplicating files.
- `app.config.from_object(Config)` — loads every uppercase attribute from the `Config` class into `app.config`.
- The `from app.routes.<feature> import <feature>_bp` line sits **inside** the function, not at the top of the file. Route files typically need to `from app.extensions import db` — importing the route module at the top of `__init__.py`, before the app/extensions are fully set up, risks circular import errors. Importing it right before use, inside the function, avoids this.

## Extensions created without an app attached

```python
# app/extensions.py
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
```
- `SQLAlchemy()` is called with no `app` argument here — deliberately. If it required `app` at creation time, every file needing `db` would need `app` to already exist, and `app` (built in `__init__.py`) would need the route files (which need `db`) to already be importable — a circular dependency.
- The two-step pattern — create empty here, attach later via `db.init_app(app)` in `create_app()` — breaks that cycle. Every other file just imports the same shared `db` object via `from app.extensions import db`, fully wired by the time any route runs.

## Blueprints — routes defined outside the main app object

```python
# app/routes/<feature>.py
from flask import Blueprint
<feature>_bp = Blueprint("<feature>", __name__)

@<feature>_bp.route("/path", methods=["GET"])
def handler():
    ...
```
- `Blueprint("<feature>", __name__)` — creates a self-contained collection of routes not yet attached to any real Flask app. The first argument is the blueprint's internal name (shows up in Flask's error messages/URL naming); `__name__` locates the file, same as `Flask(__name__)`.
- These routes only become reachable once `app.register_blueprint(<feature>_bp)` runs inside `create_app()` — that's the moment they're merged into the app's actual `url_map`.
- Splitting routes into blueprints per feature (`auth.py`, `orders.py`, etc.) is what lets a growing app scale past one file without one giant `routes.py`.

## Scaffolding the structure

```bash
mkdir -p app/routes
touch app/__init__.py app/config.py app/extensions.py app/models.py
touch app/routes/__init__.py app/routes/<feature>.py
touch run.py requirements.txt
```
- `mkdir -p app/routes` — creates both `app/` and the nested `app/routes/` in one command; `-p` also suppresses an error if the parent already exists.
- `touch` — creates each file empty (or updates its timestamp if it already exists); content is added afterward.

## Environment and dependencies

```bash
python3 -m venv venv
source venv/bin/activate
pip install flask flask-sqlalchemy
pip freeze > requirements.txt
```
- `python3 -m venv venv` — creates an isolated Python environment in a folder named `venv`, so packages installed for this project don't affect the system Python or other projects.
- `source venv/bin/activate` — activates it for the current terminal session; the prompt typically shows `(venv)` once active.
- `pip freeze > requirements.txt` — writes every installed package and its exact version to a file, so the environment can be recreated elsewhere with `pip install -r requirements.txt`.

## Entry point

```python
# run.py
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
```
- The only file actually executed directly (`python run.py`). Everything else is imported by it, directly or indirectly.
