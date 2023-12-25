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
