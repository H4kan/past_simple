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


# this two functions need to be run in loop until some condition is met

algorithm.computeAlignments(plText, enText, probs, bestAlignments);

algorithm.computeProbsFromAlignments(plText, enText, probs, bestAlignments);

# after many iterations, function sentProb() will be calculating desired probability

print(probs.fert);


