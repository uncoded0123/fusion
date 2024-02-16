'''
from machine import Pin, PWM, ADC
s = PWM(Pin(4), freq=50, duty=120) #5%-10, ~duty~40-120, angle 270 deg DS3218MG
'''
import esp32_now_receive
from machine import Pin, ADC, PWM
from time import sleep

#x = ADC(Pin(32))
#x.atten(ADC.ATTN_11DB)
x = esp32_now_receive.Receive()
s = PWM(Pin(4), freq=50)

#y=mx+b
while True:
    sleep(0.1)
    m = 0.02
    b = 40
    x1 = int(x.receive())
    print(x1)
    y = m * x1 + b
    s.duty(int(y))