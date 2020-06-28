'''
This script receives:
    
sampfreq, data = wavfile.read()
from scipy.io import wavfile

and returns onsets depending on what paremeters you set. 
Low and high pass filters-like included.
Included Transient Points.

To do:
    -Use right channel for control. 
    -Use bpm against samples or note onset for accuracy percentage
    -Compare different methods against each other to find differences and trends

https://docs.scipy.org/doc/scipy/reference/generated/scipy.fft.fft.html
https://www.w3resource.com/python-exercises/numpy/python-numpy-exercise-31.php

'''
import numpy as np
import scipy
import scipy.fftpack as fftpk
import matplotlib.pyplot as plt
import math

class Song():
    def __init__(self, audiofile, start = 0, end = 0):
        self.sampfreq = audiofile[0]
        self.data = audiofile[1]/32767 #16 bits
        self.peakAlphaIndex = 0
        try: # 1 channel only
            if len(self.data[0]) > 1: 
                self.data = [i[0] for i in self.data]
                print("2 channels detected. Using left side.")
        except:
            pass
        
        start = start * self.sampfreq
        end = end * self.sampfreq
        if end != 0:
            self.data = self.data[start:end]
        else:
            pass
        
        print("Audio file was read.")
        
    def GetRMS(self):
        return 20*np.log10((np.mean(np.absolute(self.data))))

    def FindAlphaPeak(self, start = 0, threshold = 0.8):
        index = 0
        self.peakAlpha = 0
        self.peakAlphaIndex = 0
        for i in self.data:
            if abs(i) > threshold:
                self.peakAlpha = i
                self.peakAlphaIndex = index
                break
            index +=1
        print("Alpha peak is at: " + str(self.peakAlphaIndex/self.sampfreq) + " seconds.")
        
    def GetNoteOnset(self, unit = 2048, chunk_size = 2048, threshold_ratio = 0.8, HPF = 20, LPF = 500, base = 10):
        pitch_sustain, self.notes = -1, []
        pitch_start,note_on = 0,0
        threshold = Get_Threshold(self.data, chunk_size, threshold_ratio, HPF, LPF, self.sampfreq)
        threshold = 10*math.log(threshold, base)
            
        print("Threshold found for " + str(threshold_ratio) + " ratio is: " + str(threshold))
        
        #song.length Prevents going over the limit and crashing
        self.length = len(self.data) - self.peakAlphaIndex
        
        for i in range(self.length//unit):
            start = unit*(i) + self.peakAlphaIndex
            end = unit*(i) + chunk_size + self.peakAlphaIndex
            pitch = ReadChunk(self.data[start:end], threshold, LPF, HPF, self.sampfreq, base)
            if pitch != -1 and pitch != pitch_sustain: #Note change
                note_on = start
                pitch_sustain = pitch
                pitch_start = pitch
            elif pitch == -1 and pitch_sustain>-1:
                note_release = start
                self.notes.append([note_on, note_release])
                pitch_sustain = pitch
                
                
    def GetPeaks(self, x):
        self.pks = []
        self.pksValue = []
        for i in self.notes:   
            #Limits of data
            try:
                start = i[0] - x
                end = i[1] + x
                noteSamples = self.data[start:end]
                top = np.amax(noteSamples)
                bot = np.amin(noteSamples)
            except:
                start = i[0]
                end = i[1]
                noteSamples = self.data[start:end]
                top = np.amax(noteSamples)
                bot = np.amin(noteSamples)
                
            # Circumvent indexing an absolute value
            if top > abs(bot):
                point = top
            else:
                point = bot
            
            transientPoint = int(max(np.where(noteSamples == point))[0]) + start
            self.pks.append(transientPoint)
            self.pksValue.append(point)
        
    def GetPeaks2(self,tr, skip = 2048):
        x,y = [],[]
        for i in range(self.peakAlphaIndex, len(self.data)):
            if abs(self.data[i]) > tr:
                x.append(i)
                y.append(abs(self.data[i]))
                i = i + skip
        return x,y
        
    def GetBPM(self, minBPM = 60, maxBPM = 200, kind = "mode"):
        x = [i[0] for i in self.notes]
        d = [x[i+1]-x[i] for i in range(len(x)) if i < len(x)-1]
        if kind == "mean":
            beat_s = mean(d)/self.sampfreq
        elif kind == "mode":
            beat_s = mode(d)/self.sampfreq
        elif kind == "median":
            beat_s = median(d)/self.sampfreq
        else:
            print("Error")
        bpm = 60/beat_s
        while bpm < minBPM or bpm > maxBPM:
            if bpm < minBPM:
                bpm = bpm*2
            elif bpm > maxBPM:
                bpm = bpm/2
        return bpm
        
    def GetBPM_PKS(self, minBPM, maxBPM, kind):
        d = [self.pks[i+1]-self.pks[i] for i in range(len(self.pks)) if i < len(self.pks)-1]
        if kind == "mean":
            beat_s = mean(d)/self.sampfreq
        elif kind == "mode":
            beat_s = mode(d)/self.sampfreq
        elif kind == "median":
            beat_s = median(d)/self.sampfreq
        else:
            print("Error.")
        if beat_s == 0:
            bpm = 0
        else:
            bpm = 60/beat_s
            while bpm < minBPM or bpm > maxBPM:
                if bpm < minBPM:
                    bpm = bpm*2
                elif bpm > maxBPM:
                    bpm = bpm/2
        return bpm 

    def OutNote(self, start, end):
        return np.asarray(self.data[start:end]*32767, dtype=np.int16)
    

    def PlotPeaks(self):
        x = self.pks
        y = [abs(i) for i in self.pksValue]
        y = [1 for i in self.pksValue]
        plt.xlabel("Sample Position")
        plt.ylabel("Amplitude")
        plt.scatter(x,y)
        plt.show()
    
    def SaveOnsets(self):
        self.notes
        data = ""
        for i in self.notes:
            data = data + str(i[0]/self.sampfreq) + "," + str(i[1]/self.sampfreq) + "\n"
        with open("onsets.csv", "w+") as file:
            file.write(data)
        
  
class Grid():
    def __init__(self,data):
        self.all = data
    
    def SetBPM(self, bpm):
        self.bpm = bpm
    
def GetBPM(notes, sampfreq, minBPM = 60, maxBPM = 200, kind = "mode"):
    x = [i[1] for i in notes]
    d = [x[i+1]-x[i] for i in range(len(x)) if i < len(x)-1]
    if kind == "mean":
        beat_s = mean(d)/sampfreq
    elif kind == "mode":
        beat_s = mode(d)/sampfreq
    elif kind == "median":
        beat_s = median(d)/sampfreq
    else:
        print("Error")
    bpm = 60/beat_s
    while bpm < minBPM or bpm > maxBPM:
        if bpm < minBPM:
            bpm = bpm*2
        elif bpm > maxBPM:
            bpm = bpm/2
    return bpm

def GetBPM_PKS(pks, sampfreq, minBPM, maxBPM, kind):
    d = [pks[i+1]-pks[i] for i in range(len(pks)) if i < len(pks)-1]
    if kind == "mean":
        beat_s = mean(d)/sampfreq
    elif kind == "mode":
        beat_s = mode(d)/sampfreq
    elif kind == "median":
        beat_s = median(d)/sampfreq
    else:
        print("Error.")
    bpm = 60/beat_s
    while bpm < minBPM or bpm > maxBPM:
        if bpm < minBPM:
            bpm = bpm*2
        elif bpm > maxBPM:
            bpm = bpm/2
    return bpm 


def GetNotePeaks(x, y):
    peaks_x = []
    peaks_y = []
    for i in range(len(y)):
        if i > 0 and i < len(y)-1:
            if y[i] > y[i - 1] and y[i] > y[i + 1]:
                peaks_x.append(x[i])
                peaks_y.append(y[i])
    return peaks_x, peaks_y
                
def GetTopFrequencies(spectrum, ratio):
    top = []
    for i in spectrum: #Get top frequencies
        index = np.where(i[1] > np.amax(i[1])*ratio)
        top.append(abs(i[0][index])) 
    return top
    
def PlotNote(note, sampfreq, LPF, HPF):    
    x, y = CalculateFFT_dB(note,sampfreq, LPF, HPF) 
    
    x_peaks, y_peaks = GetNotePeaks(x,y)
    plt.figure(figsize=(20,10))
    plt.xticks(x_peaks)
    plt.xlabel("Frequency")
    plt.ylabel("Amplitude (log)")
    plt.plot(x,y)
    plt.show()

def PlotNoteSpecial(note, sampfreq, LPF, HPF):    
    x, y = CalculateFFT(note,sampfreq, LPF, HPF) 
    
    scale = [i*100 for i in range(HPF//100)]
    
    maxValue = 150
    x2,y2 = [],[]
    for i in range(len(scale)):
        left = scale[i]
        try:
            right = scale[i+1]
        except:
            right = scale[i] + 100
        y_avg = []
        for j in range(len(x)):
            if x[j] >= left and x[j] < right:
                y_avg.append(y[j]/maxValue)
            
        yValue = mean(y_avg)
        x2.append(i)
        y2.append(yValue)
        
    plt.ylim(0, 1)
    plt.plot(x2,y2)
    plt.show()
    return x2,y2

def GetNotePlotSpecial(note, sampfreq, LPF, HPF):
    x, y = CalculateFFT(note,sampfreq, LPF, HPF) 
    
    scale = [i*100 for i in range(HPF//100)]
    
    maxValue = 150
    x2,y2 = [],[]
    for i in range(len(scale)):
        left = scale[i]
        try:
            right = scale[i+1]
        except:
            right = scale[i] + 100
        y_avg = []
        for j in range(len(x)):
            if x[j] >= left and x[j] < right:
                y_avg.append(y[j]/maxValue)
            
        yValue = mean(y_avg)
        x2.append(i)
        y2.append(yValue)
        
    return x2,y2

def PlotPeaks2(x, y, xticks, ylim, name):
    plt.figure(figsize=(20,10))
    plt.plot(x,y)
    plt.scatter(x,y)
    plt.ylim(ylim)
    plt.xticks(xticks)
    plt.savefig(name)
    plt.show()

def ReadChunk(chunk, threshold, LPF, HPF, sampfreq, base):
    FFT = abs(scipy.fft.fft(chunk))
    freqs = fftpk.fftfreq(len(FFT), (1.0/sampfreq))
    
    freqs = freqs[range(len(FFT)//2)]
    
    freqsHPF = freqs[freqs > HPF]
    freqsLPF = freqs[freqs < LPF]
    
    indexHPF = int(max(np.where(freqs == freqsHPF[0])))
    indexLPF = int(max(np.where(freqs == freqsLPF[len(freqsLPF)-1])))
        
    FFT = FFT[range(len(FFT)//2)]
    
    FFTF = FFT[indexHPF:indexLPF]
    freqsF = freqs[indexHPF:indexLPF]
    
    FFTF = np.log(FFTF) / np.log(base)
    FFTF = 10*FFTF
    
    if np.amax(FFTF) > threshold:
        index = np.where(FFTF == np.amax(FFTF))
        frequency = abs(freqsF[index])
        #PlotFreqs(freqs, FFT, 0, 1000)
    else:
        frequency = -1
    return frequency
    
def CalculateFFT(chunk, sampfreq, HPF, LPF):
        
    FFT = abs(scipy.fft.fft(chunk))
    freqs = fftpk.fftfreq(len(FFT), (1.0/sampfreq))
    
    freqs = freqs[range(len(FFT)//2)]
    
    freqsHPF = freqs[freqs > HPF]
    freqsLPF = freqs[freqs < LPF]
    
    indexHPF = int(max(np.where(freqs == freqsHPF[0])))
    indexLPF = int(max(np.where(freqs == freqsLPF[len(freqsLPF)-1])))
        
    FFT = FFT[range(len(FFT)//2)]
    
    FFTF = FFT[indexHPF:indexLPF]
    freqsF = freqs[indexHPF:indexLPF]
    
    return freqsF, FFTF 

def CalculateFFT_dB(chunk, sampfreq, HPF, LPF):
        
    FFT = abs(scipy.fft.fft(chunk))
    freqs = fftpk.fftfreq(len(FFT), (1.0/sampfreq))
    
    freqs = freqs[range(len(FFT)//2)]
    
    freqsHPF = freqs[freqs > HPF]
    freqsLPF = freqs[freqs < LPF]
    
    indexHPF = int(max(np.where(freqs == freqsHPF[0])))
    indexLPF = int(max(np.where(freqs == freqsLPF[len(freqsLPF)-1])))
        
    FFT = FFT[range(len(FFT)//2)]
    
    FFTF = FFT[indexHPF:indexLPF]
    freqsF = freqs[indexHPF:indexLPF]
    
    FFTF = np.log10(FFTF)
    FFTF = FFTF * 10
    return freqsF, FFTF 



def GetPartOnset(part,sampfreq = 44100, unit = 2048, chunk_size = 2048, threshold_ratio = 0.8, HPF = 20, LPF = 500):
    pitch_sustain, notes = -1, []
    pitch_start,note_on = 0,0
    threshold = Get_Threshold(part, chunk_size, threshold_ratio, HPF, LPF, sampfreq)
    
    #song.length Prevents going over the limit and crashing
    length = len(part)
    
    for i in range(length//unit):
        start = unit*(i) 
        end = unit*(i) + chunk_size
        pitch = ReadChunk(part[start:end], threshold, LPF, HPF, sampfreq)

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
            print("There was an error somewhere btw")
    
    return notes
                
def Get_Threshold(data, chunk_size, ratio, HPF, LPF, sampfreq):
        #Find the highest power in the frequency range in the whole song
        #Use it as threshold multiplied by the ratio received
        low, high = [],[]
        for i in range(int((len(data)/chunk_size))-1):
            start = chunk_size*(i)
            end = chunk_size*(i) + chunk_size
            chunk = data[start:end]
            
            FFT = abs(scipy.fft.fft(chunk))
            freqs = fftpk.fftfreq(len(FFT), (1.0/sampfreq))

            freqsHPF = freqs[freqs > HPF]
            freqsLPF = freqs[freqs < LPF]
            
            indexHPF = int(max(np.where(freqs == freqsHPF[0])))
            indexLPF = int(max(np.where(freqs == freqsLPF[len(freqsLPF)-1])))
            
            FFT = FFT[range(len(FFT)//2)]
            FFTF = FFT[indexHPF:indexLPF]

            low.append(np.amin(abs(FFTF)))
            high.append(np.amax(abs(FFTF)))

        return (max(high)) * ratio
    
def GetPeaks(part, notes, x):
        pks = []
        pksValue = []
        for i in notes:   
            #Limits of data
            try:
                start = i[0] - x
                end = i[1] + x
                noteSamples = part[start:end]
                top = np.amax(noteSamples)
                bot = np.amin(noteSamples)
            except:
                start = i[0]
                end = i[1]
                noteSamples = part[start:end]
                top = np.amax(noteSamples)
                bot = np.amin(noteSamples)
                
            # Circumvent indexing an absolute value
            if top > abs(bot):
                point = top
            else:
                point = bot
            
            transientPoint = int(max(np.where(noteSamples == point))[0]) + start
            pks.append(transientPoint)
            pksValue.append(point)   
        return pks, pksValue
    
    
def SavePeaks(peaks, sampfreq, channels, alphaPeak):
    data = ""
    for i in peaks:
        data = data + str(((alphaPeak + i) * channels)/sampfreq) + "\n"
    with open("peaks.csv", "w+") as file:
        file.write(data)
    
    
def GetRMS(part):
    rms = 20*np.log10((np.mean(np.absolute(part))))
    print("RMS is: " + str(rms) + " dB")
    return rms

def CalculateThreshold_RMS(data):
    rms = GetRMS(data)
    floor = -48
    tr = 1 - (rms/floor)
    print("Suggested treshold is: " + str(tr))
    return tr

def FitFrequencyInBands(freq, bandL, bandR, i):
    if freq >= bandL and freq < bandR:
        return True

def FrequencyBands(x,y, bandsLimits):
    bands = [[] for i in range(len(bandsLimits))]
    
    #Read frequency on x, append value on y on frequency band, forgets about x
    for i in range(len(x)):
        for j in range(len(bandsLimits)-1):
            if FitFrequencyInBands(x[i],bandsLimits[j],bandsLimits[j+1],i):
                bands[j].append(y[i])               
    return bands
'''
if x[i] >= bands[j] and x[i] < bands[j + 1]:
    eq[j].append(y[i])
'''    
    
def mode(List):  #most frequent
    return max(set(List), key = List.count) 
def mean(List): #average value
    return sum(List)/len(List)
def median(List): #middle of the list
    return sorted(List)[int(len(List)/2)]

