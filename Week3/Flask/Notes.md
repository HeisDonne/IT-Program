# Flask — Detailed Documentation

## 1. What Is Flask?

Flask is a lightweight web framework for Python.

A framework provides tools and structures that make it easier to build applications.

Flask can be used to build:

- Web applications
- REST APIs
- Backend services
- Small web services
- Prototypes

In Week 3, Flask is used to build the Employee Directory API.

---

# 2. Installing Flask

First create a virtual environment:

```
python3 -m venv .venv
```

Activate it:

```
source .venv/bin/activate
```

Install Flask:

```
pip install flask
```

Check that Flask is installed:

```
pip show flask
```

---

# 3. Importing Flask

A basic Flask program begins with:

```
from flask import Flask, jsonify, request
```

The imported objects have different purposes.

### `Flask`

Creates the Flask application.

### `jsonify`

Creates JSON responses.

### `request`

Provides access to information sent by the client.

---

# 4. Creating the Application

```
app = Flask(__name__)
```

`Flask(...)` creates the application.

`__name__` tells Flask where the application is located.

The result is stored in the variable:

```
app
```

We use this object to define routes and run the application.

---

# 5. Routes

A route connects a URL to a Python function.

Example:

```python
@app.route("/employees", methods=["GET"])
def get_employees():
    return jsonify(employees)
```

There are two important parts.

The decorator:

```python
@app.route(...)
```

tells Flask which URL and HTTP method should trigger the function.

The function:

```python
def get_employees():
```

contains the code that handles the request.

---

# 6. Understanding the Decorator

Consider:

```python
@app.route("/employees", methods=["GET"])
```

### `@`

The `@` syntax is used for a Python decorator.

### `app.route`

The Flask application's route function.

### `"/employees"`

The URL path.

### `methods=["GET"]`

Specifies which HTTP method is accepted.

The complete meaning is:

> When a GET request arrives at `/employees`, run the function immediately below this decorator.

---

# 7. GET Endpoint

Our GET endpoint is:

```python
@app.route("/employees", methods=["GET"])
def get_employees():
    return jsonify(employees)
```

The flow is:

```
GET /employees
      ↓
Flask finds matching route
      ↓
get_employees()
      ↓
jsonify(employees)
      ↓
JSON response
```

---

# 8. `request`

The Flask `request` object represents the incoming HTTP request.

For example:

```python
data = request.json
```

This reads the JSON body sent by the client.

If the client sends:

```json
{
    "name": "Emm",
    "department": "Finance"
}
```

then `data` becomes a Python dictionary-like object containing those values.

---

# 9. POST Endpoint

Our POST endpoint:

```python
@app.route("/employees", methods=["POST"])
def add_employee():
```

The purpose is to create a new employee.

We receive the JSON:

```python
data = request.json
```

Then retrieve values:

```python
name = data.get("name")
department = data.get("department")
```

Then validate:

```python
if not name or not department:
    return jsonify({
        "error": "Name and department are required"
    }), 400
```

Then create the employee:

```python
employee = {
    "id": next_id,
    "name": name,
    "department": department
}
```

Then store it:

```python
employees.append(employee)
```

Then increment the ID:

```python
next_id += 1
```

Finally:

```python
return jsonify(employee), 201
```

---

# 10. Why Validation Is Important

An API should not assume that clients always send correct information.

For example:

```
{
    "name": "Emma"
}
```

is missing the department.

Instead of allowing the program to crash, we validate:

```python
if not name or not department:
```

Then return:

```python
return jsonify({
    "error": "Name and department are required"
}), 400
```

This gives the client a useful response.

---

# 11. DELETE Endpoint

Our DELETE route:

```python
@app.route("/employees/<int:id>", methods=["DELETE"])
def delete_employee(id):
```

This contains a route parameter:

```
<int:id>
```

It means:

> Take the value from this part of the URL and convert it to an integer, then pass it to the function as `id`.

For:

```text
/employees/2
```

Flask calls:

```python
delete_employee(2)
```

---

# 12. Finding the Employee

The function loops through the employees:

```python
for employee in employees:
```

Then checks the ID:

```python
if employee["id"] == id:
```

If it matches:

```python
employees.remove(employee)
```

removes that employee.

Then:

```python
return jsonify({
    "message": "Employee deleted"
}), 200
```

sends a successful response.

---

# 13. Employee Not Found

If the loop finishes without finding the employee:

```python
return jsonify({
    "message": "Employee not found"
}), 404
```

This tells the client that the requested employee does not exist.

---

# 14. `jsonify()`

`jsonify()` creates a JSON response.

Example:

```python
return jsonify(employee)
```

For a message:

```python
return jsonify({
    "message": "Employee deleted"
})
```

A status code can also be returned:

```python
return jsonify(employee), 201
```

This means:

```text
JSON response + HTTP status code 201
```

---

# 15. `app.run()`

The Flask development server is started with:

```python
if __name__ == "__main__":
    app.run()
```

The condition checks whether the Python file is being executed directly.

If it is, Flask starts its development server.

The server normally listens at:

```text
http://127.0.0.1:5000
```

---


# 16. Understanding a Flask Error

A Flask request can produce:

```text
500 Internal Server Error
```

This usually means the request reached Flask but an unexpected error occurred while executing Python code.

For example:

```text
NameError: name 'jsonify' is not defined
```

means Python does not know what `jsonify` is.

The fix is to import it:

```python
from flask import Flask, jsonify, request
```

---

# 17. Understanding a 404

A 404 can mean the requested route does not exist.

For example:

```text
DELETE /employees/2
```

will not work unless the application has a matching DELETE route.

It can also mean the application deliberately returned:

```python
return jsonify({
    "message": "Employee not found"
}), 404
```

The first case is a routing problem.

The second case is an application-level "resource not found" response.

---

# 18. Complete Flask Structure

A simplified Flask API follows this pattern:

```python
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route("/something", methods=["GET"])
def something():
    return jsonify(data)

if __name__ == "__main__":
    app.run()
```

