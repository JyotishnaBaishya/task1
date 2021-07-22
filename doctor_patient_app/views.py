from django.shortcuts import  render, redirect
from .forms import NewUserForm, PostForm, CategoryForm, AppointmentForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.forms import AuthenticationForm
from django.views import View
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView
from .models import User, Post
import json, csv, os, datetime
import requests
from django.conf import settings
import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

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

class DocdashView(LoginRequiredMixin,UserPassesTestMixin,View):
    login_url = '/'
    redirect_field_name = 'redirect_to'
    def test_func(self):
        return self.request.user.Doctor
    template_name="Docdash.html"
    def get(self,request, *args, **kwargs):
        return render(request, self.template_name)

class PatdashView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.Patient
    login_url = '/'
    redirect_field_name = 'redirect_to'
    template_name="Patdash.html"
    def get(self,request, *args, **kwargs):
        return render(request, self.template_name)

class NewPost( LoginRequiredMixin, UserPassesTestMixin,CreateView):
    def test_func(self):
        return self.request.user.Doctor
    login_url = '/'
    model=Post
    form_class=PostForm
    template_name='Post.html'
    def form_valid(self, form):
        form.instance.doc = self.request.user
        return super().form_valid(form)
    success_url ='/myposts'

class EditPost(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    def test_func(self):
        return self.request.user.Doctor
    login_url='/'
    model=Post
    form_class=PostForm
    template_name='Post.html'
    success_url='/myposts'
    def get(self, request, pk):
        sad=Post.objects.get(pk=pk).save_as_draft
        print(sad)
        if not sad:
            return redirect('/myposts')
        else:
            return super(EditPost, self).get(request, pk)

class MyPost(LoginRequiredMixin, UserPassesTestMixin, ListView):
    def test_func(self):
        return self.request.user.Doctor
    login_url='/'
    model=Post
    context_object_name = 'posts'
    template_name='Post_List.html'
    def get_queryset(self):
        cat=self.request.GET.get('category', '')
        queryset=None
        print(cat)
        if not cat or cat=='AL':
            queryset = Post.objects.filter(doc=self.request.user).order_by('save_as_draft')
        else:
            queryset = Post.objects.filter(doc=self.request.user,category=cat)
        return queryset
    def get_context_data(self, **kwargs):
        con = super(MyPost, self).get_context_data(**kwargs)
        con['cat']=CategoryForm()
        return con

class ViewPost(LoginRequiredMixin, UserPassesTestMixin, ListView):
    def test_func(self):
        return self.request.user.Patient
    login_url='/'
    model=Post
    context_object_name = 'posts'
    template_name='View_List.html'
    def get_queryset(self):
        cat=self.request.GET.get('category', '')
        queryset=None
        print(cat)
        if not cat or cat=='AL':
            queryset = Post.objects.filter(save_as_draft=False).select_related('doc')
        else:
            queryset = Post.objects.filter(category=cat, save_as_draft=False).select_related('doc')
        print(queryset)
        return queryset
    def get_context_data(self, **kwargs):
        con = super(ViewPost, self).get_context_data(**kwargs)
        con['cat']=CategoryForm()
        return con

class PostContent(LoginRequiredMixin, DetailView):
    login_url='/'
    model=Post
    template_name='PostContent.html'
    def get(self, request, pk):
        sad=Post.objects.get(pk=pk).save_as_draft
        print(sad)
        if self.request.user.Patient and sad:
            return redirect('/viewposts')
        else:
            return super(PostContent, self).get(request, pk)

    def get_context_data(self, **kwargs):
        con = super(PostContent, self).get_context_data(**kwargs)
        if self.request.user.Doctor:
            con['temp']="Docdash.html"
        else:
            con['temp']="Patdash.html"
        return con

class ViewDoctor(LoginRequiredMixin, UserPassesTestMixin, ListView):
    def test_func(self):
        return self.request.user.Patient
    login_url='/'
    model=User
    context_object_name = 'doctors'
    template_name='Doctor_List.html'
    def get_queryset(self):
        queryset = User.objects.filter(Doctor=True)
        return queryset

class AppointmentView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.Patient
    login_url='/'
    def get(self, request, pk):
        form=AppointmentForm()
        return render(template_name="Appointment_Form.html", request=request, context={'form': form})
    def post(self, request, pk):
        form=AuthenticationForm(request, data=request.POST)
        speciality=form.data.get('speciality')
        date=form.data.get('date')
        time=form.data.get('time')
        time+=':00'
        st= datetime.datetime.strptime(time,"%H:%M:%S")
        et= st+datetime.timedelta(minutes=45)
        start=date+'T'+time+'+05:30'
        end=date+'T'+str(et.time())+'+05:30'
        name=self.request.user.first_name+' '+self.request.user.last_name
        event = {
                'summary': 'Appointment with '+name+' ,speciality= '+speciality,
                'start': {
                    'dateTime': start,
                },
                'end': {
                    'dateTime': end,
                },
                # 'attendees': [
                #     {'email': 'lpage@example.com'},
                #     {'email': 'sbrin@example.com'},
                # ],
                'reminders': {
                    'useDefault': False,
                    'overrides': [
                    {'method': 'email', 'minutes': 24 * 60},
                    {'method': 'popup', 'minutes': 10},
                    ],
                },
                }
        doc=User.objects.get(pk=pk)
        # print(doc.email)
        # print(doc.doctor_auth)
        if doc.doctor_auth is None:
            return render(template_name="Success.html", request=request, context={"msg":"Not Available"})
        c=json.loads(doc.doctor_auth)
        creds={'token': c['access_token'],
            'refresh_token': c['refresh_token'],
            'token_uri': settings.TOKEN_URI,
            'client_id': settings.CLIENT_ID,
            'client_secret': settings.CLIENT_SECRET,
            'scopes': c['scope']}
        credentials = google.oauth2.credentials.Credentials(**creds)
        service = googleapiclient.discovery.build(
            'calendar', 'v3', credentials=credentials)
        event = service.events().insert(calendarId='primary', body=event).execute()
        credentials=json.loads(credentials.to_json())
        creds={'access_token': credentials['token'],
            'refresh_token': credentials['refresh_token'],
            'scope': credentials['scopes']}
        print(event)
        doc.doctor_auth=json.dumps(creds)
        doc.save()
        return render(template_name="Success.html", request=request, context={"msg":"Appoinment Booked!", 'st':st.time(), 'et': et.time(), 'doctor': doc.first_name+' '+doc.last_name, 'date': date})


class AuthorizeView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.Doctor
    login_url='/'
    def get(self, request):
        if request.user.doctor_auth is not None:
            return redirect('/docdashboard')
        CLIENT_SECRETS_FILE = "doctor_patient_app/client_secret.json"
        SCOPES = ['https://www.googleapis.com/auth/calendar.events']
        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(CLIENT_SECRETS_FILE, scopes=SCOPES)
        flow.redirect_uri = "http://localhost:8000/complete"
        authorization_url, state = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true',
            login_hint=self.request.user.email)
        request.session['state'] = state
        print(state)
        print(request.session['state'])
        return redirect(authorization_url)

class CompleteView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.Doctor
    login_url='/'
    def get(self, request):
        state = request.session['state']
        CLIENT_SECRETS_FILE = "doctor_patient_app/client_secret.json"
        SCOPES = ['https://www.googleapis.com/auth/calendar.events']
        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(CLIENT_SECRETS_FILE, scopes=SCOPES, state=state)
        flow.redirect_uri = "http://localhost:8000/complete"
        authorization_response=request.get_full_path()
        credentials=flow.fetch_token(authorization_response=authorization_response)
        print(credentials)
        user=User.objects.get(username=request.user)
        user.doctor_auth=json.dumps(credentials)
        user.save()
        return redirect('/docdashboard')


class RevokeView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.Doctor
    login_url='/'
    def get(self, request):
        if not request.user.doctor_auth:
            return redirect('/docdashboard')
        xyz=json.loads(request.user.doctor_auth)
        print(xyz)
        revoke = requests.post('https://oauth2.googleapis.com/revoke',
            params={'token': xyz["access_token"]},
            headers = {'content-type': 'application/x-www-form-urlencoded'})

        status_code = getattr(revoke, 'status_code')
        print(status_code)
        print("OK")
        user=User.objects.get(username=request.user)
        user.doctor_auth=None
        user.save()
        print(request.user.doctor_auth)
        return redirect('/docdashboard')

def logout_request(request):
    logout(request)
    return redirect('/')


