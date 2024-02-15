# # instructions for vosk: https://medium.com/analytics-vidhya/offline-speech-recognition-made-easy-with-vosk-c61f7b720215
# change device and sample rate in speech_to_text,py if not working

from speech_to_text import ContinuousSpeechToText
import json, webbrowser

def main():
    cstt = ContinuousSpeechToText()
    try:
        while True:
            result = cstt.run()
            if result:
                text = json.loads(result).get('text', '').lower()
                print(f'text {text}')

                if ('fusion' in text) or ('huge' in text):
                    if 'go to' in text:
                        domain_name = text[13:][:-8].replace(' ','')
                        webbrowser.open(f"https://www.{domain_name}.com")

    except KeyboardInterrupt: print("Application stopped.")
    except Exception as e: print(f"Error occurred: {e}")

if __name__ == "__main__":
    main()
