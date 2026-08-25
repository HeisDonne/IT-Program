# Employee Directory API

## 1. Project Overview

The Employee Directory API is the Week 3 backend mini project.

It was built using Python and Flask.

The project demonstrates how a backend receives HTTP requests, processes data, and returns JSON responses.

The API supports:

- Retrieving employees
- Adding employees
- Deleting employees

---

# 2. Week 3 Requirement

The required endpoints are:

```text
GET /employees
POST /employees
DELETE /employees/<id>
```

Employee information is stored in memory.

A database is not used because database integration is part of Week 4.

---

# 3. Project Architecture

The basic architecture is:

```text
Client
  |
  | HTTP request
  v
Flask API
  |
  | Python logic
  v
In-memory employees list
  |
  | JSON response
  v
Client
```

The client can be `curl`, a browser, Postman, or another application.

---

# 4. Data Structure

Employees are stored in a Python list:

```python
employees = [
    {
        "id": 1,
        "name": "John",
        "department": "IT"
    },
    {
        "id": 2,
        "name": "Sarah",
        "department": "HR"
    }
]
```

The list contains dictionaries.

Each dictionary represents one employee.

---

# 5. GET /employees

The GET endpoint retrieves all employees.

```python
@app.route("/employees", methods=["GET"])
def get_employees():
    return jsonify(employees)
```

### Flow

```text
GET /employees
      ↓
get_employees()
      ↓
employees list
      ↓
jsonify()
      ↓
JSON response
```

Test:

```bash
curl http://127.0.0.1:5000/employees
```

---

# 6. POST /employees

The POST endpoint creates a new employee.

The client sends:

```json
{
    "name": "David",
    "department": "Finance"
}
```

The server receives:

```python
data = request.json
```

Then:

```python
name = data.get("name")
department = data.get("department")
```

The API validates the data:

```python
if not name or not department:
    return jsonify({
        "error": "Name and department are required"
    }), 400
```

Then creates the employee:

```python
employee = {
    "id": next_id,
    "name": name,
    "department": department
}
```

The employee is stored:

```python
employees.append(employee)
```

The ID is incremented:

```python
next_id += 1
```

The API responds:

```python
return jsonify(employee), 201
```

Test:

```bash
curl -X POST http://127.0.0.1:5000/employees \
-H "Content-Type: application/json" \
-d '{"name":"David","department":"Finance"}'
```

---

# 7. DELETE /employees/<id>

The DELETE endpoint removes an employee.

Example:

```text
DELETE /employees/2
```

The route:

```python
@app.route("/employees/<int:id>", methods=["DELETE"])
def delete_employee(id):
```

The `<int:id>` part tells Flask to capture the value from the URL and convert it to an integer.

The function searches through the list:

```python
for employee in employees:
    if employee["id"] == id:
```

If a match is found:

```python
employees.remove(employee)
```

Then:

```python
return jsonify({
    "message": "Employee deleted"
}), 200
```

If no match is found:

```python
return jsonify({
    "message": "Employee not found"
}), 404
```

Test:

```bash
curl -X DELETE http://127.0.0.1:5000/employees/2
```

---

# 8. Automatic IDs

The application uses:

```python
next_id = 3
```

When adding an employee:

```python
"id": next_id
```

After adding:

```python
next_id += 1
```

This prevents the application from always creating employee ID `3`.

For example:

```text
John    → 1
Sarah   → 2
David   → 3
Michael → 4
```

---

# 9. Why `global` Is Used

`next_id` is defined outside the function:

```python
next_id = 3
```

The POST function modifies it:

```python
global next_id
```

Without `global`, Python would treat an assignment to `next_id` inside the function as a local variable.

---

# 10. Validation

The API checks that both required fields exist:

```python
name = data.get("name")
department = data.get("department")

if not name or not department:
    return jsonify({
        "error": "Name and department are required"
    }), 400
```

This prevents incomplete employee records.

For example:

```json
{
    "name": "David"
}
```

is rejected because `department` is missing.

---

# 11. Testing

### Get employees

```bash
curl http://127.0.0.1:5000/employees
```

### Add employee

```bash
curl -X POST http://127.0.0.1:5000/employees \
-H "Content-Type: application/json" \
-d '{"name":"David","department":"Finance"}'
```

### Delete employee

```bash
curl -X DELETE http://127.0.0.1:5000/employees/2
```

### Test validation

```bash
curl -X POST http://127.0.0.1:5000/employees \
-H "Content-Type: application/json" \
-d '{"name":"David"}'
```

### Test missing employee

```bash
curl -X DELETE http://127.0.0.1:5000/employees/99
```

---

# 12. Important Limitation

The employee data is stored only in memory.

This means:

```text
Start application
      ↓
Employees exist
      ↓
Add/delete employees
      ↓
Stop application
      ↓
Memory is cleared
```

When the application starts again, it returns to the employees defined in the Python source code.

This limitation is intentional for Week 3.

Week 4 will introduce PostgreSQL so the API can store data persistently.

---

# 13. What This Project Demonstrates

This project demonstrates the complete basic backend cycle:

```text
Client
  ↓
HTTP request
  ↓
Flask route
  ↓
Python function
  ↓
Read/process data
  ↓
Validate data
  ↓
Modify in-memory data
  ↓
JSON response
  ↓
HTTP status code
  ↓
Client
```

