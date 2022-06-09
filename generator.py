from queue import PriorityQueue
from random import randint
from hypothesis import Hypothesis
from algorithm import *
from language import *
from decode_utils import *
import json

MAX_QUEUE_SIZE = 10
MAX_SINGLE_TRANSLATION = 5


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


def generate_new_hypothesis(curr_hypothesis, translation, indices, en, probs, langs):
    newWords = curr_hypothesis.words.copy()
    newWords.append(translation)

    newAlignment = curr_hypothesis.alignment.copy()
    newAlignment.append(indices)
    
    
    X = newWords
    Y = newAlignment

    newWordtoLang = [x for _,x in sorted(zip(Y,X))]

    # real score is calculated from equation: pr(P) * pr(E | P)
    al = generateAlignments(newWordtoLang, en)
    enSlice = en[0:len(newWords)]

    score = sentProb(newWords, enSlice, al, probs)     * \
        sentLangProb(newWordtoLang, langs)**0.5

    return Hypothesis(newWords, score, newAlignment, curr_hypothesis.textLength)


def apply_translation_options(curr_hypothesis, index, priority_queues, priority_queue_index, en, translation_options, probs, langs):
    phrase = en[index]
    if phrase not in translation_options:
        return

    for translation in translation_options[phrase]:
        new_hypothesis = generate_new_hypothesis(
            curr_hypothesis, translation, index, en, probs, langs)
        
        # if (new_hypothesis.score == 1):
        #     continue

        if priority_queue_index + 1 >= len(priority_queues):
            return
     

        currentQueue = priority_queues[priority_queue_index + 1]
        
        # if (priority_queue_index == 2):
        #     for h in currentQueue.queue:
        #         print(str(h))
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


def process_priority_queue(priority_queues, priority_queue_index, en, translation_options, probs, langs):
    # foreach hypothesis on priority queue
    while not priority_queues[priority_queue_index].empty():
        # print("Priority queue index: " + str(priority_queue_index))
        # print("Size: " + str(priority_queues[priority_queue_index].qsize()))
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
                    curr_hypothesis, next_index, priority_queues, priority_queue_index, en, translation_options, probs, langs)


def generate_translation_options(probs_rev):
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
    # Example sentence in English
    en = ["climate", "change", "are", "dangerous","\x00" ]
    enLength = len(en) - 1

    # Put empty hypothesis with score = 0
    priority_queues = initialize_priority_queues(enLength, MAX_QUEUE_SIZE)
    priority_queues[0].put(Hypothesis([], 0, [], enLength))

    for i in range(0, len(priority_queues) - 1):
        process_priority_queue(priority_queues, i)

    result = priority_queues[enLength].get()
    
    X = result.words
    Y = result.alignment

    res = [x for _,x in sorted(zip(Y,X))]

    print(res)
    print(result.score)

    
def fun(probs, probs_rev, langs, en, translation_options):
    enLength = len(en) - 1

    # Put empty hypothesis with score = 0
    priority_queues = initialize_priority_queues(enLength, MAX_QUEUE_SIZE)
    priority_queues[0].put(Hypothesis([], 0, [], enLength))

    for i in range(0, len(priority_queues) - 1):
        process_priority_queue(priority_queues, i, en, translation_options, probs, langs)

    result = priority_queues[enLength].get()
    
    X = result.words
    Y = result.alignment

    res = [x for _,x in sorted(zip(Y,X))]

    return res
