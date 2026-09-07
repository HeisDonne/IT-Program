from flask import Flask, jsonify, request
app = Flask(__name__)

employees = [
    {"id": 1, "name": "Donnel", "department": "IT"},
    
    {"id": 2, "name": "Glory", "department": "HR"}
]

@app.route('/employees', methods=['GET'])
def get_employees():
    return jsonify(employees)

next_id = 3
@app.route('/employees', methods=['POST'])
def add_employees():
    global next_id

    data = request.json

    name = data.get("name")
    department = data.get("department")

    if not name or not department:
        return jsonify({"error": "Name and department are required"}), 400

    employee = {
        "id": next_id,
        "name": name,
        "department": department
    }

    employees.append(employee)

    next_id += 1
    return jsonify(employee), 201

@app.route("/employees/<int:id>", methods=["DELETE"])
def delete_employee(id):

    for employee in employees:
        if employee["id"] == id:
            employees.remove(employee)
            return jsonify({"message": "Employee deleted"}), 200

    return jsonify({"message": "Employee not found"}), 404


if __name__== '__main__':
    app.run()