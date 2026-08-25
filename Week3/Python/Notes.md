# Python Fundamentals

## 1. What Is Python?

Python is a high-level programming language known for readable syntax and a large ecosystem of libraries.

Python can be used for:

- Backend development
- Automation
- Data analysis
- Artificial intelligence
- Scripting
- Networking
- Cybersecurity
- Desktop applications

In Week 3, Python is being used to build a backend API.

---

# 2. Variables

A variable is a name that refers to a value.

```python
name = "Donel"
age = 18
department = "IT"
```

Here:

- `name` stores a string.
- `age` stores an integer.
- `department` stores another string.

Python does not require us to declare the data type before creating a variable.

## Changing a variable

```python
age = 18
age = 19
```

The value stored in `age` changes from `18` to `19`.

---

# 3. Data Types

Common Python data types include:

### String

Used for text.

```python
name = "Donel"
```

Type:

```text
str
```

### Integer

Used for whole numbers.

```python
age = 18
```

Type:

```text
int
```

### Float

Used for decimal numbers.

```python
height = 1.75
```

Type:

```text
float
```

### Boolean

Represents `True` or `False`.

```python
is_student = True
```

Type:

```text
bool
```

### List

Stores multiple values.

```python
employees = ["John", "Sarah", "David"]
```

### Dictionary

Stores information as key-value pairs.

```python
employee = {
    "name": "John",
    "department": "IT"
}
```

---

# 4. Lists

A list is an ordered collection of values.

```python
employees = ["John", "Sarah", "David"]
```

## Indexing

Python lists start counting from `0`.

```python
employees[0]
```

returns:

```text
John
```

```python
employees[1]
```

returns:

```text
Sarah
```

## Adding an item

Use `.append()`.

```python
employees.append("Michael")
```

## Removing an item

Use `.remove()`.

```python
employees.remove("Sarah")
```

## Number of items

Use `len()`.

```python
len(employees)
```

## Why lists matter in our project

Our Employee Directory uses a list to store employees:

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

The list contains dictionaries, with each dictionary representing one employee.

---

# 5. Dictionaries

A dictionary stores information using key-value pairs.

```python
employee = {
    "id": 1,
    "name": "John",
    "department": "IT"
}
```

The keys are:

```text
id
name
department
```

The values are:

```text
1
John
IT
```

## Accessing a value

```python
employee["name"]
```

returns:

```text
John
```

## Using `.get()`

```python
employee.get("name")
```

`.get()` is useful when working with data supplied by users because a missing key can return `None` instead of immediately raising a `KeyError`.

For example:

```python
name = data.get("name")
```

---

# 6. Conditions

Conditions allow a program to make decisions.

```python
age = 18

if age >= 18:
    print("Adult")
else:
    print("Minor")
```

The condition:

```python
age >= 18
```

is evaluated as either `True` or `False`.

## Multiple conditions

```python
if age >= 18:
    print("Adult")
elif age >= 13:
    print("Teenager")
else:
    print("Child")
```

---

# 7. Loops

Loops repeat code.

## For loop

A `for` loop is useful for going through a list.

```python
employees = ["John", "Sarah", "David"]

for employee in employees:
    print(employee)
```

The loop takes each item from `employees` and temporarily stores it in `employee`.

## Looping through dictionaries

In our API:

```python
for employee in employees:
    if employee["id"] == id:
        ...
```

This allows us to inspect each employee until we find the requested ID.

---

# 8. Functions

A function is a reusable block of code.

```python
def greet():
    return "Hello"
```

## Calling a function

```python
greet()
```

## Parameters

A function can receive information.

```python
def greet(name):
    return "Hello " + name
```

Here, `name` is a parameter.

Calling:

```python
greet("Donel")
```

passes `"Donel"` as an argument.

## Return

`return` sends a value back from a function.

```python
def add(a, b):
    return a + b
```

Then:

```python
result = add(5, 3)
```

`result` becomes `8`.

---

# 9. Scope and Global Variables

A variable created outside a function has a wider scope.

Example:

```python
next_id = 3
```

If a function needs to modify that variable:

```python
def add_employee():
    global next_id
    next_id += 1
```

`global` tells Python that `next_id` refers to the variable outside the function.

We use this in the Employee Directory API to keep track of the next employee ID.

---

# 10. Object-Oriented Programming

Object-Oriented Programming (OOP) is a programming approach that organizes code around objects.

A class acts as a blueprint.

```python
class Employee:
    def __init__(self, name, department):
        self.name = name
        self.department = department
```

An object can be created from the class:

```python
employee = Employee("John", "IT")
```

## `__init__`

`__init__` runs when a new object is created.

It is used to initialize the object's properties.

## `self`

`self` refers to the current object.

```python
self.name = name
```

means that the object stores the supplied `name` in its own `name` property.

OOP can initially look complicated, but the basic idea is:

```text
Class → blueprint
Object → thing created from the blueprint
Property → information belonging to the object
Method → function belonging to the object
```

---

# 11. JSON

JSON means JavaScript Object Notation.

It is a common format for exchanging structured data between applications.

Example:

```json
{
    "name": "John",
    "department": "IT"
}
```

JSON is commonly used by APIs because it is easy for humans and programs to read.

A JSON object resembles a Python dictionary:

```python
{
    "name": "John",
    "department": "IT"
}
```

A JSON array resembles a Python list:

```python
[
    {"name": "John"},
    {"name": "Sarah"}
]
```

---

# 12. Python Packages

Python has packages that provide additional functionality.

Flask is one such package.

Instead of installing packages directly into the system Python environment, projects commonly use a virtual environment.

---

# 13. Virtual Environments

A virtual environment provides an isolated Python environment for a project.

Create one:

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

After activation, the terminal normally shows:

```text
(.venv)
```

Install Flask:

```bash
pip install flask
```

Deactivate:

```bash
deactivate
```

## Why use a virtual environment?

Different projects can require different package versions.

A virtual environment prevents project dependencies from unnecessarily interfering with one another.

---

# 14. Useful Python Commands

Check Python:

```bash
python3 --version
```

Find Python:

```bash
which python3
```

Check pip:

```bash
python3 -m pip --version
```

Run a Python program:

```bash
python app.py
```

Create a virtual environment:

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

---

# 15. Important Syntax to Recognize

### Variable

```python
name = "Donel"
```

### Dictionary

```python
employee = {
    "name": "John"
}
```

### List

```python
employees = []
```

### Function

```python
def greet(name):
    return "Hello " + name
```

### Condition

```python
if name:
    print(name)
```

### Loop

```python
for employee in employees:
    print(employee)
```

### Add to list

```python
employees.append(employee)
```

### Access dictionary value

```python
employee["name"]
```

### Safely retrieve dictionary value

```python
employee.get("name")
```

