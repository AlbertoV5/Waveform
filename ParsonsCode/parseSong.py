#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 27 17:22:45 2020

@author: albertovaldez
"""

import onset
from scipy.io import wavfile
import numpy as np
import parsons
import easygram as ez
import matplotlib.pyplot as plt

song = onset.Song(wavfile.read("songs/" + "pegbdisc.wav"))
tr = onset.CalculateThreshold_RMS(song.data)
song.FindAlphaPeak(0,0.33)
plotPath = "PCP/"

bpm, measure, unitSize = 128, 4, 0.25
r = range(4,17)
freqBands = [i*120 for i in r]
x_master, y_master = [],[]
numBars = 0
tr = 0.8

#ez.PlotGridEnergy(freqBands, song, bpm, 0, 1, measure, unitSize, "test.png")
#ez.PlotNotesEnergy(freqBands, song, bpm, 0, 1, measure, unitSize, tr, "test.png")
#ez.PlotNotesFrequency(freqBands, song, bpm, 0, 1, measure, unitSize, tr, "test.png")

for i in range(numBars):
    x,y = ez.GetNotesPeakFrequency(freqBands, song, bpm, i, i+1, measure, unitSize, tr, False)
    for j in range(len(y)):
        x_master.append(x[j] + (i*measure*(1/unitSize)))
        y_master.append(y[j])

y_master = parsons.GetPCode_Silence(x_master, y_master)
parsons.SaveCSV(x_master,y_master, "pc_freq.csv")

plt.figure(figsize=(30,10))
plt.grid(True)
plt.plot(x_master, y_master)
plt.scatter(x_master, y_master)
plt.xticks([i*16 for i in range(numBars+1)])
plt.savefig("pc_freq.png")
plt.show()

    
