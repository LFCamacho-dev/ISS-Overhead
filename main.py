import requests
from datetime import datetime

MY_LAT = 32.7942144
MY_LONG = -96.7835648


def check_proximity():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    # iss_latitude = float(data["iss_position"]["latitude"])
    # iss_longitude = float(data["iss_position"]["longitude"])
    iss_latitude = 27.795
    iss_longitude = -96.78
    print(f"ISS LAT: {iss_latitude}")
    print(f"ISS LON: {iss_longitude}")

    #Your position is within +5 or -5 degrees of the ISS position.
    lat_check = -5 <= (iss_latitude - MY_LAT) <= 5
    # print(f"{lat_check}: {iss_latitude - MY_LAT}")
    lon_check = -5 <= (iss_longitude - MY_LONG) <= 5

    return lat_check and lon_check


parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
}

response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
response.raise_for_status()
data = response.json()
sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

time_now = datetime.now()

print(check_proximity())
# If the ISS is close to my current position
# and it is currently dark
# Then email me to tell me to look up.
# BONUS: run the code every 60 seconds.



