"""
Use mono files (1 channel) of 16 bits pls, sample freq can vary

Recommended values:
Ratio is > 0.8
Unit is 2048
LPF is 200

"""
import onset
from scipy.io import wavfile

audio = onset.Audio(wavfile.read("sine.wav"))

audio.Get_NoteOnset(unit = 2048, chunk_size = 2048, threshold_ratio = 0.6, LPF = 500, HPF = 20)

audio.Plot_NoteOnset()

print("BPM is: " + str(audio.Get_BPM()))

#spec = audio.Get_NotesFrequencies(0.25, 512)

#audio.Plot_NotesSpectrum(spec)
