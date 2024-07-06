from machine import UART, Pin
import os
from time import sleep

led = Pin(2, Pin.OUT)
led.off()

uart = UART(2, baudrate=115200)

print("Waiting for data...")

while True:
    sleep(0.1)
    if uart.any():
        data = uart.readline()
        txt = data.decode().strip()
        print(txt)
        if 'on' in txt:
            led.on()
            sleep(5)
        else:
            led.off()



"""
import connect, send_recieve
from machine import TouchPad, Pin
from time import sleep


a = TouchPad(Pin(4))

for i in range(10):
    send_recieve.send(f'{a.read()}')
    print(a.read())
    sleep(5)
"""


"""import time, network, ssid_password
station = network.WLAN(network.STA_IF)
station.active(True)
while station.isconnected() == False:
    station.connect(ssid_password.SSID, ssid_password.PASSWORD)
    time.sleep(1)
print("Connected!")
"""