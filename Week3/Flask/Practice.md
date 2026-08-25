# Flask Practice and Command Reference

This file records the commands and syntax practiced.

## 1. Check Python

```
which python3
python3 --version
python3 -m pip --version
```

## 2. Create a Virtual Environment

```
python3 -m venv .venv
```

This creates an isolated Python environment called `.venv`.

## 3. Activate the Environment

```
source .venv/bin/activate
```

The terminal show:

```
(.venv)
```

## 4. Install Flask

```
pip install flask
```

## 5. Check Flask

```
pip show flask
```

## 6. Run the Application

```
python app.py
```

The Flask server normally becomes available at:

```
http://127.0.0.1:5000
```

---

# Flask Syntax Practice

## Import

```
from flask import Flask, jsonify, request
```

## Create Application

```
app = Flask(__name__)
```

## GET Route

```python
@app.route("/employees", methods=["GET"])
def get_employees():
    return jsonify(employees)
```

## POST Route

```
@app.route("/employees", methods=["POST"])
def add_employee():
    data = request.json
```

## Read JSON

```
name = data.get("name")
department = data.get("department")
```

## Validate

```
if not name or not department:
    return jsonify({
        "error": "Name and department are required"
    }), 400
```

## Create Dictionary

```
employee = {
    "id": next_id,
    "name": name,
    "department": department
}
```

## Add to List

```
employees.append(employee)
```

## Return JSON

```
return jsonify(employee), 201
```

## Route Parameter

```
@app.route("/employees/<int:id>", methods=["DELETE"])
def delete_employee(id):
```

## Loop

```
for employee in employees:
```

## Compare IDs

```
if employee["id"] == id:
```

## Remove

```
employees.remove(employee)
```

## Run Flask

```
if __name__ == "__main__":
    app.run()
```

---

# curl Practice

## GET

```
curl http://127.0.0.1:5000/employees
```

## POST

```
curl -X POST http://127.0.0.1:5000/employees \
-H "Content-Type: application/json" \
-d '{"name":"Emma","department":"Finance"}'
```

## Invalid POST

```
curl -X POST http://127.0.0.1:5000/employees \
-H "Content-Type: application/json" \
-d '{"name":"Emma"}'
```

Expected result:

```
400 Bad Request
```

## DELETE

```
curl -X DELETE http://127.0.0.1:5000/employees/2
```

## Delete Missing Employee

```
curl -X DELETE http://127.0.0.1:5000/employees/99
```

Expected result:

```
404 Not Found
```

