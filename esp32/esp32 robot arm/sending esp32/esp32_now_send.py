# send
import network, espnow


class Send:
    def __init__(self, mac):
        # Convert MAC address string to bytes
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        self.esp_now = espnow.ESPNow()
        self.esp_now.active(True)
        
        self.peer_mac = bytes(int(x, 16) for x in f'{mac}'.split(':'))
        self.esp_now.add_peer(self.peer_mac)

    def send(self, val):
        self.esp_now.send(self.peer_mac, f"{val}".encode())
        return f'sent: {val}'