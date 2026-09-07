from flask import Flask, jsonify, request
import psycopg2
app = Flask(__name__)

def get_db_connection():
    return psycopg2.connect(
        host="127.0.0.1",
        port=5433,
        database="employee_db",
        user="employees_api",
        password="TempTest987"
    )



@app.route('/employees', methods=['GET'])
def get_employees():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            employees.id,
            employees.name,
            departments.name AS department
        FROM employees
        JOIN departments
            ON employees.department_id = departments.id
        ORDER BY employees.id;
    """)

    rows = cursor.fetchall()

    employees = []

    for row in rows:
        employees.append({
            "id": row[0],
            "name": row[1],
            "department": row[2]
        })

    cursor.close()
    conn.close()

    return jsonify(employees)


@app.route('/employees', methods=['POST'])
def add_employees():

    data = request.json

    name = data.get("name")
    department_id = data.get("department_id")

    if not name or not department_id:
        return jsonify({"error": "Name and department_id are required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(""" INSERT INTO employees (name, department_id) 
                    VALUES (%s, %s)
                    RETURNING id, name, department_id;""",
                   (name, department_id))

    row = cursor.fetchone()
    conn.commit()
    cursor.close()
    conn.close()

    employee = {
        "id": row[0],
        "name": row[1],
        "department": row[2]
    }
    return jsonify(employee), 201

@app.route("/employees/<int:id>", methods=["DELETE"])
def delete_employee(id):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM employees WHERE id = %s RETURNING id;",
        (id,)
    )

    row = cursor.fetchone()

    if row is None:
        cursor.close()
        conn.close()
        return jsonify({"message": "Employee not found"}), 404

    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"message": "Employee deleted"}), 200


if __name__== '__main__':
    app.run()
