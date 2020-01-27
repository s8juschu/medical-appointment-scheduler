"""
Django models for this project.

A model is the single, definitive source of information about your data. It contains the essential fields
and behaviors of the data you’re storing. Generally, each model maps to a single database table.

For more information on Django models, see
https://docs.djangoproject.com/en/3.0/topics/db/models/
"""


from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser, BaseUserManager, PermissionsMixin

# Note: Instead of referring to User directly, you should reference the user model using
# django.contrib.auth.get_user_model(). This method will return the currently active user model.
# Alternatively, you can specify the custom model using the settings.AUTH_USER_MODEL setting explicitly.


CHARFIELD_DEFAULT_MAX_LENGTH = 255


class Department(models.Model):
    """
    A model containing the essential fields and behaviors of a business department.
    """

    class Meta:
        ordering = ['name']

    name = models.CharField(
        max_length=CHARFIELD_DEFAULT_MAX_LENGTH, unique=True)
    # Note: Arithmetic with DurationField works in most cases. However on all databases other
    # than PostgreSQL, comparing the value of a DurationField to arithmetic on DateTimeField
    # instances will not work as expected.
    reminder_interval = models.IntegerField(
        default=24, blank=True)  # interval is two years

    def __str__(self):
        return self.name


class Employee(models.Model):
    """
    A model containing the essential fields and behaviors of an employee.
    """

    class Meta:
        ordering = ['last_name']

    GENDER_CHOICES = (
        ('männlich', 'männlich'),
        ('weiblich', 'weiblich'),
        ('divers', 'divers')
    )
    first_name = models.CharField(max_length=CHARFIELD_DEFAULT_MAX_LENGTH)
    last_name = models.CharField(max_length=CHARFIELD_DEFAULT_MAX_LENGTH)
    gender = models.CharField(
        max_length=CHARFIELD_DEFAULT_MAX_LENGTH, choices=GENDER_CHOICES)

    # Personnel number
    employee_id = models.CharField(
        max_length=CHARFIELD_DEFAULT_MAX_LENGTH, unique=True)

    date_of_birth = models.DateField()

    # First day of employment
    date_of_entry = models.DateField()

    # Last day of employment
    date_of_exit = models.DateField(blank=True, null=True)

    # Notes associated with the employee
    notes = models.TextField(blank=True, default='')

    # Whether the employee wants to receive reminder letters for appointments
    wants_reminder = models.BooleanField(default=True)

    # Date on which the next reminder will be displayed
    next_reminder = models.DateField(blank=True, null=True)

    # Whether this employee record represents an ongoing employment relationship or an archived one
    active = models.BooleanField(default=True)

    # The employee's department
    department = models.ForeignKey(Department, max_length=CHARFIELD_DEFAULT_MAX_LENGTH,
                                   on_delete=models.PROTECT)
    # The interval at which appointment reminders are to be displayed for the employee
    reminder_interval = models.IntegerField(default=24)

    def __str__(self):
        return " ".join([self.first_name, self.last_name])


class Appointment(models.Model):
    """
    A model containing the essential fields and behaviors of an appointment.
    """

    class Meta:
        ordering = ['date']

    # Date of the appointment
    date = models.DateField()

    # The employee for whom the appointment is scheduled
    # , related_name='appointments')
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)

    note = models.TextField(blank=True, default='')

    confirmed = models.BooleanField(default=False)


class Template(models.Model):
    """
    A model containing the essential fields and behaviors of a printable letter template.
    """

    class Meta:
        ordering = ['name']

    name = models.CharField(max_length=CHARFIELD_DEFAULT_MAX_LENGTH)
    description = models.TextField(blank=True, default='')
    template_body = models.TextField(blank=True, default='')


class AccountManager(BaseUserManager):
    """
    A custom manager for the Account custom user model.

    See https://docs.djangoproject.com/en/3.0/topics/auth/customizing/
    """

    def create_user(self, email, password=None, first_name=None, last_name=None, username=None, **kwargs):
        """
        Creates and saves a User with the given email, date of
        birth and password.

        Must accept all required model fields as parameters.
        """

        if not email:
            raise ValueError('Users must have a valid email address.')

        if not first_name:
            raise ValueError('Users must have a valid first name.')

        if not last_name:
            raise ValueError('Users must have a valid last name.')

        if not username:
            raise ValueError('Users must have a valid username.')

        account = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            **kwargs
        )
        account.set_password(password)
        account.save()
        return account

    def create_superuser(self, email, password, username, **kwargs):
        """
        Creates and saves a superuser with the given email and password.
        """
        account = self.create_user(
            email=email, password=password, username=username, **kwargs)
        account.is_superuser = True
        account.is_staff = True
        account.save()
        print(
            f"is_staff: {account.is_staff}, is_superuser: {account.is_superuser}, is_active: {account.is_active}")
        return account


class Account(PermissionsMixin, AbstractBaseUser):
    """
    A custom user model to add customizations and extensions on top of Django's User model.

    See https://docs.djangoproject.com/en/3.0/topics/auth/customizing/
    """
    class Meta:
        ordering = ['email']

    objects = AccountManager()

    # The name of the field that will serve as unique identifier for logging the user in
    USERNAME_FIELD = 'email'
    # should not contain USERNAME_FIELD nor password
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    first_name = models.CharField(max_length=CHARFIELD_DEFAULT_MAX_LENGTH)
    last_name = models.CharField(max_length=CHARFIELD_DEFAULT_MAX_LENGTH)
    email = models.EmailField(
        unique=True, verbose_name='email address', max_length=CHARFIELD_DEFAULT_MAX_LENGTH)
    username = models.CharField(
        max_length=CHARFIELD_DEFAULT_MAX_LENGTH, unique=True)

    #  Designates whether this user account should be considered active.
    #  This doesn’t necessarily control whether or not the user can log in.
    #  See https://docs.djangoproject.com/en/2.2/ref/contrib/auth/
    is_active = models.BooleanField(default=True)

    # Designates whether this user account will be able to log in to and use the Django administration interface.
    is_staff = models.BooleanField(default=False)

    # Designates whether this user account will be granted all existing permissions automatically.
    is_superuser = models.BooleanField(default=False)

    date_joined = models.DateTimeField(
        auto_now_add=True)  # Designates when the object was created and non-editable after that.

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email

    def get_full_name(self):
        return ' '.join([self.first_name, self.last_name])

    def get_short_name(self):
        return self.first_name
