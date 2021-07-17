from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

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