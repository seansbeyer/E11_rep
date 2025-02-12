#!/usr/bin/env python3
# coding: utf-8

import time
import csv
import serial
from datetime import datetime
from adafruit_pm25.uart import PM25_UART

# Define the serial port for UART communication
uart = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=0.25)

# Initialize PM2.5 sensor
pm25 = PM25_UART(uart, reset_pin=None)

# File name with timestamp
filename = f"pm25_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

# Open the CSV file for writing
with open(filename, mode="w", newline="") as file:
    writer = csv.writer(file)

    # Write metadata (header)
    writer.writerow(["Timestamp", "PM1.0 (std)", "PM2.5 (std)", "PM10 (std)",
                     "PM1.0 (env)", "PM2.5 (env)", "PM10 (env)",
                     "Particles >0.3um", "Particles >0.5um", "Particles >1.0um",
                     "Particles >2.5um", "Particles >5.0um", "Particles >10um"])

    print(f"Logging PM2.5 sensor data to {filename} for 30 seconds...\n")

    start_time = time.time()
    while time.time() - start_time < 30:  # Run for 30 seconds
        time.sleep(1)

        try:
            aqdata = pm25.read()
        except RuntimeError:
            print("Unable to read from sensor, retrying...")
            continue

        # Get current timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Collect data
        row = [
            timestamp,
            aqdata["pm10 standard"], aqdata["pm25 standard"], aqdata["pm100 standard"],
            aqdata["pm10 env"], aqdata["pm25 env"], aqdata["pm100 env"],
            aqdata["particles 03um"], aqdata["particles 05um"], aqdata["particles 10um"],
            aqdata["particles 25um"], aqdata["particles 50um"], aqdata["particles 100um"]
        ]

        # Write data to CSV
        writer.writerow(row)

        # Print data to console
        print(f"{timestamp} - PM2.5: {aqdata['pm25 standard']} µg/m³")

print("Data collection complete. CSV file saved.")
