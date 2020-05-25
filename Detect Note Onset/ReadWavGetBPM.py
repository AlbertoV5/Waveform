"""
Use mono files (1 channel) of 16 bits, sample freq can vary

Recommended values:
Ratio is > 0.8
Unit is 2048
LPF is 200

"""
import onset
import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt

audio = onset.Audio(wavfile.read("takeuchi.wav"))

audio.Get_NoteOnset(unit = 2048, chunk_size = 2048, threshold_ratio = 0.8, HPF = 20, LPF = 500)

audio.Plot_NoteOnset()

print("BPM is: " + str(audio.Get_BPM()))

spectrum = audio.Get_NotesFrequencies(0.25, 512, 20, 500)

#audio.Plot_NotesSpectrum(spec)

notes = onset.GetTopFrequencies(spectrum, 0.2)

x, y = [],[]

for i in range(len(notes)):
    for j in notes[i]:
        y.append(j)
        x.append(i)
        
plt.scatter(x,y)

        
