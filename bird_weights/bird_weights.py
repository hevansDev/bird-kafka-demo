import time
from datetime import datetime
import sys
import RPi.GPIO as GPIO
from hx711 import HX711

bird_present = False

BIRD_THRESHOLD = 5  # Lightest british songbird Goldcrest 5g

def cleanAndExit():
    print("Cleaning...")
    print("Bye!")
    sys.exit()

def get_stable_weight(hx, samples=15):
    """Get a stable weight reading by taking multiple samples and filtering outliers"""
    readings = []
    
    for i in range(samples):
        reading = hx.get_weight(1)
        readings.append(reading)
        time.sleep(0.05)  # Small delay between readings
    
    # Sort readings to identify outliers
    readings.sort()
    
    # Remove extreme outliers (top and bottom 20%)
    outliers_to_remove = max(1, samples // 5)  # Remove at least 1, or 20%
    trimmed = readings[outliers_to_remove:-outliers_to_remove]
    
    # Calculate average of remaining readings
    if len(trimmed) > 0:
        stable_weight = sum(trimmed) / len(trimmed)
    else:
        stable_weight = readings[len(readings)//2]  # Fallback to median
    
    return stable_weight

def bird_landed(weight):
    """Called when a bird lands on the feeder"""
    print(f"🐦 Bird landed at {current_time.isoformat()}! Weight: {weight:.2f}g")

def bird_left():
    """Called when a bird leaves the feeder"""
    print(f"🦅 Bird left!")
    time.sleep(2)
    print("Tare done! Waiting for birds...")
    hx.tare()

# Setup HX711
hx = HX711(5, 6)
hx.set_reading_format("MSB", "MSB")

referenceUnit = -388.929792
hx.set_reference_unit(referenceUnit)

hx.reset()
hx.tare()

print("Tare done! Waiting for birds...")

while True:
    try:
        # Get stable weight reading - NO SMOOTHING
        current_weight = get_stable_weight(hx, samples=15)
        current_time = datetime.now()
        
        # Debug output
        print(f"Weight: {current_weight:.1f}g")
        
        if not bird_present and current_weight > BIRD_THRESHOLD:
            bird_present = True
            bird_landed(current_weight)
        
        elif bird_present and current_weight < BIRD_THRESHOLD:
            bird_present = False
            bird_left()

        hx.power_down()
        hx.power_up()
        time.sleep(0.2)  # Slightly longer delay for stability

    except (KeyboardInterrupt, SystemExit):
        cleanAndExit()