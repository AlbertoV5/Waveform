#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul  4 15:17:37 2020

@author: albertovaldez
"""
import pandas as pd
import matplotlib.pyplot as plt

def Grid_Unit(x, y, z):
    unitSize = 1//0.25
    grid = [i/unitSize for i in range(int((x[len(x)-1] + 1) * unitSize))]
    snaps = []
    for i in grid:
        try:
            unit = x.index(float(i))
            position =  i
            energy = y[unit] 
            frequency = z[unit]
        except:
            position = i
            energy = 0
            frequency = 0
        snaps.append([position, energy, frequency])
        
    return snaps
    
def Snaps(file):
    csv = pd.read_csv(file)
    x = [float(i) for i in csv["Position"]] 
    y = [float(i) for i in csv["Energy"]] 
    z = [float(i) for i in csv["Frequency"]] 
    return Grid_Unit(x,y,z)

def BarVSBar(bar):
    scores = []
    for b in range(1,len(bar)-1):
        score = 0
        for i in range(len(bar[b])):
            if bar[b][i][1] != 0 and bar[b+1][i][1] != 0:
                score = score + 1
        scores.append(score)
    return scores

def BarVSGrid(bar):
    scores = []
    for b in range(0,len(bar)):
        score = 0
        for i in range(len(bar[b])):
            if bar[b][i][1] != 0:
                score = score + 1
        scores.append(score)
    return scores

def Structure(snaps):
    bar, unit = [],[]
    for i in snaps:
        x,y,z = i[0],i[1],i[2]
        if x % 4 == 0:
            bar.append(unit)
            unit = []
        unit.append([x,y,z])
    
    scores = BarVSGrid(bar)
    return scores

melody = Structure(Snaps("songs/spectre/dataMelody_spectre.csv"))
snare = Structure(Snaps("songs/spectre/dataSnare_spectre.csv"))
bass = Structure(Snaps("songs/spectre/dataBass_spectre.csv"))
hats = Structure(Snaps("songs/spectre/dataHats_spectre.csv"))

l = [len(melody), len(snare), len(bass), len(hats)]
scores = []
for i in range(min(l)):
    scores.append(melody[i] + snare[i] + bass[i] + hats[i])
    
plt.figure(figsize = (10,5))
plt.xticks([i*4 for i in range((len(melody) + 4)//4)])
plt.grid(True)
plt.plot(scores)
plt.show()


