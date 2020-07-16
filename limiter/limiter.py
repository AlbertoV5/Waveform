#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 12 19:56:42 2020

@author: albertovaldez
"""

from scipy.io import wavfile
from scipy.interpolate import interp1d
import numpy as np

def RMS(fileName):

    audiofile = wavfile.read(fileName)
    data = audiofile[1] #16 bits
    rms = (np.mean(np.absolute(data)))
    rmsDB = 20*np.log10((np.mean(np.absolute(data))))
    
    print("RMS:", rms, rmsDB)
    return rms, data

def apply_transfer(signal, transfer, interpolation='linear'):
    constant = np.linspace(-1, 1, len(transfer))
    interpolator = interp1d(constant, transfer, interpolation)
    return interpolator(signal)


def limiter(x, treshold=0.3):
    transfer_len = 1000
    transfer = np.concatenate([ np.repeat(-1, int(((1-treshold)/2)*transfer_len)),
                                np.linspace(-1, 1, int(treshold*transfer_len)),
                                np.repeat(1, int(((1-treshold)/2)*transfer_len)) ])
    return apply_transfer(x, transfer)

target, targetData = RMS("camellia.wav")
sub, subData = RMS("reaction.wav")

ratio = target/sub

print(ratio)
print((1/ratio))
'''
outputData = subData * ratio
clippingIndex = outputData > 32767
outputData[clippingIndex] *= (1/ratio)
subData = subData * 1.0
belowIndex = np.abs(subData) < target
subData[belowIndex] *= ratio

'''
sr, x = wavfile.read("in.wav")
x = x / 32767


x2 = limiter(x)
x2 = x2 * (1/np.max(x2))

rms = 20*np.log10((np.mean(np.absolute(x2))))
print(rms)

x2 = np.int16(x2 * 32767)
wavfile.write("out.wav", sr, x2)


