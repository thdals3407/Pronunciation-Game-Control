import pyaudio
import wave
def Mic_device_detector(audio):
    device_list = []
    index_list = []
    for index in range(audio.get_device_count()):
        desc = audio.get_device_info_by_index(index)
        if index <5:
            if "마이크" in desc['name'] or "mic" in desc['name']:
                device_list.append(desc['name'])
                index_list.append(index)
    for i in range(len(index_list)):
        print("DEVICE: {device}, INDEX: {index}".format(
            device=device_list[i], index=index_list[i]))
    return device_list, index_list

def Mic_Recoding(duration, input_device_index):
    filename = 'AudioTest/output_{}.wav'.format(input_device_index)
    rate = 16000
    channels = 1
    frames_per_buffer = 1024
    format = pyaudio.paInt16
    stream = audio.open(format=format, channels=channels, rate=rate, input=True,
                                  frames_per_buffer=frames_per_buffer, input_device_index=input_device_index)
    frames = []
    print("recording Start")
    for i in range(int(rate / frames_per_buffer * duration)):
        data = stream.read(frames_per_buffer)
        frames.append(data)
    print("recording Finish")
    stream.stop_stream()
    stream.close()
    audio.terminate()
    frame2wav(frames, filename, rate, audio, format, channels)


def frame2wav(frames, filename, rate, audio, format=pyaudio.paInt16, channels=1):
    waveFile = wave.open(filename, 'wb')
    waveFile.setnchannels(channels)
    waveFile.setsampwidth(audio.get_sample_size(format))
    waveFile.setframerate(rate)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()

if __name__ == '__main__':
    audio = pyaudio.PyAudio()
    d_list, index_list = Mic_device_detector(audio)
    print("--------------------")
    print(d_list)
    print(index_list)
    Mic_Recoding(10, 22)
