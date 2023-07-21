import googlemaps
import re
import os
from dotenv import load_dotenv
from datetime import datetime
import prompt

# Load environment variables from .env fi
gmaps = googlemaps.Client(key='AIzaSyDJPjSk1d4yixAf-yosxQYYnXCSFjBAfy0')


# Geocoding an address
geocode_result = gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')

# Look up an address with reverse geocoding
reverse_geocode_result = gmaps.reverse_geocode((40.714224, -73.961452))



# Request directions via public transit
now = datetime.now()
directions_result = gmaps.directions("Sydney Town Hall",
                                     "Parramatta, NSW",
                                     mode="transit",
                                     departure_time=now)

start = "William Lyon Mackenzie Collegiate Institute"
end = "82 pantano drive thornhill"
transport = "transit"
directions = gmaps.directions(start, end, mode=transport, departure_time=now)


print(directions)