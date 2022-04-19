import math;
from collections import Counter;
import alignment;
import constraints;
from utils import *;
from probs import Probs;

# flattenPl = flatten(plText);
# wordsInPl = unique(flattenPl);
# wordsInEn = unique(flatten(enText));
# lenPl = len(flattenPl);

def sentProb(plSent, enSent, alignment, probs):
    res = 1;
    for i in range(0, len(plSent)):
        n_i = len(alignment[i + 1]);
        if (n_i > 0):
            res *= probs.fert[plSent[i]][n_i];
            for j in range(0, n_i):
                res *= probs.trans[plSent[i]][enSent[alignment[i + 1][j]]];
                res *= probs.dist[len(enSent)][alignment[i + 1][j]][i];
    return res;

def getBestAlignment(plSent, enSent, probs):
    algs = alignment.generateAlignments(plSent, enSent);
    maxProb = 0;
    currProb = 0;
    maxIdx = -1;
    for idx, alg in enumerate(algs):
        currProb = sentProb(plSent, enSent, alg, probs);
        if (currProb > maxProb):
            maxProb = currProb;
            maxIdx = idx;
    return algs[maxIdx];

def computeAlignments(plText, enText, probs, bestAlignments):
    for idx, plSent in enumerate(plText):
        bestAlignments[idx] = getBestAlignment(plSent, enText[idx], probs);


def computeFertFromAlignments(plText, enText, probs, bestAlignments):
    
    fertCounters = {w: [0, 0, 0, 0, 0, 0] for w in (probs.allPlWords + ["\0"])};
    for idx, plSent in enumerate(plText):
        for wordIdx, plWord in enumerate(plSent):
            fertCounters[plWord][len(bestAlignments[idx][wordIdx + 1])] += 1;
        fertCounters["\0"][len(bestAlignments[idx][0])] += 1;
    
    for word, fertProb in enumerate(probs.fert):
        countersSum = sum(fertCounters[fertProb]);
        for idx, f in enumerate(probs.fert[fertProb]):
            probs.fert[fertProb][idx] = fertCounters[fertProb][idx] / countersSum;

def computeDistFromAlignments(plText, enText, probs, bestAlignments):
    return 0;

def computeTransFromAlignments(plText, enText, probs, bestAlignments):
    return 0;

def computeProbsFromAlignments(plText, enText, probs, bestAlignments):
    computeFertFromAlignments(plText, enText, probs, bestAlignments);
    computeDistFromAlignments(plText, enText, probs, bestAlignments);
    computeTransFromAlignments(plText, enText, probs, bestAlignments);

plText = [["Ala", "ma", "kota", "i", "pieska", "tez"],
["Benek", "ma", "pieska", "i", "chomika", "tez"],]
enText = [["Ala", "has", "cat", "and", "dog", "as", "well"],
["Benek", "has", "dog", "and", "hamster", "as", "well"]];

probs = Probs(plText, enText);

plWords = ["Ala", "ma", "kota", "i", "pieska", "tez"];
enWords = ["Ala", "has", "cat", "and", "dog", "as", "well"];

algs = alignment.generateAlignments(plWords, enWords);


bestAlignments = {idx: [] for idx in range(0, len(plText))};

print(probs.fert);

computeAlignments(plText, enText, probs, bestAlignments);

computeProbsFromAlignments(plText, enText, probs, bestAlignments);

print(probs.fert);
# print(bestAlignments);


