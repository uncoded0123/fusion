from machine import Pin, ADC, PWM
from time import sleep

servo = PWM(Pin(22), freq=50) # change freq

def s_on(x):
    # duty 40-115
    if x == 'on':
        servo.duty(40)
        sleep(0.5)
        servo.duty(115)