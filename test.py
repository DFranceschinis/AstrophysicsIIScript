#!/usr/bin/python3

import AstroScript
import windowsearch as ws

AstroScript.process_all_files()

print("Start:", AstroScript.PERIODS[-2].start, "End:", AstroScript.PERIODS[-2].end)

A = ws.window_search_simple(AstroScript.NEUTRINOS, AstroScript.PERIODS, AstroScript.PERIODS[-2].start, AstroScript.PERIODS[-2].end, 10, 10, .1, AstroScript.PERIODS[-2].density, AstroScript.TOTAL_AREA)

print(A)

search_times = range(1,int(AstroScript.PERIODS[-2].end - AstroScript.PERIODS[-2].start))

B = ws.search_multiple_windows(AstroScript.NEUTRINOS, AstroScript.PERIODS, AstroScript.PERIODS[-2].start, AstroScript.PERIODS[-2].end, 1, search_times, 0.1, AstroScript.PERIODS[-2].density, AstroScript.TOTAL_AREA)

print(B)