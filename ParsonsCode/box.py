#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 17:18:43 2020

@author: albertovaldez
"""
import random
import matplotlib.pyplot as plt
import cv2
import os
    
def EasyBox(x,y,z):
    box_y, box_z = [],[]
   #v_y,v_z = random.randint(1,3), random.randint(1,3)
    v_y,v_z = 2,2

    box_y.append(v_y)
    box_z.append(v_z)
    
    for i in range(1,len(x)-1):
        if y[i+1] > y[i]:
            if v_y == 3:
                v_y = 1
            else:
                v_y = v_y + 1
        elif y[i+1] < y[i]:
            if v_y == 1:
                v_y = 3
            else:
                v_y = v_y - 1
        elif y[i+1] == y[i]:
            v_y = v_y
        
        if z[i+1] > z[i]:
            if v_z == 3:
                v_z = 1
            else:
                v_z = v_z + 1
        elif z[i+1] < z[i]:
            if v_z == 1:
                v_z = 3
            else:
                v_z = v_z - 1
        elif z[i+1] == z[i]:
            v_z = v_z   
            
        box_y.append(v_y)
        box_z.append(v_z)
        
    box_y.append(v_y)
    box_z.append(v_z)
  
    return x, box_y, box_z

def CreateFrames(fileName):
    with open (fileName, "r") as file:
        csv = file.read().split("\n")[1:]
    
    x,y,z =[],[],[]
    for i in csv:
        x.append(float(i.split(",")[0]))
        y.append(float(i.split(",")[1]))
        z.append(float(i.split(",")[2]))
        
    bx, by, bz = EasyBox(x,y,z)
    lim = int(x[len(x)-1])
    print(lim)

    a,b = -1,-1
    for i in range((lim*4)):
        unit = i / 4
        try:
            n = bx.index(unit)
            a = by[n]
            b = bz[n]
            
            plt.figure(figsize=(3,3))
            plt.xlim((0,3))
            plt.ylim((0,3))
            plt.xticks([0,1,2,3], fontsize=0)
            plt.yticks([0,1,2,3], fontsize=0)
            plt.grid(True)
            plt.scatter(a - 0.5 ,b - 0.5, s=1000, c = "b",marker = "s")
            plt.savefig("zFrames/f_" + str(i).zfill(4) + ".jpg")
            plt.close()
        except:
            
            plt.figure(figsize=(3,3))
            plt.xlim((0,3))
            plt.ylim((0,3))
            plt.xticks([0,1,2,3], fontsize=0)
            plt.yticks([0,1,2,3], fontsize=0)
            plt.grid(True)
            plt.scatter(a - 0.5 ,b - 0.5, s=1000, c = "k",marker = "s")
            plt.savefig("zFrames/f_" + str(i).zfill(4) + ".jpg")
            plt.close()
    return x
    
CreateFrames("PCP/csv/axtasia_closer.csv")

def CreateMovie(unit):
    path_input = "zFrames/"
    d = os.getcwd() + "/zFrames"
    out = os.getcwd() + "/"
    files=[]
    for file in os.listdir(d):
        files.append(path_input + file)
    
    files.sort()
    bpm = 174
    beat = 60/bpm
    fps = 1/(beat*unit)
        
    frame_array = []
    
    for file in files:
        img = cv2.imread(file)
        frame_array.append(img)
    
    height, width, layers = img.shape
    size = (width,height)
    out = cv2.VideoWriter(out + "vid.mp4",cv2.VideoWriter_fourcc(*'DIVX'), fps, size)    
    
    for i in range(len(frame_array)):
        out.write(frame_array[i])
        
    out.release()

CreateMovie(0.25)




