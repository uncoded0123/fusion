# # instructions for vosk: https://medium.com/analytics-vidhya/offline-speech-recognition-made-easy-with-vosk-c61f7b720215
# change device and sample rate in speech_to_text,py if not working

from speech_to_text import ContinuousSpeechToText
from dotenv import load_dotenv
import json, webbrowser, openai
import os
import pyttsx3
import serial


class Serial1:
    def __init__(self):
        self.ser1 = serial.Serial('ttyUSB1', 115200)
        self.ser2 = serial.Serial('ttyUSB2', 115200)

    def power(self, x='off'):
        self.ser1.write(str(x).encode())


# Serial1().power('on')


class GPT:
    def __init__(self):
        load_dotenv()  # Load .env file
        self.api_key = os.getenv('OPENAI_API')  # Access variable
        self.client = openai.OpenAI(api_key=self.api_key)

    def text_generator(self, prompt):
        stream = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": f"clear and concise as possible, in less than 20 words, {prompt}"}],
            stream=True,
            max_tokens=50)
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
                if ('fusion' in text) or ('eugune' in text):

                    if 'go to' in text:
                        domain_name = text[13:][:-8].replace(' ','')
                        webbrowser.open(f"https://www.{domain_name}.com")

                    if ('what' in text) or ('how' in text):
                        txt = gpt1.text_generator(f'{text[7:]}')
                        text_to_speech(txt)
                    
                    if 'power' in text:
                        power(ser2, 'on' if 'on' in heard else 'off')


    except KeyboardInterrupt: print("Application stopped.")
    except Exception as e: print(f"Error occurred: {e}")

if __name__ == "__main__":
    gpt1 = GPT()
    main()