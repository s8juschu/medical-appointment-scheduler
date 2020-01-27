"""
This file defines the serializers used in this project.

Serializers allow complex data such as querysets and model instances
 to be converted to native Python datatypes that can then be easily
 rendered into JSON, XML or other content types. Serializers also
 provide deserialization, allowing parsed data to be converted back
 into complex types, after first validating the incoming data.

For more information, see
https://www.django-rest-framework.org/api-guide/serializers/

Note:
    It is strongly recommended that you explicitly set all fields
    that should be serialized using the fields attribute. This will
    make it less likely to result in unintentionally exposing data
    when your models change.
"""

from django.contrib.auth.models import User
from monthdelta import monthdelta
from rest_framework import serializers
from polls.models import Employee, Department, Account, Appointment, Template
from django.contrib.auth import update_session_auth_hash


class EmployeeSerializer(serializers.ModelSerializer):
    """
    Serializer for `polls.models.Appointment`.
    """
    # appointment_set = serializers.HyperlinkedRelatedField(queryset=Appointment.objects.all(), many=True,
    #                                                       read_only=False, view_name='appointment-detail')
    # appointment_set = AppointmentSerializer(many=True, read_only=False)
    date_of_birth = serializers.DateField(
        format="%d.%m.%Y", input_formats=["%d.%m.%Y", "%Y-%m-%d"])
    date_of_entry = serializers.DateField(
        format="%d.%m.%Y", input_formats=["%d.%m.%Y", "%Y-%m-%d"])
    date_of_exit = serializers.DateField(
        format="%d.%m.%Y", input_formats=["%d.%m.%Y", "%Y-%m-%d"], required=False, allow_null=True)
    next_reminder = serializers.DateField(
        format="%d.%m.%Y", input_formats=["%d.%m.%Y", "%Y-%m-%d"], required=False, allow_null=True)

    class Meta:
        model = Employee
        fields = ['id', 'first_name', 'last_name', 'gender',
                  'date_of_birth', 'date_of_entry', 'date_of_exit',
                  'employee_id', 'department', 'wants_reminder', 'next_reminder',
                  'reminder_interval', 'notes', 'active', ]
        id = serializers.IntegerField(read_only=True)

    # automatically sets next_reminder field to date_of_entry when creating employee
    def create(self, validated_data):
        employee = Employee.objects.create(**validated_data)
        employee.next_reminder = employee.date_of_entry
        employee.save()
        return employee


class AppointmentSerializer(serializers.ModelSerializer):
    """
    Serializer for `polls.models.Appointment`.
    """

    # employee_set = EmployeeSerializer()
    date = serializers.DateField(
        format="%d.%m.%Y", input_formats=["%d.%m.%Y", "%Y-%m-%d"])

    class Meta:
        model = Appointment
        fields = ['id', 'date', 'employee', 'note', ]
        id = serializers.IntegerField(read_only=True)

    # automatically sets next_reminder of employee to date of last appointment plus reminder interval
    def create(self, validated_data):
        appointment = Appointment.objects.create(**validated_data)
        employee = appointment.employee
        employee.next_reminder = Appointment.objects.filter(employee=employee).latest('date').date + monthdelta(
            months=employee.reminder_interval)
        employee.reminder_interval = employee.department.reminder_interval
        employee.save()
        return appointment

    # automatically sets next_reminder of employee to date of last appointment plus reminder interval
    def update(self, instance, validated_data):
        instance.id = validated_data.get('id', instance.id)
        instance.date = validated_data.get('date', instance.date)
        instance.employee = validated_data.get('employee', instance.employee)
        instance.save()
        employee = instance.employee
        employee.next_reminder = Appointment.objects.filter(employee=employee).latest('date').date + monthdelta(
            months=employee.reminder_interval)
        employee.save()
        return instance


class TemplateSerializer(serializers.ModelSerializer):
    """
    Serializer for `polls.models.Template`.
    """

    class Meta:
        model = Template
        fields = ['id', 'name', 'description', 'template_body']


class DepartmentSerializer(serializers.ModelSerializer):
    """
    Serializer for `polls.models.Department`.
    """
    employee_set = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name='employee-detail')

    class Meta:
        model = Department
        fields = ['id', 'name', 'employee_set', ]
        id = serializers.IntegerField(read_only=True)


class AccountSerializer(serializers.ModelSerializer):
    """
    Serializer for `polls.models.Account`.
    """

    password = serializers.CharField(write_only=True, required=False)

    # confirm_password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Account
        fields = ('id', 'email', 'username', 'first_name', 'last_name',
                  'password', 'date_joined', 'updated_at',)

        read_only_fields = ('date_joined', 'updated_at',)

        def create(self, validated_data):
            password = validated_data.get('password', None)
            # confirm_password = validated_data.get('confirm_password', None)

            # if password and confirm_password and password == confirm_password:
            #     print(validated_data)
            #     del(validated_data['confirm_password'])
            #     return Account.objects.create(**validated_data)
            # raise RuntimeError('Password and confirmed password do not match!')

            return Account.objects.create(**validated_data)

        def update(self, instance, validated_data):
            instance.username = validated_data.get(
                'username', instance.username)

            instance.save()

            password = validated_data.get('password', None)
            confirm_password = validated_data.get('confirm_password', None)

            if password and confirm_password and password == confirm_password:
                instance.set_password(password)
                instance.save()

            update_session_auth_hash(self.context.get('request'), instance)

            return instance
