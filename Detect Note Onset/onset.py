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

sampfreq, data = wavfile.read("drums1.wav")
data = data/65536
unit = 1024
chunk_size = 2048
threshold = 50
LPF = 200
HPF = 20

def Plot(x, y):    
    fig1,ax1 = plt.subplots(subplot_kw=dict())
    ax1.plot(x[range(len(y)//2)],y[range(len(y)//2)])
    ax1.set_xlim(left = 0, right = 1000)

def ReadChunk(chunk):
    FFT = abs(scipy.fft.fft(chunk))
    freqs = fftpk.fftfreq(len(FFT), (1.0/sampfreq))
    
    low_pass_filter = freqs[abs(freqs) < LPF]
    high_pass_filter = low_pass_filter[abs(low_pass_filter) > HPF]
                        
    filtered = FFT[:len(high_pass_filter)]
    
    if np.amax(filtered) > threshold:
        index = np.where(filtered == np.amax(filtered))
        frequency = abs(high_pass_filter[index])
        #Plot(freqs, FFT)
    else:
        frequency = -1
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
    pitch_sustain, notes = -1, []
    pitch_start,note_on = 0,0
    for i in range(int(len(data)/unit)):
        start = unit*(i)
        end = unit*(i) + chunk_size
        pitch = ReadChunk(data[start:end])
        try:
            if pitch != -1 and pitch != pitch_sustain: #Note change
                note_on = start
                pitch_sustain = pitch
                pitch_start = pitch
            elif pitch == -1 and pitch_sustain>-1:
                note_release = start
                notes.append([pitch_start, note_on, note_release])
                pitch_sustain = pitch
        except:
            pass

    y = [i[0] for i in notes]
    x = [i[1] for i in notes]
    l = [i[2]-i[1] for i in notes] 
    
    plt.scatter(x,y)
    return notes, x, y, l
    
notes = Process()

x = notes[1]
print(notes[0])
d = [x[i+1]-x[i] for i in range(len(x)) if i < len(x)-1]

beat_s = most_frequent(d)/sampfreq
bpm = 60/beat_s

print("BPM is:")
print(bpm)




