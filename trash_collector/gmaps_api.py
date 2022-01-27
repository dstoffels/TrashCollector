import requests
from gmaps_api_key import GOOGLE_MAPS_API_KEY

API_LINK = f'https://maps.googleapis.com/maps/api/js?key={GOOGLE_MAPS_API_KEY}&callback=initMap&v=weekly'

def geolocate(*args):
  location = ''
  for item in args:
    location += f'{item}+'
  request = requests.get(f'https://maps.googleapis.com/maps/api/geocode/json?address={location}&key={GOOGLE_MAPS_API_KEY}')
  response = request.json()
  result = response['results'][0]['geometry']['location']
  return { 'lat': result['lat'], 'lng': result['lng'] }

