#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 27 14:28:36 2020

@author: albertovaldez
"""

import onset
from scipy.io import wavfile
import matplotlib.pyplot as plt


def SampleProfile(file, resolution):
    audio = onset.Song(wavfile.read("songs/samples/" + file))
    
    limits = [240,1680]
    note = audio.data[0:resolution]
    onset.PlotNote(note, audio.sampfreq, limits[0], limits[len(limits)-1], file.split(".")[0] + ".png")
    
    freqs, fft = onset.CalculateFFT_dB(note, audio.sampfreq, limits[0], limits[len(limits)-1])
    x, y = onset.GetSpectrumPeaks(freqs, fft)
    print(x,y)
    freq, amp = onset.GetTopFrequencies(x,y,8)
    plt.figure(figsize = (20,10))
    plt.xticks(freq)
    plt.scatter(freq,amp)
    plt.xlim(limits[0],limits[1])
    plt.ylim(10,30)

    plt.savefig("sp_" + file.split(".")[0] + ".png")
    plt.show()

bpm = 155
unit = int((60/bpm) * 0.25 * 44100)

SampleProfile("tone1.wav", unit)
SampleProfile("tone2.wav", unit)



