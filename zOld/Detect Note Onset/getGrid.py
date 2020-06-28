#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: albertovaldez
"""
import onset
from scipy.io import wavfile

songName = "marvin.wav"
song = onset.Song(wavfile.read("songs/" + songName))

tr = onset.CalculateThreshold_RMS(song.data)

song.FindAlphaPeak(0,tr)
print(song.peakAlphaIndex)
song.GetNoteOnset(unit = 2048, chunk_size = 2048, threshold_ratio = 0.6, HPF = 0, LPF = 500)

song.GetPeaks(x = 2048)
song.PlotNoteOnset()
song.PlotPeaks()

bpm1 = song.GetBPM(70, 240, "mode")
bpm2 = song.GetBPM_PKS(70, 240, "mode")

print(bpm1, bpm2)
target_bpm = bpm2

#PLOTS
#onset.PlotNote(song.data[song.peakAlphaIndex:song.peakAlphaIndex + 2048], song.sampfreq, 20, 500)

bpm = bpm2
start = song.peakAlphaIndex
duration = 15*song.sampfreq
end = start + duration

### THIS IS PART 1
part = song.data[start:end]
notes = onset.GetPartOnset(part, 44100, 2048, 2048, 0.6, 0, 500)

bpm = onset.GetBPM(notes,44100, 60, 200, "mode")
pks, pksV = onset.GetPeaks(part, notes, x = 2048)
print(pks)
bpm_pks = onset.GetBPM_PKS(pks, 44100, 60, 200, "mode")
print(bpm, bpm_pks)


notes = [[i[0], i[1] + start, i[2] + start] for i in notes]
print(notes)
'''
gridDiv = 1
gd_t = (60/bpm)
gd_s = int((60/bpm) * (gridDiv * song.sampfreq))
beatsInPart = duration//gd_s
grid = [i*gd_s for i in range(int(song.length//gd_s))]

end = start + gd_s
print(start, end)

area = 2048

for i in range(beatsInPart):
    
    leftA = start + i*gd_s - area
    rightA = start + i*gd_s + area
    
    noteA = song.data[leftA:rightA]
    
    leftB = start + (i+1)*gd_s - area
    rightB = start + (i+1)*gd_s + area
    
    noteB = song.data[leftB:rightB]
    
'''    
    
    
#wavfile.write("note1.wav", 44100, song.OutNote(start,end))
