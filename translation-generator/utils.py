import queue


def initialize_priority_queues(sentenceLength):
    priority_queues = []
    for i in range(0, sentenceLength + 1):
        priority_queues.append(queue.PriorityQueue())
    return priority_queues


def phrase_lower(phrase):
    return tuple([item.lower() for item in phrase])
