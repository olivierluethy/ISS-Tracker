import requests
import datetime
import pytz
import ephem
from geopy.geocoders import Nominatim

# Fetch TLE data from Celestrak API
response = requests.get('https://www.celestrak.com/NORAD/elements/stations.txt')
data = response.content.decode('utf-8').strip().split('\n')

# Extract TLE data for ISS
name = data[0].strip()
line1 = data[1].strip()
line2 = data[2].strip()

# Get location from user input
location_str = input("Enter the location you desire: ")
geolocator = Nominatim(user_agent="iss_tracker")
location = geolocator.geocode(location_str)

# Set observer location to user input location
obs = ephem.Observer()
obs.lat = str(location.latitude)
obs.lon = str(location.longitude)
obs.elevation = int(location.altitude)

# Initialize ISS object with TLE data
iss = ephem.readtle(name, line1, line2)

# Calculate next time ISS is visible from user input location
obs.date = datetime.datetime.utcnow()
iss.compute(obs)
tr, azr, tt, altt, ts, azs = obs.next_pass(iss)
local_time = ephem.localtime(ts)
duration = int((altt - 0.25) * 24 * 60)
print("The ISS will be visible from {} on {} for {} minutes".format(location_str, local_time, duration))