from django.db import models

from gmaps_api import geolocate
from .helpers import parse_date

class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    user = models.ForeignKey('accounts.User', blank=True, null=True, unique=True, on_delete=models.CASCADE)
    address = models.CharField(max_length=500)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=2, null=True)
    zip_code = models.CharField(max_length=5)
    weekly_pickup = models.CharField(max_length=9)
    one_time_pickup = models.DateField(null=True, blank=True)
    suspend_start = models.DateField(null=True, blank=True)
    suspend_end = models.DateField(null=True, blank=True)
    date_of_last_pickup = models.DateField(null=True, blank=True)
    balance = models.IntegerField(default=0)
    lat = models.FloatField(default=0)
    lng = models.FloatField(default=0)
    pickup_confirmed = models.BooleanField(default=False)

    def confirm_pickup(self, date):
        if self.date_of_last_pickup:
            self.pickup_confirmed = date <= self.date_of_last_pickup
            self.save()

    def convert_address(self):
        location = geolocate(self.address, self.city, self.state, self.zip_code)
        self.lat = location.lat
        self.lng = location.lng

    def __str__(self):
        return self.name