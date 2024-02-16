import connect, send_recieve
from machine import TouchPad, Pin
from time import sleep


a = TouchPad(Pin(4))

for i in range(10):
    send_recieve.send(f'{a.read()}')
    print(a.read())
    sleep(5)