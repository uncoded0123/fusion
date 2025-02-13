import network
import urequests
from time import sleep_ms
from machine import Pin, reset


d2 = Pin(2, Pin.OUT)
d4 = Pin(4, Pin.OUT)

d2.on()
sleep_ms(3000)
d2.off()
class Internet:
    def __init__(self):        
        station = network.WLAN(network.STA_IF)
        station.active(False)
        sleep_ms(1000)
        station.active(True)
        station.connect("<ssid>", "<password>")
        while not station.isconnected():
            sleep_ms(100)
        print('connected!')
        print(station.ifconfig())
        #self.p2 = Pin(2, Pin.OUT)
        #self.p4 = Pin(4, Pin.OUT)
        
    def send(self, x):
        response = urequests.get("f"{URL}/save/" + str(x))
        response.close()

    def receive(self):        
        # uncomment below for on_off
        response = urequests.get(f"{URL}/get")
        #return response.json()['test']
        return response.text
    
a = Internet()
while True:
    sleep_ms(300)
    data = a.receive().lower()
    print(data)
    try:
        if "living_room_on" in data:
            d2.on()
            d4.on()
        elif "living_room_off" in data:
            d2.off()
            d4.off()
        else:
            pass
        
    except:
        sleep_ms(1000)
        reset()
