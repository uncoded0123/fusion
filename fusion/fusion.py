# # instructions for vosk: https://medium.com/analytics-vidhya/offline-speech-recognition-made-easy-with-vosk-c61f7b720215
# change device and sample rate in speech_to_text,py if not working

from speech_to_text import ContinuousSpeechToText
from dotenv import load_dotenv
import json, webbrowser, openai
import os



load_dotenv()  # Load .env file
api_key = os.getenv('OPENAI_API')  # Access variable

def gpt(prompt):
    client = openai.OpenAI(api_key=api_key)
    stream = client.chat.completions.create(
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
                    if ('what' in text) or ('how' in text):
                        print(gpt(f'{text[7:]}'))

    except KeyboardInterrupt: print("Application stopped.")
    except Exception as e: print(f"Error occurred: {e}")

if __name__ == "__main__":
    main()