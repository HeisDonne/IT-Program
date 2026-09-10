# Flask

## Definition
Flask is a lightweight Python web framework — a library that handles the plumbing of receiving HTTP requests, routing them to Python functions, and turning what those functions return into HTTP responses. It's called a "microframework" because it intentionally ships with a small core (routing, request/response handling) and leaves things like database access, authentication, and validation to separate libraries you choose and add yourself — as opposed to a framework like Django, which bundles most of that by default.

## How a Flask app processes a request
Two distinct phases, that happen at different times:

**Phase 1 — registration, at import time.** When your Python file runs, every `@app.route(...)`-decorated function is added to an internal lookup table (`url_map`) mapping URL patterns + HTTP methods to functions. No request has happened yet — this is just Flask learning what functions exist and which paths they answer to.

**Phase 2 — dispatch, per request.** When an actual HTTP request arrives (from `curl`, Postman, a browser, another server), Flask matches its path and method against `url_map`, finds the registered function, calls it, and wraps whatever it returns into a proper HTTP response.

## Creating an app and a route

```python
from flask import Flask
app = Flask(__name__)

@app.route("/resource", methods=["GET"])
def get_resource():
    return {"message": "ok"}
```
- `Flask(__name__)` — creates the application object. `__name__` tells Flask where this file lives on disk, used internally for locating resources like templates.
- `@app.route("/resource", methods=["GET"])` — registers `get_resource` to handle `GET` requests to `/resource`. `methods` defaults to `["GET"]` if omitted.
- Returning a plain `dict` from a route function is automatically converted into a JSON response by Flask — no need to call `jsonify()` manually in this case, though `jsonify()` is used when you need more control (custom status codes, headers).

## Reading the incoming request

```python
from flask import request

@app.route("/resource", methods=["POST"])
def create_resource():
    data = request.get_json(silent=True)
    query_param = request.args.get("filter")
    header_value = request.headers.get("Authorization")
```
- `request.get_json(silent=True)` — parses the request body as JSON; `silent=True` returns `None` on missing/invalid JSON instead of raising an exception.
- `request.args.get("filter")` — reads a URL query parameter, e.g. `?filter=active`.
- `request.headers.get("Authorization")` — reads a specific HTTP header.

## Returning a response with a status code

```python
from flask import jsonify

@app.route("/resource", methods=["POST"])
def create_resource():
    return jsonify({"error": "invalid input"}), 400
```
- `jsonify(...)` — converts a Python dict into a proper JSON HTTP response, setting the `Content-Type: application/json` header.
- `, 400` — the second element of the returned tuple sets the HTTP status code; Flask defaults to `200` if omitted.

## Dynamic URL segments

```python
@app.route("/resource/<int:id>", methods=["GET"])
def get_one(id):
    ...
```
- `<int:id>` — captures a segment of the URL as a variable named `id`, converted to `int` automatically. Other converters include `<string:...>` (default if unspecified) and `<float:...>`. The captured value is passed as an argument to the function, matched by name.

## Running the app

```bash
pip install flask
```
```python
if __name__ == "__main__":
    app.run(debug=True)
```
- `app.run(debug=True)` — starts Flask's built-in development server. `debug=True` enables the auto-reloader (restarts on file changes) and detailed in-browser error pages. **Not for production** — it's single-threaded by default and can expose internal details through its error pages; production deployments use a WSGI server like Gunicorn instead.

## Related notes
- **Project Structure** — organizing routes/models/config across multiple files as an app grows
- **Password Hashing**, **JWT** — the two pieces that make an authentication system work
- **Authentication API** — all of the above applied to a real, working API
