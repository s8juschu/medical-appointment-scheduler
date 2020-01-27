import subprocess
import uuid
import json
import requests
from requests import Response
from random import randint
from typing import List, Dict, Any

from polls.test.resource import MOCK_EMPLOYEES, MOCK_USERS, MOCK_USERS_ADMIN, MOCK_USERS_NONADMIN, URL_ACCOUNTS, \
    URL_LOGIN

"""
This file provides utilities for testing purposes. 
"""

_last_employee_id = 0


def login_user(user) -> Response:
    """
    Sends an HTTP request to login a user with the given credentials.
    :param login_url: The URL to which the login request should be sent. This parameter can be used
    to, e.g., specify the next site to which a redirect should be performed in case of successful login.
    :param credentials: A dict-like object containing the authentication data.
    :return: An object representing the HTTP response, including any session cookies and authentication tokens.
    """
    credentials = {
        'username': user['username'],
        'password': user['password']
    }
    return requests.post(URL_LOGIN, json=credentials)


def create_user(user=None, as_admin=False) -> Response:
    """
    Sends an HTTP request to the given URL to create a new mock user.
    :return: An object representing the HTTP response, including any session cookies and authentication tokens.
    """
    if not user:
        if as_admin:
            user = MOCK_USERS_ADMIN[randint(0, len(MOCK_USERS_ADMIN) - 1)]
        else:
            user = MOCK_USERS_NONADMIN[randint(0, len(MOCK_USERS_NONADMIN) - 1)]
    user['email'] = str(uuid.uuid4()) + '__' + user['email']
    user['username'] = str(uuid.uuid4()) + '__' + user['username']
    print(f'Create new user at {URL_ACCOUNTS}')
    return requests.post(URL_ACCOUNTS, json=user)


def create_departments(department_list: List[str], verbose=False):
    """
    Sends HTTP requests to create mock departments.
    :param department_list: List of department names to create.
    :param verbose: If True, enables HTTP response logging for sent requests.
    """
    for department_name in department_list:
        r = requests.post('http://127.0.0.1:8000/departments/', json={"name": f'{department_name}'})
        # cmd = ["http", "POST", "http://127.0.0.1:8000/departments/", f"name={department_name}", "--ignore-stdin"]
        # if verbose:
        #     cmd += ["--verbose", ]
        # print(f'Run command: {" ".join(cmd)}\n')
        # subprocess.run(cmd)
        if verbose:
            print(r.content)
            print()


def create_missing_departments(department_list: List[str], verbose=False):
    """
    Checks if some of the specified departments are already present in the database.
    If not, sends HTTP requests to create the missing ones.
    :param verbose: If True, enables HTTP response logging for sent requests.
    :param department_list:  List of department names to check.
    """
    r = requests.get(f'http://127.0.0.1:8000/departments/')
    for department_name in department_list:
        if not any(map(lambda department: department["name"] == department_name, r.json()["results"])):
            create_departments([department_name, ], verbose)


def next_employee_id_incremental() -> int:
    """
    Creates an incremental employee ID.
    """
    global _last_employee_id
    _last_employee_id += 1
    return _last_employee_id


def next_employee_id_uuid4() -> str:
    """
    Creates an employee ID based on a random UUID.
    """
    global _last_employee_id
    _last_employee_id = str(uuid.uuid4())
    return _last_employee_id


def next_mock_employee() -> Dict[str, Any]:
    """
    Returns a dict-like employee mock object with a fresh employee ID based on a random UUID.
    """
    next_employee = MOCK_EMPLOYEES[randint(0, len(MOCK_EMPLOYEES) - 1)]
    next_employee["employee_id"] = next_employee_id_uuid4()
    return next_employee


def next_mock_user() -> Dict[str, str]:
    """
    Returns a dict-like user mock object with a fresh username based on a random UUID.
    """
    next_user = MOCK_USERS[randint(0, len(MOCK_USERS) - 1)]
    next_user['username'] = next_user['first_name'] + f'__{uuid.uuid4()}'
    return next_user


def create_employees(employee_list: List[Dict[str, str]], verbose=False):
    """
    Sends HTTP requests to create mock employees.
    :param employee_list: List of employee entries to create. An en employee entry is a dict object.
    :param verbose: If true, enables HTTP response logging for sent requests.
    """
    for employee in employee_list:
        cmd = ["http", "POST", "http://127.0.0.1:8000/employees/"] + dict_to_list(employee) + ["--ignore-stdin", ]
        if verbose:
            cmd += ["--verbose", ]
        print(f'Run command: {" ".join(cmd)}\n')
        subprocess.run(cmd)
        print()


def dict_to_list(data_dict: Dict[str, str]) -> List[str]:
    """
    Casts a Dict to a List object holding 'k=v' strings for each (k,v) item from the input Dict.
    """
    ret = list()
    for key, value in data_dict.items():
        ret.append(f'{key}={value}')
    return ret


def list_to_dict(data_list: List[str]) -> Dict[str, str]:
    """
    Casts a List to a Dict object holding (k,v) items for each 'k=v' string from the input List.
    """
    ret = dict()
    for item in data_list:
        key, value = item.split('=')
        ret[key] = value
    return ret


def str_to_dict(s: str) -> Dict[str, str]:
    """
    Casts a string-like object (string, bytes, bytestring) to a Dict object with string key-value pairs.
    """
    dict_object = json.loads(s)
    for k, v in dict_object.items():
        dict_object[k] = str(v)
    return dict_object
