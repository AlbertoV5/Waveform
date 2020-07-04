#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Get parson's code of 4 frequency bands.
Chunk Size at 2048 unless specified.
"""
import os
import onset
import easygram as ez
import parsons
from pathlib import Path
from pydub import AudioSegment

def toWAV(mp3):
    wav = mp3.split(".")[0] + ".wav"
    sound = AudioSegment.from_mp3(mp3)
    sound.export(wav, format="wav")
    print("Converted mp3 to wav.")
    return wav

def Song(file):
    p = Path(file)
    directory = str(p.parent) + "/"
    if ".mp3" in file:
        wavFile = toWAV(file)
        song = onset.Song(wavFile)
    else:
        song = onset.Song(file)
    
    songName = file.split("/")[-1:][0]
    print(songName)
    u1 = int(input(("Press 1 if your song has no fade-in, Press 2 if the fade-in is quiet. Press 3 if the fade-in is loud. Press 4 if the fade-in is very loud.\n")))
    
    if u1 == 1:
        songTR = 0.1
    elif u1 == 2:
        songTR = 0.5
    elif u1 == 3:
        songTR = 0.8
    elif u1 == 4:
        songTR = 0.96
    else:
        songTR = 0.5
        
    alphaPeak = song.FindAlphaPeak(0,songTR)

    u2 = str(input("Press 1 to get a list of suggested BPMs. Press any other key to skip:\n"))
    if u2 == "1":
        onset.GetBPMS(song, onset.CalculateThreshold_RMS(song.data))
    
    bpm_user = float(input("Enter selected BPM: \n"))
    measure_user = int(input("Enter how many beats are in a bar: \n"))
    
    bpm, measure = bpm_user, measure_user
    maxBars = int((song.length_seconds * (1/(60/bpm)) / measure ))
    print("Song duration in bars: " + str(maxBars))
        
    def Melody():
        noteThreshold = 0.5
        unitSize = 0.25
        # Continuous, Peaks, 4 by 4, unit 0.25
        x_all, y_energy, z_freq  = [],[],[]
        freqBands = [300,1800] 
        barBlock = 4
        for i in range(maxBars//barBlock):
            barNum = i*barBlock
            x,y,z = ez.GetNotesPeaks3D_Continuous(freqBands, song, bpm, barNum, barNum+barBlock, measure, unitSize, noteThreshold)
            offset = i*barBlock*measure*(1/unitSize)
            for j in range(len(y)):
                x_all.append(x[j] + offset)
                y_energy.append(y[j])
                z_freq.append(z[j])
            
        peaks = []
        for i in x_all:
            peaks.append(i * (60/bpm)*unitSize * song.sampfreq)
            
        onset.SavePeaks(peaks, song.sampfreq, 1, song.peakAlphaIndex, directory + "peaksMelody" + "_" + songName.split(".")[0] + ".csv")
        
        pc_e,pc_f = parsons.GetPCode(x_all, y_energy),parsons.GetPCode(x_all, z_freq)
        x = [i*unitSize for i in x_all]
        ez.PlotComplete(x, pc_e, pc_f, bpm, maxBars, measure, unitSize, freqBands, directory, "plotMelody_" + songName, noteThreshold, song.GetRMS(), alphaPeak)
        parsons.SaveCSV5D(x, pc_e,pc_f,y_energy,z_freq,directory, "dataMelody_" + songName)
        print("Done.")
        
    def Snare():
        noteThreshold = 0.5
        unitSize = 0.5
        # Step, Peaks, 4 by 4, unit 0.5
        x_all, y_energy, z_freq  = [],[],[]
        freqBands = [120,300] 
        barBlock = 4
        for i in range(maxBars//barBlock):
            barNum = i*barBlock
            x,y,z = ez.GetNotesPeaks3D_Step(freqBands, song, bpm, barNum, barNum+barBlock, measure, unitSize, noteThreshold)
            offset = i*barBlock*measure*(1/unitSize)
            for j in range(len(y)):
                x_all.append(x[j] + offset)
                y_energy.append(y[j])
                z_freq.append(z[j])
            
        peaks = []
        for i in x_all:
            peaks.append(i * (60/bpm)*unitSize * song.sampfreq)
            
        onset.SavePeaks(peaks, song.sampfreq, 1, song.peakAlphaIndex, directory + "peaksSnare" + "_" + songName.split(".")[0] + ".csv")
        
        pc_e,pc_f = parsons.GetPCode(x_all, y_energy),parsons.GetPCode(x_all, z_freq)
        x = [i*unitSize for i in x_all]
        ez.PlotComplete(x, pc_e, pc_f, bpm, maxBars, measure, unitSize, freqBands, directory, "plotSnare_" + songName, noteThreshold, song.GetRMS(), alphaPeak)
        parsons.SaveCSV5D(x, pc_e,pc_f,y_energy,z_freq,directory, "dataSnare_" + songName)
        print("Done.")
    
    def Bass():
        noteThreshold = 0.6
        unitSize = 0.25
        # Continuous, Peaks, all bars, unit 0.25
        x_all, y_energy, z_freq  = [],[],[]
        freqBands = [0,120] 
        barBlock = maxBars
        for i in range(maxBars//barBlock):
            barNum = i*barBlock
            x,y,z = ez.GetNotesPeaks3D_Continuous_4096(freqBands, song, bpm, barNum, barNum+barBlock, measure, unitSize, noteThreshold)
            offset = i*barBlock*measure*(1/unitSize)
            for j in range(len(y)):
                x_all.append(x[j] + offset)
                y_energy.append(y[j])
                z_freq.append(z[j])
            
        peaks = []
        for i in x_all:
            peaks.append(i * (60/bpm)*unitSize * song.sampfreq)
            
        onset.SavePeaks(peaks, song.sampfreq, 1, song.peakAlphaIndex, directory + "peaksBass" + "_" + songName.split(".")[0] + ".csv")
        
        pc_e,pc_f = parsons.GetPCode(x_all, y_energy),parsons.GetPCode(x_all, z_freq)
        x = [i*unitSize for i in x_all]
        ez.PlotComplete(x, pc_e, pc_f, bpm, maxBars, measure, unitSize, freqBands, directory, "plotBass_" + songName, noteThreshold, song.GetRMS(), alphaPeak)
        parsons.SaveCSV5D(x, pc_e,pc_f,y_energy,z_freq,directory, "dataBass_" + songName)
        print("Done.")

    def Hats():
        noteThreshold = 0.5
        unitSize = 0.25
        # Continuous, Peaks, all bars, unit 0.25
        x_all, y_energy, z_freq  = [],[],[]
        freqBands = [9000,16000] 
        barBlock = maxBars
        for i in range(maxBars//barBlock):
            barNum = i*barBlock
            x,y,z = ez.GetNotesPeaks3D_Continuous_Sum(freqBands, song, bpm, barNum, barNum+barBlock, measure, unitSize, noteThreshold)
            offset = i*barBlock*measure*(1/unitSize)
            for j in range(len(y)):
                x_all.append(x[j] + offset)
                y_energy.append(y[j])
                z_freq.append(z[j])
            
        peaks = []
        for i in x_all:
            peaks.append(i * (60/bpm)*unitSize * song.sampfreq)
            
        onset.SavePeaks(peaks, song.sampfreq, 1, song.peakAlphaIndex, directory + "peaksHats" + "_" + songName.split(".")[0] + ".csv")
        
        pc_e,pc_f = parsons.GetPCode(x_all, y_energy),parsons.GetPCode(x_all, z_freq)
        x = [i*unitSize for i in x_all]
        ez.PlotComplete(x, pc_e, pc_f, bpm, maxBars, measure, unitSize, freqBands, directory, "plotHats_" + songName, noteThreshold, song.GetRMS(), alphaPeak)
        parsons.SaveCSV5D(x, pc_e,pc_f,y_energy,z_freq,directory,"dataHats_" + songName)

        print("Done.")

    print("\nObtaining Melody...")
    Melody()
    
    print("\nObtaining Snare...")
    Snare()
    
    print("\nObtaining Bass...")
    Bass()
    
    print("\nObtaining HiHats...")
    Hats()
    
    os.remove(wavFile)
    
    
print("Drag and drop your song:")    
Song(input().strip("\'"))

