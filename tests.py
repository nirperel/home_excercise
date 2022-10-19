import random
from typing import Union

import requests

from client import get_employees

base_url = "http://127.0.0.1:8000"
url_employee = base_url + "/employee"
url_employee_delete = url_employee + "/{}"
url_employees = url_employee + "s"


def test_add_employee():
	name = "test_name" + str(random.randint(1, 1000))
	resp = requests.post(url_employee, json={"name": name, "title": "worker", "salary": 50000})
	assert resp.status_code == 200
	return name


def test_delete_inexistent_employee():
	resp = requests.delete(url_employee_delete.format("NON EXISTENT NAME"))
	assert resp.status_code == 200


def test_delete_employee(name: Union[str, None]):
	if name:
		name_to_test = name
	else:
		name_to_test = "test_name"
	requests.post(url_employee, json={"name": name_to_test, "title": "worker", "salary": 50000})
	resp = requests.delete(url_employee_delete.format(name_to_test))
	assert resp.status_code == 200


def test_add_employee_with_existing_name():
	name_to_test = "test_name"
	requests.post(url_employee, json={"name": name_to_test, "title": "worker", "salary": 50000})
	resp = requests.post(url_employee, json={"name": name_to_test, "title": "worker", "salary": 50000})
	assert resp.status_code == 400


def test_get_all_employees():
	employees = get_employees()
	number_of_employees = len(employees)
	added_name = test_add_employee()
	assert len(get_employees()) - 1 == number_of_employees
	test_delete_employee(added_name)
