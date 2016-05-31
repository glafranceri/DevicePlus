
# umbrella_stand.py

'''
## License

The MIT License (MIT)

GrovePi for the Raspberry Pi: an open source platform for connecting Grove Sensors
to the Raspberry Pi. Copyright (C) 2015  Dexter Industries

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
'''

# This is a project that uses the Grove LED, and buzzer attached to an umbrella
# stand to give a visual and audio notification to remind people to take their
# umbrella if it's raining or going to rain that day.

# You will need to modify the first few lines for this project work for you.
# Fee free to modify the rest of the program to make it
# behave the way you want it to.


# Enter your 5-digit zip code (or Postal Code) on the following line.
zipcode = 'YOUR_ZIP_CODE'

# Once you have gotten an API Key from Wunderground (see tutorial),
# pleave provide it here.
api_key = 'YOUR_API_KEY'

# this is the delay between each polling of Wunderground.
# It's set to poll once every 5 minutes.
# You may prefer a faster polling.
# the Wunderground free account does set a 500 poll per day limit.
DELAY = 5*60  # in seconds

# Do you prefer to work in metric or imperial?
# set METRIC to 1 to use the metric system
# set METRIC to 0 to use imperial system
METRIC = 0

# Rain threshold: what's your safety zone before you need an umbrella?
# if METRIC is set to 1, this will be in millimeters
# if METRIC is set to 0, this will be in inches
RAIN_THRESHOLD = 0

# This set the set the distance from the stand that the buzzer will active
# and give a audio notification that there is rain in the forcast
# Grove Rangefinder uses Centimeters
PROXIMITY = 60

# Connect the LED to D7
rainled = 7

# Connect the Ultrasonic Ranger to D4
ranger = 4

# Connect the Buzzer to D8
buzzer = 8

#################################################################################
# nothing needs to be modified after this
# if you are familiar with Python, feel free to change anything to improve this
# we welcome additions and suggestions
#################################################################################

import urllib2
import json
from grovepi import *
import time
import sys

digitalWrite(rainled, 0)
digitalWrite(buzzer, 0)

def assign_rain(status):
    if status is True:  # there will be rain
        # Light the RAIN LED on the umbrella stand
        led_blink(DELAY)  
    else:  # no rain in forecast
        # turn off the RAIN LED on the umbrella
        digitalWrite(rainled, 0)
        time.sleep(DELAY)

def led_blink(blinkdelay):
    count = 0.0
    blinkrate = 0.4
    while count < float(blinkdelay):
        digitalWrite(rainled, 1)
        time.sleep(blinkrate)
        distance=ultrasonicRead(ranger)
        if distance <= float(PROXIMITY):
            digitalWrite(buzzer, 1)
        else:
            digitalWrite(buzzer, 0)
        digitalWrite(rainled, 0)
        time.sleep(blinkrate)
        count += (2*blinkrate)

#########################################################################################

# wunderground api url
url = 'http://api.wunderground.com/api/' + api_key + '/conditions/q/' + zipcode + '.json'

pinMode(ranger,"INPUT")
pinMode(buzzer,"OUTPUT")
pinMode(rainled, "OUTPUT")

if len(sys.argv) > 1 and sys.argv[1] == 'test':
    try:
        led_blink(5)
    except KeyboardInterrupt:
        digitalWrite(rainled, 0)
    quit()

try:
    while True:
        f = urllib2.urlopen(url)
        json_string = f.read()
        f.close()
        parsed_json = json.loads(json_string)

        if METRIC is 0:
            precip_today = parsed_json['current_observation']['precip_today_in']
        else:
            precip_today = parsed_json['current_observation']['precip_today_metric']

        if float(precip_today) > float(RAIN_THRESHOLD):
            print("Rain today, take the umbrella")
            assign_rain(True)
        else:
            print("No Rain today")
            assign_rain(False)


except KeyboardInterrupt:
    digitalWrite(buzzer, 0)
    digitalWrite(rainled, 0)
