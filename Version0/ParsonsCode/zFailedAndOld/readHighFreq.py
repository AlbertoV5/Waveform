#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 26 19:40:38 2020

@author: albertovaldez
"""

import parsons as ps
import matplotlib.pyplot as plt

with open("simpleSpectrogram.csv","r") as file:
    data = file.read().split("\n")
  
freqs = []
limits = []

for i in range(len(data)):
    if i > 0:
        freqs.append([])
        for j in data[i].split(","):
            try:
                freqs[i-1].append(float(j))
            except:
                pass
    else:
        for i in data[i].split(","):
            try:
                limits.append(int(i))
            except:
                pass
  
bandSeq = ps.LoudestBand(limits,freqs)
print(bandSeq)
print(ps.GetPCode(bandSeq))

pCodeNum = ps.GetPCode_Num(bandSeq)

plt.figure(figsize = (20,5))
plt.scatter(range(len(pCodeNum)), pCodeNum)
plt.plot(range(len(pCodeNum)), pCodeNum)
plt.xticks([i*16 for i in range(len(freqs)//16)])
plt.savefig("parsonsSeq.png")
plt.show()