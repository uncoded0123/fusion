import esp32_now_send, time
from machine import Pin, ADC

x = ADC(Pin(32))
x.atten(ADC.ATTN_11DB)
    
mac = # <enter mac here>
s = esp32_now_send.Send(mac)


while True:
    time.sleep(0.1)
    x1 = x.read()
    print(x1)
    s.send(x1)