from machine import I2S
from m5stack import *
import wave
import _thread

def playWav(filePath):
    if type(filePath) != str:
        raise ImportError("wav name must be string")
    wav = wave.open(filePath)
    i2s = I2S(mode=I2S.MODE_MASTER | I2S.MODE_TX | I2S.MODE_DAC_BUILT_IN)
    i2s.set_dac_mode(i2s.DAC_RIGHT_EN)
    i2s.sample_rate(wav.getframerate())
    i2s.bits(wav.getsampwidth() * 8)
    i2s.nchannels(wav.getnchannels())
    i2s.volume(70)
    while True:
        data = wav.readframes(256)
        if len(data) > 0:
            i2s.write(data)
        else:
            wav.close()
            i2s.deinit()
            break