from random import randint
import uuid

"""
This file provides prepared mock data for testing purposes.

Note: Use next_mock_department() and next_mock_employee() methods from the testing utils class 
in order to get an arbitrary number of mock employee records with dynamically generated unique ids. 
"""

##########################
# TEST URLs
##########################

PROTOCOL = 'http'
HOST = '127.0.0.1'
BACKEND_PORT = '8000'
FRONTEND_PORT = '4200'

URL_BACKEND = f'{PROTOCOL}://{HOST}{":" + BACKEND_PORT if BACKEND_PORT else ""}'
URL_FRONTEND = f'{PROTOCOL}://{HOST}{":" + FRONTEND_PORT if FRONTEND_PORT else ""}'

URL_ACCOUNTS = f'{URL_BACKEND}/accounts/'
URL_LOGIN = f'{URL_BACKEND}/rest-auth/login/'

##########################
# TEST DEPARTMENT DATA
##########################

MOCK_DEPARTMENTS = [
    "Wohnen",
    "Finanzierung",
    "Psychologische Beratung",
    "Internationales",
    "IT",
    "Mensa",
    "Personal",
    "Buchhaltung",
    "Kita"
]


##########################
# TEST EMPLOYEE DATA
##########################

def next_employee_id_uuid4() -> str:
    """
    Creates an employee ID based on a random UUID.
    """
    return str(uuid.uuid4())


def next_employee_id_randint() -> str:
    """
    Creates an employee ID consisting of random digits.
    """
    return randint(10000000, 99999999)


MOCK_EMPLOYEE_FIONA = {
    'first_name': 'Fiona',
    'last_name': 'Köhler',
    'gender': 'weiblich',
    'date_of_birth': '2019-11-28',
    'date_of_entry': '2019-11-28',
    'employee_id': next_employee_id_randint(),
    'department': MOCK_DEPARTMENTS[randint(1, len(MOCK_DEPARTMENTS) - 1)],
    'notes': f'shreklich!',
    'wants_reminder': True
}

MOCK_EMPLOYEE_BIANCA = {
    'first_name': 'Bianca',
    'last_name': 'Lange',
    'gender': 'weiblich',
    'date_of_birth': '2019-11-28',
    'date_of_entry': '2019-11-28',
    'employee_id': next_employee_id_randint(),
    'department': MOCK_DEPARTMENTS[randint(1, len(MOCK_DEPARTMENTS) - 1)],
    'wants_reminder': True
}

MOCK_EMPLOYEE_LUISA = {
    'first_name': 'Luisa',
    'last_name': 'Hofman',
    'gender': 'weiblich',
    'date_of_birth': '2019-11-28',
    'date_of_entry': '2019-11-28',
    'employee_id': next_employee_id_randint(),
    'department': MOCK_DEPARTMENTS[randint(1, len(MOCK_DEPARTMENTS) - 1)],
    'wants_reminder': True
}

MOCK_EMPLOYEE_SARAH = {
    'first_name': 'Sarah',
    'last_name': 'O\' Connor',
    'gender': 'divers',
    'date_of_birth': '2019-11-28',
    'date_of_entry': '2019-11-28',
    'employee_id': next_employee_id_randint(),
    'department': MOCK_DEPARTMENTS[randint(1, len(MOCK_DEPARTMENTS) - 1)],
    'notes': f'singt gern und laut, aufgepasst!',
    'wants_reminder': True
}

MOCK_EMPLOYEE_ANNE = {
    'first_name': 'Anne',
    'last_name': 'Wolff-Mayer',
    'gender': 'weiblich',
    'date_of_birth': '2019-11-28',
    'date_of_entry': '2019-11-28',
    'employee_id': next_employee_id_randint(),
    'department': MOCK_DEPARTMENTS[randint(1, len(MOCK_DEPARTMENTS) - 1)],
    'wants_reminder': True
}

MOCK_EMPLOYEE_ROBERT = {
    'first_name': 'Robert',
    'last_name': 'Bergmann',
    'gender': 'männlich',
    'date_of_birth': '2019-11-28',
    'date_of_entry': '2019-11-28',
    'employee_id': next_employee_id_randint(),
    'department': MOCK_DEPARTMENTS[randint(1, len(MOCK_DEPARTMENTS) - 1)],
    'wants_reminder': True
}

MOCK_EMPLOYEE_NIELS = {
    'first_name': 'Niels',
    'last_name': 'Huber',
    'gender': 'divers',
    'date_of_birth': '2019-11-28',
    'date_of_entry': '2019-11-28',
    'employee_id': next_employee_id_randint(),
    'department': MOCK_DEPARTMENTS[randint(1, len(MOCK_DEPARTMENTS) - 1)],
    'wants_reminder': True
}

MOCK_EMPLOYEE_EMMANUEL = {
    'first_name': 'Emmanuel Jean-Michel Frédéric',
    'last_name': 'Macron',
    'gender': 'männlich',
    'date_of_birth': '2019-11-28',
    'date_of_entry': '2019-11-28',
    'employee_id': next_employee_id_randint(),
    'department': MOCK_DEPARTMENTS[randint(1, len(MOCK_DEPARTMENTS) - 1)],
    'notes': f'liberté, egalité, pfefferminztee',
    'wants_reminder': True
}

MOCK_EMPLOYEE_FELIX = {
    'first_name': 'Felix',
    'last_name': 'Jäger',
    'gender': 'männlich',
    'date_of_birth': '2019-11-28',
    'date_of_entry': '2019-11-28',
    'employee_id': next_employee_id_randint(),
    'department': MOCK_DEPARTMENTS[randint(1, len(MOCK_DEPARTMENTS) - 1)],
    'notes': f'Nascht heimlich vom Rindergulasch in der Mensa ^^',
    'wants_reminder': True
}
MOCK_EMPLOYEE_JONAS = {
    'first_name': 'Jonas',
    'last_name': 'Paul',
    'gender': 'männlich',
    'date_of_birth': '2019-11-28',
    'date_of_entry': '2019-11-28',
    'employee_id': next_employee_id_randint(),
    'department': MOCK_DEPARTMENTS[randint(1, len(MOCK_DEPARTMENTS) - 1)],
    'notes': f'Nascht heimlich vom Rindergulasch in der Mensa ^^',
    'wants_reminder': True
}
MOCK_EMPLOYEE_JONAS_MOD = {
    'first_name': 'Jonas',
    'last_name': 'Paul',
    'gender': 'männlich',
    'date_of_birth': '2019-11-20',
    'date_of_entry': '2019-11-28',
    'employee_id': next_employee_id_randint(),
    'department': MOCK_DEPARTMENTS[randint(1, len(MOCK_DEPARTMENTS) - 1)],
    'notes': f'Nascht heimlich vom Rindergulasch in der Mensa ^^',
    'wants_reminder': True
}

MOCK_EMPLOYEE_GRETCHEN = {
    'first_name': 'Margarete',
    'last_name': 'Faustus',
    'gender': 'weiblich',
    'date_of_birth': '1996-01-01',
    'date_of_entry': '2020-01-01',
    'employee_id': next_employee_id_randint(),
    'department': MOCK_DEPARTMENTS[randint(1, len(MOCK_DEPARTMENTS) - 1)],
    'notes': 'Nach Golde drängt,\n'
             + 'Am Golde hängt\n'
             + 'Doch alles.',
    'wants_reminder': True
}

MOCK_EMPLOYEE_BERTELS_BYTES = b'{"id":"5","first_name":"Bertels","last_name":"Mann","employee_id":2,"gender":"divers",' \
                              b'"date_of_birth":"2019-11-28","date_of_entry":"2019-11-28","date_of_exit":"2019-11-28",' \
                              b'"next_appointment":null,"department":1,"notes":"","wants_reminder":true,"active":true}'

MOCK_EMPLOYEES = [
    MOCK_EMPLOYEE_FIONA,
    MOCK_EMPLOYEE_BIANCA,
    MOCK_EMPLOYEE_LUISA,
    MOCK_EMPLOYEE_SARAH,
    MOCK_EMPLOYEE_ANNE,
    MOCK_EMPLOYEE_ROBERT,
    MOCK_EMPLOYEE_NIELS,
    MOCK_EMPLOYEE_EMMANUEL,
    MOCK_EMPLOYEE_FELIX,
    MOCK_EMPLOYEE_GRETCHEN
]

######################################
# TEST USER DATA
######################################

MOCK_USER_ROLAND_NOT_ADMIN = {
    'email': 'roland@test.de',
    'first_name': 'Roland',
    'last_name': 'Kaiser',
    'username': 'roland',
    'password': 'supersecret',
}

MOCK_USER_HERBERT_ADMIN = {
    'email': 'herbert@test.de',
    'first_name': 'Herbert',
    'last_name': 'Grönemeyer',
    'username': 'herbert',
    'password': 'supersecret'
}

MOCK_USERS = [
    MOCK_USER_HERBERT_ADMIN,
    MOCK_USER_ROLAND_NOT_ADMIN
]

MOCK_USERS_ADMIN = [
    MOCK_USER_HERBERT_ADMIN,
]

MOCK_USERS_NONADMIN = [
    MOCK_USER_ROLAND_NOT_ADMIN,
]
