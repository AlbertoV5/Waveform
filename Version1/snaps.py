#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul  4 15:17:37 2020

@author: albertovaldez
"""
import pandas as pd
import matplotlib.pyplot as plt

def Grid_Unit(x, y, z, unit):
    unitSize = 1//unit
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
    
def Snaps(file, unit):
    csv = pd.read_csv(file)
    x = [float(i) for i in csv["Position"]] 
    y = [float(i) for i in csv["Energy"]] 
    z = [float(i) for i in csv["Frequency"]] 
    return Grid_Unit(x,y,z, unit)

def BarVSBar(bar):
    scores = []
    for b in range(1,len(bar)-1):
        score = 0
        for i in range(len(bar[b])):
            if bar[b][i][1] != 0 and bar[b+1][i][1] != 0:
                score = score + 1
        scores.append(1-(score/len(bar[b])))
    
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

def ROC(snaps):
    bar, unit = [],[]
    for i in snaps:
        x,y,z = i[0],i[1],i[2]
        if x % 4 == 0:
            bar.append(unit)
            unit = []
        unit.append([x,y,z])
    
    scores = BarVSBar(bar)
    return scores


def Density(path):
    bass = Structure(Snaps(path + "dataBass.csv", 0.25))
    hats = Structure(Snaps(path + "dataHats.csv", 0.25))
    melody = Structure(Snaps(path + "dataMelody.csv", 0.25))
    snare = Structure(Snaps(path + "dataSnare.csv", 0.5))
    
    l = [len(melody), len(snare), len(bass), len(hats)]
    scores = []
    for i in range(max(l)):
        try:
            m = melody[i]
        except:
            m = 0
        try:
            s = snare[i]
        except:
            s = 0
        try:
            b = bass[i]
        except:
            b = 0
        try:
            h = hats[i]
        except:
            h = 0

        scores.append(m+s+b+h)
    
    csv = "Bar,Density"
    x = 0
    for i in scores:
        csv = csv + "\n" + str(x) + "," + str(i)
        x+= 1
    with open(path + "snapsDensity.csv", "w+") as file:
        file.write(csv)
        
    plt.figure(figsize = (20,10))
    plt.xticks([i*4 for i in range((len(melody) + 4)//4)])
    plt.title("Density Change")
    plt.xlabel("Time (bars)")
    plt.grid(True)
    plt.plot(scores)
    plt.scatter(range(len(scores)), scores)
    plt.savefig(path + "snapsDensity.png")
    plt.show()
    
def RateOfChange(path):
    bass = ROC(Snaps(path + "dataBass.csv", 0.25))
    hats = ROC(Snaps(path + "dataHats.csv", 0.25))
    melody = ROC(Snaps(path + "dataMelody.csv", 0.25))
    snare = ROC(Snaps(path + "dataSnare.csv", 0.5))
    
    l = [len(melody), len(snare), len(bass), len(hats)]
    scores = []
    for i in range(max(l)):
        try:
            m = melody[i]
        except:
            m = 0
        try:
            s = snare[i]
        except:
            s = 0
        try:
            b = bass[i]
        except:
            b = 0
        try:
            h = hats[i]
        except:
            h = 0

        scores.append(1 - ((m+s+b+h)/4))
        
    csv = "Bar,RateOfChange"
    x = 0
    for i in scores:
        csv = csv + "\n" + str(x) + "," + str(i)
        x+= 1
    with open(path + "snapsRateOfChange.csv", "w+") as file:
        file.write(csv)
        
    plt.figure(figsize = (20,10))
    plt.xticks([i*4 for i in range((len(melody) + 4)//4)])
    plt.title("Rate of Change")
    plt.xlabel("Time (bars)")
    plt.grid(True)
    plt.plot(scores)
    plt.scatter(range(len(scores)), scores)
    plt.savefig(path + "snapsRateOfChange.png")
    plt.show()    
    
#Master("songs/2Hertz - Backbeat  Ninety9Lives Release_48/")