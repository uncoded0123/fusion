# import speech_recognition as sr
# for index, name in enumerate(sr.Microphone.list_microphone_names()):
#     print(f"Microphone with name \"{name}\" found for `Microphone(device_index={index})`")
def freq_check():
    import sounddevice as sd
    def print_supported_sample_rates(device):
        test_rates = [8000, 16000, 32000, 44100, 48000, 96000]  # Common sample rates
        print(f"Supported sample rates for device {device}:")
        for rate in test_rates:
            try:
                sd.check_input_settings(device=device, samplerate=rate)
                print(f"{rate} Hz")
            except Exception as e:
                print(f"{rate} Hz: Not supported")

    print_supported_sample_rates(device=4)  # Replace with your device index


def mic_search():
    import speech_recognition as sr
    for index, name in enumerate(sr.Microphone.list_microphone_names()):
        print(f"Microphone with name \"{name}\" found for `Microphone(device_index={index})`")



def bg_noise():
    import speech_recognition as sr
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1)  # Adjust duration as needed
        audio = r.listen(source)

# mic_search()
freq_check()