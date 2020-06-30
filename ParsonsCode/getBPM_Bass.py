#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: albertovaldez
"""
import onset

def GetBPM(song, tr):
    #tr = onset.CalculateThreshold_RMS(song.data)
    
    print("\nCalculating Possible BPMs...")
    song.FindAlphaPeak(0,0.7)
    song.GetNoteOnset(unit = 2048, chunk_size = 4096, threshold_ratio = tr, HPF = 0, LPF = 240, base = 10)
    song.GetPeaks(x = 1024)
    print("\nCalculated possible BPMs:")
    
    magicRatio = (128/129.19921875)
    magicRatio2 = 1
    
    bpm1 = song.GetBPM()*magicRatio
    
    bpm2 = int(song.GetBPM_PKS()*magicRatio2*100)/100
    bpmBatch = [bpm1, bpm1*1.5, bpm2, bpm2*1.5]
    
    print(bpmBatch)
    
    #onset.SavePeaks(song.pks, song.sampfreq, 1, 0, "reaper/Files/peaks.csv") 
    #song.PlotPeaks()    
    #limits = [i*120 for i in range(16)]   
    #GetSimpleSpectrogram_FromNotes(limits)
    
    return bpmBatch

def GetSimpleSpectrogram_FromNotes(limits, song):
    multiband = []
    for i in range(len(song.notes)):
        start, end = song.notes[i][0], song.notes[i][0] + 4096
        chunk = song.data[start:end]
        
        freqs, fft = onset.CalculateFFT_dB(chunk, song.sampfreq, limits[0], limits[len(limits)-1])
        #x, y = onset.GetSpectrumPeaks(freqs, fft)
        x, y = freqs, fft
        
        freqBandsAmp = onset.FrequencyBands(x,y,limits)
        onset.PlotPeaks2(limits, freqBandsAmp, limits, (0,300), "plots/" + str(i+1) + ".png")
        multiband.append(freqBandsAmp) 
    
    onset.SaveSimpleSpectrogram(limits, multiband)

