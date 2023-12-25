from audio.recorder import AudioRecorder, list_recording_devices
from audio.effects import tremolo_effect
from scipy.io import wavfile
import numpy as np

# main loop of the programm
def main():
    if(input("Do you want to record an audio file? (y/n): ") == "y"):
        list_recording_devices()

        # user can select recording device by entering the index and the filename by entering a name
        index = int(input("Enter the index of the recording device you want to choose: "))
        filename = input("Enter the desired filename (without extension): ")

        # if button pressed
        recorder = AudioRecorder(index)
        recorder.record_audio(filename)

        '''
        # if button pressed
        recorder.audio_playback()
        '''

    # Effects

    # Apply tremolo effect
    file = input("Do you want to apply the audio effect to your recording? (y/n): ")
    if file == "n":
        input_filename = input("Enter the desired filename (without extension): ")
        output_filename = input("Enter the desired filename (without extension): ")
        tremolo_rate = int(input("Enter the tremolo rate between 1 - 10: "))
        tremolo_depth = float(input("Enter the tremolo depth between 0 - 1: "))
        tremolo_audio = tremolo_effect(input_filename, output_filename, tremolo_rate, tremolo_depth)
    else:
        input_filename = filename
        output_filename = input("Enter the desired filename (without extension): ")
        tremolo_rate = int(input("Enter the tremolo rate as integer: "))
        tremolo_depth = float(input("Enter the tremolo depth as float: "))
        tremolo_audio = tremolo_effect(input_filename, output_filename, tremolo_rate, tremolo_depth)



if __name__ == "__main__":
    main()