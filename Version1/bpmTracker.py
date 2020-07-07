#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  6 17:46:04 2020

@author: albertovaldez
"""

import onset
import os

def Tempo(fileName):
    song = onset.Song(fileName)
    print("RMS: ", song.GetRMS())
    
    tr = song.CalculateThreshold_RMS()
    song.FindAlphaPeak(0, tr)
    
    print("Peak: ", song.peakAlphaIndex, song.peakAlphaIndex / song.sampfreq)
    bpms = onset.GetBPMS_All(song, tr)
    print("Mode BPM:", onset.mode(bpms))
    print("Median BPM:", onset.median(bpms))
    print("Mean BPM:", onset.mean(bpms))

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
        print(start, power)
    '''
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
    '''
    
#RMSFlux("songs/spectre/spectre.mp3")     

songs = []
for file in os.listdir(os.getcwd() + "/songs/bpmExperiment"):
    if "mp3" in file:
        songs.append(file)
    
songs = sorted(songs)

for i in songs:
    fileName = os.getcwd() + "/songs/bpmExperiment/" + i
    print(i)
    Tempo(fileName)
    print("----------------")

