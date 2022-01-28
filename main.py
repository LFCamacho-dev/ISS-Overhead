import requests
from datetime import datetime, timezone
import time
import smtplib

# region MAIL AUTH
email = "*********@gmail.com"
password = "***************"
SMTP_SERVER = "smtp.gmail.com"
PORT = 587
SSL_PORT = 465
send_to = "**********@hotmail.com"
# endregion MAIL AUTH

MY_LAT = 32.820194
MY_LONG = -96.784688
start_time = time.time()

parameters = {"lat": MY_LAT, "lng": MY_LONG, "formatted": 0}


def check_proximity():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])
    # iss_latitude = 29.795  # for testing
    # iss_longitude = -96.78  # for testing

    print(f"ISS Latitude: {iss_latitude}, My Latitude: {MY_LAT}")
    print(f"ISS Longitude: {iss_longitude}, My Longitude: {MY_LONG}")

    # Your position is within +5 or -5 degrees of the ISS position.
    lat_check = -5 <= (iss_latitude - MY_LAT) <= 5
    lon_check = -5 <= (iss_longitude - MY_LONG) <= 5

    return lat_check and lon_check


def check_if_night():
    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    # print(data)
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now(timezone.utc)
    return (time_now.hour <= sunrise) or (time_now.hour >= sunset)


while True:
    if check_proximity():
        print("The ISS is in range!")
        if not check_if_night(): print("...but it's too bright out there to see it :(")
        elif check_if_night():
            print("Look up! you should be able to see it, sending email...")

            with smtplib.SMTP_SSL(SMTP_SERVER, SSL_PORT) as connection:
                connection.login(user=email, password=password)
                connection.sendmail(
                    from_addr=email,
                    to_addrs=send_to,
                    msg=f"Subject: LOOK UP!\n\n "
                        f"The ISS is right above you, look up!")

            print("Email sent :D")

    else: print("The ISS is too far to see...")

    time.sleep(60.0 - ((time.time() - start_time) % 60.0))
