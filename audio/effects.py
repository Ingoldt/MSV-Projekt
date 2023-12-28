from scipy.io import wavfile
import numpy as np
import os

# contains all functions that alter the recorded audio via an implemented effect
WAVE_OUTPUT_FILENAME = ".wav"  # Output file extension
INPUT_PATH = os.path.normpath(os.path.join(os.getcwd(), "Recordings"))
OUTPUT_PATH = os.path.normpath(os.path.join(os.getcwd(), "Effects"))

def tremolo_effect(input_filename, output_filename, rate, depth):
    # Construct full paths
    input_path = os.path.join(INPUT_PATH, input_filename + WAVE_OUTPUT_FILENAME)
    output_path = os.path.join(OUTPUT_PATH, output_filename + WAVE_OUTPUT_FILENAME)

    # Load the wave file
    sample_rate, audio_data = wavfile.read(input_path)

    # Define time array, tremolo wave and normalizing depth
    time = np.arange(len(audio_data)) / float(sample_rate)
    depth_normalized = (depth * 1.5)
    tremolo_wave = 1 + depth_normalized * np.sin(2 * np.pi * rate * time)

    # Mono audio
    tremolo_wav = np.resize(tremolo_wave, len(audio_data))
    audio_data_tremolo = (audio_data * tremolo_wav).astype(np.int16)

    # Normalize the resulting audio within the valid range for 16-bit PCM
    max_amplitude = np.iinfo(np.int16).max
    normalized_audio = (audio_data_tremolo / np.max(np.abs(audio_data_tremolo))) * max_amplitude

    # Save the modified audio
    wavfile.write(output_path, sample_rate, normalized_audio.astype(np.int16))
    print("Audio file saved to", output_path)
    return normalized_audio

def distortion_effect(input_filename, output_filename, gain, clipping_threshhold):
    # Construct full paths
    input_path = os.path.join(INPUT_PATH, input_filename + WAVE_OUTPUT_FILENAME)
    output_path = os.path.join(OUTPUT_PATH, output_filename + WAVE_OUTPUT_FILENAME)

    # Load the wave file
    sample_rate, audio_data = wavfile.read(input_path)

    # Apply gain
    distorted_audio = audio_data * gain
    # Apply clipping
    distorted_audio = np.clip(distorted_audio, -clipping_threshhold, clipping_threshhold)

    # Save the modified audio
    wavfile.write(output_path, sample_rate, distorted_audio.astype(np.int16))
    print("Audio file saved to", output_path)
    return distorted_audio.astype(np.int16)


def echo_effect(input_filename, output_filename, echo_delay_seconds=1, echo_amplifier=0.25):
    # Construct full paths
    input_path = os.path.join(INPUT_PATH, input_filename + WAVE_OUTPUT_FILENAME)
    output_path = os.path.join(OUTPUT_PATH, output_filename + WAVE_OUTPUT_FILENAME)

    # Load the wave file
    sample_rate, audio_data = wavfile.read(input_path)

    # Apply echo
    echo_delay_samples = int(echo_delay_seconds * sample_rate)
    for i in range(echo_delay_samples, len(audio_data)):
        audio_data[i] += (audio_data[i - echo_delay_samples] * echo_amplifier)

    # Save the modified audio
    wavfile.write(output_path, sample_rate, audio_data.astype(np.int16))
    print("Audio file saved to", output_path)
    return audio_data.astype(np.int16)


def hall_effect(input_filename, output_filename, hall_delay_seconds=0.1, hall_length=0.5, hall_amplifier=0.5, hall_repeat=3):
    # Construct full paths
    input_path = os.path.join(INPUT_PATH, input_filename + WAVE_OUTPUT_FILENAME)
    output_path = os.path.join(OUTPUT_PATH, output_filename + WAVE_OUTPUT_FILENAME)

    # Load the wave file
    sample_rate, audio_data = wavfile.read(input_path)

    # Calculate variables
    delay_samples = int(hall_delay_seconds * sample_rate)
    repeat_delay_samples = int((hall_length / hall_repeat) * sample_rate)
    sample_length = len(audio_data)

    # For every sample
    for i in range(sample_length):
        sample_position = i + delay_samples
        count = 0

        while (sample_position < sample_length) & (count < hall_repeat):
            # Add hall
            repeat_amplifier = (hall_repeat - count) / hall_repeat
            audio_data[sample_position] += (audio_data[i] * repeat_amplifier * hall_amplifier)

            # Increase values
            sample_position += repeat_delay_samples
            count += 1

    # Save the modified audio
    wavfile.write(output_path, sample_rate, audio_data.astype(np.int16))
    print("Audio file saved to", output_path)
    return audio_data.astype(np.int16)
