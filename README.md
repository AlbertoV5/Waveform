# Waveform Parsons Code
 Read waveform and do stuff

Python 3.7

Required:
- Numpy
- Scipy
- Matplot
Extra:
- Pydub for converting .mp3 if you don't want to conver to WAV 16 bits manually
- CV2 if you want to generate the 4x4 video reference.


What it does:

- Read a song and output 4 parson code sequences (Melody, Bass, Snare, HiHats) or (300-1.8k Hz, 0-120 Hz, 120-300 Hz, 9k-16k Hz.)
- Save the sequences as plot, data (position, energy, frequency) .csv and "peaks" .csv.
- Reascript for importing peaks to Reaper not included.

Applications:

- Rhythm Games, automatic map generation.
- General song analysis/comparison.
- Not a reliable "automatic music transcriber".

To do:

- Reading and exporting the data is pretty much done, need to interpret the pc in more creative ways:
 - Cancelling octave frequencies from adjacent bands like melody and hihats in order to remove "sss" from vocals bleeding into hihats.
 - Classify same frequency sequences as a sustained note.
- Add the "timbre" frequency band as in 1.8k-9k Hz to get more info. about the instruments/genres or section of the song.
- Add a section function to determine different sections of the song, include RMS, timbre and "Snapshot method" for similarities between bars and repetitions.
- Add an actual BPM detection function that can verify the bpm from more information apart from bass note onset.
- Considering harmonic detection for sections as a tonal reference.
