if bluetooth earbuds not working:
1. check OBS if they are working for mic
2. check anything like listen to a youtube video to see if playback speaker is working
3. run "pactl list sources short"
4. find something like this: "330     bluez_input.A1_A7_25_B6_57_82.0 PipeWire        s16le 1ch 16000Hz       SUSPENDED
331     bluez_output.A1_A7_25_B6_57_82.1.monitor        PipeWire        s16le 1ch 16000Hz       SUSPENDED"

5. place this in python fusion code:
    def listen(self, duration=10):
        filename = 'audio.wav'
        subprocess.run(['ffmpeg', '-f', 'pulse', '-i', 'bluez_input.A1_A7_25_B6_57_82.0', 
               '-t', str(duration), '-y', filename])
        text = self.model.transcribe(filename)["text"].lower()
        print(f"Transcribed text: {text}")
        return text
