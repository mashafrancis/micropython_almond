import time
import json

from dht import DHT11
from machine import Pin
from umqtt.robust import MQTTClient
from config import SENSOR_ID, BROKER, INTERVAL, DHT_PIN

TOPIC = "led"

sensor_data = {'temperature': 0, 'humidity': 0}

client = MQTTClient(SENSOR_ID, BROKER, 1883)
client.connect()


def main():
    try:
        while True:
            d = DHT11(Pin(DHT_PIN))
            d.measure()

            temperature = d.temperature()
            humidity = d.humidity()
            # print(self.payload)
            print("Temp: {:.1f} *C \t Humidity: {}%".format(temperature, humidity))
            # sensor.Sensor.json()
            sensor_data['temperature'] = temperature
            sensor_data['humidity'] = humidity
            client.publish('sensor', json.dumps(sensor_data))

            next_reading = time.time()
            next_reading += INTERVAL
            sleep_time = next_reading - time.time()
            if sleep_time > 0:
                time.sleep(sleep_time)
    except KeyboardInterrupt:
        pass

    client.disconnect()


if __name__ == '__main__':
    main()