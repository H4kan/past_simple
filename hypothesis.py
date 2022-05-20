class Hypothesis:
    def __init__(self, words, score, alignment, textLength):
        self.words = words  # eg. ["he", "is", "hungry"]
        self.score = score  # pr(P) * pr(E | P)
        self.alignment = alignment  # eg. [1, 2, 3]
        self.textLength = textLength  # eg. 6
    
    def __str__(self):
        return str(self.words) + " " + str(self.alignment) + " " + str(self.score)

    # needed for priority queue
    def __lt__(self, other):
        """self < obj."""
        return self.score > other.score
