#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: albertovaldez
"""
import onset
from scipy.io import wavfile
import numpy as np

songName = "prizm love.wav"

sampfreq, data = wavfile.read("songs/" + songName)

ratio = 1.16666

newsamp = int(sampfreq*ratio)

wavfile.write("spedup.wav", newsamp, data)



