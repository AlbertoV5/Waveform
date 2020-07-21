#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 17:19:41 2020

@author: albertovaldezquinto
"""

import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
import onset
from scipy import stats

audioPath = "drums.wav"

song = onset.Song(audioPath)
rms = onset.GetRMS(song.data)
print("RMS:", rms, "dB")

data = song.data
sr = song.sampfreq

tempo, beats = librosa.beat.beat_track(y=data, sr=sr, units = "samples")

print("BPM", tempo)

def GetBeatFrequencySnapshot(x, chunkSize, filterLow, filterHigh):
    chunksInData = len(x)//chunkSize
    frequencies = np.empty(0)
    energies = np.empty(0)
    for i in range(chunksInData - 1):
        start = int(i*chunkSize)
        end = int(i*chunkSize) + chunkSize
        chunk = x[start:end]
        
        freq, fft = onset.CalculateFFT_dB(chunk,sr, filterLow, filterHigh)
        energy = np.sum(fft)
        frequency = np.average(freq, weights=fft)
        
        energies = np.append(energies, energy)
        frequencies = np.append(frequencies, frequency)
        
    freq = np.average(frequencies)
    power = np.average(energies)
    #index = np.where(frequencies == mode)
    #np.average(frequencies)
    return np.array([freq, power])

def GetBeatBlueprint(tempo, beats):
    low, mid, high = np.empty(2), np.empty(2), np.empty(2)
    beatSecond = 60/tempo
    beatSampleSize = int(beatSecond * sr)
    for i in beats:
        x = data[i:i + beatSampleSize]
        low = np.vstack((low,GetBeatFrequencySnapshot(x, 2048, 0, 120)))
        mid = np.vstack((mid,GetBeatFrequencySnapshot(x, 2048, 120, 300)))
        high = np.vstack((high,GetBeatFrequencySnapshot(x, 2048, 4000, 8000)))
        #spectral_centroids = librosa.feature.spectral_centroid(x, sr=sr, n_fft = 2048, hop_length = 2048)[0]
        #print("Spectral Centroid:", np.mean(spectral_centroids))
        
    return low, mid, high

low, mid, high = GetBeatBlueprint(tempo, beats)

x = range(len(beats))

plt.figure(figsize= (20,10))
y = low[:,1]
y *= (1 / np.max(y))
y = y[y > 0.01]
plt.scatter(range(len(y)),y)

y = mid[:,1]
y *= (1 / np.max(y))
y = y[y > 0.01]
plt.scatter(range(len(y)),y)

y = high[:,1]
y = y[y < 11000]
y *= (1 / (np.max(y) + 0.001))
y = y[y > 0.01]
plt.scatter(range(len(y)),y)

plt.legend(["Low 0-120 Hz", "Mid 120-300 Hz", "High 4-8 kHz"], fontsize = 18)
plt.title("Spectral Centroid by Frequency Band", fontsize = 20)
plt.savefig("fig.png")
plt.show()





    
    
