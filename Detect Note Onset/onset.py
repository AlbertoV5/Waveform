'''
This script receives:
    
sampfreq, data = wavfile.read()
from scipy.io import wavfile

and returns onsets depending on what paremeters you set. 
Low and high pass filters-like included.

It has to be expanded for more options, as well as getting a better undestanding of 
the threshold for "frequency amplitude" as it is not clear to me what's the best
way to limit it to fit the audio file automatically

https://docs.scipy.org/doc/scipy/reference/generated/scipy.fft.fft.html
https://www.w3resource.com/python-exercises/numpy/python-numpy-exercise-31.php

'''
import numpy as np
import scipy
import scipy.fftpack as fftpk
import matplotlib.pyplot as plt

class Audio():
    def __init__(self, audiofile):
        self.sampfreq = audiofile[0]
        self.data = audiofile[1]/65536 #16 bits
        
    def Get_NoteOnset(self, unit = 1024, chunk_size = 2048, threshold = 50, LPF = 1000, HPF = 20):
        pitch_sustain, self.notes = -1, []
        pitch_start,note_on = 0,0
        for i in range(int(len(self.data)/unit)):
            start = unit*(i)
            end = unit*(i) + chunk_size
            pitch = ReadChunk(self.data[start:end], threshold, LPF, HPF, self.sampfreq)
            try:
                if pitch != -1 and pitch != pitch_sustain: #Note change
                    note_on = start
                    pitch_sustain = pitch
                    pitch_start = pitch
                elif pitch == -1 and pitch_sustain>-1:
                    note_release = start
                    self.notes.append([pitch_start, note_on, note_release])
                    pitch_sustain = pitch
            except:
                print("There was an error somewhere btw")
    
    def Plot_NoteOnset(self):
        self.y = [i[0] for i in self.notes]
        self.x = [i[1]/self.sampfreq for i in self.notes]
        self.l = [i[2]-i[1] for i in self.notes] 
        plt.xlabel("Time (s)")
        plt.ylabel("Frequency (Hz)")
        plt.scatter(self.x,self.y)
    
    def Get_BPM(self, minBPM = 60, maxBPM = 200):
        x = [i[1] for i in self.notes]
        d = [x[i+1]-x[i] for i in range(len(x)) if i < len(x)-1]
        beat_s = most_frequent(d)/self.sampfreq
        bpm = 60/beat_s
        while bpm < minBPM or bpm > maxBPM:
            if bpm < minBPM:
                bpm = bpm*2
            elif bpm > maxBPM:
                bpm = bpm/2
        return bpm

# For visualizing chunks
def Plot(x, y, l, r):    
    fig1,ax1 = plt.subplots(subplot_kw=dict())
    ax1.plot(x[range(len(y)//2)],y[range(len(y)//2)])
    ax1.set_xlim(left = l, right = r)

def ReadChunk(chunk, threshold, LPF, HPF, sampfreq):
    FFT = abs(scipy.fft.fft(chunk))
    freqs = fftpk.fftfreq(len(FFT), (1.0/sampfreq))
    
    #The term is not accurate to synthesis but its a similar idea
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

def most_frequent(List): 
    return max(set(List), key = List.count) 
def avg(List):
    return sum(List)/len(List)


