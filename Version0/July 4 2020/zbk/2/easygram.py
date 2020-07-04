#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SIMPLEGRAM: Simple Spectrogram
@author: albertovaldez
"""
import onset
import numpy as np
import matplotlib.pyplot as plt

def Easygram(limits,song,bpm,barIn,barEnd,measure,unitSize,save=False):
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
    save : TYPE, optional
        Save .csv file for multiband array.

    Returns
    -------
    multiband : TYPE
        An array of energy by frequency bands.
    energy : TYPE
        Total amount of energy in the chunk.
    topFrequencies : TYPE
        The frequency band(s) with highest energy.

    TO DO: Add number of top frequencies > 1, add option to enable PlotPeaks2
    '''
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
    threshold = (max(energy)-min(energy))*tr + min(energy)
    
    x, y, z, lastEnergy = [],[],[], 0
    for i in range(len(topFrequencies)):
        if energy[i] > threshold:
            if energy[i] > lastEnergy:
                for j in range(len(topFrequencies[i][0])): #[freq, energy]
                    x.append(i)
                    y.append(topFrequencies[i][1][j])
                    z.append(topFrequencies[i][0][j])
            lastEnergy = energy[i]
    return x, y, z

def GetNotesPeakFrequency(limits, song, bpm, barIn, barEnd, measure, unitSize, tr, save):
    multiband, energy, topFrequencies = Easygram(limits, song, bpm, barIn, barEnd, measure, unitSize, save)
    threshold = (max(energy)-min(energy))*tr + min(energy)

    x_peakFreq, y_peakFreq = [],[]
    for i in range(len(topFrequencies)):
        if energy[i] > threshold:
            for j in topFrequencies[i][0]: #[freq, energy]
                x_peakFreq.append(i)
                y_peakFreq.append(j)
            
    return x_peakFreq, y_peakFreq

def GetNotesPeakEnergy(limits, song, bpm, barIn, barEnd, measure, unitSize, tr, save):
    multiband, energy, topFrequencies = Easygram(limits, song, bpm, barIn, barEnd, measure, unitSize, save)
    threshold = (max(energy)-min(energy))*tr + min(energy)

    x_peakEnergy, y_peakEnergy = [],[]
    for i in range(len(topFrequencies)):
        if energy[i] > threshold:
            for j in topFrequencies[i][1]: #[freq, energy]
                x_peakEnergy.append(i)
                y_peakEnergy.append(j)
            
    return x_peakEnergy, y_peakEnergy

def GetNotesTotalEnergy(limits, song, bpm, barIn, barEnd, measure, unitSize, tr, save):
    multiband, energy, topFrequencies = Easygram(limits, song, bpm, barIn, barEnd, measure, unitSize, save)
    threshold = (max(energy)-min(energy))*tr + min(energy)
    
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
    plt.xticks([int(i*(1/unitSize)) for i in range(int(maxBars*measure)+1)])
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
    print("Saved plot to path.")

    
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