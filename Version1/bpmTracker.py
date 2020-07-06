#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  6 17:46:04 2020

@author: albertovaldez
"""

import onset

song = onset.Song("songs/spectre/spectre.mp3")

onset.GetBPMS(song, song.CalculateThreshold_RMS())

