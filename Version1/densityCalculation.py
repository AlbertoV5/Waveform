#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
"""
import os
import onset
import numpy as np

def FindEnding(song):
    chunkSize = 44100
    amountOfUnits = song.length // chunkSize
    unitStart = song.peakAlphaIndex
    for i in range(amountOfUnits):
        start = unitStart + int(i * chunkSize)
        end = start + chunkSize
        chunk = song.data[start:end]
        if onset.GetRMS(chunk) < - 64:
            song.length = end - song.peakAlphaIndex
            break
        
def NewOnset(song, limits, chunkSize):
    energy, topFrequencies = [],[]
    unitStart = song.peakAlphaIndex
    amountOfUnits = song.length // chunkSize
    for i in range(amountOfUnits):
        start = unitStart + int(i * chunkSize)
        end = start + chunkSize
        chunk = song.data[start:end]
        freqs, fft = onset.CalculateFFT_dB(chunk, song.sampfreq, limits[0], limits[len(limits)-1])
        energy.append(np.max(fft))
        topFrequencies.append(onset.GetTopFrequencies(freqs, fft, start, 1))
    return energy,topFrequencies

def GetNotes_Continuous(song, limits, chunkSize, tr):
    energy, topFrequencies = NewOnset(song, limits, chunkSize)
    threshold = (max(energy)-min(energy))*tr + min(energy)
    notes = []
    for i in range(len(topFrequencies)):
        if energy[i] > threshold:
            notes.append(topFrequencies[i])
    return notes

def EasyOnsets(song, limits, chunkSize, tr):
    energy = []
    unitStart = song.peakAlphaIndex
    amountOfUnits = song.length // chunkSize
    for i in range(amountOfUnits):
        start = unitStart + int(i * chunkSize)
        end = start + chunkSize
        chunk = song.data[start:end]
        freqs, fft = onset.CalculateFFT_dB(chunk, song.sampfreq, limits[0], limits[len(limits)-1])
        energy.append(np.max(np.absolute(fft)))
        
    threshold = (max(energy)-min(energy))*tr + min(energy)
    notes = []
    for i in range(len(energy)):
        if energy[i] > threshold:
            notes.append(energy[i])
    return notes

files=[]
for file in os.listdir("/Volumes/AV5 HD B/02Samples/Music/RGM/Funky Panda"):
    if ".mp3" in file:
        files.append("/Volumes/AV5 HD B/02Samples/Music/RGM/Funky Panda/" + file)

data = []
csv = "Song, Low, Mid, High, Total, RMS"
with open("data.csv", "w+") as file:
    file.write(csv)
    
for file in files:
    print(file)
    try:
        song = onset.Song(file)
        tr = song.CalculateThreshold_RMS()
        song.FindAlphaPeak(0,tr)
        rms = song.GetRMS()
        print("RMS:", rms, "Threshold:", tr, "Alpha Peak:", song.peakAlphaIndex/song.sampfreq)
        
        FindEnding(song)
        sl = int((song.length / song.sampfreq)*1000)/1000
        print("Song Length, seconds", sl)
        
        notes = EasyOnsets(song, [0,120], 2048, tr)
        low = int((len(notes)*4 / sl)*1000)/1000
            
        notes = EasyOnsets(song, [300,1800], 2048, tr)
        mid = int((len(notes) / sl)*1000)/1000
    
        notes = EasyOnsets(song, [14000,16000], 2048, tr)
        high = int((len(notes)*0.875 / sl)*1000)/1000
        print("\nTotal Density:", low, mid, high)
        
        name = file.split("/")
        nam = name[len(name)-1]
        data = [nam, low, mid, high, sum([low, mid, high])]
        
        with open("data.csv", "r") as file:
            csv = file.read()
            
        csv = csv + "\n" + str(data[0]) + "," + str(data[1]) + "," + str(data[2]) + "," + str(data[3]) + "," + str(data[4]) + "," + str(rms)
        with open("data.csv", "w+") as file:
            file.write(csv)

        print("----------")
    except:
        print("FAILED FILE")
        print("----------")    



