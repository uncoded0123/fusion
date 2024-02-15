# instructions for vosk: https://medium.com/analytics-vidhya/offline-speech-recognition-made-easy-with-vosk-c61f7b720215

# hi Mom

from speech_to_text import ContinuousSpeechToText
import json
import pyttsx3
import time
import sounddevice as sd

print(sd.query_devices())

class SpeechResponder:
    def __init__(self):
        self.engine = pyttsx3.init()
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[17].id)  # Adjust based on available voices
        self.last_action_time = time.time()
        self.action_cooldown = 2  # Seconds to wait before allowing another action

    def respond_to_trigger(self, text):
        current_time = time.time()
        if current_time - self.last_action_time > self.action_cooldown:
            self.engine.say('-- '+text)
            self.engine.runAndWait()
            self.last_action_time = current_time

def main():
    cstt = ContinuousSpeechToText()  # Initialize continuous speech-to-text
    responder = SpeechResponder()
    
    triggers = {
        "hi": "Hello, how can I help you?",
        "what is the time": "Checking the current time for you.",
        "sup": "- What's poppin homie?"

        # Add more triggers and responses as needed
    }
    def web(url):
        import webbrowser
        print(f'url {url}')
        webbrowser.open(f'https://www.{url}.com')

    def power(state='off'):
        pass

    try:
        while True:
            result_json = cstt.run()
            if result_json:
                result = json.loads(result_json)
                text = result.get('text', '').strip().lower()  # Use final result and normalize case
                for trigger, response in triggers.items():
                    print(f'text {text}')
                    if ('fusion' in text) or ('asian' in text):
                        print('said fusion')
                        if 'go to' in text:
                            rm_fusion = text[7:]
                            rm_go_to = rm_fusion[6:]
                            rm_dot_com = rm_go_to[:-8]
                            web(url=rm_dot_com)
                            # responder.respond_to_trigger(response)

                        if 'power' in text:
                            power(state='on')

                        if 'off' in text:
                            power(state='off')

                        break  # Exit loop after first trigger match to avoid multiple responses
    except KeyboardInterrupt:
        print("Application stopped.")
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        cstt.stop()

if __name__ == "__main__":
    main()
