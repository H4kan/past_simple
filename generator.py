from queue import PriorityQueue
from random import randint
from hypothesis import Hypothesis
from algorithm import *
from language import *
from decode_utils import *
import json

MAX_QUEUE_SIZE = 3
MAX_SINGLE_TRANSLATION = 3


# Available translations to English taken from translation module
# translation_options = {
#     "er": ["he", "it"],
#     "geht": ["is", "are", "goes", "go"],
#     "ja": ["yes", "is"],
#     "nicht": ["not", "not"],
#     "nach": ["after", "to", "in"],
#     "hause": ["house", "home"],
# }

# polish_words = []
def generateAlignments(plSent, enSent):
    res = []
    res += [[]]
    for i in range(len(plSent)):
        a = []
        if (i < len(enSent)):
            a.append([i])
            res += a
        else:
            res += [[]]
    return res


def generate_new_hypothesis(curr_hypothesis, translation, indices):
    newWords = curr_hypothesis.words.copy()
    newWords.append(translation)

    newAlignment = curr_hypothesis.alignment.copy()
    newAlignment.append(indices)

    # real score is calculated from equation: pr(P) * pr(E | P)
    al = generateAlignments(newWords, en)
    enSlice = en[0:len(newWords)]

    score = sentProb(newWords, enSlice, al, probs) * \
        sentLangProb(newWords, langs)
    if (newWords[0] == "jestem"):
        print("")
    return Hypothesis(newWords, score, newAlignment, curr_hypothesis.textLength)


def apply_translation_options(curr_hypothesis, index, priority_queues, priority_queue_index):
    phrase = en[index]
    if phrase not in translation_options:
        return

    for translation in translation_options[phrase]:
        new_hypothesis = generate_new_hypothesis(
            curr_hypothesis, translation, index)

        if priority_queue_index + 1 >= len(priority_queues):
            return
        if priority_queue_index == 2:
            print("")

        currentQueue = priority_queues[priority_queue_index + 1]

        currentQueue.put(new_hypothesis)

        # recombine
        elements = queue_to_array(currentQueue)
        removedIndices = []
        for i in range(len(elements)):
            for j in range(len(elements)):
                if (i != j and hypothesis_equals(elements[i], elements[j])):
                    if elements[i].score < elements[j].score:
                        removedIndices.append(i)
                    else:
                        removedIndices.append(j)

        for i in removedIndices:
            elements.remove(elements[i])  # remove with worse score

        if len(elements) == MAX_QUEUE_SIZE:
            # find worst h
            elements.remove(max(elements))

        for e in elements:
            currentQueue.put(e)


def process_priority_queue(priority_queues, priority_queue_index):
    # foreach hypothesis on priority queue
    while not priority_queues[priority_queue_index].empty():
        print("Priority queue index: " + str(priority_queue_index))
        print("Size: " + str(priority_queues[priority_queue_index].qsize()))
        curr_hypothesis = priority_queues[priority_queue_index].get()

        indices = curr_hypothesis.alignment  # all translated indices

        indices.sort()

        # Aktualna hipoteza: *____
        # znajdujemy pierwszy wolny index
        # iterujemy po kolejnych indeksach
        # np. *_*__
        # dopasowujemy do niego translation options i wrzucamy na stack

        # Potem iterujemy po kolejnych dwojkach
        # np. ***__, *_**_
        # dopasowujemy translation options skladajace sie z dwoch wyrazow
        counter = 0
        for i in range(0, curr_hypothesis.textLength):
            if i not in indices:
                next_index = i
                apply_translation_options(
                    curr_hypothesis, next_index, priority_queues, priority_queue_index)


def generate_translation_options():
    # TODO: zmienic strukture maxP i bestTrans
    d = {}
    for key, value in probs_rev.trans.items():
        if (len(value) > MAX_SINGLE_TRANSLATION):
            maxP = []
            bestTrans = []
            for key2, value2 in value.items():
                if key2 == '\x00':
                    continue
                if len(maxP) < MAX_SINGLE_TRANSLATION:
                    maxP.append(value2)
                    bestTrans.append(key2)
                elif value2 > min(maxP):
                    i = maxP.index(min(maxP))
                    maxP.pop(i)
                    bestTrans.pop(i)
                    maxP.append(value2)
                    bestTrans.append(key2)
            d[key] = dict(zip(bestTrans, maxP))
        else:
            d[key] = value
    return d


if __name__ == '__main__':
    with open('probs_rev.json') as json_file:
        probs_revJSON = json.load(json_file)

    with open('probs.json') as json_file:
        probsJSON = json.load(json_file)

    with open('lang.json') as json_file:
        langsJSON = json.load(json_file)

    langs = langFromJson(langsJSON)

    probs_rev = Probs(None, None,
                      probs_revJSON["allPlWords"],
                      probs_revJSON["allEnWords"],
                      probs_revJSON["fert"],
                      probs_revJSON["dist"],
                      probs_revJSON["trans"])
    probs = Probs(None, None,
                  probsJSON["allPlWords"],
                  probsJSON["allEnWords"],
                  probsJSON["fert"],
                  probsJSON["dist"],
                  probsJSON["trans"])
    translation_options = generate_translation_options()
    # Example sentence in German
    en = ["he", "very", "good", "\x00"]
    enLength = len(en) - 1

    # Put empty hypothesis with score = 0
    priority_queues = initialize_priority_queues(enLength, MAX_QUEUE_SIZE)
    priority_queues[0].put(Hypothesis([], 0, [], enLength))

    for i in range(0, len(priority_queues) - 1):
        process_priority_queue(priority_queues, i)

    result = priority_queues[enLength].get()

    print(result.words)
    print(result.score)
    print(result.alignment)
