
import numpy as np;
import constraints;
from utils import flatten, unique;


class Probs:

    def __init__(self, plText, enText):

        self.allPlWords = unique(flatten(plText));
        self.allEnWords = unique(flatten(enText));

        self.fert = {w: constraints.baseFert for w in (self.allPlWords + ["\0"])};

        self.dist = {sentLen: {frIdx: {plIdx: 1 / sentLen for plIdx in range(0, constraints.MAX_PL_LEN)} for frIdx in range(0, sentLen)} for sentLen in range(1, constraints.MAX_EN_LEN + 1)}
                
        self.trans = {pl: {en: 0 for en in self.allEnWords} for pl in self.allPlWords};

        for enSentIdx, enSent in enumerate(enText):
            for enWord in enSent:
                ratio = 1 / len(flatten(plText));
                for plWord in plText[enSentIdx]:
                    self.trans[plWord][enWord] += ratio;