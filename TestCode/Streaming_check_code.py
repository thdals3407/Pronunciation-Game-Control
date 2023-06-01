import pyaudio
import audioop
import time

from util.ToolArray import Mic_device_detector

CHUNK = 3000
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000

# 오디오 스트림 생성 및 초기화
p = pyaudio.PyAudio()
device_list, index_list = Mic_device_detector(p)
device_index = 1


stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK,
                input_device_index=device_index)

Check_text = ""
start_time = time.time()
frame_count = 0
while True:
    data = stream.read(CHUNK)
    rms = audioop.rms(data, 2)  # RMS 값을 계산하여 소리 크기를 결정p
    if rms > 2000:
        Check_text += "-"
    else:
        Check_text = ""
    #print(f"Volume: {rms}")
    #print("Sound Detection", Check_text)
    current_time = time.time()
    elapsed_time = current_time - start_time
    frame_count += 1
    fps = frame_count / elapsed_time
    print(f"FPS: {fps:.2f}", "Sound Detection", Check_text, rms)
    frame_count = 0
    start_time = current_time
# 리소스 정리
stream.stop_stream()
stream.close()
p.terminate()