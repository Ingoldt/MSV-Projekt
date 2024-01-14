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
    tremolo_wave = (np.sin(2 * np.pi * rate * time + (3 / 2) * np.pi) * 0.5 + 0.5) * depth + (1 - depth)

    tremolo_wav = np.resize(tremolo_wave, len(audio_data))

    if audio_data.ndim == 1:
        # Mono audio
        audio_data_tremolo = (audio_data * tremolo_wav).astype(np.int16)
    elif audio_data.ndim == 2:
        # Stereo audio
        audio_data_tremolo_left = ((audio_data[:, 0]) * tremolo_wav).astype(np.int16)
        audio_data_tremolo_right = ((audio_data[:, 1]) * tremolo_wav).astype(np.int16)
        audio_data_tremolo = np.stack((audio_data_tremolo_left, audio_data_tremolo_right), axis=1)
    else:
        raise Exception("Too many dimensions")

    # Save the modified audio
    wavfile.write(output_path, sample_rate, audio_data_tremolo.astype(np.int16))
    print("Audio file saved to", output_path)
    return audio_data_tremolo

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

    if audio_data.ndim == 1:
        # Mono audio
        for i in range(echo_delay_samples, len(audio_data)):
            audio_data[i] += (audio_data[i - echo_delay_samples] * echo_amplifier)
    elif audio_data.ndim == 2:
        # Stereo audio
        audio_data_left = audio_data[:, 0]
        audio_data_right = audio_data[:, 1]

        for i in range(echo_delay_samples, len(audio_data)):
            audio_data_left[i] += (audio_data_left[i - echo_delay_samples] * echo_amplifier)
            audio_data_right[i] += (audio_data_right[i - echo_delay_samples] * echo_amplifier)

        audio_data = np.stack((audio_data_left, audio_data_right), axis=1)
    else:
        raise Exception("Too many dimensions")

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

    if audio_data.ndim == 1:
        # Mono audio
        # Apply reverb using lfilter
        reverb_signal = lfilter([1.0], impulse_response, audio_data)
    elif audio_data.ndim == 2:
        # Stereo audio
        # Apply reverb using lfilter
        reverb_signal_left = lfilter([1.0], impulse_response, audio_data[:, 0])
        reverb_signal_right = lfilter([1.0], impulse_response, audio_data[:, 1])
        reverb_signal = np.stack((reverb_signal_left, reverb_signal_right), axis=1)
    else:
        raise Exception("Too many dimensions")

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

    if audio_data.ndim == 1:
        # Mono audio
        output = np.zeros([audio_data.shape[0]])
        is_stereo = False
    elif audio_data.ndim == 2:
        # Stereo audio
        output = np.zeros([audio_data.shape[0], 2])
        audio_data_left = audio_data[:, 0]
        audio_data_right = audio_data[:, 1]
        is_stereo = True
    else:
        raise Exception("Too many dimensions")

    for i in range(len(lfo)):
        filter_frequency = min_frequency + lfo[i] * (max_frequency - min_frequency)

        # Calculate Bandpass
        nyquist = 0.5 * sample_rate
        lowcut = (filter_frequency - 0.5 * bandwidth) / nyquist
        highcut = (filter_frequency + 0.5 * bandwidth) / nyquist
        b, a = butter(1, [lowcut, highcut], btype='band')
        j = i

        if is_stereo:
            temp_data_left = lfilter(b, a, audio_data[:, 0])
            temp_data_right = lfilter(b, a, audio_data[:, 1])

            # Use Bandpass
            while j < len(output):
                output[j][0] = temp_data_left[j] * 0.5 + audio_data_left[j] * 0.5
                output[j][1] = temp_data_right[j] * 0.5 + audio_data_right[j] * 0.5
                j += len(lfo)
        else:
            temp_data = lfilter(b, a, audio_data)

            # Use Bandpass
            while j < len(output):
                output[j] = temp_data[j] * 0.5 + audio_data[j] * 0.5
                j += len(lfo)

        print(i, len(lfo))

    # Save the modified audio
    wavfile.write(output_path, sample_rate, output)
    print("Audio file saved to", output_path)
    return output
