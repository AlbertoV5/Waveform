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

songName = "acemarino.wav"

song = onset.Audio(wavfile.read("songs/" + songName))

size = 2048
song.GetNoteOnset(unit = 2048, chunk_size = size, threshold_ratio = 0.8, HPF = 20, LPF = 300)

song.GetTransientPoints(x = size)

# BPM_TP seems to be more precise due to the transient points
# mode, mean, median

bpm1 = song.GetBPM(70,240, "mode")
bpm2 = song.GetBPM_TP(70, 240, "mode")

print("BPM:", bpm1, bpm2)

# "mode" is best for whole songs, "mean" and "median" are better for small sections
# depending on the song, BPM_TP may be wildly different than BPM on "mode" 