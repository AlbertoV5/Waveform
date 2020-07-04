#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Easygram: Easy spectrogram
@author: albertovaldez
"""
import onset
import numpy as np
import matplotlib.pyplot as plt

def Easygram(limits,song,bpm,barIn,barEnd,measure,unitSize):
    '''
    Easy spectrogram that uses Frequency Peaks and Frequency Bands to simplify the waveform information.

    Parameters
    ----------
    limits : TYPE
        Receive a list of frequency bands of same length.
    song : TYPE
        Song object from onset, used to localize the chunk.
    bpm : TYPE
        Bpm of the song.
    barIn : TYPE
        Bar Number for chunk start.
    barEnd : TYPE
         Bar Number for chunk end.
    measure : TYPE
        Number of beats in bar.
    unitSize : TYPE
        Grid division by beat size, 1/16 of 1/4 is 0.25.

    Returns
    -------
    energy : TYPE
        Total amount of energy in the chunk.
    topFrequencies : TYPE
        The frequency band(s) with highest energy.

    TO DO: Add number of top frequencies > 1, add option to enable PlotPeaks2
    '''
    energy, topFrequencies = [], []
    unitStar = int(barIn * measure * (1/unitSize))
    amountOfUnits = int(barEnd * measure * (1/unitSize))

    unit = (60/bpm) * song.sampfreq * unitSize
    unitRange = 2048
    pai = song.peakAlphaIndex
    
    for i in range(unitStar,amountOfUnits):
        start, end = pai + int(i * unit), pai + int(i * unit) + unitRange
        chunk = song.data[start:end]
        freqs, fft = onset.CalculateFFT_dB(chunk, song.sampfreq, limits[0], limits[len(limits)-1])
        energy.append(np.max(fft)) # max energy point
        topFrequencies.append(onset.GetTopFrequencies(freqs, fft, start, 1))
        
    return energy,topFrequencies

def Easygram_Sum(limits,song,bpm,barIn,barEnd,measure,unitSize):
    energy, topFrequencies = [], []
    unitStart = int(barIn * measure * (1/unitSize))
    amountOfUnits = int(barEnd * measure * (1/unitSize))

    unit = (60/bpm) * song.sampfreq * unitSize
    unitRange = 2048
    pai = song.peakAlphaIndex
    
    for i in range(unitStart,amountOfUnits):
        start, end = pai + int(i * unit), pai + int(i * unit) + unitRange
        chunk = song.data[start:end]
        freqs, fft = onset.CalculateFFT_dB(chunk, song.sampfreq, limits[0], limits[len(limits)-1])
        energy.append(np.sum(fft)) # min energy point
        topFrequencies.append(onset.GetTopFrequencies(freqs, fft, start, 1))
        
    return energy,topFrequencies

def GetNotesPeaks3D_Step(limits, song, bpm, barIn, barEnd, measure, unitSize, tr):
    energy, topFrequencies = Easygram(limits, song, bpm, barIn, barEnd, measure, unitSize)
    threshold = (max(energy)-min(energy))*tr + min(energy)
    x, y, z, lastEnergy = [],[],[], 0
    for i in range(len(topFrequencies)):
        if energy[i] > threshold:
            if i % 4 == 0:
                lastEnergy = 0
            if energy[i] > lastEnergy*1.0:
                for j in range(len(topFrequencies[i][0])): #[freq, energy]
                    x.append(i)
                    y.append(topFrequencies[i][1][j])
                    z.append(topFrequencies[i][0][j])
                lastEnergy = energy[i]
            else:
                lastEnergy = lastEnergy
        else:
            lastEnergy = energy[i]
    return x, y, z

def GetNotesPeaks3D_Step_Sum(limits, song, bpm, barIn, barEnd, measure, unitSize, tr):
    energy, topFrequencies = Easygram_Sum(limits, song, bpm, barIn, barEnd, measure, unitSize)
    threshold = (max(energy)-min(energy))*tr + min(energy)
    x, y, z, lastEnergy = [],[],[], 0
    for i in range(len(topFrequencies)):
        if energy[i] > threshold:
            if energy[i] > lastEnergy*1.0:
                for j in range(len(topFrequencies[i][0])): #[freq, energy]
                    x.append(i)
                    y.append(topFrequencies[i][1][j])
                    z.append(topFrequencies[i][0][j])
                lastEnergy = energy[i]
            else:
                lastEnergy = lastEnergy
        else:
            lastEnergy = energy[i] #failed to pass
    return x, y, z

def GetNotesPeaks3D_Continuous(limits, song, bpm, barIn, barEnd, measure, unitSize, tr):
    energy, topFrequencies = Easygram(limits, song, bpm, barIn, barEnd, measure, unitSize)
    threshold = (max(energy)-min(energy))*tr + min(energy)
    x, y, z = [],[],[]
    for i in range(len(topFrequencies)):
        if energy[i] > threshold:
            for j in range(len(topFrequencies[i][0])): #[freq, energy]
                x.append(i)
                y.append(topFrequencies[i][1][j])
                z.append(topFrequencies[i][0][j])
    return x, y, z

def GetNotesPeaks3D_Continuous_Sum(limits, song, bpm, barIn, barEnd, measure, unitSize, tr):
    energy, topFrequencies = Easygram_Sum(limits, song, bpm, barIn, barEnd, measure, unitSize)
    threshold = (max(energy)-min(energy))*tr + min(energy)
    x, y, z = [],[],[]
    for i in range(len(topFrequencies)):
        if energy[i] > threshold:
            for j in range(len(topFrequencies[i][0])): #[freq, energy]
                x.append(i)
                y.append(topFrequencies[i][1][j])
                z.append(topFrequencies[i][0][j])
    return x, y, z

def PlotGridEnergy(limits, song, bpm, barIn, barEnd, measure, unitSize, name):
    multiband,energy,topFrequencies = Easygram(limits, song, bpm, barIn, barEnd, measure, unitSize, False)
    x, y = range(len(energy)), energy
    xticks = [i*(1/unitSize) for i in range(1 + (barEnd*measure) - (barIn*measure))]
    ylim = (0,3000)
    
    Plot(x,y,xticks,ylim, "Amplitude (Energy)", "Time (Beats)", name)

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
    
def PlotPart(x,y,maxBars,measure,unitSize,name):
    plt.figure(figsize=(40,10))
    plt.grid(True)
    plt.plot(x, y)
    plt.scatter(x, y)
    plt.xticks([int(i*(measure/unitSize)) for i in range(int(maxBars*unitSize)+1)])
    plt.xlabel("Position (beats)")
    plt.savefig(name)
    plt.show()
    
def PlotComplete(x,y_e_pc,y_f_pc,bpm,maxBars,measure,unitSize,freqBands,plotPath,songName, tr, rms, peakAlpha):
    name = plotPath + songName.split(".")[0] + ".png"
    title = "Name: " + songName.split(".")[0] + ", BPM: " + str(bpm) + ", FreqBands: " + str(freqBands[0])
    title = title + " to " + str(freqBands[len(freqBands)-1]) + " Hz, RMS: " + str(rms) + " dB"
    title = title + ", Threshold: " + str(tr) + ", Starts at: " + str(peakAlpha) + " sec"

    plt.figure(figsize=(50,10))
    plt.xticks([int(i*(1/0.25)) for i in range(int(maxBars*measure)+1)])
    plt.grid(True)
    
    plt.plot(x, y_e_pc, color = "r")
    plt.plot(x, y_f_pc, color = "b")
    
    plt.legend(["Energy", "Frequency"], fontsize = 20)
    plt.scatter(x, y_f_pc, color = "b")
    plt.scatter(x, y_e_pc, color = "r")
    
    plt.title(title, fontsize = 24)
    plt.ylabel("Parsons Code", fontsize = 20)
    plt.xlabel("Position (beats)", fontsize = 20)
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
