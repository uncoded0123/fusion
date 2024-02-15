import urequests, connect, ssid_password

def send(x):
    response = urequests.get(ssid_password.SEND_URL + str(x))
    response.close()

def recieve():
    response = urequests.get(ssid_password.RECEIVE_URL)
    return response.text # response.<whatever> (eg, response.text, or response.json())
    
    # uncomment below for on_off
    # response = urequests.get(ssid_password.ON_OFF_URL)
    # return response.json()['test']