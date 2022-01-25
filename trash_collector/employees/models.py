from django.db import models

# Create your models here.

# TODO: Create an Employee model with properties required by the user stories

class Employee(models.Model):
  first_name = models.CharField(max_length=50)
  last_name = models.CharField(max_length=50)
  user = models.ForeignKey('accounts.User', blank=True, null=True, unique=True, on_delete=models.CASCADE)
  zip_code = models.CharField(max_length=5)