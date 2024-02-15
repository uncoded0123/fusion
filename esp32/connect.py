import time, network, ssid_password
station = network.WLAN(network.STA_IF)
station.active(True)
while station.isconnected() == False:
    station.connect(ssid_password.SSID, ssid_password.PASSWORD)
    time.sleep(1)
print("Connected!")
