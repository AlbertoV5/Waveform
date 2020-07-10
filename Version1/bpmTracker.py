#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  6 17:46:04 2020

@author: albertovaldez
"""

import onset
import os
import matplotlib.pyplot as plt

def TruePeak(song):
    size = 4096
    unit = 256
    rms = []
    index = []
    
    for i in range(size // unit):
        start = song.peakAlphaIndex - size + i*unit
        end = start + unit
        rms.append(onset.GetRMS(song.data[start:end]))
        index.append(start)
    return  index[rms.index(max(rms))]

def Tempo(fileName):
    song = onset.Song(fileName)
    print("RMS:", song.GetRMS(), "dB")
    
    tr = song.CalculateThreshold_RMS()
    song.FindAlphaPeak(0, tr)
    song.peakAlphaIndex = TruePeak(song)
    
    print("Peak: ", song.peakAlphaIndex, song.peakAlphaIndex / song.sampfreq, "seconds.")
    bpms = onset.GetBPMS_All(song, tr)
    
    print("BPMS:",bpms)

def RMSFlux(fileName):
    song = onset.Song(fileName)
    song.FindAlphaPeak(0, 0.8)
    rms = []
    quiet = []
    len_samp = 5 * song.sampfreq
    for i in range((len(song.data) // len_samp)):
        start = i * len_samp
        end = i * len_samp + len_samp
        power = onset.GetRMS(song.data[start:end])
        rms.append([start/song.sampfreq, power])
    for i in range(len(rms)-1):
        a = rms[i + 1][1]
        b = rms[i][1]
        if b - a > 10:
            quiet.append(rms[i + 1])
        
    before = int(quiet[0][0]*song.sampfreq) - int(5*song.sampfreq)
    len_samp = int(0.5*song.sampfreq)
    zoomRMS = []
    for i in range(11):
        start = before + len_samp * i 
        end = before + len_samp * i + len_samp
        power = onset.GetRMS_100(song.data[start:end])
        zoomRMS.append([start, power])
        print(start, power)
    
    
def RMSFluxStart(fileName):
    song = onset.Song(fileName)
    rms = song.GetRMS()
    print("RMS:", rms)
    x,y = [],[]
    on = []
    len_samp = 5 * song.sampfreq
    total = 60 * song.sampfreq
    for i in range(total // len_samp):
        start = i * len_samp
        end = i * len_samp + len_samp
        power = onset.GetRMS(song.data[start:end])
        x.append(start/song.sampfreq)
        y.append(power)
        
    # 5 SECOND RULE
    for i in range(len(y)-1):
        a = y[i]
        b = y[i + 1]
        if abs(a) - abs(b) > 9:
            on = [x[i+1],y[i+1]]
            break
    
    intro = on[0] * song.sampfreq // 2
    unit = song.sampfreq
    length = 5
    
    x, y = [],[]
    print(intro/song.sampfreq)
    for i in range(length):
        start = int(intro + (unit * i))
        end = start + unit
        chunkRMS = onset.GetRMS(song.data[start:end])
        x.append(start)
        y.append(chunkRMS)
        
    for i in range(len(y)-1):
        a = y[i]
        b = y[i + 1]
        if abs(a) - abs(b) > 9:
            on = [x[i+1], y[i+1]]
            break
            
    print(max(y), x[y.index(max(y))])

    intro = on[0]
    unit = song.sampfreq // 20
    length = 20
    
    x, y = [],[]
    for i in range(length):
        start = int(intro + (unit * i))
        end = start + unit
        chunkRMS = onset.GetRMS(song.data[start:end])
        x.append(start)
        y.append(chunkRMS)
        
    print(max(y), x[y.index(max(y))])
    
    intro = x[y.index(max(y))] - 8192
    unit = 1024
    length = 8
    
    x, y = [],[]
    for i in range(length):
        start = int(intro + (unit * i))
        end = start + unit
        chunkRMS = onset.GetRMS(song.data[start:end])
        x.append(start)
        y.append(chunkRMS)
        
    print(max(y), x[y.index(max(y))])
    
    plt.plot(x,y)     
        
        
RMSFluxStart("songs/spectre.mp3")
     
'''
songs = []
for file in os.listdir(os.getcwd() + "/songs/_bpm"):
    if "mp3" in file and "reapeaks" not in file:
        songs.append(file)
    
songs = sorted(songs)

for i in songs:
    fileName = os.getcwd() + "/songs/_bpm/" + i
    print(i)
    Tempo(fileName)
    print("----------------")
'''
