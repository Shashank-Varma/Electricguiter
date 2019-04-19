import wave
import numpy as np
import matplotlib.pyplot as plt
import sys

wr = wave.open('sample.wav', 'r')
# Set the parameters for the output file.
par = list(wr.getparams())
par[3] = 0
par = tuple(par)
ww = wave.open('output.wav', 'w')
ww.setparams(par)

fr = 20
sz = wr.getframerate()//fr  # Read and process 1/fr second at a time.
c = int(wr.getnframes()/sz)  # count of the whole file
shift = 1000//fr  # shifting 1000 Hz
for num in range(c):
    da = np.fromstring(wr.readframes(sz), dtype=np.int16)
    left, right = da[0::2], da[1::2]  # left and right channel
    lf, rf = np.fft.rfft(left), np.fft.rfft(right)
    lf, rf = np.roll(lf, shift), np.roll(rf, shift)
    lf[0:shift], rf[0:shift] = 0, 0
    nl, nr = np.fft.irfft(lf), np.fft.irfft(rf)
    ns = np.column_stack((nl, nr)).ravel().astype(np.int16)
    ww.writeframes(ns.tostring())
wr.close()
ww.close()

w1 = wave.open('sample.wav','r')

signal = w1.readframes(-1)
signal = np.fromstring(signal, 'Int16')
