from polls.test.resource import MOCK_DEPARTMENTS
from polls.test.testing_utils import create_missing_departments, next_mock_employee, next_mock_user, login_user, \
    create_user

from django.test import TestCase
from rest_framework import status
from typing import Dict
import requests
from requests import Response

# See https://docs.djangoproject.com/en/2.2/topics/testing/

# All test method names MUST begin with 'test'

# python manage.py test polls
from polls.test.testing_utils import dict_to_list


class EmployeeApiTest(TestCase):
    """
    API test case for the `polls.views.EmployeeViewSet` endpoints.
    """

    employee: Dict[str, str] = None

    def setUp(self):
        """
        Runs once for each test.
        """
        pass

    @classmethod
    def setUpClass(cls):
        """
        Runs once for entire test case.
        """
        super(EmployeeApiTest, cls).setUpClass()
        create_missing_departments(MOCK_DEPARTMENTS)
        cls.employee = next_mock_employee()  # use same mock employee in all tests
        cls.user = next_mock_user()  # used to establish a login session
        login_user(cls.user)

    def test_create_employee(self):
        r = create_employee_request(self.employee)
        created_employee = r.json()
        print(f'The created employee has employee ID '
              f'{created_employee["employee_id"]} and internal ID {created_employee["id"]}')

        print('Verify employee fields')
        for k, v in self.employee.items():
            if v is not None:
                assert v == created_employee[k], f'Created employee has unexpected "{k}" value, ' \
                                                 f'expected: "{v}", got: "{created_employee[k]}"'

        assert created_employee["active"], f'Created employee must not be archived upon creation'

        print('Open employee detail page')
        r = requests.get(f'http://127.0.0.1:8000/employees/{created_employee["id"]}/')
        assert r.status_code == status.HTTP_200_OK, \
            f'Received unexpected status code for employee detail page request, expected: 200, ' \
            f'got: {r.status_code}\nResponse: {r.text}'

        print('Clean up employee')
        delete_employee(created_employee["id"])

    def test_archive_existing_employee(self):
        created_employee = create_employee_request(self.employee).json()
        assert created_employee["active"], f'Employee must not be archived in order to archive it'

        internal_id = created_employee["id"]
        print(f'Archive employee {internal_id}')
        diff = {"active": False}
        r = requests.patch(f'http://127.0.0.1:8000/employees/{internal_id}/', diff)
        assert r.status_code == status.HTTP_200_OK, \
            f'Received unexpected status code for employee archiving (PATCH) request, expected: 200, ' \
            f'got: {r.status_code}\nResponse: {r.text}'

        print(f'Verify employee fields')
        archived_employee = r.json()
        assert archived_employee["id"] == internal_id, \
            f'Archived employee has unexpected internal id", ' \
            f'expected: "{internal_id}", got: "{archived_employee["id"]}"'

        assert not archived_employee["active"], \
            f'Unexpected "active" value of employee with internal id {internal_id} after archiving it, ' \
            f'expected: False, got: {archived_employee["active"]}\nEmployee:{archived_employee}'

        print('Clean up employee')
        delete_employee(created_employee["id"])

    def test_partially_modify_existing_employee(self):
        # partially modify --> PATCH
        r = create_employee_request(self.employee)

        print(f'Modify employee fields')
        created_employee = r.json()
        diff = {k: v for k, v in created_employee.items() if v != 'None' and k != 'id'}
        diff["last_name"] = created_employee["last_name"][::-1]  # reverse string
        diff["notes"] = created_employee["notes"] + "abc\n\ntest"
        r = requests.patch(f'http://127.0.0.1:8000/employees/{created_employee["id"]}/', diff)
        assert r.status_code == status.HTTP_200_OK, \
            f'Received unexpected status code for employee modification (PATCH) request, expected: 200, ' \
            f'got: {r.status_code}\nResponse: {r.text}'

        print(f'Verify employee fields')
        modified_employee = r.json()
        for k in ["last_name", "notes"]:
            assert diff[k] == modified_employee[k], \
                f'Modified employee has unexpected "{k}" value, expected: "{diff[k]}", got: "{modified_employee[k]}"'

        print('Clean up employee')
        delete_employee(created_employee["id"])

    def test_fully_modify_existing_employee(self):
        # fully modify --> PUT
        r = create_employee_request(self.employee)

        print(f'Modify employee fields')
        created_employee = r.json()
        diff = {k: v for k, v in created_employee.items() if v != 'None' and k != 'id'}
        diff["last_name"] = created_employee["last_name"][::-1]  # reverse string
        diff["first_name"] = created_employee["first_name"][::-1]  # reverse string
        if created_employee["gender"] is "weiblich":
            diff["gender"] = "männlich"
        else:
            diff["gender"] = "weiblich"
        # diff["date_of_entry"] = str(timezone.now())
        diff["wants_reminder"] = not created_employee["wants_reminder"]
        diff["active"] = not created_employee["active"]
        diff["notes"] = created_employee["notes"] + "abc\n\ntest"
        r = requests.put(f'http://127.0.0.1:8000/employees/{created_employee["id"]}/', diff)
        assert r.status_code == status.HTTP_200_OK, \
            f'Received unexpected status code for employee modification (PUT) request, expected: 200, ' \
            f'got: {r.status_code}\nResponse: {r.text}'

        print(f'Verify employee fields')
        modified_employee = r.json()
        for k in ["last_name", "first_name", "gender", "date_of_entry", "notes"]:
            assert diff[k] == modified_employee[k], \
                f'Modified employee has unexpected "{k}" value, expected: "{diff[k]}", got: "{modified_employee[k]}"'
        for k in ["wants_reminder", "active"]:
            assert bool(diff[k]) & bool(modified_employee[k]) == diff[k], \
                f'Modified employee has unexpected "{k}" value, expected: "{diff[k]}", got: "{modified_employee[k]}"'
        print('Clean up employee')
        delete_employee(created_employee["id"])

    def test_delete_existing_employee(self):
        internal_id = create_employee_request(self.employee).json()["id"]

        print(f'Delete employee {internal_id}')
        r = requests.delete(f'http://127.0.0.1:8000/employees/{internal_id}/')
        expected_staus_codes = [status.HTTP_200_OK, status.HTTP_202_ACCEPTED, status.HTTP_204_NO_CONTENT]
        assert r.status_code in expected_staus_codes, \
            f'Received unexpected status code for employee delete request, ' \
            f'expected one of {expected_staus_codes}, got: {r.status_code}\nResponse: {r.text}'

        r = requests.get(f'http://127.0.0.1:8000/employees/{internal_id}/')
        assert r.status_code == status.HTTP_404_NOT_FOUND, \
            f'Employee {internal_id} seems to still exist after deletion!'


def create_employee_request(employee: Dict[str, str]) -> Response:
    print(
        f'Create new employee "{employee["first_name"]} {employee["last_name"]}" with employee ID {employee["employee_id"]}')
    r = requests.post('http://127.0.0.1:8000/employees/', json=employee)
    assert r.status_code == status.HTTP_201_CREATED, \
        f'Received unexpected status code for create employee request, expected: 201, ' \
        f'got: {r.status_code}\nResponse: {r.text}'
    print(f'Created')
    return r


def delete_employee(internal_employee_id: int) -> Response:
    print(f'Delete employee with internal ID {internal_employee_id}')
    return requests.delete(f'http://127.0.0.1:8000/employees/{internal_employee_id}/')


class AccountApiTest(TestCase):
    """
    API test case for the `polls.views.AccountViewSet` endpoints.
    """

    user: Dict[str, str] = None

    def setUp(self):
        """
        Runs once for each test.
        """
        pass

    @classmethod
    def setUpClass(cls):
        """
        Runs once for entire test case.
        """
        super(AccountApiTest, cls).setUpClass()
        # cls.user = next_mock_user()  # use same mock user in all tests

    def test_create_nonadmin_user(self):
        r = create_user(self.user)
        created_user = r.json()

        assert r.status_code == status.HTTP_201_CREATED, \
            f'Received unexpected status code for create user request, expected: 201, ' \
            f'got: {r.status_code}\nResponse: {r.text}'

        print('Verify user fields')
        for k, v in created_user.items():
            if v is not None and k in ['first_name', 'last_name', 'email', 'password']:
                assert v == created_user[k], f'Created employee has unexpected "{k}" value, ' \
                                             f'expected: "{v}", got: "{created_user[k]}"'
