from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings


class User(AbstractUser):
	Doctor = models.BooleanField(default=False)
	Patient = models.BooleanField(default=False)
	email = models.EmailField(unique=True, blank=False)
	first_name=models.CharField(max_length=50, null=False, blank=False)
	last_name=models.CharField(max_length=50 ,null=False, blank=False)
	Profile_Image = models.ImageField(upload_to='uploads/', null=True, blank=True, default="uploads/default.png")
	Address_Line_1 = models.CharField(max_length=100)
	City=models.CharField(max_length=50)
	State=models.CharField(max_length=50)
	Pin_Code = models.IntegerField(validators=[MaxValueValidator(999999), MinValueValidator(10000)])

class Post(models.Model):
	MENTAL_HEALTH='MH'
	HEART_DISEASE='HD'
	COVID19='CV'
	IMMUNISATION='IM'
	CATEGORY_CHOICES =[
		(MENTAL_HEALTH, 'Mental Health'),
		(HEART_DISEASE, 'Heart Disease'),
		(COVID19, 'Covid19'),
		(IMMUNISATION, 'Immunisation'),
	]
	doc = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
	title=models.CharField(max_length=100)
	image=models.ImageField(upload_to='post/', null=False, blank=False, default="posts/default.png")
	category=models.CharField(max_length=2, choices=CATEGORY_CHOICES, null=False, blank=False, default=None)
	summary=models.CharField(max_length=1000)
	content=models.TextField()
	save_as_draft=models.BooleanField(default=True)
