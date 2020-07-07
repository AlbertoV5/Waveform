#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  6 17:46:04 2020

@author: albertovaldez
"""

import onset

song = onset.Song("songs/camellia/camellia.mp3")

song.FindAlphaPeak(0, 0.8)
print(song.peakAlphaIndex)

gen = song.peakAlphaIndex - 1024
flux, starts = [], []
for i in range(17):
    start = gen + i*64
    end = gen + i*64 + 512
    chunk = song.data[start:end]
    rms = onset.GetRMS(chunk)
    flux.append(rms)
    starts.append(start)
    
realPeak = starts[flux.index(max(flux))]
print(realPeak)

bpms = onset.GetBPMS_All(song, 0.8)
