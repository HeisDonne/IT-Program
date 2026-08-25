import json

employee = {
   "id":1,
   "name": "John",
   "department": "IT"
}

json_data = json.dumps(employee)
print(json_data)
