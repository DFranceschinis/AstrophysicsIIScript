#!/usr/bin/python3

import AstroScript

AstroScript.process_all_files()

A = AstroScript.window_search_simple(AstroScript.NEUTRINOS, AstroScript.PERIODS, AstroScript.PERIODS[0].start, AstroScript.PERIODS[0].end, 10, 10, .1, AstroScript.PERIODS[0].density)

for a in A:
	print(a)


