import AstroScript
import os
import matplotlib.pyplot as plt
import math
from useful_functions import *
from windowsearch import *


__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

### MatchedDATA is the list of MJDs from the 86B plotted subset
MatchedDATA = []
### logDATA is the list of log10 weights from the plotted subset
logDATA = []


Matcheddatapoints = open(os.path.join(__location__,"data/86bMatchedPoints.csv"), 'r', encoding='utf-8-sig').readlines()
for line in Matcheddatapoints:
	l=line.strip()
	l.replace
	MatchedDATA.append(float(l))

Weighteddatapoints = open(os.path.join(__location__,"data/WeightedDataPoints.csv"), 'r', encoding='utf-8-sig')
for line in Weighteddatapoints:
	l = line.strip().split(',')
	logDATA.append(l[1])

### PlotDATA is the list of MJDs and corresponding log10 weights from subset
PlotDATA = list(zip(MatchedDATA, logDATA))

### WeightedSUBSET is the plotted subset of neutrinos with the weighted values appended
WeightedSUBSET = []

AstroScript.process_all_files()

for MJD, W in PlotDATA:
	for p in AstroScript.NEUTRINOS:
		if ((round(float(MJD),2))==(round(p.MJD,2))):
			p.weight = float(W)
			WeightedSUBSET.append(p)
			continue


### Lists for plotting values against Weightings
Seps = [p.separation.value for p in WeightedSUBSET]
Ens = [p.ENERGY for p in WeightedSUBSET]
Ws = [p.weight for p in WeightedSUBSET]

# plt.scatter(Seps, Ws)
# plt.title("Separation vs Log10 Weight")
# plt.xlabel("Separation")
# plt.ylabel("log10 Weight")
# plt.show()

# plt.scatter(Ens, Ws)
# plt.title("Energy vs Log10 Weight")
# plt.xlabel("Energy")
# plt.ylabel("log10 Weight")
# plt.show()

# Comb = [a/b for a,b in zip(Ens, Seps)]
# plt.scatter(Comb, Ws)
# plt.title("Combination vs Log10 Weight")
# plt.xlabel("Combination")
# plt.ylabel("log10 Weight")
# plt.show()


# B = list(find_points_in_time_window(56067.076728,57159.599401, AstroScript.NEUTRINOS))

<<<<<<< HEAD
BEnergy = [N.ENERGY for N in B]
counts,bins,c = plt.hist(BEnergy, 10)

HistCounts = counts.tolist()
HistBins = bins.tolist()
=======
# BEnergy = [N.ENERGY for N in B]

# plt.hist(BEnergy, 10, histtype='bar', align='mid', orientation='vertical')

# a = plt.hist(BEnergy, 10, histtype='bar', align='mid', orientation='vertical')
# print(a)
>>>>>>> 58d3361946999e17f96f0f5e58bb763c0d3e67d0

# plt.show()

eB = []

midBIN = []
for b in range(len(HistBins) - 1):
	middle = HistBins[b] + ((HistBins[b+1]-HistBins[b])/2)
	midBIN.append(middle)


es = []
exp = []
wgt = []
untm = []
angsep = []
whole = []
unsq = []


for p in WeightedSUBSET:
	UncSq = math.pow(p.UNC,2)
	AngSepSq = math.pow(p.separation.value,2)
	
	UncTerm = 1/(2*math.pi*UncSq)
	Exponential = math.exp(-(AngSepSq)/(2*(UncSq)))
	Weight = math.pow(10,p.weight)

	untm.append(UncTerm)
	exp.append(Exponential)
	wgt.append(Weight)
	angsep.append(AngSepSq)
	unsq.append(UncSq)

	print (p.MJD, p.ENERGY, p.weight)

	for b in range(len(HistBins) - 1):
		if HistBins[b]<= p.ENERGY and p.ENERGY < HistBins[b+1]:
			countVal = HistCounts[b]/math.pow(midBIN[b],10)
			eq = Weight*countVal/(Exponential*UncTerm)
			es.append(math.log10(eq))
			# print (countVal,eq,math.log10(eq))


plt.scatter(Ens, es)
# plt.scatter(wgt, exp)
# plt.title("Energy vs EpsS")
# plt.xlabel("Weight")
# plt.ylabel("Exp Value")
plt.show()
