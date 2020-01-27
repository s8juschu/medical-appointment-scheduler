"""polls URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.urls import path
from django.conf.urls import include
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken.views import obtain_auth_token
from polls import views
from rest_framework import routers

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'accounts', views.AccountViewSet)
router.register(r'employees', views.EmployeeViewSet)
router.register(r'departments', views.DepartmentViewSet)
router.register(r'appointments', views.AppointmentViewSet)
router.register(r'templates', views.TemplateViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls'), name='api-auth'),
    # path('api-token-auth/', obtain_auth_token, name='api-token-auth'),
    path('gen-pdf/<int:pk>/', views.GenerateCoverLetterAsPDF.as_view(),
         name='pdf_generation'),
    path('gen-html/<int:pk>/', views.GenerateCoverLetterAsHtml.as_view(),
         name='html_generation'),
    path('update-template/', views.UpdateCoverLetterTemplate.as_view(),
         name='update_template'),
    path('get-template/', views.GetCoverLetterTemplateRaw.as_view(),
         name='get_template'),
    path('rest-auth/', include('rest_auth.urls')),
    path("templates/<int:pk>/<int:ek>/",
         views.FilledTemplateViewSet.as_view(), name="templates")
    # path('rest-auth/login/', views.LoginView.as_view(), name='rest-login'),
    #path('rest-auth/logout/', views.LogoutView.as_view(), name='rest-logout'),

    # path('drf-auth/login/', views.LoginView.as_view(), name='rest-login'),
    # path('drf-auth/logout/', views.LogoutView.as_view(), name='rest-logout'),
]
