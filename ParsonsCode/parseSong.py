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

songName = "pegbdisc.wav"
song = onset.Song(wavfile.read("songs/" + songName))
tr = onset.CalculateThreshold_RMS(song.data)
song.FindAlphaPeak(0,0.33)

def GetSimpleSpectrogram_FromNotes(limits, bpm, barIn, bars, measure, unitSize):
    multiband = []
    energy = []
    freqHighest = []
    unitStar = int(barIn * measure * (1/unitSize))
    amountOfUnits = int(bars * measure * (1/unitSize))
    
    unit = (60/bpm) * song.sampfreq * unitSize
    unitRange = 4096
    
    pai = song.peakAlphaIndex
    
    for i in range(unitStar,amountOfUnits):
        start, end = pai + int(i * unit), pai + int(i * unit) + unitRange
        chunk = song.data[start:end]
        
        freqs, fft = onset.CalculateFFT_dB(chunk, song.sampfreq, limits[0], limits[len(limits)-1])
        x, y = freqs, fft
        
        freqBandsAmp = onset.FrequencyBands(x,y,limits)
        #onset.PlotPeaks2(limits, freqBandsAmp, limits, (0,250), "plotUnits/" + str(i+1) + ".png")
        
        multiband.append(freqBandsAmp) 
        
        totalEnergy = np.sum(freqBandsAmp)
        energy.append(totalEnergy)
        
        pks_x, pks_y = list(limits), list(freqBandsAmp)
        topFreqs, amplitude = onset.GetTopFrequencies(pks_x, pks_y, 1)
        
        freqHighest.append([amplitude,topFreqs])        
        
    xticks = [i*(measure/unitSize) for i in range(1 + bars - barIn)]
    xticks = [i*(1/unitSize) for i in range(1 + (bars*measure) - (barIn*measure))]
    path = "PCP/"
    
    onset.SaveSimpleSpectrogram(limits, multiband)
    
    onset.PlotPeaks2(range(len(energy)),energy,xticks,(min(energy),max(energy)),path + "energy_" + str(barIn) + ".png")
    
    threshold = max(energy)*0.75
    x_h, y_h = [],[]
    for i in range(len(energy)):
        if energy[i] > threshold:
            y_h.append(energy[i])
            x_h.append(i)
    
    #onset.PlotPeaks2(x_h,y_h,xticks,(min(energy),max(energy)),path + "energyTop_" + str(barIn) + ".png")
    
    x_f, y_f = [],[]
    for i in range(len(freqHighest)):
        if energy[i] > threshold:
            for j in freqHighest[i][1]:
                x_f.append(i)
                y_f.append(j)
            
    xlim = amountOfUnits - unitStar

    #onset.PlotTopFreqs(x_f,y_f,xticks,xlim,path + "freqTop_" + str(barIn) + ".png")
    
    csv = ""
    for i in range(len(x_f)):
        csv = csv + str(x_f[i]) + "," + str(y_f[i]) + "\n"
        
    with open("freqNotes.csv", "w+") as file:
        file.write(csv)
        
    y_f = parsons.GetPCode_Silence(x_f, y_f)
    onset.PlotTopFreqs(x_f,y_f,xticks,xlim,path + "pc_" + str(barIn) + ".png")
    print("Got parsons code of bar: " + str(barIn))

freqLimits = [i*120 for i in range(3,17)]


for i in range(16):
    GetSimpleSpectrogram_FromNotes(freqLimits, bpm = 128, barIn = i, bars = i+1, measure = 4, unitSize = 0.25)



