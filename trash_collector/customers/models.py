from django.db import models

from gmaps_api import geolocate

class Customer(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey('accounts.User', blank=True, null=True, unique=True, on_delete=models.CASCADE)
    address = models.CharField(max_length=500)
    zip_code = models.CharField(max_length=5)
    weekly_pickup = models.CharField(max_length=9)
    one_time_pickup = models.DateField(null=True, blank=True)
    suspend_start = models.DateField(null=True, blank=True)
    suspend_end = models.DateField(null=True, blank=True)
    date_of_last_pickup = models.DateField(null=True, blank=True)
    balance = models.IntegerField(default=0)
    lat = models.FloatField(default=0)
    lng = models.FloatField(default=0)

    def convert_address(self):
        location = geolocate(self.address, self.zip_code)
        self.lat = location.lat
        self.lng = location.lng

    def __str__(self):
        return self.name