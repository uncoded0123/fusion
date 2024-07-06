# instructions for vosk: https://medium.com/analytics-vidhya/offline-speech-recognition-made-easy-with-vosk-c61f7b720215
# change device and sample rate in speech_to_text,py if not working

from dotenv import load_dotenv
import json, webbrowser, openai
import os
import pyttsx3
import serial
import requests
import queue
import sys
import sounddevice as sd
from vosk import Model, KaldiRecognizer
import serial.tools.list_ports



class ContinuousSpeechToText:
    def __init__(self, lang="en-us", samplerate=48000, device_index=4):  # laptop webcam audio samplerate=48000 device_index=4, desktop=?
        self.q = queue.Queue()
        self.model = Model(lang=lang)
        self.samplerate = samplerate
        self.recognizer = KaldiRecognizer(self.model, self.samplerate)
        self.stream = sd.RawInputStream(samplerate=self.samplerate, blocksize=8000, device=device_index, dtype="int16", channels=1, callback=self.audio_callback)  # Use device_index here
        self.stream.start()

    def audio_callback(self, indata, frames, time, status):
        if status:
            print(status, file=sys.stderr)
        self.q.put(bytes(indata))

    def run(self):
        if not self.q.empty():
            data = self.q.get()
            if self.recognizer.AcceptWaveform(data):
                return self.recognizer.Result()
            else:
                return self.recognizer.PartialResult()

    def stop(self):
        self.stream.stop()
        self.stream.close()


class CheckPorts:
    def __init__(self):
        ports = serial.tools.list_ports.comports()

    def check(self):
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


class GPT:
    def __init__(self):
        load_dotenv()  # Load .env file
        self.api_key = os.getenv('OPENAI_API')  # Access variable
        self.client = openai.OpenAI(api_key=self.api_key)

    def text_generator(self, prompt):
        stream = self.client.chat.completions.create(
            
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": f"clear, concise, < 20 words: {prompt}"}],
                    #   {"role": "system", "content": "your name is fusion, you are like Jarvis from ironman"}],
            stream=True,
            max_tokens=40)
        answer_lst = []
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                answer = chunk.choices[0].delta.content
                answer_lst.append(answer)
                # print(chunk.choices[0].delta.content, end="")
        return ''.join(answer_lst)
    

class TextToSpeech:
    def __init__(self):
        pass

    def text_to_speech(self, text):
        engine = pyttsx3.init("espeak")
        voices = engine.getProperty('voices')
        engine.setProperty('voice',voices[11].id) #English
        engine.setProperty('rate', 110)
        engine.say(f"-h {text}")
        engine.runAndWait()


class Main:
    def __init__(self):
        pass

    def main(self):
        cstt = ContinuousSpeechToText()
        tts = TextToSpeech()
        try:
            while True:
                result = cstt.run()
                if result:
                    text = json.loads(result).get('text', '').lower()
                    print(f'text {text}')
                    if ('hey fusion' in text) or ('a fusion' in text):

                        if 'go to' in text:
                            domain_name = text[17:][:-8].replace(' ','')
                            webbrowser.open(f"https://www.{domain_name}.com")

                        elif ('punk' in text) or ('park' in text):
                            tts.text_to_speech("hey, don't call me punk")

                        elif (('what' in text) or ('how' in text) or ('is' in text)
                            or ('tell' in text) or ('you' in text)):
                            txt = gpt_obj.text_generator(f'{text[11:]}')
                            tts.text_to_speech(txt)
                        
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
    m = Main()
    m.main()