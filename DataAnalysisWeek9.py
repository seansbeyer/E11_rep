#!/usr/bin/env python
# coding: utf-8

# In[1]:


import RPi.GPIO as GPIO
import datetime
import time
import csv
import sys

print(sys.argv)
if len(sys.argv) < 2:
    print("This script requires an input argument specifying the run time in seconds.")
    sys.exit()
    #runtime = 10
else:
    run_time = int(sys.argv[1])


filename = 'radiation_count.csv'

with open(filename, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Timestamp"])

    count = 0

    def my_callback(channel):
        global count
        count += 1
        timestamp = str(datetime.datetime.now())
        print(f'Falling edge detected at {timestamp}')
        writer.writerow([timestamp])

    try:
        print("Begin falling edge detected")
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(6, GPIO.IN)

        GPIO.add_event_detect(6, GPIO.FALLING, callback=my_callback, bouncetime=200)

        start_time = time.time()
        elapsed_time = 0

        while elapsed_time < run_time:
            time.sleep(60)
            print(f"Total counts = {count}")
            count = 0
            elapsed_time = time.time() - start_time

    except KeyboardInterrupt:
        print("Quit program")

    finally:
        GPIO.cleanup()




