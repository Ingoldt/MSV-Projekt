from audio.recorder import list_recording_devices
from audio.recorder import record_audio

# main loop of the programm
def main():

    list_recording_devices()

    # user can select recording device by entering the index and the filename by entering a name
    index = int(input("Enter the index of the recording device you want to choose: "))
    filename = input("Enter the desired filename (without extension): ")

    record_audio(index,filename)


if __name__ == "__main__":
    main()