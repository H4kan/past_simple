import queue


def initialize_priority_queues(sentenceLength, maxSize):
    priority_queues = []
    for i in range(0, sentenceLength + 1):
        priority_queues.append(queue.PriorityQueue(maxSize))
    return priority_queues


def phrase_lower(phrase):
    return tuple([item.lower() for item in phrase])


def queue_to_array(priorityQueue):
    res = []
    while not priorityQueue.empty():
        temp = priorityQueue.get()
        res.append(temp)
    return res


def hypothesis_equals(h1, h2):
    return h1.words == h2.words and h1.alignment == h2.alignment
