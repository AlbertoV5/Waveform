#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: albertovaldez
"""
import onset
from scipy.io import wavfile
import parsons as psc

songName = "vulf.wav"
song = onset.Song(wavfile.read("songs/" + songName))

tr = onset.CalculateThreshold_RMS(song.data)

tr = 0.5
song.FindAlphaPeak(0,tr)
song.GetNoteOnset(unit = 4096, chunk_size = 4096, threshold_ratio = tr, HPF = 20, LPF = 1300, base = 10)
song.SaveOnsets()

song.GetPeaks(x = 2048)

onset.SavePeaks(song.pks, song.sampfreq, 1, 0)

loops = range(8)
noteSize = 4096
data = []

for i in loops:
    note = i
    chunk = song.data[song.notes[note][0]:song.notes[note][0]+noteSize]
    #onset.PlotNote(chunk, song.sampfreq, 20, 2000)
    
    freqs, fft = onset.CalculateFFT_dB(chunk, song.sampfreq, 20, 1300)
    x, y = onset.GetNotePeaks(freqs, fft)
    
    limits = [0, 60, 120, 240, 480, 720, 960, 1200]
    freqBands = onset.FrequencyBands(x,y, bandsLimits = limits)
    
    y = []
    x = limits
    for j in freqBands:
        y.append(sum(j))
    
    #n = str(song.notes[note][0]/song.sampfreq)+".png"
    n = str(note+1) + ".png"
    onset.PlotPeaks2(x, y, xticks = limits, ylim = (0,200), name = n)
    
    data.append(y)

bandSeq = psc.LoudestBand(limits,data)
print(bandSeq)
print(psc.GetPCode(bandSeq))


#song.PlotNoteOnset()
#song.PlotPeaks()

'''
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


tr = 0.8
x,y = song.GetPeaks2(tr, 8000)

onset.SavePeaks(x,song.sampfreq,1,0)
 
#onset.PlotPeaks2(x,y)
'''