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

songName = "tobu_suchfun.wav"
#songName = str(input("Input song: ")).strip("'").replace(" ", "")

plotPath, csvPath = "PCP/plots/", "PCP/csv/"
song = onset.Song("songs/" + songName)

tr = onset.CalculateThreshold_RMS(song.data)
tr = int(tr * 10000)/10000

bpms = bpmb.GetBPM(song, tr)
bpm_user = int(input("Enter selected BPM: \n"))

noteTR = 0.7
songTR = 0.5
alphaPeak = song.FindAlphaPeak(0,songTR)

bpm, measure, unitSize = bpm_user, 4, 0.25
freqBands = [i*120 for i in range(3,14)] # 360 to 1920 by 120

maxBars = int((song.length_seconds * (1/(60/bpm)) / measure ))
print("Song duration in bars: " + str(maxBars))

# GET FREQUENCY AND ENERGY SEQUENCE AND PARSONS CODE

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

ez.PlotComplete(x_freq, pc_e, pc_f, bpm, maxBars, freqBands, plotPath, songName, noteTR, song.GetRMS(), alphaPeak)
parsons.SaveCSV3D(x_freq,pc_e,pc_f, csvPath, songName)

'''
BAR BY BAR PLOTS

#ez.PlotGridEnergy(freqBands, song, bpm, 0, 1, measure, unitSize, "test.png")
#ez.PlotNotesEnergy(freqBands, song, bpm, 0, 1, measure, unitSize, tr, "test.png")
#ez.PlotNotesFrequency(freqBands, song, bpm, 0, 1, measure, unitSize, tr, "test.png")

COMPLETE SONG PLOTS

ez.PlotPart(x_freq,y_freq, maxBars, plotPath + "full_freq.png")
ez.PlotPart(x_energy,y_energy, maxBars, plotPath + "full_energy.png")

parsons.SaveCSV(x_freq,y_freq, csvPath + "full_freq.csv")
parsons.SaveCSV(x_energy,y_energy, csvPath + "full_energy.csv")

ez.PlotPart(x_freq,y_f_pc,maxBars, plotPath + "fullPC_freq.png")
ez.PlotPart(x_energy,y_e_pc, maxBars, plotPath + "fullPC_energy.png")

parsons.SaveCSV(x_freq,y_f_pc, csvPath + "fullPC_freq.csv")
parsons.SaveCSV(x_energy,y_e_pc, csvPath + "fullPC_energy.csv")
'''


    
