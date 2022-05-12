
import numpy as np;
import constraints;
from utils import flatten, unique;


class Probs:

    def __init__(self, plText, enText):

        self.allPlWords = unique(flatten(plText));
        self.allEnWords = unique(flatten(enText));

        self.fert = {w: constraints.baseFert for w in (self.allPlWords + ["\0"])};
        self.fert["\0"] = constraints.baseNullFert;

        self.dist = {sentLen: {enIdx: {plIdx: 1 / sentLen for plIdx in range(0, constraints.MAX_PL_LEN)} for enIdx in range(0, sentLen)} for sentLen in range(1, constraints.MAX_EN_LEN + 1)}
                
        self.trans = {pl: {en: 0 for en in (self.allEnWords + ["\0"])} for pl in (self.allPlWords + ["\0"])};


        ratio = 1 / (len(flatten(plText)) + len(plText));
        for enSentIdx, enSent in enumerate(enText):
            for enWord in enSent:
                for plWord in plText[enSentIdx]:
                    self.trans[plWord][enWord] += ratio;
                self.trans["\0"][enWord] += ratio;
            for plWord in plText[enSentIdx]:
                self.trans[plWord]["\0"] += ratio;