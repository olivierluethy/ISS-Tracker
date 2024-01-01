import requests
import pytz
import ephem
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from datetime import datetime

def wo_ist_die_iss():
    antwort = requests.get("http://api.open-notify.org/iss-now.json")
    if antwort.status_code == 200:
        daten = antwort.json()
        iss_position = daten["iss_position"]
        return iss_position
    else:
        return None

def checksum(line):
    L = line.strip()
    cksum = 0
    for i in range(68):
        c = L[i]
        if c in [' ', '.', '+'] or c.isalpha():
            continue
        elif c == '-':
            cksum += 1
        else:
            cksum += int(c)
    cksum %= 10
    return cksum

from datetime import datetime

def berechne_verbleibende_zeit(location_lat, location_lon):
    # TLE set for the ISS from: https://live.ariss.org/tle/
    line1 = '1 25544U 98067A   24001.66506447  .00052203  00000-0  91650-3 0  9991'
    line2 = '2 25544  51.6444  65.4073 0003179 343.4458 120.7618 15.50002034432578'
    
    # Validate the checksums
    if checksum(line1) != int(line1[-1]) or checksum(line2) != int(line2[-1]):
        print("Invalid TLE data!")
        return None

    iss = ephem.readtle('ISS', line1, line2)
    
    observer = ephem.Observer()
    observer.lat = str(location_lat)
    observer.lon = str(location_lon)
    
    next_pass = observer.next_pass(iss)
    rise_time = next_pass[0]
    
    # Convert the rise time to your local timezone
    local_tz = pytz.timezone('Europe/Zurich')  # Timezone for Lucerne
    rise_time = ephem.localtime(rise_time).replace(tzinfo=pytz.utc).astimezone(local_tz)
    
    # Calculate the remaining time in hours, minutes, and seconds
    now = datetime.now(local_tz)
    remaining_time = rise_time - now
    hours, remainder = divmod(remaining_time.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    remaining_time_str = f"{hours} hours, {minutes} minutes, {seconds} seconds"
    
    return remaining_time_str

def iss_karte(location_lat, location_lon):
    iss_position = wo_ist_die_iss()
    if iss_position:
        lon = float(iss_position['longitude'])
        lat = float(iss_position['latitude'])

        # Calculate the time until ISS reaches the specific location
        remaining_time = berechne_verbleibende_zeit(location_lat, location_lon)

        # Create a new figure with a title
        plt.figure(num='ISS Tracking', facecolor='lightblue')

        # Now create your axes
        ax = plt.axes(projection=ccrs.PlateCarree())
        ax.stock_img()

        # Plot ISS current position
        plt.plot(lon, lat, 'ro', markersize=10, transform=ccrs.Geodetic())

        # Set your title
        plt.title(f"Aktuelle Position der ISS\nVerbleibende Zeit bis zur Ankunft: {remaining_time}")

        # Show your plot
        plt.show()

    else:
        print("Fehler beim Abrufen der ISS-Position!")

def dms_to_dd(degrees, minutes, seconds, direction):
    dd = float(degrees) + float(minutes)/60 + float(seconds)/(60*60);
    if direction == 'S' or direction == 'W':
        dd *= -1
    return dd

def parse_location(location_str):
    try:
        # Try to parse the location as DD
        location = float(location_str)
        return location
    except ValueError:
        # If that fails, try to parse the location as DMS
        degrees, minutes, seconds, direction = location_str.split()
        location = dms_to_dd(degrees, minutes, seconds, direction)
        return location

if __name__ == "__main__":
    # Ask the user for the coordinates of the location they want
    print("For which location do you want to calculate?")
    location_lat_str = input("Enter the latitude (DD or DMS format): ")
    location_lon_str = input("Enter the longitude (DD or DMS format): ")
    
    # Parse the locations
    location_lat = parse_location(location_lat_str)
    location_lon = parse_location(location_lon_str)
    
    iss_karte(location_lat, location_lon)
