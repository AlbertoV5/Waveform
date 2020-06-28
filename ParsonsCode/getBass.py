#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: albertovaldez
"""
import onset
from scipy.io import wavfile

songName = "pegbdisc.wav"
song = onset.Song(wavfile.read("songs/" + songName))
tr = onset.CalculateThreshold_RMS(song.data)
song.FindAlphaPeak(0,0.5)
song.GetNoteOnset(unit = 2048, chunk_size = 4096, threshold_ratio = tr, HPF = 0, LPF = 180, base = 10)
song.GetPeaks(x = 1024)
    
onset.SavePeaks(song.pks, song.sampfreq, 1, 0, "reaper/Files/peaks.csv") 
song.PlotPeaks()

print("Calculated BPMs: \n" + str(song.GetBPM()) + ", " + str(song.GetBPM_PKS()))

def GetSimpleSpectrogram_FromNotes(limits):
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


limits = [i*120 for i in range(16)]   
#GetSimpleSpectrogram_FromNotes(limits)

