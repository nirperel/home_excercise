import json
import random
import requests

base_url = "http://127.0.0.1:8000"
url_employee = base_url + "/employee"
url_employee_delete = url_employee + "/{}"
url_employees = url_employee + "s"


def add_employee():
	requests.post(url_employee, json={"name": "gil" + str(random.randint(1, 1000)), "title": "worker", "salary": 50000})


def add_employees_from_file(file_path: str):
	with open(file_path, "r") as raw_data:
		requests.post(url_employees, json=json.load(raw_data))
	
	
def get_employees() -> json:
	resp = requests.get(url_employees)
	return resp.json()


def delete_employee(name: str):
	return requests.delete(url_employee_delete.format(name))


print(delete_employee("Tommy").json())
