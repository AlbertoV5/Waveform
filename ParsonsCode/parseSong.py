#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 27 17:22:45 2020

@author: albertovaldez
"""

import onset
from scipy.io import wavfile
import parsons
import easygram as ez
import matplotlib.pyplot as plt

song = onset.Song(wavfile.read("songs/" + "pegbdisc.wav"))
tr = onset.CalculateThreshold_RMS(song.data)
song.FindAlphaPeak(0,0.33)
plotPath = "PCP/"

bpm, bars, measure, unitSize = 128, 64, 4, 0.25
freqBands = [i*120 for i in range(4,17)]
x_master, y_master = [],[]
tr = 0.8

#ez.PlotGridEnergy(freqBands, song, bpm, 0, 1, measure, unitSize, "test.png")
#ez.PlotNotesEnergy(freqBands, song, bpm, 0, 1, measure, unitSize, tr, "test.png")
#ez.PlotNotesFrequency(freqBands, song, bpm, 0, 1, measure, unitSize, tr, "test.png")

for i in range(bars):
    x,y = ez.GetNotesPeakFrequency(freqBands, song, bpm, i, i+1, measure, unitSize, tr, False)
    for j in range(len(y)):
        x_master.append(x[j] + (i*measure*(1/unitSize)))
        y_master.append(y[j])

#y_master = parsons.GetPCode(x_master, y_master)
parsons.SaveCSV(x_master,y_master, plotPath + "base_freq.csv")

plt.figure(figsize=(30,10))
plt.grid(True)
plt.plot(x_master, y_master)
plt.scatter(x_master, y_master)
plt.xticks([i*16 for i in range(bars+1)])
plt.savefig(plotPath + "base_freq.png")
plt.show()

    
