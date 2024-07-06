from time import sleep
from machine import TouchPad, Pin, reset, UART
import network
import urequests
import os


class Internet:
    def __init__(self):
        station = network.WLAN(network.STA_IF)
        station.active(True)
        station.connect("ssid", "password")
        while not station.isconnected():
            sleep(0.1)
        print('connected!')
        print(station.ifconfig())
        self.p2 = Pin(2, Pin.OUT)
        self.p4 = Pin(4, Pin.OUT)
        
    def send(self, x):
        response = urequests.get("URL/data_test1/" + str(x))
        response.close()

    def receive(self):        
        # uncomment below for on_off
        response = urequests.get("URL/on_off_test")
        return response.json()['test']
    
    def read(self):
        sleep(0.3)
        a = self.receive().lower()
        print(a)
        if 'light on' in a:
            self.p2.on()
        elif 'light of' in a:
            self.p2.off()
            
        if ('fan on' in a) or ('ban on' in a):
            self.p4.on()
        elif ('fan of' in a) or ('ban of' in a):
            self.p4.off()
    

def serial_read():
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

def touch():
    a = TouchPad(Pin(4))

    for i in range(10):
        send_recieve.send(f'{a.read()}')
        print(a.read())
        sleep(5)

def esp32_now():
    # Initialize Wi-Fi in STA mode
    wlan = network.WLAN(network.STA_IF)
    wlan.active(False)
    sleep(3)
    wlan.active(True)

    # Initialize ESP-NOW
    e = espnow.ESPNow()
    e.active(True)

    # Setup GPIO pin for LED
    led = Pin(2, Pin.OUT)

    def handle_message(msg):
        if msg == b'on':
            led.value(1)
        elif msg == b'off':
            led.value(0)

    # Main loop to receive messages
    while True:
        host, msg = e.recv()
        if msg:
            handle_message(msg)



try:
    i = Internet()
    while True:
        sleep(1)
        i.read()
except Exception as e:
    sleep(5)
    print('exception =', e)
    reset()