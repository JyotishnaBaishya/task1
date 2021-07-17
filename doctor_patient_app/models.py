from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator

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