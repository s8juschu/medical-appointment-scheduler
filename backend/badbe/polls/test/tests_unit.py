from django.test import TestCase

# Create your tests here.
from django.utils import timezone
from django.test import TestCase
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from polls.test.resource import MOCK_DEPARTMENTS, MOCK_EMPLOYEE_BIANCA
import io

from polls.models import Employee, Department, Appointment, Template, Account
from polls.serializers import EmployeeSerializer, DepartmentSerializer, AppointmentSerializer, TemplateSerializer, \
    AccountSerializer


# See https://docs.djangoproject.com/en/2.2/topics/testing/

# All test method names must begin with the string 'test' for the Django testing framework to detect them.
# Running all tests in the project: python manage.py test polls


class EmployeeTest(TestCase):
    """
    Unit test case for the Employee model.
    """

    def setUp(self):
        for name in MOCK_DEPARTMENTS:
            Department(name=name).save()

    def create_employee(self):
        return Employee.objects.create(employee_id='33', first_name='J', last_name='Lo',
                                       date_of_birth=timezone.now().date(),
                                       date_of_entry=timezone.now().date(), date_of_exit=timezone.now().date(),
                                       department=Department.objects.get(name="Mensa"))

    def test_employee_creation(self):
        w = self.create_employee()
        self.assertTrue(isinstance(w, Employee))
        self.assertEqual(w.__str__(), " ".join([w.first_name, w.last_name]))


class AppointmentTest(TestCase):
    """
    Unit test case for the Appointment model.
    """

    def setUp(self):
        for name in MOCK_DEPARTMENTS:
            Department(name=name).save()

    def create_appointment(self):
        e = Employee(employee_id='33', first_name='J', last_name='Lo', date_of_birth=timezone.now().date(),
                     date_of_entry=timezone.now().date(), date_of_exit=timezone.now().date(),
                     department=Department.objects.get(name="Mensa"))
        e.save()
        return Appointment.objects.create(employee=e, date=timezone.now().date())

    def test_appointment_creation(self):
        w = self.create_appointment()
        self.assertTrue(isinstance(w, Appointment))


class DepartmentTest(TestCase):
    """
    Unit test case for the Department model.
    """

    def create_department(self):
        return Department.objects.create(name="Mensa")

    def test_department_creation(self):
        d = self.create_department()
        self.assertTrue(isinstance(d, Department))
        self.assertEqual(d.__str__(), " ".join([d.name]))


class TemplateTest(TestCase):
    """
    Unit test case for the Template model.
    """

    def create_template(self):
        return Template.objects.create(name="new", description="Hello")

    def test_template_creation(self):
        t = self.create_template()
        self.assertTrue(isinstance(t, Template))


class AccountTest(TestCase):
    """
    Unit test case for the Account user model.
    """

    def create_account(self):
        return Account.objects.create(username="Mary", email="maria@m.de", first_name="Maria", last_name="Mario")

    def test_account_creation(self):
        a = self.create_account()
        self.assertTrue(isinstance(a, Account))
        self.assertEqual(a.__str__(), " ".join([a.email]))
        self.assertEqual(a.get_full_name(), " ".join([a.first_name, a.last_name]))
        self.assertEqual(a.get_short_name(), " ".join([a.first_name]))


class EmployeeSerializerTest(TestCase):
    """
    Unit test case for the EmployeeSerializer.
    """

    def setUp(self):
        for name in MOCK_DEPARTMENTS:
            Department(name=name).save()

    def test_serialize_employee(self):
        e = Employee(employee_id='1', first_name='John', last_name='Doe', date_of_birth=timezone.now().date(),
                     date_of_entry=timezone.now().date(), date_of_exit=timezone.now().date(),
                     department=Department.objects.get(name="Mensa"))
        # e = Employee(str(MOCK_EMPLOYEE_BIANCA).encode().replace(b"'", b'"'))
        e.save()
        serializer = EmployeeSerializer(e)
        content = JSONRenderer().render(serializer.data)
        print(f"Serialized:\n{content}")

    def test_deserialize_new_employee(self):
        # content = EMPLOYEE_BERTELS_BYTES
        content = str(MOCK_EMPLOYEE_BIANCA).encode().replace(b"'", b'"')  # note: this also affects names like O'Connor
        stream = io.BytesIO(content)
        data = JSONParser().parse(stream)
        print(f"Data:\n{repr(data)}")
        serializer = EmployeeSerializer(data=data)
        assert serializer.is_valid(raise_exception=True)
        print(serializer.validated_data)
        serializer.save()
        serializer = EmployeeSerializer(Employee.objects.all(), many=True)
        content = JSONRenderer().render(serializer.data)
        print(f"Query Set:\n{content}")


class AppointmentSerializerTest(TestCase):
    """
    Unit test case for the AppointmentSerializer.
    """

    def setUp(self):
        for name in MOCK_DEPARTMENTS:
            Department(name=name).save()

    def test_serialize_appointment(self):
        employee_a = Employee(employee_id='22', first_name='Jay', last_name='Z', date_of_birth=timezone.now().date(),
                              date_of_entry=timezone.now().date(), date_of_exit=timezone.now().date(),
                              department=Department.objects.get(name="Mensa"))
        employee_a.save()
        a = Appointment(date=timezone.now().date(), employee=employee_a)
        # e = Employee(str(MOCK_EMPLOYEE_BIANCA).encode().replace(b"'", b'"'))
        a.save()
        serializer = AppointmentSerializer(a)
        content = JSONRenderer().render(serializer.data)
        print(f"Serialized:\n{content}")


class DepartmentSerializerTest(TestCase):
    """
    Unit test case for the DepartmentSerializer.
    """

    def test_query(self):
        d = Department(name="Mensa")
        d.save()
        serializer = DepartmentSerializer(d)
        content = JSONRenderer().render(serializer.data)
        print(f"Serialized:\n{content}")


class TemplateSerializerTest(TestCase):
    """
    Unit test case for the TemplateSerializer.
    """

    def test_query(self):
        t = Template(name="new", description="Hello")
        t.save()
        serializer = TemplateSerializer(t)
        content = JSONRenderer().render(serializer.data)
        print(f"Serialized:\n{content}")


class AccountSerializerTest(TestCase):
    """
    Unit test case for the AccountSerializer.
    """

    def test_query(self):
        a = Account(username="Mary", email="maria@m.de", first_name="Maria", last_name="Mario")
        a.save()
        serializer = AccountSerializer(a)
        content = JSONRenderer().render(serializer.data)
        print(f"Serialized:\n{content}")
