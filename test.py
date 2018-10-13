#!/usr/bin/python3

import AstroScript
import windowsearch as ws
import MatchedData as MD


print("Start:", AstroScript.PERIODS[-2].start, "End:", AstroScript.PERIODS[-2].end)

A = ws.window_search_simple_box(MD.WeightedSUBSET, AstroScript.PERIODS, AstroScript.PERIODS[-2].start, AstroScript.PERIODS[-2].end, 1, 158, .1, AstroScript.PERIODS[-2].density, AstroScript.TOTAL_AREA)

print(A,"Probability",A.p_value,A.midTime, A.width)


print('\n\nThis is the proper search\n\n')

search_times = range(1,int(AstroScript.PERIODS[-2].end - AstroScript.PERIODS[-2].start))

B = ws.search_multiple_windows_box(MD.WeightedSUBSET, AstroScript.PERIODS, AstroScript.PERIODS[-2].start, AstroScript.PERIODS[-2].end, 1, search_times, 0.1, AstroScript.PERIODS[-2].density, AstroScript.TOTAL_AREA)

print('\n\nResults:')

print(B, "midTime:", B.midTime, "width:", B.width, "minProb:", B.p_value, "#_pts_inside", len(B.points))