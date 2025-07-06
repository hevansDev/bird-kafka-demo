import time
from datetime import datetime
import sys
import RPi.GPIO as GPIO
from hx711 import HX711

bird_present = False

BIRD_THRESHOLD = 5 # Lightest british songbird Goldcrest 5g

def cleanAndExit():
    print("Cleaning...")
        
    print("Bye!")
    sys.exit()

hx = HX711(5, 6)


hx.set_reading_format("MSB", "MSB")

referenceUnit = 416.71
hx.set_reference_unit(referenceUnit)

hx.reset()

hx.tare()

print("Tare done! Waiting for birds...")

def bird_landed(weight):
    """Called when a bird lands on the feeder"""
    print(f"🐦 Bird landed at {current_time.isoformat()}! Weight: {weight:.2f}g")

def bird_left():
    """Called when a bird leaves the feeder"""
    print(f"🦅 Bird left!")
    time.sleep(2)
    print("Tare done! Waiting for birds...")
    hx.tare()

while True:
    try:
        current_weight = hx.get_weight(5)
        current_time = datetime.now()
        val = hx.get_weight(5)

        if not bird_present and current_weight > BIRD_THRESHOLD:
            bird_present=True
            bird_landed(current_weight)
        
        elif bird_present and current_weight < BIRD_THRESHOLD:
            bird_present=False
            bird_left()

        hx.power_down()
        hx.power_up()
        time.sleep(0.1)

    except (KeyboardInterrupt, SystemExit):
        cleanAndExit()
