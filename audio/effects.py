from scipy.io import wavfile
from scipy.signal import lfilter, butter
from audio.converter import audio_data_to_float32, audio_data_to_int16
import numpy as np
import os

# contains all functions that alter the recorded audio via an implemented effect
WAVE_OUTPUT_FILENAME = ".wav"  # Output file extension
INPUT_PATH = os.path.normpath(os.path.join(os.getcwd(), "Recordings"))
OUTPUT_PATH = os.path.normpath(os.path.join(os.getcwd(), "Effects"))

def tremolo_effect(input_path, output_filename, rate=4, depth=0.6):
    # Construct full paths
    output_path = os.path.join(OUTPUT_PATH, output_filename + WAVE_OUTPUT_FILENAME)

    # Load the wave file
    sample_rate, audio_data = wavfile.read(input_path)
    audio_data = audio_data_to_int16(audio_data)

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

def distortion_effect(input_path, output_filename, gain=1, clipping_threshold_percentage=0.4):
    # Construct full paths
    output_path = os.path.join(OUTPUT_PATH, output_filename + WAVE_OUTPUT_FILENAME)

    # Load the audio file
    sample_rate, audio_data = wavfile.read(input_path)
    audio_data = audio_data_to_int16(audio_data)

    max_amplitude = np.max(np.abs(audio_data))

    # apply gain
    amplified_audio = audio_data * gain

    clipping_threshold = clipping_threshold_percentage * max_amplitude

    distorted_audio = np.clip(amplified_audio, -clipping_threshold , clipping_threshold)

    # Save the distorted audio
    wavfile.write(output_path, sample_rate, distorted_audio.astype(np.int16))

    '''
    # Plot the original and modified audio waveforms
    plt.figure(figsize=(10, 4))
    plt.plot(audio_data, label='Original')
    plt.plot(distorted_audio, label='Distortion Effect')
    plt.legend()
    plt.title('Original and Modified Audio Waveforms')
    plt.xlabel('Sample')
    plt.ylabel('Amplitude')
    plt.show()
    '''

    print("Audio file saved to", output_path)
    return distorted_audio.astype(np.int16)

def echo_effect(input_path, output_filename, echo_delay_seconds=1, echo_amplifier=0.25):
    # Construct full paths
    output_path = os.path.join(OUTPUT_PATH, output_filename + WAVE_OUTPUT_FILENAME)

    # Load the wave file
    sample_rate, audio_data = wavfile.read(input_path)
    audio_data = audio_data_to_int16(audio_data)

    # Apply echo
    echo_delay_samples = int(echo_delay_seconds * sample_rate)
    for i in range(echo_delay_samples, len(audio_data)):
        audio_data[i] += (audio_data[i - echo_delay_samples] * echo_amplifier)

    # Save the modified audio
    wavfile.write(output_path, sample_rate, audio_data.astype(np.int16))
    print("Audio file saved to", output_path)
    return audio_data.astype(np.int16)

def reverb_effect(input_path, output_filename, reverb_delay_ms=100, decay=0.5):
    # Construct full paths
    output_path = os.path.join(OUTPUT_PATH, output_filename + WAVE_OUTPUT_FILENAME)

    # Load the wave file
    sample_rate, audio_data = wavfile.read(input_path)
    audio_data = audio_data_to_int16(audio_data)

    # Generate reverb impulse response with adjustable delay in milliseconds
    delay_length = int(reverb_delay_ms * sample_rate / 1000)  # Convert milliseconds to samples
    impulse_response = np.zeros(delay_length)
    impulse_response[0] = 1.0
    impulse_response[-1] = decay

    # Apply reverb using lfilter
    reverb_signal = lfilter([1.0], impulse_response, audio_data)

    '''
    # Plot the original and modified audio waveforms
    plt.figure(figsize=(10, 4))
    plt.plot(audio_data, label='Original')
    plt.plot(reverb_signal, label='Reverb Effect')
    plt.legend()
    plt.title('Original and Modified Audio Waveforms')
    plt.xlabel('Sample')
    plt.ylabel('Amplitude')
    plt.show()
    '''

    # Save the modified audio
    wavfile.write(output_path, sample_rate, reverb_signal.astype(np.int16))
    print("Audio file saved to", output_path)
    return reverb_signal.astype(np.int16)

def wah_wah_effect(input_path, output_filename, lfo_frequency=4.0, min_frequency=200, max_frequency=2000, bandwidth=200):
    # Construct full paths
    output_path = os.path.join(OUTPUT_PATH, output_filename + WAVE_OUTPUT_FILENAME)

    # Load the wave file
    sample_rate, audio_data = wavfile.read(input_path)
    audio_data = audio_data_to_float32(audio_data)

    # Calculate LFO
    lfo_samples = np.linspace(0., 1 / lfo_frequency, int(sample_rate / lfo_frequency), endpoint=False)
    lfo = np.sin(2 * np.pi * lfo_frequency * lfo_samples) * 0.5 + 0.5

    output = np.zeros([len(audio_data)])
    for i in range(len(lfo)):
        filter_frequency = min_frequency + lfo[i] * (max_frequency - min_frequency)

        # Calculate Bandpass
        nyquist = 0.5 * sample_rate
        lowcut = (filter_frequency - 0.5 * bandwidth) / nyquist
        highcut = (filter_frequency + 0.5 * bandwidth) / nyquist
        b, a = butter(1, [lowcut, highcut], btype='band')

        temp_data = lfilter(b, a, audio_data)
        j = i

        # Use Bandpass
        while j < len(output):
            output[j] = temp_data[j] * 0.5 + audio_data[j] * 0.5
            j += len(lfo)

        print(i, len(lfo))

    # Save the modified audio
    wavfile.write(output_path, sample_rate, output)
    print("Audio file saved to", output_path)
    return output
