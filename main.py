from audio.recorder import AudioRecorder, list_recording_devices
from audio.effects import tremolo_effect, distortion_effect, echo_effect, reverb_effect
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

    effect = input("Which effect do you wish to apply (Echo/Hall/Reverb/Distortion/Tremolo): ")
    if effect == "Echo":
        # Apply tremolo effect
        file = input("Do you want to apply the audio effect to your recording? (y/n): ")

        if file == "n":
            input_filename = input("Enter the desired filename (without extension): ")
            output_filename = input("Enter the desired filename (without extension): ")
            echo_delay_seconds = int(input("Enter the delay in seconds (int): "))
            echo_amplifier = float(input("Enter a number the effect should be amplified with (float): "))
            echo_audio = echo_effect(input_filename, output_filename, echo_delay_seconds, echo_amplifier)
        else:
            input_filename = filename
            output_filename = input("Enter the desired filename (without extension): ")
            echo_delay_seconds = int(input("Enter the delay in seconds (int): "))
            echo_amplifier = float(input("Enter a number the effect should be amplified with (float): "))
            echo_audio = echo_effect(input_filename, output_filename, echo_delay_seconds, echo_amplifier)

    elif effect == "Reverb":
        # Apply tremolo effect
        file = input("Do you want to apply the audio effect to your recording? (y/n): ")

        if file == "n":
            input_filename = input("Enter the desired filename (without extension): ")
            output_filename = input("Enter the desired filename (without extension): ")
            reverb_delay_ms = int(input("Enter the reverb delay in milliseconds (int): "))
            decay = float(input("Enter the decay (float): "))
            reverb_audio = reverb_effect(input_filename, output_filename, reverb_delay_ms, decay)

        else:
            input_filename = filename
            output_filename = input("Enter the desired filename (without extension): ")
            reverb_delay_ms = int(input("Enter the reverb delay in milliseconds (int): "))
            decay = float(input("Enter the decay (float): "))
            reverb_audio = reverb_effect(input_filename, output_filename, reverb_delay_ms, decay)


    elif effect == "Distortion":
        # Apply tremolo effect
        file = input("Do you want to apply the audio effect to your recording? (y/n): ")

        if file == "n":
            input_filename = input("Enter the desired filename (without extension): ")
            output_filename = input("Enter the desired filename (without extension): ")
            gain = float(input("Enter the gain (float): "))
            clipping_threshold_percentage = float(input("Enter the clipping threshhold (float): "))
            distortion_audio = distortion_effect(input_filename, output_filename, gain, clipping_threshold_percentage)

        else:
            input_filename = filename
            output_filename = input("Enter the desired filename (without extension): ")
            gain = float(input("Enter the gain (float): "))
            clipping_threshold_percentage = float(input("Enter the clipping threshhold (float): "))
            distortion_audio = distortion_effect(input_filename, output_filename, gain, clipping_threshold_percentage)

    elif effect == "Tremolo":
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
            tremolo_rate = int(input("Enter the tremolo rate between 1 - 10: "))
            tremolo_depth = float(input("Enter the tremolo depth between 0 - 1: "))
            tremolo_audio = tremolo_effect(input_filename, output_filename, tremolo_rate, tremolo_depth)


if __name__ == "__main__":
    main()