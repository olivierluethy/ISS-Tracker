import requests
import datetime
import pytz
import ephem

# Fetch TLE data from Celestrak API
response = requests.get('https://www.celestrak.com/NORAD/elements/stations.txt')
data = response.content.decode('utf-8').strip().split('\n')

# Extract TLE data for ISS
name = data[0].strip()
line1 = data[1].strip()
line2 = data[2].strip()

# Set observer location to Lucerne
obs = ephem.Observer()
obs.lon = '8.30519'
obs.lat = '47.04936'
obs.elevation = 450 # meters above sea level

# Initialize ISS object with TLE data
iss = ephem.readtle(name, line1, line2)

# Calculate next time ISS is visible from Lucerne
obs.date = datetime.datetime.utcnow()
iss.compute(obs)
tr, azr, tt, altt, ts, azs = obs.next_pass(iss)
local_time = ephem.localtime(ts)
duration = int((altt - 0.25) * 24 * 60)
print("The ISS will be visible from Lucerne on {} for {} minutes".format(local_time, duration))