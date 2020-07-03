#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GET FREQUENCY AND ENERGY SEQUENCE AND PARSONS CODE

@author: albertovaldez
"""
import onset
import parsons
import easygram as ez
import getBPM_Bass as bpmb

songName = "spectre.mp3"
plotPath, csvPath = "PCP/plots/", "PCP/csv/"
wavFile = mp3.toWAV(songName, "mp3/")
song = onset.Song(wavFile)

tr = onset.CalculateThreshold_RMS(song.data)
#bpms = bpmb.GetBPM(song, tr)
bpm_user = int(input("Enter selected BPM: \n"))

#SONG THRESHOLD FOR ALPHA PEAK, 0.0 if cut, 0.1 if instant, 0.5 if soft fade in, 0.8 if loud fade in
songTR = 0.8
noteTR = 0.7
alphaPeak = song.FindAlphaPeak(0,songTR)

bpm, measure, unitSize = bpm_user, 4, 0.25
#freqBands = [i*60 for i in range(5,26)] # Melody/Lead use continuous
#freqBands = [i*60 for i in range(2,6)] # Body/Snare use step
#freqBands = [9000, 16000] # High/Hats need custom de-peak process
freqBands = [i*60 for i in range(0,3)] # Bass/Kick use continuous

maxBars = int((song.length_seconds * (1/(60/bpm)) / measure ))
print("Song duration in bars: " + str(maxBars))

x_all, y_energy, z_freq  = [],[],[]

barBlock = 4
barBlock = maxBars
for i in range(maxBars//barBlock):
    barNum = i*barBlock
    x,y,z = ez.GetNotesPeaks3D_Continuous(freqBands, song, bpm, barNum, barNum+barBlock, measure, unitSize, noteTR)
    offset = i*barBlock*measure*(1/unitSize)
    #print(x,y,z)
    for j in range(len(y)):
        x_all.append(x[j] + offset)
        y_energy.append(y[j])
        z_freq.append(z[j])
    
peaks = []
for i in x_all:
    peaks.append(i * (60/bpm)*unitSize * song.sampfreq)
    
onset.SavePeaks(peaks, song.sampfreq, 1, 0, "reaper/Files/peaks.csv")

pc_e,pc_f = parsons.GetPCode(x_all, y_energy),parsons.GetPCode(x_all, z_freq)
x = [i*unitSize for i in x_all]

ez.PlotComplete(x, pc_e, pc_f, bpm, maxBars, measure, unitSize, freqBands, plotPath, songName, noteTR, song.GetRMS(), alphaPeak)
parsons.SaveCSV3D(x, pc_e,pc_f, csvPath, songName)

'''
ez.PlotPart(x,y_freq, maxBars, measure, unitSize, plotPath + "zRefs/" + str(songName.split(".")[0]) + "_freq.png")
ez.PlotPart(x,y_energy, maxBars, measure, unitSize, plotPath + "zRefs/" + str(songName.split(".")[0]) + "_energy.png")
parsons.SaveCSV(x,y_freq, csvPath + "zRefs/" + str(songName.split(".")[0]) + "_freq.csv")
parsons.SaveCSV(x,y_energy, csvPath + "zRefs/" + str(songName.split(".")[0]) + "_energy.csv")

BAR BY BAR PLOTS

#ez.PlotGridEnergy(freqBands, song, bpm, 0, 1, measure, unitSize, "test.png")
#ez.PlotNotesEnergy(freqBands, song, bpm, 0, 1, measure, unitSize, tr, "test.png")
#ez.PlotNotesFrequency(freqBands, song, bpm, 0, 1, measure, unitSize, tr, "test.png")

COMPLETE SONG PLOTS

ez.PlotPart(x_freq,y_f_pc,maxBars, plotPath + "fullPC_freq.png")
ez.PlotPart(x_energy,y_e_pc, maxBars, plotPath + "fullPC_energy.png")

parsons.SaveCSV(x_freq,y_f_pc, csvPath + "fullPC_freq.csv")
parsons.SaveCSV(x_energy,y_e_pc, csvPath + "fullPC_energy.csv")
'''

