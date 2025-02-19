
import adafruit_bme680
import time
import board
from datetime import datetime
import csv
import serial
from adafruit_pm25.uart import PM25_UART
import sys


# Create sensor object, communicating over the board's default I2C bus
i2c = board.I2C()   # uses board.SCL and board.SDA
bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c)

# change this to match the location's pressure (hPa) at sea level
bme680.sea_level_pressure = 1013.25

#counter = 0

#print(time.ctime())


#while counter < 10:
#    a = "Temperature: %0.1f C" % bme680.temperature
#    b = "Gas: %d ohm" % bme680.gas
#    c = "Humidity: %0.1f %%" % bme680.relative_humidity
#    d = "Pressure: %0.3f hPa" % bme680.pressure
#    e = "Altitude = %0.2f meters" % bme680.altitude
#    print(a + b + c + d + e)
#    counter += 1
#    time.sleep(2)

################################

print(sys.argv)
if len(sys.argv) < 2:
  print("This script requires an input argument specifying the run time in seconds.")
  exit()
  #runtime = 10
else:
  run_time = int(sys.argv[1])

  
# Define the serial port for UART communication
uart = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=0.25)

# Initialize PM2.5 sensor
pm25 = PM25_UART(uart, reset_pin=None)

# File name with timestamp
filename = "air_data.csv"

# Open the CSV file for writing
with open(filename, mode="w", newline="") as file:
    writer = csv.writer(file)

    # Write metadata (header)
    writer.writerow(["Timestamp", "PM1.0 (std)", "PM2.5 (std)", "PM10 (std)",
                     "PM1.0 (env)", "PM2.5 (env)", "PM10 (env)",
                     "Particles >0.3um", "Particles >0.5um", "Particles >1.0um",
                     "Particles >2.5um", "Particles >5.0um", "Particles >10um", "Temperature: %0.1f C" , "Gas: %d ohm", "Humidity: %0.1f %%", "Pressure: %0.3f hPa", "Altitude = %0.2f meters"])

    print(f"Logging PM2.5 sensor data to {filename} for 30 seconds...\n")

    start_time = time.time()
    elapsed_time = 0
    
    while elapsed_time < run_time:  # Run for 30 seconds
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
            aqdata["particles 25um"], aqdata["particles 50um"], aqdata["particles 100um"], bme680.temperature, bme680.gas, bme680.relative_humidity, bme680.pressure, bme680.altitude
        ]

        # Write data to CSV
        writer.writerow(row)

        # Print data to console
        print(f"{timestamp} - Data read")

        # Update elapsed time
        elapsed_time = time.time() - start_time

    print("Data collection complete. CSV file saved.")
