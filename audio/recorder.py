import os
import wave
from threading import Thread

import pyaudio
import keyboard

# contains the functionality to record the audio

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
WAVE_OUTPUT_FILENAME = ".wav"  # Output file extension
audio = pyaudio.PyAudio()


def list_recording_devices():
    print("----recording device list----")
    device_info_host = audio.get_host_api_info_by_index(0)
    device_number = device_info_host.get('deviceCount')
    for i in range(device_number):
        device_info = audio.get_device_info_by_index(i)
        if device_info.get('maxInputChannels') > 0:
            print("Input Device ID ", i, " - ", device_info.get('name'))
    print("-----------------------------")


class AudioRecorder:
    def __init__(self, index):
        self.index = index
        self.file_path = None
        self.is_recording = False

    def record_audio(self, filename="recording.wav"):
        print("recording via index " + str(self.index))

        # Create the full path for saving the file in the "Recordings" subdirectory
        output_directory = os.path.normpath(os.path.join(os.getcwd(), "Recordings"))
        os.makedirs(output_directory, exist_ok=True)  # Create the directory if it doesn't exist

        output_filename = filename + WAVE_OUTPUT_FILENAME
        stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True,
                            input_device_index=self.index, frames_per_buffer=CHUNK)
        print("Recording...")

        # This will be change to a ui button later on !!!!!
        # Record until the user presses the specified key

        RecordAudio = []

        while True:
            data = stream.read(CHUNK)
            RecordAudio.append(data)

            if not self.is_recording:
                break

        print("Recording stopped")

        stream.stop_stream()
        stream.close()

        waveFile = wave.open(os.path.join(output_directory, output_filename), 'wb')
        waveFile.setnchannels(CHANNELS)
        waveFile.setsampwidth(audio.get_sample_size(FORMAT))
        waveFile.setframerate(RATE)
        waveFile.writeframes(b''.join(RecordAudio))
        waveFile.close()

        self.file_path = os.path.join(output_directory, output_filename)
        print(f"Audio recorded and saved as {output_filename} under {output_directory}")

    '''
    def audio_playback(self):
        if self.file_path:
            wave_file = AudioSegment.from_wav(self.file_path)
            play(wave_file)
        else:
            print("No recorded audio to play.")

    '''

    def start_recording(self):
        self.is_recording = True
        Thread(target=self.record_audio).start()

    def stop_recording(self):
        self.is_recording = False
