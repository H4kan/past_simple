from numpy import double
from utils import flatten
from collections import defaultdict
import json
from progressBar import printProgressBar

BIGRAM_VAL = 0.3


class Lang:

    def __init__(self, text):
        self.singles = defaultdict(dict)
        self.doubles = defaultdict(dict)
        self.singCount = 0
        self.addBatch(text)

    def addBatch(self, text):
        for idx, sentence in enumerate(text):
            printProgressBar(idx, len(text), "Training: ")
            paddedSentence = [None] + sentence
            for idx, word in enumerate(paddedSentence):
                if(word != None):
                    if(word in self.singles):
                        self.singles[word] += 1
                    else:
                        self.singles[word] = 1
                    self.singCount += 1

                if(idx > 0):
                    if(paddedSentence[idx-1] in self.doubles and word in self.doubles[paddedSentence[idx-1]]):
                        self.doubles[paddedSentence[idx-1]][word] += 1
                    else:
                        self.doubles[paddedSentence[idx-1]][word] = 1
        printProgressBar(len(text), len(text), "Training: ")

    def toJSON(self):
        return json.dumps(self.__dict__)


def langFromJson(jsonLoads):
    lang = Lang([])
    lang.singles = jsonLoads['singles']
    lang.doubles = jsonLoads['doubles']
    lang.singCount = jsonLoads['singCount']
    return lang


def wordLangProb(word, lang: Lang):
    if(word in lang.singles):
        return lang.singles[word]/lang.singCount
    else:
        return 1/lang.singCount


def pairLangProb(w1, w2, lang: Lang):
    if(w1 in lang.doubles):
        if(w2 in lang.doubles[w1]):
            return lang.doubles[w1][w2] / (sum(lang.doubles[w1].values(), 0))
        else:
            return 1/lang.singles[w1]
    else:
        return 1/lang.singCount


def sentLangProb(sentence, lang: Lang):
    prob = 1
    for idx, word in enumerate(sentence):
        if(idx > 0):
            prob *= (BIGRAM_VAL * pairLangProb(sentence[idx-1], word, lang) + (
                1-BIGRAM_VAL) * wordLangProb(word, lang))
        else:
            prob *= (BIGRAM_VAL * pairLangProb(None, word, lang) + (
                1-BIGRAM_VAL) * wordLangProb(word, lang))
    return prob


if __name__ == "__main__":
    # plText = [["Ala", "ma", "kota", "i", "pieska", "tez"],
    #           ["Benek", "ma", "pieska", "i", "chomika", "tez"], ]

    # plWords = ["Ala", "ma", "kota"]

    # lang = Lang(plText)
    # sentLangProb(plWords, lang)
    # y = lang.toJson()
    f = open("lang.json", "r")
    w = langFromJson(json.load(f))
    # print(w)
