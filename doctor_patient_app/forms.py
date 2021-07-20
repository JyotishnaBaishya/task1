from django import forms
from crispy_forms.helper import FormHelper
from django.contrib.auth.forms import UserCreationForm
from .models import User, Post

class NewUserForm(UserCreationForm):
	# First_Name = forms.CharField(max_length=100)

	# mobile = PhoneNumberField()
	# Captcha = CaptchaField()
	class Meta:
		model = User
		fields=("username", "first_name", "last_name","email","Profile_Image", "Address_Line_1", "City", "State", "Pin_Code", "password1", "password2")

	def save_doctor(self):
		user = super().save(commit=True)
		user.Doctor = True
		user.save()
		return user

	def save_patient(self):
		user = super().save(commit=True)
		user.Patient = True
		user.save()
		return user

class PostForm(forms.ModelForm):
	image=forms.ImageField(required=False, widget=forms.FileInput)
	summary= forms.CharField(required=True, widget=forms.Textarea(attrs={'rows': 3}))
	class Meta:
		model=Post
		fields=['title', 'image','category','summary','content', 'save_as_draft']

class CategoryForm(forms.Form):
	ALL='AL'
	MENTAL_HEALTH='MH'
	HEART_DISEASE='HD'
	COVID19='CV'
	IMMUNISATION='IM'
	CATEGORY_CHOICES =[
		(ALL, 'All'),
		(MENTAL_HEALTH, 'Mental Health'),
		(HEART_DISEASE, 'Heart Disease'),
		(COVID19, 'Covid19'),
		(IMMUNISATION, 'Immunisation'),
	]
	category=forms.ChoiceField(choices=CATEGORY_CHOICES)
	def __init__(self, *args, **kwargs):
		super(CategoryForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_show_labels = False