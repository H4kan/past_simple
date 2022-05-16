import math;
from collections import Counter;
import alignment;
import constraints;
from utils import *;
from probs import Probs;
import algorithm;



plText = [["Ala", "ma", "kota", "i", "pieska", "tez"],
["Benek", "ma", "pieska", "i", "chomika", "tez"],]
enText = [["Ala", "has", "cat", "and", "dog", "as", "well"],
["Benek", "has", "dog", "and", "hamster", "as", "well"]];

probs = Probs(plText, enText);

plWords = ["Ala", "ma", "kota", "i", "pieska", "tez"];
enWords = ["Ala", "has", "cat", "and", "dog", "as", "well"];

algs = alignment.generateAlignments(enWords, plWords);

bestAlignments = {idx: [] for idx in range(0, len(plText))};

maxSteps = 100;

prevBestProb = 0;
prevRatio = -1;

# this two functions need to be run in loop until some condition is met

for i in range(0, maxSteps):

    algorithm.computeAlignments(plText, enText, probs, bestAlignments);

    algorithm.computeProbsFromAlignments(plText, enText, probs, bestAlignments);

#     # convergence condition, not sure how to formulate it best way
    currBestProb = 0;
    for idx in range(0, len(plText)):
        currBestProb = max(currBestProb, algorithm.sentProb(plText[idx], enText[idx], bestAlignments[idx], probs));

    if currBestProb > 0 and abs(prevBestProb / currBestProb - prevRatio) < 1e-5: 
        break;

    prevRatio = prevBestProb / currBestProb;
    prevBestProb = currBestProb;


# after many iterations, function sentProb() will be calculating desired probability
