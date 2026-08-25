# APIs and HTTP

## 1. What Is an API?

API stands for Application Programming Interface.

An API provides a defined way for one program to communicate with another program.

For example:

```text
Client → API → Server
```

The client sends a request.

The server processes the request.

The server sends a response.

---

# 2. Client and Server

In our Employee Directory project:

```text
curl
  ↓
Flask API
  ↓
Python code
  ↓
Employee data
```

`curl` acts as the client.

Flask acts as the backend server.

Python code processes the request.

---

# 3. What Is an Endpoint?

An endpoint is a specific URL provided by an API.

Our API has:

```text
GET     /employees
POST    /employees
DELETE  /employees/<id>
```

The HTTP method and URL together describe what operation the client wants.

---

# 4. HTTP Methods

HTTP methods tell the server what type of operation the client wants.

## GET

GET is normally used to retrieve information.

Example:

```http
GET /employees
```

Our endpoint:

```python
@app.route("/employees", methods=["GET"])
def get_employees():
    return jsonify(employees)
```

---

# 5. POST

POST is normally used to send data to the server and create a new resource.

Example:

```http
POST /employees
```

The request body contains JSON:

```json
{
    "name": "David",
    "department": "Finance"
}
```

The server receives the data and creates an employee.

---

# 6. DELETE

DELETE is used to remove a resource.

Example:

```http
DELETE /employees/2
```

The `2` identifies the employee to remove.

---

# 7. HTTP Request

A request can contain:

- Method
- URL
- Headers
- Body

Example:

```text
POST /employees
```

Header:

```text
Content-Type: application/json
```

Body:

```json
{
    "name": "David",
    "department": "Finance"
}
```

---

# 8. HTTP Response

A response commonly contains:

- Status code
- Headers
- Body

Example:

```text
201 Created
```

Body:

```json
{
    "id": 3,
    "name": "David",
    "department": "Finance"
}
```

---

# 9. HTTP Status Codes

## 200 — OK

The request succeeded.

We use it when an employee is successfully deleted.

## 201 — Created

A new resource was successfully created.

We use it when a new employee is added.

## 400 — Bad Request

The client sent invalid or incomplete information.

Our API returns this if required employee information is missing.

## 404 — Not Found

The requested resource does not exist.

Our DELETE endpoint returns this when the requested employee ID cannot be found.

## 500 — Internal Server Error

Something unexpected went wrong on the server.

A Python exception can cause a 500 response.

---

# 10. curl

`curl` is a command-line tool used to make network requests.

It is useful for testing APIs without needing a graphical API client.

GET:

```bash
curl http://127.0.0.1:5000/employees
```

POST:

```bash
curl -X POST http://127.0.0.1:5000/employees \
-H "Content-Type: application/json" \
-d '{"name":"David","department":"Finance"}'
```

DELETE:

```bash
curl -X DELETE http://127.0.0.1:5000/employees/2
```

---

# 11. Breaking Down the POST curl Command

```bash
curl -X POST http://127.0.0.1:5000/employees \
-H "Content-Type: application/json" \
-d '{"name":"David","department":"Finance"}'
```

### `curl`

Runs the curl program.

### `-X POST`

Specifies that the HTTP method is POST.

### URL

```text
http://127.0.0.1:5000/employees
```

This identifies the server and endpoint.

### `-H`

Adds an HTTP header.

```text
Content-Type: application/json
```

This tells the server that the request body contains JSON.

### `-d`

Provides data for the request body.

```json
{
    "name": "David",
    "department": "Finance"
}
```

---

# 12. API Request Flow

For our POST request:

```text
curl
  ↓
HTTP POST
  ↓
/employees
  ↓
Flask route
  ↓
request.json
  ↓
Validate data
  ↓
Create employee
  ↓
Store employee
  ↓
jsonify(employee)
  ↓
HTTP 201 response
  ↓
curl displays response
```

---

# 13. REST

REST is a common architectural style for designing web APIs.

Our project follows a simple REST-style structure:

```text
GET     /employees
POST    /employees
DELETE  /employees/<id>
```

The URL identifies the resource and the HTTP method describes the operation.

