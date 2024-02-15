# # instructions for vosk: https://medium.com/analytics-vidhya/offline-speech-recognition-made-easy-with-vosk-c61f7b720215

# from speech_to_text import ContinuousSpeechToText
# import json

# def main():
#     cstt = ContinuousSpeechToText()

#     def web(url):
#         import webbrowser
#         print(f'url {url}')
#         webbrowser.open(f'https://www.{url}.com')

#     try:
#         while True:
#             result_json = cstt.run()
#             if result_json:
#                 result = json.loads(result_json)
#                 text = result.get('text', '').strip().lower()  # Use final result and normalize case
#                 print(f'text {text}')
#                 if ('fusion' in text) or ('asian' in text):
#                     print('said fusion')
#                     if 'go to' in text:
#                         rm_fusion = text[7:]
#                         rm_go_to = rm_fusion[6:]
#                         rm_dot_com = rm_go_to[:-8]
#                         web(url=rm_dot_com)

#     except KeyboardInterrupt:
#         print("Application stopped.")
#     except Exception as e:
#         print(f"Error occurred: {e}")
#     finally:
#         cstt.stop()

# if __name__ == "__main__":
#     main()



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
