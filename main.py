import requests
import pytz
import matplotlib.pyplot as plt
import cartopy.crs as ccrs

def wo_ist_die_iss():
    antwort = requests.get("http://api.open-notify.org/iss-now.json")
    if antwort.status_code == 200:
        daten = antwort.json()
        iss_position = daten["iss_position"]
        return iss_position
    else:
        return None

def iss_karte():
    iss_position = wo_ist_die_iss()
    if iss_position:
        lon = float(iss_position['longitude'])
        lat = float(iss_position['latitude'])

        # Create a new figure with a title
        plt.figure(num='ISS Tracking', facecolor='lightblue')

        # Now create your axes
        ax = plt.axes(projection=ccrs.PlateCarree())
        ax.stock_img()

        # Plot your data
        plt.plot(lon, lat, 'ro', markersize=10, transform=ccrs.Geodetic())

        # Set your title
        plt.title("Aktuelle Position der ISS")

        # Show your plot
        plt.show()

    else:
        print("Fehler beim Abrufen der ISS-Position!")

if __name__ == "__main__":
    iss_karte()
