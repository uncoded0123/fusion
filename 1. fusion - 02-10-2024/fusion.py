


def v1():
    from speech_to_text_ai import ContinuousSpeechToText
    import json
    import pyttsx3
    import time

    class SpeechResponder:
        def __init__(self):
            self.engine = pyttsx3.init()
            voices = self.engine.getProperty('voices')
            self.engine.setProperty('voice', voices[0].id)  # Adjust based on available voices
            self.last_action_time = time.time()
            self.action_cooldown = 2  # Seconds to wait before allowing another action

        def respond_to_trigger(self, text):
            current_time = time.time()
            if current_time - self.last_action_time > self.action_cooldown:
                self.engine.say(text)
                self.engine.runAndWait()
                self.last_action_time = current_time

    def perform_custom_actions(text):
        # Define custom actions here based on the recognized text
        if 'news' in text:
            print("User is interested in news.")
            # Perform action related to news
        elif 'play music' in text:
            print("User wants to play music.")
            # Perform action to play music
        elif 'stop' in text:
            print("User said stop, performing shutdown or stop action.")
            # Perform shutdown or stop action
        else:
            print(f"Triggered custom action with text: {text}")
            # Default or other custom actions

    def main():
        cstt = ContinuousSpeechToText(device_index=1)  # Initialize continuous speech-to-text
        responder = SpeechResponder()
        
        try:
            while True:
                result_json = cstt.run()
                if result_json:
                    result = json.loads(result_json)
                    text = result.get('text', '').strip().lower()  # Use final result and normalize case
                    perform_custom_actions(text)  # Call custom action function based on recognized text
        except KeyboardInterrupt:
            print("Application stopped.")
        except Exception as e:
            print(f"Error occurred: {e}")
        finally:
            cstt.stop()

    if __name__ == "__main__":
        main()


def v2():
    from speech_to_text_ai import ContinuousSpeechToText
    import pyttsx3, time, json

    def perform_actions(text):
        print('yoyo')

        # actions = {'news': 'interested in news', 'play music': 'wants to play music', 'stop': 'said stop, stopping'}
        # print(f"User {actions.get(text, f'triggered custom action with: {text}')}")

    class SpeechResponder:
        def __init__(self, cooldown=2):
            self.engine = pyttsx3.init()
            self.engine.setProperty('voice', self.engine.getProperty('voices')[0].id)
            self.cooldown, self.last = cooldown, time.time()

        def respond(self, text):
            if time.time() - self.last > self.cooldown:
                self.engine.say(text); self.engine.runAndWait(); self.last = time.time()

    def main():
        cstt, responder = ContinuousSpeechToText(device_index=1), SpeechResponder()
        try:
            while True:
                if (result := cstt.run()): perform_actions(json.loads(result).get('text', '').strip().lower())
        except (KeyboardInterrupt, Exception) as e: print(f"Stopped: {e}")
        finally: cstt.stop()

    if __name__ == "__main__": main()
v2()