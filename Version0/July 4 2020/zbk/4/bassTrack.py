#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  1 18:30:55 2020

@author: albertovaldez
"""

import onset

song = onset.Song("songs/axtasia_closer.wav")

song.FindAlphaPeak(0,0.5)
tr = onset.CalculateThreshold_RMS(song.data)

tr = 0.8
song.GetNoteOnset(unit = 2048, chunk_size = 2048, threshold_ratio = tr, HPF = 0, LPF = 120, base = 10)

song.GetPeaks(x = 0)

bpm1, bpm2 = song.GetBPM(), song.GetBPM_PKS()

print(bpm1,bpm2)

onset.SavePeaks(song.pks, song.sampfreq, 1, -song.peakAlpha, "reaper/Files/peaks.csv")
print("done")