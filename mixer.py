from pydub import AudioSegment
import time,os
from pydub.playback import play
import sys,wave
import pyaudio
WAVE_OUTPUT_FILENAME = "sample.wav"
chunk = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 10
p = pyaudio.PyAudio()
do = AudioSegment.from_mp3("audio/piano/1do.mp3")
re = AudioSegment.from_mp3("audio/piano/2re.mp3")
mi = AudioSegment.from_mp3("audio/piano/3mi.mp3")
fa = AudioSegment.from_mp3("audio/piano/4fa.mp3")
so = AudioSegment.from_mp3("audio/piano/5so.mp3")
la = AudioSegment.from_mp3("audio/piano/6la.mp3")
ti = AudioSegment.from_mp3("audio/piano/7ti.mp3")
doo = AudioSegment.from_wav("audio/piano/8doo.wav")
# stream = p.open(format=FORMAT,
# 		channels=CHANNELS,
# 		rate=RATE,
# 		input=True,
# 		output=True,
# 		frames_per_buffer=chunk)
# frames = []
# for i in range(0, 44100 / chunk * RECORD_SECONDS):
#     data = stream.read(chunk)
#     frames.append(data)
# print "playing..."
# waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
# waveFile.setnchannels(CHANNELS)
# waveFile.setsampwidth(p.get_sample_size(FORMAT))
# waveFile.setframerate(RATE)
# waveFile.writeframes(b''.join(frames))
# waveFile.close()
# test = AudioSegment.from_wav(WAVE_OUTPUT_FILENAME)
play(do[:450]+25)
#play(data)
