from django.test import TestCase, TransactionTestCase, LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait

from polls.test.resource import *
from django.conf import settings
from typing import Dict, List
from polls.test.testing_utils import next_mock_employee


# LiveServerTestCase does basically the same as TransactionTestCase with one extra feature: it launches a live
# Django server in the background on setup, and shuts it down on teardown. This allows the use of automated
# test clients other than the Django dummy client such as, for example, the Selenium client, to execute a series
# of functional tests inside a browser and simulate a real user’s actions.
#
# The live server listens on localhost and binds to port 0 which uses a free port assigned by the operating system.
# The server’s URL can be accessed with self.live_server_url during the tests.


class SeleniumTests(LiveServerTestCase):
    """
        System tests building on the Selenium framework for browser automatization.
        The tests in this class evaluate the system's compliance with the specified requirements
        for the complete integrated system.

        Selenium is a portable framework for browser automatization and web application testing.
        See https://selenium.dev/documentation/ and https://selenium-python.readthedocs.io/
    """

    # The Selenium web driver used for browser automatization
    driver = None

    @classmethod
    def setUpTestData(cls):
        """
        Sets up data for the whole TestCase
        """
        pass

    @classmethod
    def setUpClass(cls):
        """
        Runs once for entire test case.
        """
        super().setUpClass()
        # cls.driver = webdriver.Firefox(executable_path=settings.POLLS['PATH_GECKODRIVER_EXECUTABLE'])
        cls.driver = webdriver.Chrome(settings.POLLS['PATH_CHROMEDRIVER_EXECUTABLE'])
        cls.driver.implicitly_wait(5)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def setUp(self):
        """
        Runs once for each test.
        """
        self.try_login('admin@test.de', 'supersecret')

    def test_create_new_employee(self):
        """
        Tests if an employee can be created successfully.
        """

        # Test data
        employee = next_mock_employee()

        # Test
        print(f"Welcome to the Create New Employee Test!")
        # Open home page
        self.driver.get(f"{URL_FRONTEND}")

        # Create new employee
        self.create_employee(**employee)

        assert "/mitarbeiter" in self.driver.current_url, "Was not redirected to employee overview page"
        print(f'Was redirected to {self.driver.current_url}')

        # Verify that the new employee appears in the employee overview
        print('Checking if creation was successful (if the new employee is listed in the overview)')
        self.check_is_employee_in_overview(employee)
        print('Successfully created a new employee!')

    def test_archive_dearchive_existing_employee(self):
        # Test data
        employee = next_mock_employee()

        # Test
        print(f"Welcome to the Archive Employee Test!")
        # Open home page
        self.driver.get(f"{URL_FRONTEND}")

        # Create new employee
        self.create_employee(**employee)

        print('Opening employee details page')
        # self.driver.get(f'{URL_FRONTEND}/mitarbeiter/{employee["employee_id"]}')
        self.find_employee_in_table(employee).click()

        print("Archiving employee")
        self.driver.find_element_by_id('verwaltenArchivieren').click()
        wait = WebDriverWait(self.driver, 3)
        self.driver.find_element_by_id('verwaltenModalArchJa').click()
        wait.until(lambda driver: '/archiv' in self.driver.current_url,
                   f'Was not redirected to "/archiv" page, instead current url is: {self.driver.current_url}')

        row_element = self.check_find_employee_row_in_archive(employee)
        assert row_element is not None, \
            f'Failed to find the archived employee on the archive page.'

        print('Successfully archived employee')
        print("De-archiving employee again")
        row_element.find_element_by_id('archiveDearchive').click()
        self.driver.find_element_by_id('verwaltenModalDeArchJa').click()

        self.check_is_employee_in_overview(employee)

    def test_search_existing_employee(self):
        """
        Tests if an existing employee gets listed on the employee overview page.
        """

        print('Welcome to the Search Existing Employee Test')

        # Open home page
        self.driver.get(f"{URL_FRONTEND}")
        employee = next_mock_employee()

        # Create an employee
        self.create_employee(**employee)

        print(f'Open page Angestellte')
        self.driver.find_element_by_id('navEmployee').click()

        print(f'Try to find employee with ID {employee["employee_id"]}')
        self.check_is_employee_in_overview(employee)
        print('Successfully searched for an employee successful!')

    def test_preview_invitation_letter(self):
        """
        Tests if an invitation letter can be previewed, edited and downloaded successfully for an existing employee.
        """

        print('Welcome to the Print Invitation Letter Test')

        # Open home page
        self.driver.get(f"{URL_FRONTEND}")

        # Open employee overview page
        self.driver.find_element_by_id('navEmployee').click()

        # Select an employee or create a new one
        elements = self.driver.find_elements_by_class_name('employeeRow')
        employee = dict()
        if len(elements) == 0:
            employee = next_mock_employee()
            self.create_employee(**employee)
        self.driver.find_elements_by_class_name('employeeRow')[0].click()
        # Todo: Don't know how to get the input field values, since the fields'
        #  value attribute is empty strin Seems to be some Angular/Bootstrap magic here...
        # employee['first_name'] = self.driver.find_element_by_id('staticVorname').text
        # employee['last_name'] = self.driver.find_element_by_id('staticNachname').text
        # employee['employee_id'] = self.driver.find_element_by_id('staticPerNum').text
        # employee['department'] = self.driver.find_element_by_id('staticAbteilung').text

        # Generate an invitation letter
        self.driver.find_element_by_id('generate').click()
        self.driver.find_element_by_id('modalJa').click()

        # Check whether the ivitation letter contains particular expected strings, e.g. the employee's full name
        template_paragraphs = self.driver.find_element_by_id('letterEditor').find_elements_by_tag_name('p')
        expected_strings = [
            'PERSÖNLICH/PERSONALSACHE',
            'eine arbeitsmedizinische',
            'Guten Tag',
            # f'{employee["first_name"]} {employee["last_name"]}',
            # employee["department"],
        ]
        for string in expected_strings:
            assert any(list(map(lambda p: string in p.text, template_paragraphs))), \
                f'Could not find expected string "{string}" in the invitation letter'

        # Check if the PDF download button is present. Selenium has no capabilities to interact with a browser's
        # download dialog.
        self.driver.find_element_by_id('letterPrint')

        print('Successfully generated an invitation letter')

    def test_login_existing_user(self):
        """
        Tests if an existing user is able to log in successfully.
        """
        print('Welcome to the Login Existing User Test')

        # If logged in, log out first
        print('There is an active login session.')
        self.try_logout()

        login_protected_path = '/'
        credentials = {
            'username': 'admin@test.de',
            'password': 'supersecret'
        }

        # Open a page which is protected by login
        self.driver.get(f"{URL_FRONTEND}{login_protected_path}")

        assert '/login' in self.driver.current_url, \
            f'Was not redirected to login page, instead current url is: {self.driver.current_url}'

        self.try_login(credentials['username'], credentials['password'])

        # Verify we were redirected to the protected page after clicking the login button
        assert f'{URL_FRONTEND}{login_protected_path}' == self.driver.current_url, \
            f'Was not redirected to {login_protected_path} after hitting login button, instead current url is ' \
            f'{self.driver.current_url}'

        print('Successfully logged in an existing user!')

    def try_login(self, username: str, password: str, navigate_to_homepage: bool = True):
        print("Logging in")

        # Open home page, which is password protected
        if navigate_to_homepage:
            self.driver.get(f"{URL_FRONTEND}")

        # if not logged in, we get redirected to the login page
        if "/login" in self.driver.current_url:
            # Fill in username and password
            self.driver.find_element_by_id('loginUsername').send_keys(username)
            self.driver.find_element_by_id('loginPswd').send_keys(password)
            wait = WebDriverWait(self.driver, 3)
            self.driver.find_element_by_id('loginSubmit').click()
            wait.until(lambda driver: '/login' not in self.driver.current_url)
            return True
        return False

    def try_logout(self):
        print('Logging out')
        wait = WebDriverWait(self.driver, 3)
        self.driver.find_element_by_id("userDropdown").click()
        self.driver.find_element_by_id("logoutBtn").click()
        wait.until(lambda driver: '/login' in self.driver.current_url, f'Was not redirected to "/login" after '
                                                                       f'hitting logout button, instead current url is '
                                                                       f'{self.driver.current_url}')

    def create_employee(self, **kwargs):
        """
        Opens the employee overview page and fills the form for creating a new employee using the given data.
        :param kwargs: A dict-like object holding the employee data.
        """
        print(f'Open page Angestellte')
        self.driver.find_element_by_id('navEmployee').click()  # 'Angestellte' button

        print(f'Try to create new employee with ID {kwargs["employee_id"]}')
        self.driver.find_element_by_id('employeeAdd').click()  # 'Neuen Mitarbeiter hinzufügen' button

        # Fill in the form
        if kwargs['gender'] == 'männlich':
            geschlecht_checkbox = self.driver.find_element_by_id('verwaltenGenderM')
        elif kwargs['gender'] == 'weiblich':
            geschlecht_checkbox = self.driver.find_element_by_id('verwaltenGenderF')
        elif kwargs['gender'] == 'divers':
            geschlecht_checkbox = self.driver.find_element_by_id('verwaltenGenderD')
        else:
            assert False, f'Employee to create has unexpected gender \"{kwargs["gender"]}\"'
        geschlecht_checkbox.click()

        self.driver.find_element_by_id('staticVorname').send_keys(kwargs["first_name"])
        self.driver.find_element_by_id('staticNachname').send_keys(kwargs["last_name"])
        self.driver.find_element_by_id('staticGebDatum').send_keys(kwargs["date_of_birth"])
        self.driver.find_element_by_id('staticEinDatum').send_keys(kwargs["date_of_entry"])
        self.driver.find_element_by_id('staticPerNum').send_keys(kwargs["employee_id"])

        if not self.select_dropdown_option(self.driver.find_element_by_id('staticAbteilung'), kwargs["department"]):
            self.driver.find_element_by_id('newAbteilung').click()
            self.driver.find_element_by_id('newAbteilungName').send_keys(kwargs['department'])
            self.driver.find_element_by_id('newAbteilungModalNewSave').click()
        # assert self.try_select_option(self.driver.find_element_by_id('staticAbteilung'), f' {kwargs["department"]} '), \
        #     f'Failed to select/create department "{kwargs["department"]}"'

        if kwargs['wants_reminder']:
            erinnerungen_checkbox = self.driver.find_element_by_id('erinnerungJa')
        else:
            erinnerungen_checkbox = self.driver.find_element_by_id('erinnerungNein')
        erinnerungen_checkbox.click()

        self.driver.find_element_by_id('staticTurnus').send_keys(kwargs.get('turnus', '24'))
        self.driver.find_element_by_id('verwaltenNote').send_keys(kwargs.get('notes', ''))

        print('Clicking Save button.')
        self.driver.find_element_by_id('verwaltenSave').click()
        self.driver.find_element_by_id('verwaltenModalSaveJa').click()

    def select_dropdown_option(self, dropdown_element: WebElement, expected_value: str) -> bool:
        """
        Checks if the given value is present in a select (dropdown) element. If yes, selects the option.
        :return: True if the option is present, else False.
        """
        # Todo: Bootstrap does not play dropdown with Selenium :(
        # See https://flowfx.de/blog/testing-bootstrap-select-dropdown-field-with-selenium-python/

        if expected_value not in list(map(lambda o: o.text.lstrip().rstrip(), Select(dropdown_element).options)):
            return False

        # Approach 1:
        # dropdown_element.click()
        # dropdown_element.send_keys(expected_value)
        # dropdown_element.send_keys(Keys.ENTER)
        # return True

        # Approach 2:
        dropdown_element.click()
        options = dropdown_element.find_elements_by_tag_name('option')
        for opt in options:
            if expected_value == opt.text.lstrip().rstrip():
                opt.click()
                return True
        return False

        # Approach 3:
        # dropdown_element.click()
        # # handle = self.driver.current_window_handle
        # select = Select(dropdown_element)
        # if expected_value in list(map(lambda o: o.text.lstrip().rstrip(), select.options)):
        #     if expected_value not in list(map(lambda o: o.text.lstrip().rstrip(), select.all_selected_options)):
        #         select.select_by_visible_text(expected_value)
        #         assert expected_value in list(map(lambda o: o.text.lstrip().rstrip(), select.all_selected_options)), \
        #             f'Failed to select existing option "{expected_value}"'
        #         # self.driver.switch_to.default_content()
        #         # self.driver.switch_to(handle)
        #         # dropdown_element.send_keys(Keys.TAB)
        #     return True
        # return False

    def check_is_employee_in_overview(self, employee: Dict[str, str]) -> bool:
        """
        Checks if the page that lists all employees contains the given employee.
        :param employee: The employee to find.
        :return: True if present, else False.
        """

        # Search the table row containing the employee id
        elements = self.driver.find_elements_by_xpath(f'//*[contains(text(), \"{employee["employee_id"]}\")]')
        assert len(elements) == 1, \
            f'Did not find any employee with ID of the new employee in list! Expected: 1, found: {len(elements)}'
        row_td_cells = self.driver.find_elements_by_xpath(
            f'//*[contains(text(), \"{employee["employee_id"]}\")]/..//td')

        # Check if all values in the table row are correct
        assert any(list(map(lambda e: e.text == employee["first_name"], row_td_cells))), \
            'First name ("{employee["first_name"]}")of new employee not found in list! '
        assert any(list(map(lambda e: e.text == employee["last_name"], row_td_cells))), \
            f'Last name ("{employee["last_name"]}") of new employee not found in list! '
        if employee["wants_reminder"]:
            assert any(list(map(lambda e: e.text == 'Ja', row_td_cells))), \
                'No or false reminder choice of new employee found in list!'
        else:
            assert any(list(map(lambda e: e.text == 'Nein', row_td_cells))), \
                'No or false reminder choice of new employee found in list!'

        print(f'Found employee with ID {employee["employee_id"]} in overview')

    def check_find_employee_row_in_archive(self, employee: Dict[str, str]) -> WebElement:
        """
        Checks if the page that lists all archived employees and checks contains the given employee.
        :param employee: The employee to find.
        :return: The table row element of the archived employee
        """
        employee_row = self.find_employee_in_table(employee)

        # Check if all values in the table row are correct
        row_td_cells = self.driver.find_elements_by_xpath(
            f'//*[contains(text(), \"{employee["employee_id"]}\")]/..//td')
        assert any(list(map(lambda e: e.text == employee["first_name"], row_td_cells))), \
            'First name ("{employee["first_name"]}")of new employee not found in list! '
        assert any(list(map(lambda e: e.text == employee["last_name"], row_td_cells))), \
            f'Last name ("{employee["last_name"]}") of new employee not found in list! '

        return employee_row

    def find_employee_in_table(self, employee: Dict[str, str]) -> WebElement:
        # Search the table row containing the employee id
        elements = self.driver.find_elements_by_xpath(f'//*[contains(text(), \"{employee["employee_id"]}\")]')
        assert len(elements) == 1, \
            f'Did not find any employee with ID of the new employee in list! Expected: 1, found: {len(elements)}'
        return self.driver.find_elements_by_xpath(f'//*[contains(text(), \"{employee["employee_id"]}\")]/..')[0]
