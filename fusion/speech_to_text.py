# instructions for vosk: https://medium.com/analytics-vidhya/offline-speech-recognition-made-easy-with-vosk-c61f7b720215
# change device and sample rate if not working

import queue
import sys
import sounddevice as sd
from vosk import Model, KaldiRecognizer

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

# Remember to stop the stream when your application exits
if __name__ == "__main__":
    try:
        cstt = ContinuousSpeechToText()
        while True:
            result = cstt.run()
            if result:
                print(result)
    except KeyboardInterrupt:
        cstt.stop()
        print("Terminated by user")