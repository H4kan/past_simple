class Hypothesis:
    def __init__(self, words, score, matching, textLength):
        self.words = words  # eg. [("he", "is"), ("hungry")]
        self.score = score  # pr(P) * pr(E | P)
        self.matching = matching  # eg. [(1), (3)]
        self.textLength = textLength  # eg. 6

    # needed for priority queue
    def __lt__(self, other):
        """self < obj."""
        return self.score > other.score
