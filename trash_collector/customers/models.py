from django.db import models
import requests

class Customer(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey('accounts.User', blank=True, null=True, unique=True, on_delete=models.CASCADE)
    address = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=5)
    weekly_pickup = models.CharField(max_length=9)
    one_time_pickup = models.DateField(null=True, blank=True)
    suspend_start = models.DateField(null=True, blank=True)
    suspend_end = models.DateField(null=True, blank=True)
    date_of_last_pickup = models.DateField(null=True, blank=True)
    balance = models.IntegerField(default=0)
    # geolocation = models.CharField(max_length=200, default='')
    lat = models.FloatField(default=0)
    lng = models.FloatField(default=0)

    def convert_address(self):
        request = requests.get(f'https://maps.googleapis.com/maps/api/geocode/json?address={self.address}+{self.zip_code}&key=AIzaSyAJcgG_ZuV1DtM0lq7chYco4AI75_KPx3U')
        response =  request.json()
        result = response['results'][0]

        self.lat = result['geometry']['location']['lat']
        self.lng = result['geometry']['location']['lng']

    def __str__(self):
        return self.name