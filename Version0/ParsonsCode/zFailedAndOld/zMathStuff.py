#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 28 15:58:25 2020

@author: albertovaldez
"""

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import math

with open("pc_freq.csv", "r") as file:
    csv = file.read().split("\n")
    
with open("pc_amp.csv", "r") as file:
    csv = file.read().split("\n")
    
x, y = [],[]
for i in csv:
    try:
        a = float(i.split(",")[0])
        b = float(i.split(",")[1])
        x.append(a)
        y.append(b)
    except:
        pass
    
slopes, barSlopes = [],[]
lastBar = 0

for i in range(len(y)):
    m = y[i]
    
    bar = int(x[i]/16)
    if bar > lastBar:
        barSlopes.append(sum(slopes))
        slopes = []
        lastBar = bar
        
    slopes.append(m)
    
plt.plot(barSlopes)
plt.show()
    


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot(x,y,z)
    
    
    
    
    