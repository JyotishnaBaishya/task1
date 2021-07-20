from django.urls import path
from . import views
from django.conf.urls import url

app_name = "main"


urlpatterns = [
	path('register/', views.registerview, name="register"),
	path('registerdoc/', views.DoctorRegisterView.as_view(), name="registerdoc"),
	path('', views.loginview, name="login"),
	path('registerpat', views.PatientRegisterView.as_view(), name="resregisterpat"),
	path('docdashboard', views.DocdashView.as_view(), name="docdash"),
	path('patdashboard', views.PatdashView.as_view(), name="patdash"),
	path('addpost', views.NewPost.as_view(), name='addpost'),
	path('editpost/<int:pk>', views.EditPost.as_view(), name='editpost'),
	path('myposts', views.MyPost.as_view(), name="myposts"),
	path('viewposts', views.ViewPost.as_view(), name="viewposts"),
	path('postcontent/<int:pk>', views.PostContent.as_view(), name="postcontent"),
	path('logout/', views.logout_request, name="logout"),
	]