import requests
from datetime import datetime, timezone

MY_LAT = 32.820194
MY_LONG = -96.784688

parameters = {"lat": MY_LAT, "lng": MY_LONG, "formatted": 0}


def check_proximity():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])
    iss_latitude = 29.795
    iss_longitude = -96.78
    print(f"ISS LAT: {iss_latitude}")
    print(f"ISS LON: {iss_longitude}")

    # Your position is within +5 or -5 degrees of the ISS position.
    lat_check = -5 <= (iss_latitude - MY_LAT) <= 5
    lon_check = -5 <= (iss_longitude - MY_LONG) <= 5

    return lat_check and lon_check

def check_if_night():

    print(MY_LAT)
    print(MY_LONG)
    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    print(data)
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now(timezone.utc)
    return (time_now.hour <= sunrise) or (time_now.hour >= sunset)



if check_proximity():
    print("both values are true")
    if check_if_night():
        print("it's dark outside")
    else: print("too bright to see the ISS")
# If the ISS is close to my current position
# ,and it is currently dark
# Then email me to tell me to look up.
# BONUS: run the code every 60 seconds.
