from utils import flatten
from collections import defaultdict

BIGRAM_VAL = 0.3


class Lang:

    def __init__(self, text):
        self.singles = defaultdict()
        self.doubles = defaultdict(dict)
        self.singCount = 0
        for sentence in text:
            paddedSentence = [None] + sentence
            for idx, word in enumerate(paddedSentence):
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


def wordLangProb(word, lang: Lang):
    if(word in lang.singles):
        return lang.singles[word]/lang.singCount
    else:
        return 1/lang.singCount


def pairLangProb(w1, w2, lang: Lang):
    if(w1 in lang.doubles):
        if(w2 in lang.doubles[w1]):
            return lang.doubles[w1][w2] / (lang.singles[w1])
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


plText = [["Ala", "ma", "kota", "i", "pieska", "tez"],
          ["Benek", "ma", "pieska", "i", "chomika", "tez"], ]

plWords = ["Ala", "ma", "kota"]

lang = Lang(plText)
print(lang.singles)
print(lang.doubles)
print(sentLangProb(plWords, lang))
print(sentLangProb(["pi", "Ala"], lang))
