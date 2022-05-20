import math
from collections import Counter
import alignment
import constraints
from utils import *
from probs import Probs

# this calculates sentence probability based on current probs


def sentProb(plSent, enSent, alignment, probs):
    res = 1
    for i in range(0, len(plSent)):
        n_i = len(alignment[i + 1])
        res *= probs.fert[plSent[i]][n_i]
        if (n_i > 0):
            for j in range(0, n_i):
                if (enSent[alignment[i + 1][j]] in probs.trans[plSent[i]]):
                    res *= probs.trans[plSent[i]][enSent[alignment[i + 1][j]]]
                else:
                    res *= 1
                if (alignment[i + 1][j] in probs.dist[str(len(enSent))]):
                    res *= probs.dist[len(enSent)][alignment[i + 1][j]][i]
                else:
                    res *= 1
        else:
            res *= probs.trans[plSent[i]]["\0"]
    res *= probs.fert["\0"][len(alignment[0])]
    for i in range(0, len(alignment[0])):
        res *= probs.trans["\0"][enSent[alignment[0][i]]]

    return res


def getBestAlignment(plSent, enSent, probs):

    algs = alignment.generateAlignments(plSent, enSent)
    maxProb = 0
    currProb = 0
    maxIdx = -1

    for idx, alg in enumerate(algs):

        currProb = sentProb(plSent, enSent, alg, probs)
        if (currProb > maxProb):
            maxProb = currProb
            maxIdx = idx

    return algs[maxIdx]


def computeAlignments(plText, enText, probs, bestAlignments):
    for idx, plSent in enumerate(plText):
        bestAlignments[idx] = getBestAlignment(plSent, enText[idx], probs)


def computeFertFromAlignments(plText, enText, probs, bestAlignments):

    fertCounters = {w: [0, 0, 0, 0, 0, 0] for w in (probs.allPlWords + ["\0"])}
    for idx, plSent in enumerate(plText):
        for wordIdx, plWord in enumerate(plSent):
            fertCounters[plWord][len(bestAlignments[idx][wordIdx + 1])] += 1
        fertCounters["\0"][len(bestAlignments[idx][0])] += 1

    for idx, word in enumerate(probs.fert):
        countersSum = sum(fertCounters[word])
        for i in range(0, len(probs.fert[word])):
            probs.fert[word][i] = fertCounters[word][i] / countersSum


def computeDistFromAlignments(plText, enText, probs, bestAlignments):

    distCounter = {sentLen: {enIdx: {plIdx: 0 for plIdx in range(0, constraints.MAX_PL_LEN)} for enIdx in range(
        0, sentLen)} for sentLen in range(1, constraints.MAX_EN_LEN + 1)}
    generalCounter = {sentLen: {enIdx: 0 for enIdx in range(
        0, sentLen)} for sentLen in range(1, constraints.MAX_EN_LEN + 1)}

    for idx, plSent in enumerate(plText):
        for wordIdx, plWord in enumerate(plSent):
            if len(bestAlignments[idx][wordIdx + 1]) > 0:
                for enIdx in bestAlignments[idx][wordIdx + 1]:
                    distCounter[len(enText[idx])][enIdx][wordIdx] += 1
                    generalCounter[len(enText[idx])][enIdx] += 1

    for sentLen in range(1, constraints.MAX_EN_LEN + 1):
        for enIdx in range(0, sentLen):
            for plIdx in range(0, constraints.MAX_PL_LEN):
                if generalCounter[sentLen][enIdx] > 0:
                    probs.dist[sentLen][enIdx][plIdx] = distCounter[sentLen][enIdx][plIdx] / \
                        generalCounter[sentLen][enIdx]
                else:
                    probs.dist[sentLen][enIdx][plIdx] = 0


def computeTransFromAlignments(plText, enText, probs, bestAlignments):

    transCounter = {pl: {en: 0 for en in (
        probs.allEnWords + ["\0"])} for pl in (probs.allPlWords + ["\0"])}
    generalCounter = {pl: 0 for pl in (probs.allPlWords + ["\0"])}

    for idx, plSent in enumerate(plText):
        for wordIdx, plWord in enumerate(["\0"] + plSent):
            if len(bestAlignments[idx][wordIdx]) == 0:
                transCounter[plWord]["\0"] += 1
                generalCounter[plWord] += 1
            else:
                for enIdx in bestAlignments[idx][wordIdx]:
                    transCounter[plWord][enText[idx][enIdx]] += 1
                    generalCounter[plWord] += 1

    for plWord in (probs.allPlWords + ["\0"]):
        for enWord in (probs.allEnWords + ["\0"]):
            probs.trans[plWord][enWord] = transCounter[plWord][enWord] / \
                generalCounter[plWord]


def computeProbsFromAlignments(plText, enText, probs, bestAlignments):
    computeFertFromAlignments(plText, enText, probs, bestAlignments)
    computeDistFromAlignments(plText, enText, probs, bestAlignments)
    computeTransFromAlignments(plText, enText, probs, bestAlignments)
