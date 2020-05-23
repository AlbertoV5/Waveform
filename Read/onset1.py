'''
https://docs.scipy.org/doc/scipy/reference/generated/scipy.fft.fft.html
https://www.w3resource.com/python-exercises/numpy/python-numpy-exercise-31.php
'''
from scipy.io import wavfile
import numpy as np
from scipy.fft import fft
import scipy
import scipy.fftpack as fftpk
import matplotlib.pyplot as plt

sampfreq, data = wavfile.read("lektrique.wav")
data = data/65536
unit = 1024
offset = 2048
threshold = 120
LPF = 100
unit_range = 1

def Plot(x, y):    
    fig1,ax1 = plt.subplots(subplot_kw=dict())
    ax1.plot(x[range(len(y)//2)],y[range(len(y)//2)])
    ax1.set_xlim(left = 0, right = 1000)

def ReadChunk(chunk):
    FFT = abs(scipy.fft.fft(chunk))
    freqs = fftpk.fftfreq(len(FFT), (1.0/sampfreq))
    
    bands = freqs[abs(freqs) < LPF]
    filtered = FFT[:len(bands)]
    
    if np.amax(filtered) > threshold:
        index = np.where(filtered == np.amax(filtered))
        #print(np.amax(filtered))
        frequency = max(abs(bands[index]))
        #print(frequency)
        #Plot(freqs, FFT)
    else:
        frequency = 0
    return frequency

def ReadPitch(chunk):
    FFT = abs(scipy.fft.fft(chunk))
    freqs = fftpk.fftfreq(len(FFT), (1.0/sampfreq))  
    index = np.where(FFT == np.amax(FFT))
    return max((abs(freqs[index])))

def most_frequent(List): 
    return max(set(List), key = List.count) 
def avg(List):
    return sum(List)/len(List)

def Process():  
    pitch_sustain = 0
    notes = []
    pitch_collection = []
    for i in range(int(len(data)/unit)):
        start = unit*(i)
        end = unit*(i+unit_range)
        pitch = ReadChunk(data[start:end])
        if pitch > 0 and pitch != pitch_sustain: #Note change
            note_on = start
            pitch_sustain = pitch
            pitch_start = pitch
        elif pitch == 0 and pitch_sustain > 0:
            note_release = start
            notes.append([pitch_start, note_on, note_release])
            pitch_sustain = 0
            pitch_collection = []
     
    y = [i[0] for i in notes]
    x = [i[1] for i in notes]
    l = [i[2]-i[1] for i in notes] 
    
    plt.scatter(x,y)
    return notes, x, y, l
    
notes = Process()
x = notes[1]
d = [x[i+1]-x[i] for i in range(len(x)) if i < len(x)-1]

print(most_frequent(d))

beat_s = most_frequent(d)/sampfreq
bpm = 60/beat_s

print(bpm)




