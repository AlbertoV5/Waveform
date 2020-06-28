#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 26 17:48:38 2020

@author: albertovaldez
"""

def LoudestBand(x,y):
    highest = []
    for i in range(len(y)):
        m = max(y[i])
        ind = y[i].index(m)
        freq = x[ind]
        highest.append(freq)
    return highest
    
def GetPCode(sequence):
    code = ["*"]
    for i in range(len(sequence)-1):
        if sequence[i+1] > sequence[i]:
            code.append("U")
        elif sequence[i+1] == sequence[i]:
            code.append("R")
        elif sequence[i+1] < sequence[i]:
            code.append("D")
    return code
    