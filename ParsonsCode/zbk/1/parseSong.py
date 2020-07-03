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

songName = "axtasia_closer.wav"
plotPath, csvPath = "PCP/plots/", "PCP/csv/"
song = onset.Song("songs/" + songName)

tr = onset.CalculateThreshold_RMS(song.data)
bpms = bpmb.GetBPM(song, tr)
bpm_user = int(input("Enter selected BPM: \n"))

noteTR = 0.7
#SONG THRESHOLD FOR ALPHA PEAK, 0.0 if cut, 0.1 if instant, 0.5 if soft fade in, 0.8 if loud fade in
songTR = 0.1
alphaPeak = song.FindAlphaPeak(0,songTR)

bpm, measure, unitSize = bpm_user, 4, 0.25
freqBands = [i*60 for i in range(5,26)] # 300 to 1500 by 60

maxBars = int((song.length_seconds * (1/(60/bpm)) / measure ))
print("Song duration in bars: " + str(maxBars))

x_freq, y_freq, x_energy, y_energy  = [],[],[],[]

for i in range(maxBars):
    try:
        x,y = ez.GetNotesPeakFrequency(freqBands, song, bpm, i, i+1, measure, unitSize, noteTR, False)
        for j in range(len(y)):
            x_freq.append(x[j] + (i*measure*(1/unitSize)))
            y_freq.append(y[j])
            
        x,y = ez.GetNotesPeakEnergy(freqBands, song, bpm, i, i+1, measure, unitSize, noteTR, False)
        for j in range(len(y)):
            x_energy.append(x[j] + (i*measure*(1/unitSize)))
            y_energy.append(y[j])
    except:
        break

pc_e = parsons.GetPCode(x_energy, y_energy)
pc_f = parsons.GetPCode(x_freq, y_freq)

x = [i*unitSize for i in x_freq]

ez.PlotComplete(x, pc_e, pc_f, bpm, maxBars, measure, unitSize, freqBands, plotPath, songName, noteTR, song.GetRMS(), alphaPeak)
parsons.SaveCSV3D(x, pc_e,pc_f, csvPath, songName)

ez.PlotPart(x,y_freq, maxBars, measure, unitSize, plotPath + "zRefs/" + str(songName.split(".")[0]) + "_freq.png")
ez.PlotPart(x,y_energy, maxBars, measure, unitSize, plotPath + "zRefs/" + str(songName.split(".")[0]) + "_energy.png")

parsons.SaveCSV(x,y_freq, csvPath + "zRefs/" + str(songName.split(".")[0]) + "_freq.csv")
parsons.SaveCSV(x,y_energy, csvPath + "zRefs/" + str(songName.split(".")[0]) + "_energy.csv")

'''
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


    
