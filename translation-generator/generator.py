"""
TODO:
    [] recombination
    [] queues pruning
"""


from random import randint
from hypothesis import Hypothesis
from utils import initialize_priority_queues, phrase_lower


# Available translations to English taken from translation module
translation_options = {
    ("er",): [("he",), ("it",)],
    ("geht",): [("is",), ("are",), ("goes",), ("go",)],
    ("ja",): [("yes",), ("is",)],
    ("nicht",): [("not",), ("do", "not"), ("does", "not"), ("is", "not")],
    ("nach",): [("after",), ("to",), ("in",)],
    ("hause",): [("house",), ("home",)],
    ("er", "geht"): [("it", "is")],
    ("ja", "nicht"): [("does", "not"), ("is", "not")],
    ("nach", "house"): [("home",)],
    ("geht", "ja", "nicht"): [("is", "not")]
}


def generate_new_hypothesis(curr_hypothesis, translation, indices):
    newWords = curr_hypothesis.words.copy()
    newWords.append(translation)

    newMatching = curr_hypothesis.matching.copy()
    newMatching.append(indices)

    # real score is calculated from equation: pr(P) * pr(E | P)
    score = randint(0, 420)

    return Hypothesis(newWords, score, newMatching, curr_hypothesis.textLength)


def apply_translation_options(curr_hypothesis, indices, priority_queues, priority_queue_index):
    phrase = phrase_lower([de[x] for x in indices])

    if phrase not in translation_options:
        return

    for translation in translation_options[phrase]:
        new_hypothesis = generate_new_hypothesis(
            curr_hypothesis, translation, indices)

        if priority_queue_index + len(indices) >= len(priority_queues):
            return

        priority_queues[priority_queue_index +
                        len(indices)].put(new_hypothesis)


def process_priority_queue(priority_queues, priority_queue_index):
    # foreach hypothesis on priority queue
    while not priority_queues[priority_queue_index].empty():
        print("Priority queue index: " + str(priority_queue_index))
        print("Size: " + str(priority_queues[priority_queue_index].qsize()))
        curr_hypothesis = priority_queues[priority_queue_index].get()

        indices = []  # all translated indices
        for match in curr_hypothesis.matching:
            indices += [item for item in match]
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
            if i not in indices and counter < 3:
                counter += 1
                # pojedyncze slowa
                next_index = (i,)
                apply_translation_options(
                    curr_hypothesis, next_index, priority_queues, priority_queue_index)

                # podwojne wyrazenia
                for k in range(0, 2):
                    if (i + k + 1 < curr_hypothesis.textLength) and (not i + k in indices) and (not i + k + 1 in indices):
                        next_index = (i + k, i + k + 1)
                        apply_translation_options(
                            curr_hypothesis, next_index, priority_queues, priority_queue_index)


if __name__ == '__main__':
    # Example sentence in German
    de = ["er", "geht"]  # , "ja", "nicht", "nach", "hause"]
    deLength = len(de)

    priority_queues = initialize_priority_queues(deLength)

    # Put empty hypothesis with score = 0
    priority_queues[0].put(Hypothesis([], 0, [], deLength))

    for i in range(0, len(priority_queues) - 1):
        process_priority_queue(priority_queues, i)

    result = priority_queues[deLength].get()
    print(result.words)
    print(result.score)
    print(result.matching)
