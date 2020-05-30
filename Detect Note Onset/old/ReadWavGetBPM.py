"""
Use mono files (1 channel) of 16 bits, sample freq can vary

Recommended values:
Ratio is > 0.8 for most music
Unit is 2048
LPF is 200

"""
import onset
from scipy.io import wavfile
import matplotlib.pyplot as plt

audio = onset.Audio(wavfile.read("acemarino.wav"))

audio.GetNoteOnset(unit = 2048, chunk_size = 2048, threshold_ratio = 0.9, HPF = 20, LPF = 240)

audio.PlotNoteOnset()

print("BPM is: " + str(audio.GetBPM()))

spectrum = audio.GetNotesFrequencies(0.25, 512, 20, 240)

#audio.Plot_NotesSpectrum(spec)

notes = onset.GetTopFrequencies(spectrum, ratio = 0.3)

x, y = [],[]

for i in range(len(notes)):
    for j in notes[i]:
        y.append(j)
        x.append(i)
        
plt.scatter(x,y)


        
