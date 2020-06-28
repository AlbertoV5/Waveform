#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
https://en.wikipedia.org/wiki/Parsons_code
https://en.wikipedia.org/wiki/Linear_time-invariant_system
"""
def GetPC(t):
    last = 0
    pc = [] 
    for i in t:
        if last == 0:
            last = i
            pc.append("*")
        else:
            if i > last:
                pc.append("u")
            elif i < last:
                pc.append("d")
            elif i == last:
                pc.append("r")
    return pc
        
t = [6,7,6,4,8,3,1,5]

print(GetPC(t))

