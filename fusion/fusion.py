# # instructions for vosk: https://medium.com/analytics-vidhya/offline-speech-recognition-made-easy-with-vosk-c61f7b720215
# change device and sample rate in speech_to_text,py if not working

from speech_to_text import ContinuousSpeechToText
from dotenv import load_dotenv
import json, webbrowser, openai
import os
import pyttsx3
import serial
import requests



import serial.tools.list_ports
ports = serial.tools.list_ports.comports()
for port, desc, hwid in sorted(ports):
        print(f"{port}: {desc} [{hwid}]")


class Serial1:
    def __init__(self):
        # self.ser0 = serial.Serial('/dev/ttyUSB0', 115200)
        # self.ser1 = serial.Serial('/dev/ttyUSB1', 115200)
        # self.ser2 = serial.Serial('/dev/ttyUSB2', 115200)
        pass
    # def power(self, x='off'):
    #     self.ser1.write(str(x).encode())


# Serial1().power('off')


class GPT:
    def __init__(self):
        load_dotenv()  # Load .env file
        self.api_key = os.getenv('OPENAI_API')  # Access variable
        self.client = openai.OpenAI(api_key=self.api_key)

    def text_generator(self, prompt):
        stream = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": f"clear and concise as possible, in less than 20 words {prompt}"}],
            stream=True,
            max_tokens=40)
        answer_lst = []
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                answer = chunk.choices[0].delta.content
                answer_lst.append(answer)
                # print(chunk.choices[0].delta.content, end="")
        return ''.join(answer_lst)
    

def text_to_speech(text):
    engine = pyttsx3.init("espeak")
    voices = engine.getProperty('voices')
    engine.setProperty('voice',voices[11].id) #English
    engine.setProperty('rate', 100)
    engine.say(f"-h {text}")
    engine.runAndWait()


def main():
    cstt = ContinuousSpeechToText()
    try:
        while True:
            result = cstt.run()
            if result:
                text = json.loads(result).get('text', '').lower()
                print(f'text {text}')
                if ('hey fusion' in text) or ('a fusion' in text):

                    if 'go to' in text:
                        domain_name = text[13:][:-8].replace(' ','')
                        webbrowser.open(f"https://www.{domain_name}.com")

                    elif ('punk' in text) or ('park' in text):
                        text_to_speech("hey, don't call me punk")

                    elif (('what' in text) or ('how' in text)or ('is' in text)
                           or ('tell' in text)):
                        txt = gpt_obj.text_generator(f'{text[7:]}')
                        text_to_speech(txt)
                    
                    elif 'power on' in text:
                        requests.get(f"{os.getenv('URL')}/data_test1/on")
                        # ser_obj.power('on' if ' on' in text else 'off')
                    
                    elif "power off" in text:
                        requests.get(f"{os.getenv('URL')}/data_test1/off")



    except KeyboardInterrupt: print("Application stopped.")
    except Exception as e: print(f"Error occurred: {e}")

if __name__ == "__main__":
    gpt_obj = GPT()
    ser_obj = Serial1()
    main()