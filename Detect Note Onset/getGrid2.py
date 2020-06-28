#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: albertovaldez
"""
import onset
from scipy.io import wavfile
import numpy as np

songName = "test.wav"
song = onset.Song(wavfile.read("songs/" + songName))

tr = onset.CalculateThreshold_RMS(song.data)

song.FindAlphaPeak(0,tr)
print(song.peakAlphaIndex)
song.GetNoteOnset(unit = 2048, chunk_size = 2048, threshold_ratio = tr, HPF = 20, LPF = 2000)

song.GetPeaks(x = 2048)
song.PlotNoteOnset()
song.PlotPeaks()

# MF_BPM
bpm1 = song.GetBPM(70, 240, "mode")
bpm2 = song.GetBPM_PKS(70, 240, "mode")

print(bpm1, bpm2)
target_bpm = bpm2

#beatsample
bs = int((60/target_bpm)*44100)
#Export

out = []

for i in song.pks:
    start = int(i) - 48
    end = start + bs
    newNote = song.OutNote(start,end)
    
    out.append(newNote)

newsong = np.concatenate([i for i in out])
wavfile.write("newsong.wav", 44100, newsong)
