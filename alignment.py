import itertools
import constraints;
from utils import *;

# jeszcze k ciagow, jestesmy na p tym znaku w wejsciowym
def recurSeqPartial(lst, n, k, p, res, currSerie):
    if k == 1:
        if isAscending(lst[p:n]) and p + constraints.MAX_GEN_WORD >= n:
            res.append(currSerie + [n]);
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
    res = []
 
    res += [[]]
    
    for i in range(len(plSent)):
        a = []
        if (i < len(enSent)):
            a.append([i])
            res += a
        else:
            res += [[]]
        

 
    
    return [ res ]
    i = 0
    for permutation in itertools.permutations(list(range(0, len(enSent)))):
        # if i == 2:
        #     print(alignments)
        
        alignments += generateSeqPartial(list(permutation), len(plSent) + 1);
        # i += 1
        
  
    return alignments;


# lst = [1, 2, 3, 4, 5];

# print(generateSeqPartial(lst, 5));


# plWords = ["Ala", "ma", "kota", "i", "pieska", "tez"];
# enWords = ["Ala", "has", "cat", "and", "dog", "as", "well"];

# algs = generateAlignments(enWords, plWords);

# print(algs[0]);

