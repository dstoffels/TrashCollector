from django.db import models

# Create your models here.

class Employee(models.Model):
  first_name = models.CharField(max_length=50)
  last_name = models.CharField(max_length=50)
  user = models.ForeignKey('accounts.User', blank=True, null=True, unique=True, on_delete=models.CASCADE)
  zip_code = models.CharField(max_length=5)
  pickups_active = models.BooleanField(default=False)

  def toggle_pickups(self):
    self.pickups_active = not self.pickups_active
    self.save()