from django.shortcuts import  render, redirect
from .forms import NewUserForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.forms import AuthenticationForm
from django.views import View
from django.views.generic.edit import CreateView
from .models import User

def registerview(request):
	return render(request=request, template_name="RegisterHome.html")
class DoctorRegisterView(CreateView):
    model = User
    form_class=NewUserForm
    template_name = 'Register.html'
    def form_valid(self, form):
        user = form.save_doctor()
        return redirect('/')
class PatientRegisterView(CreateView):
    model = User
    form_class=NewUserForm
    template_name = 'Register.html'
    def form_valid(self, form):
        user = form.save_patient()
        return redirect('/')

def loginview(request):
    if request.method == "POST":
        form=AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password')
            user=authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                print(user.Doctor)
                print(user.Patient)
                if user.Patient:
                    return redirect('/patdashboard')
                elif user.Doctor:
                    return redirect('/docdashboard')
            else:
                messages.error(request,"Invalid username or password.")
        else:
            messages.error(request,"Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="Login.html", context={"login_form":form})

class DocdashView(View, LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.Doctor
    template_name="Docdash.html"
    def get(self,request, *args, **kwargs):
        return render(request, self.template_name)

class PatdashView(View, LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.Patient
    template_name="Patdash.html"
    def get(self,request, *args, **kwargs):
        return render(request, self.template_name)

def logout_request(request):
    logout(request)
    return redirect('/')