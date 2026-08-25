# JSON — JavaScript Object Notation

## 1. What Is JSON?

JSON stands for JavaScript Object Notation.

It is a lightweight text format used to represent and exchange structured data.

APIs commonly use JSON because different programming languages can easily work with it.

For example, a server can send:

```json
{
    "name": "John",
    "department": "IT"
}
```

A Python application, JavaScript application, mobile application, or another system can read this data.

---

# 2. JSON Objects

A JSON object contains key-value pairs.

```json
{
    "name": "John",
    "department": "IT"
}
```

Here:

```text
name → John
department → IT
```

The keys are strings and are written in double quotes.

---

# 3. JSON Arrays

A JSON array contains multiple values.

```json
[
    "John",
    "Sarah",
    "David"
]
```

An array can also contain objects:

```json
[
    {
        "name": "John",
        "department": "IT"
    },
    {
        "name": "Sarah",
        "department": "HR"
    }
]
```

This structure is similar to a Python list containing dictionaries.

---

# 4. JSON Data Types

JSON supports:

- String
- Number
- Boolean
- Object
- Array
- `null`

Example:

```json
{
    "name": "John",
    "age": 25,
    "active": true,
    "department": null
}
```

---

# 5. JSON and Python

Python dictionaries are commonly used to represent JSON objects.

Python:

```python
employee = {
    "name": "John",
    "department": "IT"
}
```

JSON:

```json
{
    "name": "John",
    "department": "IT"
}
```

Python lists can represent JSON arrays.

Python:

```python
employees = [
    {"name": "John"},
    {"name": "Sarah"}
]
```

---

# 6. Receiving JSON in Flask

When a client sends JSON to Flask, the JSON body can be accessed through:

```python
data = request.json
```

For example, a client might send:

```json
{
    "name": "David",
    "department": "Finance"
}
```

Flask can receive it:

```python
data = request.json
```

Then the values can be retrieved:

```python
name = data.get("name")
department = data.get("department")
```

---

# 7. Why Use `.get()`?

This:

```python
data["name"]
```

expects the key to exist.

If `"name"` is missing, Python can raise an error.

This:

```python
data.get("name")
```

returns the value if it exists, and `None` if it does not.

This is useful when validating data supplied by an API client.

---

# 8. Returning JSON from Flask

Flask provides `jsonify()` for creating JSON responses.

```python
return jsonify(employee)
```

For a list:

```python
return jsonify(employees)
```

For a message:

```python
return jsonify({
    "message": "Employee deleted"
})
```

---

# 9. JSON in the Employee Directory API

The POST endpoint receives JSON:

```json
{
    "name": "David",
    "department": "Finance"
}
```

The Flask application reads it:

```python
data = request.json
```

Then:

```python
name = data.get("name")
department = data.get("department")
```

The application creates a Python dictionary:

```python
employee = {
    "id": next_id,
    "name": name,
    "department": department
}
```

Finally, Flask returns JSON:

```python
return jsonify(employee), 201
```

The overall flow is:

```text
Client
  ↓
JSON request
  ↓
Flask
  ↓
request.json
  ↓
Python dictionary
  ↓
Application processing
  ↓
jsonify()
  ↓
JSON response
  ↓
Client
```

---

# 10. Common JSON Mistakes

JSON uses double quotes:

```json
{
    "name": "John"
}
```

Do not use Python-style single quotes in standard JSON:

```text
{'name': 'John'}
```

Also make sure commas and braces are correctly placed.

