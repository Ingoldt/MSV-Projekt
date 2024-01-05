import numpy as np

def audio_data_to_float32(audio_data):
    data_type = audio_data.dtype.name
    if data_type == "uint8":
        return (audio_data.astype(np.float32) - 128) / 127
    elif data_type == "int16":
        return audio_data.astype(np.float32) / 32767
    elif data_type == "int32":
        return audio_data.astype(np.float32) / 2147483392
    elif data_type == "float32":
        return audio_data
    else:
        message = "Unknown data type for audio data: " + data_type
        raise Exception(message)

def audio_data_to_int16(audio_data):
    data_type = audio_data.dtype.name
    if data_type == "uint8":
        return (((audio_data.astype(np.float32) - 128) / 127) * 32767).astype(np.int16)
    elif data_type == "int16":
        return audio_data
    elif data_type == "int32":
        return ((audio_data.astype(np.float32) / 2147483392) * 32767).astype(np.int16)
    elif data_type == "float32":
        return (audio_data * 32767).astype(np.int16)
    else:
        message = "Unknown data type for audio data: " + data_type
        raise Exception(message)
