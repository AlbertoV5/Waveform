#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
"""
import matplotlib.pyplot as plt
import cv2
import os

def EasyBox(x,y,z):
    box_y, box_z = [],[]
    v_y,v_z = 2,2

    box_y.append(v_y)
    box_z.append(v_z)
    
    for i in range(1,len(x)-1):
        if y[i+1] > y[i]:
            if v_y == 4:
                v_y = 1
            else:
                v_y = v_y + 1
        elif y[i+1] < y[i]:
            if v_y == 1:
                v_y = 4
            else:
                v_y = v_y - 1
        elif y[i+1] == y[i]:
            v_y = v_y
        
        if z[i+1] > z[i]:
            if v_z == 4:
                v_z = 1
            else:
                v_z = v_z + 1
        elif z[i+1] < z[i]:
            if v_z == 1:
                v_z = 4
            else:
                v_z = v_z - 1
        elif z[i+1] == z[i]:
            v_z = v_z   
            
        box_y.append(v_y)
        box_z.append(v_z)
        
    box_y.append(v_y)
    box_z.append(v_z)
  
    return x, box_y, box_z

def FreqBox(x,y,z):
    box_y, box_z = [],[]
    v_y,v_z = 2,2

    box_y.append(v_y)
    box_z.append(v_z)
    
    for i in range(1,len(x)-1):
        if y[i+1] > y[i]:
            if v_y == 4 and v_z != 4:
                v_y = v_y
                v_z = v_z + 1
            elif v_y == 4 and v_z == 4:
                v_y = 1
                v_z = 1
            elif v_z == 4 and v_y != 4:
                v_y = v_y + 1
                v_z = v_z
            elif v_y < 4 and v_z < 4:
                v_y = v_y + 1  
                v_z = v_z
                
        elif y[i+1] < y[i]:
            if v_y == 1 and v_z != 1:
                v_y = v_y
                v_z = v_z - 1
            elif v_y == 1 and v_z == 1:
                v_y = 4
                v_z = 4
            elif v_z == 1 and v_y != 1:
                v_y = v_y - 1
                v_z = v_z
            elif v_y > 1 and v_z > 1:
                v_y = v_y - 1
                v_z = v_z
                
        elif y[i+1] == y[i]:
            v_y = v_y
            v_z = v_z
            
        box_y.append(v_y)
        box_z.append(v_z)
        
    box_y.append(v_y)
    box_z.append(v_z)
  
    return x, box_y, box_z

def BasicFrames(path, color1, color2):
    x = [1,2,3,4]
    y = [1,2,3,4]
    a, b = -1,-1
    for i in range(len(x)):
        for j in range(len(y)):
            a = x[i]
            b = y[j]
            plt.figure(figsize=(3,3))
            plt.xlim((0,4))
            plt.ylim((0,4))
            plt.xticks([0,1,2,3,4], fontsize=0)
            plt.yticks([0,1,2,3,4], fontsize=0)
            plt.grid(True)
            plt.scatter(a - 0.5 ,b - 0.5, s=1000, c = color1, marker = "s")
            plt.savefig(path + "/" + "f_" + str(color2) + "_" + str(i + 1) + "_" + str(j + 1) + ".jpg")
            plt.close()
    
    for i in range(len(x)):
        for j in range(len(y)):
            a = x[i]
            b = y[j]
            plt.figure(figsize=(3,3))
            plt.xlim((0,4))
            plt.ylim((0,4))
            plt.xticks([0,1,2,3,4], fontsize=0)
            plt.yticks([0,1,2,3,4], fontsize=0)
            plt.grid(True)
            plt.scatter(a - 0.5 ,b - 0.5, s=1000, c = color2, marker = "s")
            plt.savefig(path + "/" + "f_" + str(color1) + "_" + str(i + 1) + "_" + str(j + 1) + ".jpg")
            plt.close()
    

def CreateVideo(path, fileName, bpm, color1, color2):
    framepath = path + "frames"
    try:
        os.mkdir(framepath)
    except:
        print("Frame directory already exists.")
    
    BasicFrames(framepath, color1, color2)
    
    with open (path + fileName + ".csv", "r") as file:
        csv = file.read().split("\n")[1:]
        
    x,y,z =[],[],[]
    for i in csv:
        x.append(float(i.split(",")[0]))
        y.append(float(i.split(",")[1]))
        z.append(float(i.split(",")[2]))
        
    x, y, z = FreqBox(x,y,z)
    lim = int(x[len(x)-1])
            
    beat = 60/128
    fps = 1/(beat*0.25)
    
    frame_array = []
    a,b = -1, -1
    for i in range(lim*4):
        try:
            pos = x.index(i/4)
            file = framepath + "/f_" + str(color1) + "_" + str(y[pos]) + "_" + str(z[pos]) + ".jpg"
            a, b = y[pos], z[pos]
        except:
            file = framepath + "/f_" + str(color2) + "_" + str(a) + "_" + str(b) + ".jpg"
        
        img = cv2.imread(file)
        frame_array.append(img)
     
    height, width, layers = img.shape
    size = (width,height)
    out = cv2.VideoWriter(path + fileName + ".mp4",cv2.VideoWriter_fourcc(*'DIVX'), fps, size)    
    
    for i in range(len(frame_array)):
        out.write(frame_array[i])
        
    out.release()

CreateVideo(os.getcwd() + "/mp3/", "dataMelody_spectre", 128, "b", "k")



