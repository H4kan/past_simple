from queue import PriorityQueue
from random import randint
from hypothesis import Hypothesis
from utils import *

MAX_SIZE = 3

# Available translations to English taken from translation module
translation_options = {
    "er": ["he", "it"],
    "geht": ["is", "are", "goes", "go"],
    "ja": ["yes", "is"],
    "nicht": ["not", "not"],
    "nach": ["after", "to", "in"],
    "hause": ["house", "home"],
}

polish_words = []


def getProb(polish_word, english_word):
    return 0.5


def get_best_single_translations(eng):
    bestProbs = []
    for word in polish_words:
        min_best_probs = min(bestProbs)
        new_prob = getProb(word, eng)
        if new_prob > min_best_probs:
            bestProbs.remove(min_best_probs)
            bestProbs.append(new_prob)
    return bestProbs


def generate_new_hypothesis(curr_hypothesis, translation, indices):
    newWords = curr_hypothesis.words.copy()
    newWords.append(translation)

    newAlignment = curr_hypothesis.alignment.copy()
    newAlignment.append(indices)

    # real score is calculated from equation: pr(P) * pr(E | P)
    score = randint(0, 420)

    return Hypothesis(newWords, score, newAlignment, curr_hypothesis.textLength)


def apply_translation_options(curr_hypothesis, index, priority_queues, priority_queue_index):
    phrase = de[index]
    if phrase not in translation_options:
        return

    for translation in translation_options[phrase]:
        new_hypothesis = generate_new_hypothesis(
            curr_hypothesis, translation, index)

        if priority_queue_index + 1 >= len(priority_queues):
            return

        currentQueue = priority_queues[priority_queue_index + 1]

        currentQueue.put(new_hypothesis)

        # recombine
        elements = queue_to_array(currentQueue)
        removedIndices = []
        for i in range(len(elements)):
            for j in range(len(elements)):
                if (i != j and hypothesis_equals(elements[i], elements[j])):
                    if elements[i].score > elements[j].score:
                        removedIndices.append(i)
                    else:
                        removedIndices.append(j)

        for i in removedIndices:
            elements.remove(elements[i])  # remove with worse score

        if len(elements) == MAX_SIZE:
            # find worst h
            elements.remove(min(elements))

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


if __name__ == '__main__':
    # Example sentence in German
    de = ["er", "geht", "ja", "nicht", "nach", "hause"]
    deLength = len(de)

    # Put empty hypothesis with score = 0
    priority_queues = initialize_priority_queues(deLength, MAX_SIZE)
    priority_queues[0].put(Hypothesis([], 0, [], deLength))

    for i in range(0, len(priority_queues) - 1):
        process_priority_queue(priority_queues, i)

    result = priority_queues[deLength].get()

    print(result.words)
    print(result.score)
    print(result.alignment)
