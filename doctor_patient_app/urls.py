from django.urls import path
from . import views
from django.conf.urls import url

app_name = "main"


urlpatterns = [
	path('register/', views.registerview, name="register"),
	path('registerdoc/', views.DoctorRegisterView.as_view(), name="registerdoc"),
	path('', views.loginview, name="login"),
	path('registerpat/', views.PatientRegisterView.as_view(), name="resregisterpat"),
	path('docdashboard/', views.DocdashView.as_view(), name="docdash"),
	path('patdashboard/', views.PatdashView.as_view(), name="patdash"),
	path('logout/', views.logout_request, name="logout"),
	]