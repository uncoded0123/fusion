# check mic location port number

import whisper
from openai import OpenAI
import subprocess
import os
import webbrowser
import requests


class Assistant:
    def __init__(self):
        # load_dotenv()
        self.model = whisper.load_model("base")
        self.client = OpenAI(
            api_key=os.getenv("DEEPINFRA_API_KEY"),  # <- Replace this
            base_url="https://api.deepinfra.com/v1/openai")
        
    def listen(self, duration=5):
        filename = 'audio.wav'
        try:
            subprocess.run(['arecord', '-D', 'hw:1,0', '-f', 'S16_LE', '-c1', 
                        '-r', '48000', '-d', str(duration), filename], check=True)
        except:
            subprocess.run(['arecord', '-D', 'hw:4,0', '-f', 'S16_LE', '-c1', 
                        '-r', '48000', '-d', str(duration), filename], check=True)
        text = self.model.transcribe(filename)["text"].lower()
        print(f"Transcribed text: {text}")
        return text
    
    def think(self, text):
        print("Sending to DeepInfra:", text)
        try:
            response = self.client.chat.completions.create(
                model="meta-llama/Meta-Llama-3-70B-Instruct",
                messages=[{"role": "user", "content": f"clear, concise, < 25 words: {text}"}],
                max_tokens=40)
            return response.choices[0].message.content
        except Exception as e:
            print(f"DeepInfra API error: {e}")
            return "Error connecting to DeepInfra"
    
    def speak(self, text):
        print("Speaking:", text)
        subprocess.run(["espeak", text], check=True)
    
    def run(self):
        print("waiting for wake words)")
        while True:
            try:
                text = self.listen().lower()
                
                if any(x in text for x in ['hey fusion', 'hi fusion', 'hey vision', 'a fusion']):
                    print("Wake word detected!")

                    if 'go to' in text:
                        webbrowser.open(f"https://www.{text[18:-1].replace(' ','')}")

                    elif any(x in text for x in ['what', 'how', 'tell', 'can']):
                        # self.speak(self.think(text[11:]))
                        text = text[9:]
                        response = self.think(text)
                        print(f"DeepInfra response: {response}")
                        self.speak(response)

                    elif ('kitchen' in text) and (' on' in text):
                        requests.get(f"{os.getenv('URL')}/kitchen_on")
                        requests.get(f"{os.getenv('URL2')}/Turn_On")
                    
                    elif ('living room' in text) and (' on' in text):
                        requests.get(f"{os.getenv('URL')}/living_room_on")
                    
                    elif (('mower' in text) or ('more' in text)) and (' on' in text):
                        requests.get(f"{os.getenv('URL')}/mower_on")

                    elif ('kitchen' in text) and (' off' in text):
                        requests.get(f"{os.getenv('URL')}/kitchen_off")
                        requests.get(f"{os.getenv('URL2')}/fusion/Turn_Off")
                                            
                    elif ('living room' in text) and (' off' in text):
                        requests.get(f"{os.getenv('URL')}/living_room_off")
                    
                    elif (('mower' in text) or ('more' in text)) and (' off' in text):
                        requests.get(f"{os.getenv('URL')}/mower_off")
                        
                    elif (any(x in text for x in ['kitchen', 'living room', 'mower', 'mower'])
                          and ('off' in text)):
                        requests.get(f"{os.getenv('URL')}/off")
                        
                    else:
                        print("No wake word detected")


            except Exception as e:
                print(f"Error in main loop: {e}")
                continue


if __name__ == "__main__":
    Assistant().run()
