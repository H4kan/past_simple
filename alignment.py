import itertools
import constraints;
from utils import *;

# jeszcze k ciagow, jestesmy na p tym znaku w wejsciowym
def recurSeqPartial(lst, n, k, p, res, currSerie):
    # if len(currSerie) > 0 and (
    #     (currSerie[len(currSerie) - 1] > 0 and lst[currSerie[len(currSerie) - 1] - 1] > len(currSerie) + 1 + constraints.MAX_SHIFT_PROD) or 
    #     (len(currSerie) > 1 and currSerie[len(currSerie) - 2] < len(lst) and lst[currSerie[len(currSerie) - 2]] < len(currSerie) - 2 - constraints.MAX_SHIFT_PROD)):
    #     return;
    if k == 1:
        currSerie = currSerie + [n];
        if isAscending(lst[p:n]) and p + constraints.MAX_GEN_WORD >= n:
            res.append(currSerie);
        return;
    recurSeqPartial(lst, n, k - 1, p, res, currSerie + [p]);
    if p < n:
        recurSeqPartial(lst, n, k - 1, p + 1, res, currSerie + [p + 1]);
    for ln in range(p + 2, min(p + constraints.MAX_GEN_WORD, n) + 1):
        if lst[ln-1] > lst[ln-2]:
            recurSeqPartial(lst, n, k - 1, ln, res, currSerie + [ln]);
        else: 
            break;

def generateSeqPartial(lst, n):
    resSeqPartial = [];
    recurSeqPartial(lst, len(lst), n, 0, resSeqPartial, []);
    res = [];
    for partition in resSeqPartial:
        actualRes = [];
        prevPos = 0;
        for position in partition:
            actualRes += [lst[prevPos:position]];
            prevPos = position;
        res += [actualRes];
    return res;

def generateAlignments(plSent, enSent):
        
    alignments = [];

    for permutation in itertools.permutations(list(range(0, len(enSent)))):
        l = list(permutation);
        cond = True;
        for i in range(0, len(enSent)):
            if abs(i - l[i]) > constraints.MAX_SHIFT_PROD:
                cond = False;
                break;
        if cond:        
            alignments += generateSeqPartial(l, len(plSent) + 1);    
  
    return alignments;


# lst = [1, 2, 3, 4, 5];

# print(generateSeqPartial(lst, 5));


# plWords = ["Ala", "ma", "kota", "i", "pieska", "tez"];
# enWords = ["Ala", "has", "cat", "and", "dog", "as", "well"];

# algs = generateAlignments(enWords, plWords);

# for i in algs:
#     # if i[0] == 0 and i[1] == 1:
#     print(i)
# print(algs);
# print(algs[0]);
# print(algs[len(algs) - 1]);
# print(algs);
# print(len(algs));

