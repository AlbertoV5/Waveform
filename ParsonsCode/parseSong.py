#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GET FREQUENCY AND ENERGY SEQUENCE AND PARSONS CODE

@author: albertovaldez
"""
import onset
from scipy.io import wavfile
import parsons
import easygram as ez
import matplotlib.pyplot as plt

def Plot(x,y,name):
    plt.figure(figsize=(30,10))
    plt.grid(True)
    plt.plot(x, y)
    plt.scatter(x, y)
    plt.xticks([i*16 for i in range(maxBars+1)])
    plt.savefig(name)
    plt.show()

song = onset.Song(wavfile.read("songs/" + "pegbdisc.wav"))
tr = onset.CalculateThreshold_RMS(song.data)
song.FindAlphaPeak(0,0.33)
plotPath = "PCP/"
csvPath = "PCP/csv/"

bpm, bars, measure, unitSize = 128, 64, 4, 0.25
freqBands = [i*120 for i in range(3,17)] # 360 to 1920 by 120 
x_master, y_master = [],[]
tr = 0.8

maxBars = int((song.length_seconds * (1/(60/bpm)) / measure ))
print("Song duration in bars: " + str(maxBars))

#ez.PlotGridEnergy(freqBands, song, bpm, 0, 1, measure, unitSize, "test.png")
#ez.PlotNotesEnergy(freqBands, song, bpm, 0, 1, measure, unitSize, tr, "test.png")
#ez.PlotNotesFrequency(freqBands, song, bpm, 0, 1, measure, unitSize, tr, "test.png")


# GET FREQUENCY AND ENERGY SEQUENCE AND PARSONS CODE

for i in range(maxBars):
    try:
        x,y = ez.GetNotesPeakFrequency(freqBands, song, bpm, i, i+1, measure, unitSize, tr, False)
        for j in range(len(y)):
            x_master.append(x[j] + (i*measure*(1/unitSize)))
            y_master.append(y[j])
    except:
        break

y_pc = parsons.GetPCode(x_master, y_master)

Plot(x_master,y_master, plotPath + "full_freq.png")
parsons.SaveCSV(x_master,y_master, csvPath + "full_freq.csv")

Plot(x_master,y_pc, plotPath + "fullPC_freq.png")
parsons.SaveCSV(x_master,y_pc, csvPath + "fullPC_freq.csv")


x_master, y_master = [],[]

for i in range(maxBars):
    try:
        x,y = ez.GetNotesPeakEnergy(freqBands, song, bpm, i, i+1, measure, unitSize, tr, False)
        for j in range(len(y)):
            x_master.append(x[j] + (i*measure*(1/unitSize)))
            y_master.append(y[j])
    except:
        break

y_pc = parsons.GetPCode(x_master, y_master)

Plot(x_master,y_master, plotPath + "full_energy.png")
parsons.SaveCSV(x_master,y_master, csvPath + "full_energy.csv")

Plot(x_master,y_pc, plotPath + "fullPC_energy.png")
parsons.SaveCSV(x_master,y_pc, csvPath + "fullPC_energy.csv")


    
