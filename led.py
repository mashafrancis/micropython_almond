from machine import Pin
from config import BROKER
from umqtt.simple import MQTTClient
import ubinascii
import machine

led = Pin(0, Pin.OUT, value=1)

state = 0

CLIENT_ID = ubinascii.hexlify(machine.unique_id())
TOPIC = b"led"


def sub_cb(topic, msg):
    global state
    print(topic, msg)
    if msg == b"light_on":
        led.value(0)
        state = 1
    elif msg == b"light_off":
        led.value(1)
        state = 0
    elif msg == b"toggle":
        led.value(state)
        state = 1 - state


def main():
    client = MQTTClient(CLIENT_ID, BROKER, 1883)
    client.set_callback(sub_cb)
    client.connect()
    client.subscribe(TOPIC)
    print("Connected to %s, subscribed to %s topic" % (BROKER, TOPIC))

    try:
        while 1:
            client.wait_msg()
    finally:
        client.disconnect()


if __name__ == '__main__':
    main()