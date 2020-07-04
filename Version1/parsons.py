#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
"""
def GetPCode_Old(sequence):
    code = ["*"]
    for i in range(len(sequence)-1):
        if sequence[i+1] > sequence[i]:
            code.append("U")
        elif sequence[i+1] == sequence[i]:
            code.append("R")
        elif sequence[i+1] < sequence[i]:
            code.append("D")
    return code
    
def GetPCode_Num(sequence):
    value = 0
    code = [value]
    for i in range(len(sequence)-1):
        if sequence[i+1] > sequence[i]:
            value = value + 1 
            code.append(value)
        elif sequence[i+1] == sequence[i]:
            value = value
            code.append(value)
        elif sequence[i+1] < sequence[i]:
            value = value - 1
            code.append(value)
    return code

def GetPCode(x,y):
    value = 0
    code = [value]
    for i in range(len(y)-1):
        if y[i+1] > y[i]:
            value = value + 1 
            code.append(value)
        elif y[i+1] == y[i]:
            value = value
            code.append(value)
        elif y[i+1] < y[i]:
            value = value - 1
            code.append(value)
    return code

def SaveCSV(x,y,name):
    csv = ""
    for i in range(len(y)):
        csv = csv + str(x[i]) + "," + str(y[i]) + "\n"
    
    with open(name, "w+") as file:
        file.write(csv)

def SaveCSV3D(x, e, f, path, name):
    csv = "Position,Energy,Frequency"
    name = name.split(".")[0]
        
    for i in range(len(x)):
        csv = csv + "\n" + str(x[i]) + "," + str(e[i]) + "," + str(f[i])
        
    with open(path + name + ".csv", "w+") as file:
        file.write(csv)
    
def SaveCSV5D(x, e_pc, f_pc, energy, frequency, path, name):
    csv = "Position,EnergyPC,FrequencyPC,Energy,Frequency"
    name = name.split(".")[0]
        
    for i in range(len(x)):
        csv = csv + "\n" + str(x[i]) + "," + str(e_pc[i]) + "," + str(f_pc[i]) + "," + str(energy[i]) + "," + str(frequency[i])
        
    with open(path + name + ".csv", "w+") as file:
        file.write(csv)
        
