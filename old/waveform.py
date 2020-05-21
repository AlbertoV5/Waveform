from scipy.io import wavfile
from scipy.fft import fft
import numpy as np
import matplotlib.pyplot as plt
import cv2
import os

d = os.getcwd()

sampfreq, data = wavfile.read("leltrique128BPM.wav")
bass = np.array(data,dtype=float)
bassabs = np.absolute(bass)
top = 6.55*(10**4)/2 #16 bits
norm = np.array([i/top for i in bass.tolist()])

def PlotWaveform(data):
    fig,ax = plt.subplots(subplot_kw=dict())
    ax.plot(data)
    ax.set_ylim(bottom = -1, top = 1)
    fig.show()

#PlotWaveform(norm)

def GetChunkFFT(chunk, LPF, HPF):
    _fft = fft(chunk)
    fft_normalized = [abs(_fft[i]) for i in range(len(_fft)//2)]
    return [fft_normalized[i] for i in range(HPF, LPF)]
  
def PlotFFT(data, name, color):
    fig1,ax1 = plt.subplots(subplot_kw=dict())
    ax1.plot(data, color = color)
    ax1.set_ylim(bottom = 0, top = 500)
    
    fig1.savefig(name)
    fig1.show()    
  
def AllFFT(unit):
    chunk_size = 1024
    for i in range(64):
        chunk = [norm[i] for i in range((i*unit)-chunk_size,(i*unit)+chunk_size)]
        if i%4 == 0:
            if i%8 == 0:
                color = "g"
            else:
                color = "r"
        else:
            color = "k"
        
        spectrum = GetChunkFFT(chunk, LPF, HPF)
        PlotFFT(spectrum, str(i).zfill(3), color)
        
bpm = 128
beat = 60/bpm
unit_sec = beat/4
fps = 1/unit_sec

s_sec = int(sampfreq) #samples
s_beat = int(sampfreq*beat)
unit = int(s_beat/4)
s_custom = 1024
HPF, LPF = 0,40

AllFFT(unit)

files = [f for f in os.listdir(d) if ".png" in f]
files.sort()
print(files)

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
    