#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SIMPLEGRAM: Simple Spectrogram
@author: albertovaldez
"""
import onset
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def Easygram(limits,song,bpm,barIn,barEnd,measure,unitSize,save=False):
    multiband, energy, topFrequencies = [], [], []
    unitStar = int(barIn * measure * (1/unitSize))
    amountOfUnits = int(barEnd * measure * (1/unitSize))

    unit = (60/bpm) * song.sampfreq * unitSize
    unitRange = 4096
    pai = song.peakAlphaIndex
    
    for i in range(unitStar,amountOfUnits):
        start, end = pai + int(i * unit), pai + int(i * unit) + unitRange
        chunk = song.data[start:end]
        freqs, fft = onset.CalculateFFT_dB(chunk, song.sampfreq, limits[0], limits[len(limits)-1])
        
        x,y = onset.GetFrequencyPeaks(freqs, fft)
        freqBandsAmp = onset.FrequencyBands(x,y,limits)
        #onset.PlotPeaks2(limits, freqBandsAmp, limits, (0,250), "plotUnits/" + str(i+1) + ".png")
        
        multiband.append(freqBandsAmp) # energy in bands
        energy.append(np.sum(freqBandsAmp)) # total energy in spectrum
        topFrequencies.append(onset.GetTopFrequencies(limits, freqBandsAmp, 1))
        
    if save == True:
        SaveSimpleSpectrogram(limits, multiband)
        
    return multiband,energy,topFrequencies

def GetNotesPeaks3D(limits, song, bpm, barIn, barEnd, measure, unitSize, tr, save):
    multiband, energy, topFrequencies = Easygram(limits, song, bpm, barIn, barEnd, measure, unitSize, save)
    threshold = max(energy)*tr
    x, y, z = [],[],[]
    for i in range(len(topFrequencies)):
        if energy[i] > threshold:
            for j in range(len(topFrequencies[i][0])): #[freq, energy]
                x.append(i)
                y.append(topFrequencies[i][1][j])
                z.append(topFrequencies[i][0][j])
    return x, y , z

def GetNotesPeakFrequency(limits, song, bpm, barIn, barEnd, measure, unitSize, tr, save):
    multiband, energy, topFrequencies = Easygram(limits, song, bpm, barIn, barEnd, measure, unitSize, save)
    threshold = max(energy)*tr

    x_peakFreq, y_peakFreq = [],[]
    for i in range(len(topFrequencies)):
        if energy[i] > threshold:
            for j in topFrequencies[i][0]: #[freq, energy]
                x_peakFreq.append(i)
                y_peakFreq.append(j)
            
    return x_peakFreq, y_peakFreq

def GetNotesPeakEnergy(limits, song, bpm, barIn, barEnd, measure, unitSize, tr, save):
    multiband, energy, topFrequencies = Easygram(limits, song, bpm, barIn, barEnd, measure, unitSize, save)
    threshold = max(energy)*tr

    x_peakEnergy, y_peakEnergy = [],[]
    for i in range(len(topFrequencies)):
        if energy[i] > threshold:
            for j in topFrequencies[i][1]: #[freq, energy]
                x_peakEnergy.append(i)
                y_peakEnergy.append(j)
            
    return x_peakEnergy, y_peakEnergy

def GetNotesTotalEnergy(limits, song, bpm, barIn, barEnd, measure, unitSize, tr, save):
    multiband, energy, topFrequencies = Easygram(limits, song, bpm, barIn, barEnd, measure, unitSize, save)
    threshold = max(energy)*tr
    
    x_totalEnergy, y_totalEnergy = [],[]
    for i in range(len(energy)):
        if energy[i] > threshold:
            y_totalEnergy.append(energy[i])
            x_totalEnergy.append(i)
            
    return x_totalEnergy, y_totalEnergy

def PlotGridEnergy(limits, song, bpm, barIn, barEnd, measure, unitSize, name):
    multiband,energy,topFrequencies = Easygram(limits, song, bpm, barIn, barEnd, measure, unitSize, False)
    x, y = range(len(energy)), energy
    xticks = [i*(1/unitSize) for i in range(1 + (barEnd*measure) - (barIn*measure))]
    ylim = (0,3000)
    
    Plot(x,y,xticks,ylim, "Amplitude (Energy)", "Time (Beats)", name)
    

def PlotNotesEnergy(limits, song, bpm, barIn, barEnd, measure, unitSize, tr, name):
    x, y = GetNotesPeakEnergy(limits, song, bpm, barIn, barEnd, measure, unitSize, tr, False)
    xticks = [i*(1/unitSize) for i in range(1 + (barEnd*measure) - (barIn*measure))]
    ylim = (0,3000)

    Plot(x,y,xticks,ylim, "Amplitude (Energy)", "Time (Beats)", name)


def PlotNotesFrequency(limits, song, bpm, barIn, barEnd, measure, unitSize, tr, name):
    x, y = GetNotesPeakFrequency(limits, song, bpm, barIn, barEnd, measure, unitSize, tr, False)
    xticks = [i*(1/unitSize) for i in range(1 + (barEnd*measure) - (barIn*measure))]
    ylim = (limits[0],limits[len(limits)-1])
    
    Plot(x,y,xticks,ylim, "Frequency (Hz)", "Time (Beats)", name)


def Plot(x, y, xticks, ylim, ylabel, xlabel, name):
    plt.figure(figsize=(20,10))
    plt.grid(True)
    plt.xticks(xticks)
    plt.plot(x,y)
    plt.scatter(x,y)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    plt.savefig(name)
    plt.show()
    
    
def SaveSimpleSpectrogram(limits, simpleSpectrogram):
    csv = ""
    for i in limits:
        csv = csv + str(i) + ","
    
    for i in simpleSpectrogram:
        csv = csv + "\n"
        for j in i:
            csv = csv + str(j) + ","
    
    with open("simpleSpectrogram.csv", "w+") as file:
        file.write(csv)      