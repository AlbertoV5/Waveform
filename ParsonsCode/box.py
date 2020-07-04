#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
"""
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

def BasicFrames(color):
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
            plt.scatter(a - 0.5 ,b - 0.5, s=1000, c = color,marker = "s")
            plt.savefig("zFrames/f_" + str(color) + "_" + str(i + 1) + "_" + str(j + 1) + ".jpg")
            plt.close()
    
BasicFrames("b")
BasicFrames("k")

with open ("mp3/dataMelody_spectre.csv", "r") as file:
    csv = file.read().split("\n")[1:]
    
x,y,z =[],[],[]
for i in csv:
    x.append(float(i.split(",")[0]))
    y.append(float(i.split(",")[1]))
    z.append(float(i.split(",")[2]))
    
x, y, z = EasyBox(x,y,z)
lim = int(x[len(x)-1])
print(lim)
    
path_input = "zFrames/"
d = os.getcwd() + "/zFrames"
out = os.getcwd() + "/"

bpm = 128
beat = 60/128
fps = 1/(beat*0.25)

frame_array = []
a,b = -1, -1
for i in range(lim*4):
    try:
        pos = x.index(i/4)
        file = path_input + "f_" + "b" + "_" + str(y[pos]) + "_" + str(z[pos]) + ".jpg"
        a, b = y[pos], z[pos]
    except:
        file = path_input + "f_" + "k" + "_" + str(a) + "_" + str(b) + ".jpg"
    
    img = cv2.imread(file)
    frame_array.append(img)
 
height, width, layers = img.shape
size = (width,height)
out = cv2.VideoWriter(out + "vid.mp4",cv2.VideoWriter_fourcc(*'DIVX'), fps, size)    

for i in range(len(frame_array)):
    out.write(frame_array[i])
    
out.release()






