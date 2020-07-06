#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
"""
import numpy as np
import scipy
import matplotlib.pyplot as plt
from scipy.io import wavfile
import scipy.fftpack as fftpk
from pydub import AudioSegment
import os

def toWAV(mp3):
    wav = mp3.split(".")[0] + ".wav"
    sound = AudioSegment.from_mp3(mp3)
    sound.export(wav, format="wav")
    print("Converted mp3 to wav.")
    return wav

class Song():
    def __init__(self, songName, start_sec = 0, end_sec = 0):
        if ".mp3" in songName:
            songName = toWAV(songName)
            clear = True
            
        print("Reading audio file...")
        audiofile = wavfile.read(songName)
        self.sampfreq, self.data = audiofile[0], audiofile[1]/32767 #16 bits
        self.peakAlphaIndex = 0
        self.length = len(self.data) - self.peakAlphaIndex
        self.length_seconds = self.length / 44100

        self.channels = len(self.data[0])
        if self.channels == 2: # checks for stereo
            self.data = np.add(self.data[:, [0]], self.data[:, [1]]) / self.channels
            print(len(self.data))
            
        if end_sec != 0:
            self.data = self.data[int(start_sec * self.sampfreq):int(end_sec * self.sampfreq)]
            
        print("\nAudio file was read.")
        if clear:
            os.remove(songName)
        
    def GetRMS(self): # decibels
        rms = 20*np.log10((np.mean(np.absolute(self.data))))
        return int(rms*100)/100

    def FindAlphaPeak(self, start = 0, threshold = 0.8):
        for i in range(len(self.data)):
            if abs(self.data[i]) > threshold:
                self.peakAlpha = self.data[i]
                self.peakAlphaIndex = i
                self.length = len(self.data) - self.peakAlphaIndex
                self.length_seconds = self.length / 44100
                return int((self.peakAlphaIndex/self.sampfreq)*1000)/1000
        
    def GetNoteOnset(self, unit = 2048, chunk_size = 2048, threshold_ratio = 0.8, HPF = 20, LPF = 500):
        sus, on, self.notes = -1, -1, []
        note_on = 0
        threshold = Get_Threshold(self.data, chunk_size, threshold_ratio, HPF, LPF, self.sampfreq)
        print("Ratio: " + str(threshold_ratio) + " = Threshold: " + str(threshold))
                
        for i in range(self.length//unit):
            start = unit*(i) + self.peakAlphaIndex
            end = unit*(i) + chunk_size + self.peakAlphaIndex
            
            on = ReadChunk(self.data[start:end], threshold, LPF, HPF, self.sampfreq)
            if on == 1 and sus == -1: #Note change
                note_on = start
                sus = 1
            elif on == -1 and sus == 1:
                note_release = start
                self.notes.append([note_on, note_release])
                sus = -1
                    
    def GetPeaks(self, x):
        self.pks, self.pksValue = [],[]
        for i in self.notes: #notes as an array of start,end pairs
            try:
                start = i[0] - x
                end = i[1] + x
                noteSamples = self.data[start:end]
                point = np.amax(np.absolute(noteSamples))
            except:
                start = i[0]
                end = i[1]
                noteSamples = self.data[start:end]
                point = np.amax(np.absolute(noteSamples))
            
            transientPoint = np.min(np.where(np.absolute(noteSamples) == point)) + start
            self.pks.append(transientPoint)
            self.pksValue.append(point)
        
    def GetBPM(self, minBPM = 80, maxBPM = 210, kind = "mode"):
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
        
    def GetBPM_PKS(self, minBPM = 80, maxBPM = 210, kind = "mode"):
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
    
    def CalculateThreshold_RMS(self):
        rms = GetRMS(self.data)
        floor = -96
        tr = 1 - (rms/floor)
        return int(tr * 10000)/10000

    def PlotPeaks(self):
        x = self.pks
        y = [abs(i) for i in self.pksValue]
        y = [1 for i in self.pksValue]
        plt.figure(figsize = (20,5))
        plt.xlabel("Sample Position")
        plt.ylabel("Amplitude")
        plt.grid(True)
        plt.scatter(x,y)
        plt.savefig("song peaks.png")
        plt.show()
    
    def SaveOnsets(self):
        self.notes
        data = ""
        for i in self.notes:
            data = data + str(i[0]/self.sampfreq) + "," + str(i[1]/self.sampfreq) + "\n"
        with open("onsets.csv", "w+") as file:
            file.write(data)


def GetFrequencyPeaks(x, y):
    peaks_x = []
    peaks_y = []
    for i in range(len(y)):
        if i > 0 and i < len(y)-1:
            if y[i] > y[i - 1] and y[i] > y[i + 1]:
                peaks_x.append(x[i])
                peaks_y.append(y[i])
    return peaks_x, peaks_y

                    
def PlotNote(note, sampfreq, LPF, HPF, name):    
    x, y = CalculateFFT_dB(note,sampfreq, LPF, HPF) 
    x_peaks, y_peaks = GetFrequencyPeaks(x,y)
    plt.figure(figsize=(20,10))
    #plt.xticks(x_peaks)
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Amplitude (dB)")
    plt.plot(x,y)
    plt.savefig(name)
    plt.show()

def PlotNote2(note, sampfreq, LPF, HPF, name, xticks):    
    x, y = CalculateFFT_dB(note,sampfreq, LPF, HPF) 
    plt.figure(figsize=(20,10))
    plt.xticks(xticks)
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Amplitude (dB)")
    plt.plot(x,y)
    plt.savefig(name)
    plt.show()


def PlotPeaks2(x, y, xticks, ylim, name):
    plt.figure(figsize=(20,10))
    plt.grid(True)
    plt.plot(x,y)
    plt.scatter(x,y)
    plt.ylim(ylim)
    plt.xticks(xticks)
    plt.savefig(name)
    plt.show()

def ReadChunk(chunk, threshold, LPF, HPF, sampfreq):
    FFT = abs(scipy.fft.fft(chunk))
    freqs = fftpk.fftfreq(len(FFT), (1.0/sampfreq))
    
    freqs = freqs[range(len(FFT)//2)]
    
    freqsHPF = freqs[freqs > HPF]
    freqsLPF = freqs[freqs < LPF]
    
    indexHPF = int(max(np.where(freqs == freqsHPF[0])))
    indexLPF = int(max(np.where(freqs == freqsLPF[len(freqsLPF)-1])))
        
    FFT = FFT[range(len(FFT)//2)]
    FFTF = FFT[indexHPF:indexLPF]
    
    if np.sum(np.absolute(FFTF)) > threshold:
        frequency = 1
    else:
        frequency = -1
    return frequency
    

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
    
    return freqsF, FFTF 


def Get_Threshold(data, chunk_size, ratio, HPF, LPF, sampfreq):
        #Find the highest power in the frequency range in the whole data
        #Use it as threshold multiplied by the ratio received
        high = []
        for i in range(int((len(data)/chunk_size))-1):
            start = chunk_size*(i)
            end = chunk_size*(i) + chunk_size
            chunk = data[start:end]
            
            FFT = abs(scipy.fft.fft(chunk))
            freqs = fftpk.fftfreq(len(FFT), (1.0/sampfreq))

            freqs = freqs[range(len(FFT)//2)]

            freqsHPF = freqs[freqs > HPF]
            freqsLPF = freqs[freqs < LPF]
            
            indexHPF = int(max(np.where(freqs == freqsHPF[0])))
            indexLPF = int(max(np.where(freqs == freqsLPF[len(freqsLPF)-1])))
            
            FFT = FFT[range(len(FFT)//2)]
            
            FFTF = FFT[indexHPF:indexLPF]
            
            high.append(np.sum(np.absolute(FFTF)))
            
        threshold = (np.max(high))
        return threshold * ratio
    
    
def SavePeaks(peaks, sampfreq, channels, alphaPeak, name):
    data = ""
    for i in peaks:
        data = data + str(((alphaPeak + i) * channels)/sampfreq) + "\n"
    with open(name, "w+") as file:
        file.write(data)
    
def GetRMS(part):
    rms = 20*np.log10((np.mean(np.absolute(part))))
    print("RMS is: " + str(rms) + " dB")
    return rms

def CalculateThreshold_RMS(data):
    rms = GetRMS(data)
    floor = -96
    tr = 1 - (rms/floor)
    print("Suggested ratio is: " + str(tr))
    return int(tr * 10000)/10000

def CalculateThreshold_RMS2(data):
    rms = GetRMS(data)
    floor = -48
    tr = 0.5 + (rms/floor)
    print("Suggested ratio is: " + str(tr))
    return tr

def FitFrequencyInBands(freq, bandL, bandR, i):
    if freq >= bandL and freq < bandR:
        return True
    
def FrequencyBands(freqs,amplitude, bandsLimits):
    bands = [[] for i in range(len(bandsLimits))]
    #Read frequency on x, append value on y on frequency band, forgets about x
    for i in range(len(freqs)):
        for j in range(len(bandsLimits)-1):
            if FitFrequencyInBands(freqs[i],bandsLimits[j],bandsLimits[j+1],i):
                bands[j].append(amplitude[i])  
                
    return AmplitudeSum(bands)

def AmplitudeSum(freqBands):
    y = []
    for j in freqBands:
        y.append(sum(j))
    return y

    
def GetTopFrequencies(a,b,start,num = 5):
    x, y = list(a), list(b)
    freq,amp = [],[]
    for i in range(num):
        m = (max(y))
        f = x[y.index(m)]
        freq.append(f)
        amp.append(m)
        
        index = y.index(m)
        y.pop(index)
        x.pop(index)
        
    return [freq, amp, start]

def mode(List):  #most frequent
    return max(set(List), key = List.count) 
def mean(List): #average value
    return sum(List)/len(List)
def median(List): #middle of the list
    return sorted(List)[int(len(List)/2)]


def GetBPMS(song, tr):
    
    print("\nCalculating Possible BPMs...")
    song.FindAlphaPeak(0,tr)
    song.GetNoteOnset(unit = 2048, chunk_size = 2048, threshold_ratio = tr, HPF = 0, LPF = 120)
    song.GetPeaks(x = 1024)
    print("\nCalculated possible BPMs:")
    
    magicRatio = (128/129.19921875)
    magicRatio2 = 1
    
    bpm1 = song.GetBPM()*magicRatio
    
    bpm2 = int(song.GetBPM_PKS()*magicRatio2*100)/100
    bpmBatch = [bpm1, bpm1*1.5, bpm2, bpm2*1.5]
    
    print(bpmBatch)
    
    return bpmBatch

