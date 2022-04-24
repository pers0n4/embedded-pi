import time

import adafruit_dht
import board

device = adafruit_dht.DHT22(board.D18)


while True:
    try:
        temperature = device.temperature
        humidity = device.humidity
        print(f"Temp: {temperature:.1f}°C, Humidity: {humidity}% ")

    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        print(error.args[0])
        time.sleep(1.0)
        continue
    except Exception as error:
        device.exit()
        raise error

    time.sleep(1.0)
