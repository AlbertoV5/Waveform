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

def Structure(snaps):
    bar, unit = [],[]
    for i in snaps:
        x,y,z = i[0],i[1],i[2]
        if x % 4 == 0:
            bar.append(unit)
            unit = []
        unit.append([x,y,z])
    
    scores = []
    for b in range(1,len(bar)-1):
        score = 0
        for i in range(len(bar[b])):
            if bar[b][i][1] != 0 and bar[b+1][i][1] != 0:
                score = score + 1
        scores.append(score)
    
    print(scores)
    plt.grid(True)
    plt.plot(scores)
    plt.show()

Structure(Snaps("songs/spectre/dataMelody_spectre.csv"))
Structure(Snaps("songs/spectre/dataSnare_spectre.csv"))
Structure(Snaps("songs/spectre/dataBass_spectre.csv"))
Structure(Snaps("songs/spectre/dataHats_spectre.csv"))



