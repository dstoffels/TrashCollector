import requests
from gmaps_api_key import GOOGLE_MAPS_API_KEY

API_LINK = f'https://maps.googleapis.com/maps/api/js?key={GOOGLE_MAPS_API_KEY}&callback=initMap&v=weekly'

class LatLng:
  def __init__(self, lat, lng):
    self.lat = lat
    self.lng = lng

def geolocate(*args):
  location = ''
  for item in args:
    location += f'{item}+'
  request = requests.get(f'https://maps.googleapis.com/maps/api/geocode/json?address={location}&key={GOOGLE_MAPS_API_KEY}')
  response = request.json()
  result = response['results'][0]['geometry']['location']
  return LatLng(result['lat'], result['lng'])

def average_latlng(customer_set):
  # customer_set = [item for item in customer_set]
  lats = 0
  lngs = 0
  for customer in customer_set:
    lats += customer.lat
    lngs += customer.lng

  lat = lats/len(customer_set)
  lng = lngs/len(customer_set)

  return LatLng(lat,lng)

