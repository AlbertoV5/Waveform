#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  7 15:58:28 2020

@author: albertovaldez
"""

import onset
from scipy.io import wavfile

songName = "marvin.wav"
song = onset.Audio(wavfile.read("songs/" + songName))

