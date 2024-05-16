import RPi.GPIO as GPIO
import time

# Set GPIO mode
GPIO.setmode(GPIO.BCM)

# Define GPIO pins for Set 4
TRIG = 16
ECHO = 20
RED_LED = 13
YELLOW_LED = 19
GREEN_LED = 26
PHOTO_RES = 21

# GPIO pin setup
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(GREEN_LED, GPIO.OUT)
GPIO.setup(YELLOW_LED, GPIO.OUT)
GPIO.setup(RED_LED, GPIO.OUT)
GPIO.setup(PHOTO_RES, GPIO.IN)

# Initial LED state
GPIO.output(GREEN_LED, GPIO.HIGH)
GPIO.output(YELLOW_LED, GPIO.LOW)
GPIO.output(RED_LED, GPIO.LOW)

# Distance function
def distance():
    GPIO.output(TRIG, False)
    time.sleep(0.1)

    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    pulse_start, pulse_end = 0, 0

    timeout = time.time() + 1
    while GPIO.input(ECHO) == 0 and time.time() < timeout:
        pulse_start = time.time()

    timeout = time.time() + 1
    while GPIO.input(ECHO) == 1 and time.time() < timeout:
        pulse_end = time.time()

    if time.time() >= timeout:
        return 99999

    pulse_duration = pulse_end - pulse_start
    distance_cm = pulse_duration * 17150
    distance_cm = round(distance_cm, 2)

    return distance_cm

# Photoresistor function
def read_photoresistor():
    GPIO.setup(PHOTO_RES, GPIO.OUT)
    GPIO.output(PHOTO_RES, GPIO.LOW)
    time.sleep(0.1)
    
    GPIO.setup(PHOTO_RES, GPIO.IN)
    start_time = time.time()
    while GPIO.input(PHOTO_RES) == GPIO.LOW:
        if time.time() - start_time > 1:
            return 0
    end_time = time.time()
    resistance = end_time - start_time
    
    m = 1000
    b = 10
    lux = m * resistance + b
    return lux

try:
    while True:
        dist = distance()
        lux = read_photoresistor()

        print(f"Set 4 - Distance: {dist} cm")
        print(f"Set 4 - Lux: {lux:.2f}")

        if dist < 20 and lux == 0:
            GPIO.output(GREEN_LED, GPIO.LOW)
            GPIO.output(RED_LED, GPIO.HIGH)
        else:
            GPIO.output(GREEN_LED, GPIO.HIGH)
            GPIO.output(RED_LED, GPIO.LOW)

        time.sleep(1)

except KeyboardInterrupt:
    print("Measurement stopped by user")
    GPIO.cleanup()
