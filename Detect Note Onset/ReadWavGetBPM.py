"""
Created on Sat May 23 19:34:05 2020

@author: albertovaldez
"""
import onset
from scipy.io import wavfile

audio = onset.Audio(wavfile.read("lektrique.wav"))

audio.Get_NoteOnset(unit = 2048, chunk_size = 2048, threshold = 150, LPF = 200, HPF = 20)

audio.Plot_NoteOnset()

print("BPM is: " + str(audio.Get_BPM()))


