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