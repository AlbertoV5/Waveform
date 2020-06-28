#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Recommended values for most songs:
0.9 > Ratio > 0.7
Unit 2048, 1024, 4096

Transient Points are the highest value sample within a certain range of NoteOnset

'''
import onset
from scipy.io import wavfile
import matplotlib.pyplot as plt
import numpy as np

songName = "lektrique.wav"

song = onset.Audio(wavfile.read("songs/" + songName))

song.FindAlphaPeak(0,0.8)

size = 2048
song.GetNoteOnset(unit = 2048, chunk_size = size, threshold_ratio = 0.7, HPF = 100, LPF = 500)

song.PlotNoteOnset()

song.GetPeaks(x = 1024)

song.PlotPeaks()
print(song.pks)

# BPM_TP seems to be more precise due to the transient points
# mode, mean, median

bpm1 = song.GetBPM(70,240, "mode")
bpm2 = song.GetBPM_PKS(70, 240, "mode")

print("BPM:", bpm1, bpm2)

# "mode" is best for complete songs, "mean" and "median" are better for small sections
# depending on the song, BPM_TP may be wildly different than BPM on "mode" 

print(song.notes[0])
print(song.pks[0])

start = song.pks[0]
bpm = bpm2
unitSample = (60/bpm)/4 #1/16 of a bar, 1/4 of a beat










