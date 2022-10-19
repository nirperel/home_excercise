import json
import random

import uvicorn
from fastapi import FastAPI, HTTPException, Request
from urllib3 import HTTPResponse

from employee import Employee

EMPLOYEES_FILE = "entities.json"
MAX_EMPLOYEES = 1000
app = FastAPI()


# Add employee to file. Finds a unique id for the new employee listing
# If employee name is not unique will return an error
def add_employee(employee: Employee):
    with open(EMPLOYEES_FILE, "r") as file:
        content = json.load(file)
        found_id = False
        employee_id = random.randint(1, MAX_EMPLOYEES)
        for name in content:
            if name == employee.name:
                raise HTTPException(
                    status_code=400,
                    detail="Name {} already exists".format(employee.name),
                )
        while not found_id:
            found_id = True
            for existing_employee in content:
                if content[existing_employee]["id"] == employee_id:
                    found_id = False
            if not found_id:
                employee_id = random.randint(1, MAX_EMPLOYEES)
        content[employee.name] = {"id": employee_id, "title": employee.title, "salary": employee.salary}
    with open(EMPLOYEES_FILE, "w") as file:
        json.dump(content, file)

@app.post("/employee")
def add_employee_endpoint(employee: Employee):
    add_employee(employee)
    return HTTPResponse(status=200, body="Employee {} was added".format(employee.name))


@app.post("/employees")
async def add_employees(request: Request):
    employees = await request.json()
    for name in employees:
        employee_to_add = Employee(name=name, title=employees[name]["title"], salary=employees[name]["salary"])
        if employee_to_add:
            await add_employee(employee_to_add)


@app.get("/employees")
def get_employees():
    with open(EMPLOYEES_FILE, "r") as data_file:
        return json.load(data_file)


@app.delete("/employee/{employee_name}")
def delete_employee(employee_name: str):
    employees = get_employees()
    print(type(employees))
    if employee_name in employees:
        del employees[employee_name]
        with open(EMPLOYEES_FILE, "w") as file:
            json.dump(employees, file)
    return HTTPResponse(status=204)

if __name__ == '__main__':
    uvicorn.run("server:app", port=8000, reload=True)
