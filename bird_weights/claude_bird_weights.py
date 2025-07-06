import time
import sys
import statistics
from collections import deque
import RPi.GPIO as GPIO
from hx711 import HX711

def cleanAndExit():
    print("Cleaning...")
    print("Bye!")
    sys.exit()

def bird_landed(weight, baseline_mean):
    """Called when a bird lands on the feeder"""
    weight_change = weight - baseline_mean
    print(f"🐦 Bird landed! Weight change: +{weight_change:.2f}g")

def bird_left(baseline_mean):
    """Called when a bird leaves the feeder"""
    print(f"🦅 Bird left! Returning to baseline: {baseline_mean:.2f}g")

hx = HX711(5, 6)
hx.set_reading_format("MSB", "MSB")

referenceUnit = 416.71
hx.set_reference_unit(referenceUnit)

hx.reset()
hx.tare()

print("Collecting initial baseline... (30 seconds)")

# Rolling baseline configuration
BASELINE_WINDOW = 50  # Number of recent readings to keep for baseline
STDDEV_THRESHOLD = 2.0  # Number of standard deviations to trigger event
UPDATE_DELAY = 2.0  # Seconds to wait after bird event before updating baseline

# Use deque for efficient rolling window
baseline_readings = deque(maxlen=BASELINE_WINDOW)
last_event_time = 0

# Bird presence tracking
bird_present = False

# Collect initial baseline data
for i in range(BASELINE_WINDOW):
    val = hx.get_weight(3)
    baseline_readings.append(val)
    print(f"Initial reading {i+1}/{BASELINE_WINDOW}: {val:.2f}g")
    time.sleep(0.3)

# Calculate initial baseline statistics
baseline_mean = statistics.mean(baseline_readings)
baseline_stddev = statistics.stdev(baseline_readings)

print(f"Initial baseline established:")
print(f"  Mean: {baseline_mean:.2f}g")
print(f"  Std Dev: {baseline_stddev:.2f}g")
print(f"  Trigger threshold: ±{STDDEV_THRESHOLD * baseline_stddev:.2f}g")
print("Bird feeder ready!")

# Main monitoring loop
while True:
    try:
        current_weight = hx.get_weight(5)
        current_time = time.time()
        
        # Calculate how many standard deviations away from baseline
        deviation = abs(current_weight - baseline_mean)
        stddev_multiplier = deviation / baseline_stddev if baseline_stddev > 0 else 0
        
        # Check if this is a significant weight change
        is_significant_change = stddev_multiplier >= STDDEV_THRESHOLD
        
        # Bird state logic
        if is_significant_change:
            if current_weight > baseline_mean and not bird_present:
                # Bird landed
                bird_present = True
                bird_landed(current_weight, baseline_mean)
                last_event_time = current_time
                time.sleep(2)  # Brief pause after event
                
            elif current_weight <= baseline_mean and bird_present:
                # Bird left (weight returned to baseline)
                bird_present = False
                bird_left(baseline_mean)
                last_event_time = current_time
                time.sleep(2)  # Brief pause after event
        
        # Update baseline only if enough time has passed since last bird event
        # This prevents bird weights from contaminating the baseline
        time_since_event = current_time - last_event_time
        if time_since_event >= UPDATE_DELAY and not is_significant_change:
            # Add current reading to rolling baseline
            baseline_readings.append(current_weight)
            
            # Recalculate baseline statistics with new reading
            baseline_mean = statistics.mean(baseline_readings)
            baseline_stddev = statistics.stdev(baseline_readings)
            
            # Optional: Print baseline updates (comment out to reduce output)
            print(f"Baseline updated - Mean: {baseline_mean:.2f}g, StdDev: {baseline_stddev:.2f}g")
        
        # Optional: Print current status (comment out to reduce output)
        print(f"Weight: {current_weight:.2f}g | Deviation: {stddev_multiplier:.1f}σ | Bird: {bird_present} | Baseline: {baseline_mean:.2f}g")
        
        hx.power_down()
        hx.power_up()
        time.sleep(0.5)

    except (KeyboardInterrupt, SystemExit):
        cleanAndExit()