from django.http import HttpResponse, Http404
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.contrib.auth.mixins import UserPassesTestMixin, AccessMixin
from django.utils import timezone
from django.utils.safestring import mark_safe
from rest_framework import status, mixins, generics, permissions, viewsets
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from polls.models import Employee, Department, Account, Template, Appointment
from polls.serializers import EmployeeSerializer, DepartmentSerializer, AccountSerializer, AppointmentSerializer, \
    TemplateSerializer
from polls.permissions import IsAccountOwner
from django.views.generic import ListView
from django.db.models import Q, F
from django_filters import rest_framework as filters
from datetime import date
from rest_framework.decorators import action
from polls.utils import render_to_pdf, render_to_html, fill_template
import json
import datetime
import calendar


@api_view(['GET'])
def api_root(request, format=None):
    """
    A function-based view for the root of the API.
    """
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'employees': reverse('employee-list', request=request, format=format),
        'departments': reverse('department-list', request=request, format=format)
    })


class EmployeeFilter(filters.FilterSet):
    """
    A filter which determines attributes by which employees can be filtered.
    """

    firstname = filters.CharFilter(field_name="first_name", lookup_expr='contains')
    lastname = filters.CharFilter(field_name="last_name", lookup_expr='contains')
    e_id = filters.CharFilter(field_name="employee_id", lookup_expr='startswith')
    reminder_before = filters.DateFilter(field_name="next_reminder", lookup_expr='lte')
    reminder_after = filters.DateFilter(field_name="next_reminder", lookup_expr='gte')

    class Meta:
        model = Employee
        fields = ['firstname', 'lastname', 'e_id', 'gender', 'date_of_birth', 'date_of_entry', 'wants_reminder', 'active',
                  'reminder_after', 'reminder_before']


class EmployeeViewSet(viewsets.ModelViewSet):
    """
    ViewSet for the `polls.models.Employee` model.
    Provides endpoints or listing, creating, updating and modifying employees.
    """
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    # permission_classes = [permissions.IsAuthenticated]

    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = EmployeeFilter


class TemplateViewSet(viewsets.ModelViewSet):
    """
    ViewSet for the `polls.models.Template` model.
    Provides endpoints or listing, creating, updating and modifying printable letter templates.
    """
    queryset = Template.objects.all()
    serializer_class = TemplateSerializer
    # permission_classes = [permissions.IsAuthenticated]


class FilledTemplateViewSet(APIView):
    def get(self, request, pk, ek, format=None):
        print(pk)
        employee = Employee.objects.get(pk=ek)
        template = Template.objects.get(pk=pk)

        serializer = EmployeeSerializer(employee)
        html = fill_template(template.template_body, serializer.data)

        if html:
            return HttpResponse(json.dumps({"template_body": html, "name": template.name}), content_type='application/json')
        else:
            return Response({
                'status': 'Internal Error',
                'message': 'HTML could not be generated'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DepartmentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for the `polls.models.Department` model.
    Provides endpoints or listing, creating, updating and modifying departments.
    """
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    # permission_classes = [permissions.IsAuthenticated]


class AppointmentFilter(filters.FilterSet):
    """
    Determines by which attributes appointments can be filtered.
    """

    min_date = filters.DateFilter(field_name="date", lookup_expr='gte')
    max_date = filters.DateFilter(field_name="date", lookup_expr='lte')

    class Meta:
        model = Appointment
        fields = ['min_date', 'max_date', 'employee']


class AppointmentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for the `polls.models.Appointment` model.
    """
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    # permission_classes = [permissions.IsAuthenticated]

    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = AppointmentFilter


class AccountViewSet(viewsets.ModelViewSet):
    """
    ViewSet for the `polls.models.Account` custom user model.
    """
    lookup_field = 'id'
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    # permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return permissions.AllowAny(),
        if self.request.method == 'POST':
            return permissions.AllowAny(),
        return permissions.IsAuthenticated(), IsAccountOwner(),

    def create(self, request, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.run_validation(request.data)
        if serializer.is_valid():
            Account.objects.create_user(**serializer.validated_data)
            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)
        return Response({
            'status': 'Bad request',
            'message': f'Account could not be created with received data: {request.data}'
        }, status=status.HTTP_400_BAD_REQUEST)


class LoginView(UserPassesTestMixin, APIView):
    def test_func(self):
        """
        See UserPassesTestMixin.
        """
        # TODO: implement email check
        return True

    def post(self, request, format=None):
        data = json.loads(request.body)

        email = data.get('email', None)
        password = data.get('password', None)

        account = authenticate(email=email, password=password)

        if account is not None:
            if account.is_active:
                login(request, account)

                serialized = AccountSerializer(account)

                return Response(serialized.data)
            else:
                return Response({
                    'status': 'Unauthorized',
                    'message': 'This account has been disabled.'
                }, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({
                'status': 'Unauthorized',
                'message': 'Username/password combination invalid.'
            }, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    # permission_classes = [permissions.IsAuthenticated,]

    def post(self, request, format=None):
        logout(request)
        return Response({}, status=status.HTTP_204_NO_CONTENT)


# employee details are taken from the database matching the pk
# pdf rendered from the cover letter template passing the employee details(currently just last name necessary)
# returns PDF file on success
class GenerateCoverLetterAsPDF(APIView):
    def get_employee(self, pk):
        try:
            return Employee.objects.get(pk=pk)
        except Employee.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        employee_obj = self.get_employee(pk)

        today = timezone.now()
        # dictionary as expected by the renderer
        employee = {"employee": {
            'first_name': employee_obj.first_name,
            'last_name': employee_obj.last_name,
            'id': employee_obj.id,
            'gender': employee_obj.gender,
            'department': employee_obj.department,
        },
            'today': today
        }
        pdf = render_to_pdf('cover_letter/cover_letter.html', employee)

        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            return response
        else:
            return Response({
                'status': 'Internal Error',
                'message': 'PDF could not be generated'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# employee details are taken from the database matching the pk
# html rendered from the cover letter template passing the employee details(currently just last name necessary)
# returns HTML file on success
class GenerateCoverLetterAsHtml(APIView):
    def get_employee(self, pk):
        try:
            return Employee.objects.get(pk=pk)
        except Employee.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        employee_obj = self.get_employee(pk)
        today = timezone.now()
        employee = {"employee": {
            'first_name': employee_obj.first_name,
            'last_name': employee_obj.last_name,
            'id': employee_obj.id,
            'gender': employee_obj.gender,
            'department': employee_obj.department,
        },
            'today': today
        }
        html = render_to_html('cover_letter/cover_letter.html', employee)

        if html:
            response = HttpResponse(html, content_type='text/html')
            return response
        else:
            return Response({
                'status': 'Internal Error',
                'message': 'HTML could not be generated'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# overwrites the coverletter template with the data from POST request
# complete html has to be send from the front end as it is just a blind write here
class UpdateCoverLetterTemplate(APIView):
    def post(self, request, format=None):
        # overwrites the template everytime on a post
        with open("templates/cover_letter/cover_letter.html", "w") as temp_file:
            new_template_string = str(request.body.decode("utf-8"))

            new_template_string = new_template_string.replace('\\n', '')
            try:
                temp_file.write(new_template_string)
                temp_file.close()
                return HttpResponse(status.HTTP_200_OK)
            except IOError as e:
                print("Couldn't open or write to file (%s)." % e)
                temp_file.close()
                return Response({
                    'status': 'Internal Error',
                    'message': 'Template could not be saved'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# returns the plane cover letter template
class GetCoverLetterTemplateRaw(APIView):
    def get(self, request, format=None):
        with open("templates/cover_letter/cover_letter.html", "r") as template_raw:

            if template_raw:
                response = HttpResponse(template_raw, content_type='text/html')
                return response
            else:
                return Response({
                    'status': 'Internal Error',
                    'message': 'HTML could not be generated'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
