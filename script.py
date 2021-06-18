'''
Script: Covid Vaccine Slot Availability Notifier
By Ayushi Rawat
'''

import requests
from pygame import mixer
from datetime import datetime, timedelta
import time

# Insert search parameters here
age = 19
pincodes = ["641011"]
num_days = 6
dose = 1
polling_interval = 3

print_flag = 'Y'

print("Starting search for Covid vaccine slots!")

actual = datetime.today()
list_format = [actual + timedelta(days=i) for i in range(num_days)]
actual_dates = [i.strftime("%d-%m-%Y") for i in list_format]

num_searches = 0
while True:
    counter = 0
    for pincode in pincodes:
        for given_date in actual_dates:

            URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={}&date={}".format(
                pincode, given_date)
            header = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}

            result = requests.get(URL, headers=header)

            if result.ok:
                response_json = result.json()
                if response_json["centers"]:
                    if(print_flag.lower() == 'y'):
                        for center in response_json["centers"]:
                            for session in center["sessions"]:
                                if (session["min_age_limit"] <= age and session[f"available_capacity_dose{dose}"] > 0):
                                    print('Pincode: ' + pincode)
                                    print("Available on: {}".format(given_date))
                                    print("\t", center["name"])
                                    print("\t", center["block_name"])
                                    print("\t Age: ", session["min_age_limit"])
                                    print("\t Price: ", center["fee_type"])
                                    print("\t Availablity : ",
                                          session["available_capacity"])
                                    print("\t Dose: ", dose)

                                    if(session["vaccine"] != ''):
                                        print("\t Vaccine type: ", session["vaccine"])
                                    print("\n")
                                    counter = counter + 1
            else:
                print("No Response!")

    if counter == 0:
        print("No Vaccination slot available!, Search number:", num_searches)
        num_searches += 1
    else:
        mixer.init()
        mixer.music.load('sound/dingdong.wav')
        mixer.music.play()
        print("Search Completed! Slots available")

    dt = datetime.now() + timedelta(minutes=3)

    while datetime.now() < dt:
        time.sleep(1)
