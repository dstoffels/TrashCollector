import requests
from api_keys import GOOGLE_MAPS_API_KEY

LINK = f'https://maps.googleapis.com/maps/api/js?key={GOOGLE_MAPS_API_KEY}&callback=initMap&v=weekly'

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

def average_latlng(customer_set, employee_zip):
  lat = 0
  lng = 0
  for customer in customer_set:
    lat += customer.lat
    lng += customer.lng

  if len(customer_set) > 0:
    lat /= len(customer_set)
    lng /= len(customer_set)
  else:
    employee_coords = geolocate(employee_zip)
    lat = employee_coords.lat
    lng = employee_coords.lng

  return LatLng(lat,lng)

