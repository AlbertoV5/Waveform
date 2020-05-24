"""
Created on Sat May 23 19:34:05 2020

@author: albertovaldez
"""

import onset
from scipy.io import wavfile

audio = onset.Audio(wavfile.read("drums1.wav"))

audio.Get_NoteOnset(unit = 1024, chunk_size = 2048, threshold = 50, LPF = 500, HPF = 20)

audio.Plot_NoteOnset()

print("BPM is: " + str(audio.Get_BPM()))
