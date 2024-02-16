# receive
import network, espnow

class Receive:
    def __init__(self):
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        self.esp_now = espnow.ESPNow()
        self.esp_now.active(True)

    def receive(self):
        _, msg = self.esp_now.recv()
        if msg != None:
            return msg
        while self.esp_now.any():
            self.esp_now.recv()
