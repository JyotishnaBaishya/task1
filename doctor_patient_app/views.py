from django.shortcuts import  render, redirect
from .forms import NewUserForm, PostForm, CategoryForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.forms import AuthenticationForm
from django.views import View
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView
from .models import User, Post
from django import forms

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



def logout_request(request):
    logout(request)
    return redirect('/')