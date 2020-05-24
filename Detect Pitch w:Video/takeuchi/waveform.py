from scipy.io import wavfile
from scipy.fft import fft
import scipy.fftpack as fftpk
import numpy as np
import scipy
import matplotlib.pyplot as plt
import cv2
import os

d = os.getcwd()

sampfreq, data = wavfile.read("takeuchi.wav")
data = np.divide(np.array(data,dtype=float),6000000)

def PlotWaveform(data):
    fig,ax = plt.subplots(subplot_kw=dict())
    ax.plot(data)
    ax.set_ylim(bottom = -1, top = 1)
    fig.show()

#PlotWaveform(norm)

def GetChunkFFT(chunk):
    _fft = abs(scipy.fft(chunk))
    freqs = fftpk.fftfreq(len(_fft), (1.0/sampfreq))
    return freqs, _fft
  
def PlotFFT(x,y, name, color, HPF, LPF):
    fig1,ax1 = plt.subplots(subplot_kw=dict())
    ax1.plot(x[range(len(y)//2)],y[range(len(y)//2)], color = color)
    ax1.set_ylim(bottom = 0, top = 1)
    ax1.set_xlim(left = HPF, right = LPF)
    fig1.savefig(name)
    fig1.show()
  
  
def AllFFT(unit):
    chunk_size = 1024
    for i in range(64):
        chunk = np.array([data[i] for i in range((i*unit),(i*unit)+chunk_size)])
        if i%4 == 0:
            if i%8 == 0:
                color = "g"
            else:
                color = "r"
        else:
            color = "k"
        
        x,y = GetChunkFFT(chunk)
        PlotFFT(x,y, str(i).zfill(3), color, HPF = 0, LPF = 1000)
        
bpm = 103.23
beat = 60/bpm
unit_sec = beat/4
fps = 1/unit_sec

s_sec = int(sampfreq) #samples
s_beat = int(sampfreq*beat)
unit = int(s_beat/4)
s_custom = 1024
HPF, LPF = 0,500

AllFFT(unit)
files = [f for f in os.listdir(d) if ".png" in f]
files.sort()

frame_array = []
for i in range(len(files)):
    filename=d + "/" + files[i]
    img = cv2.imread(filename)
    height, width, layers = img.shape
    size = (width,height)
    frame_array.append(img)

out = cv2.VideoWriter("vid.mp4",cv2.VideoWriter_fourcc(*'DIVX'), fps, size)    
for i in range(len(frame_array)):
    out.write(frame_array[i])
out.release()
    