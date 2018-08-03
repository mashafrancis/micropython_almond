import gc
import network
import esp

from machine import Pin
from config import WIFI_ESSID, WIFI_PASSWORD, WIFI_PIN


def connect():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(WIFI_ESSID, WIFI_PASSWORD)
        while not sta_if.isconnected():
            wifi_led()
    print('network config:', sta_if.ifconfig())


def no_debug():
    # you can run this from the REPL as well
    esp.osdebug(None)


def wifi_led():
    pin = Pin(WIFI_PIN, Pin.OUT)
    pin.on()


gc.collect()
no_debug()
connect()