import adafruit_bme680
import time
import board
import datetime

# Create sensor object, communicating over the board's default I2C bus
i2c = board.I2C()   # uses board.SCL and board.SDA
bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c)

# change this to match the location's pressure (hPa) at sea level
bme680.sea_level_pressure = 1013.25

counter = 0

print(time.ctime())


while counter < 10:
    a = "Temperature: %0.1f C" % bme680.temperature
    b = "Gas: %d ohm" % bme680.gas
    c = "Humidity: %0.1f %%" % bme680.relative_humidity
    d = "Pressure: %0.3f hPa" % bme680.pressure
    e = "Altitude = %0.2f meters" % bme680.altitude
    print(a + b + c + d + e)
    counter += 1
    time.sleep(2)
