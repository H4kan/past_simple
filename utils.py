import numpy as np;


def isAscending(lst):
    if len(lst) == 0:
        return True;
    previous = lst[0]
    for number in lst:
        if number < previous:
            return False;
        previous = number
    return True;


def flatten(t):
    return [item for sublist in t for item in sublist];

def unique(list):
    x = np.array(list)
    return np.unique(x).tolist();


