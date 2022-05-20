from configparser import *
from probs import Probs
import algorithm


def read_configuration():
    Config = ConfigParser()
    Config.read("config.ini")

    enDataPath = Config.get('TranslationModule', 'EnData')
    plDataPath = Config.get('TranslationModule', 'PlData')

    return {
        "enDataPath": enDataPath,
        "plDataPath": plDataPath
    }


def get_data(configuration):
    enDataFile = open(configuration["enDataPath"], 'r', encoding="utf8")
    plDataFile = open(configuration["plDataPath"], 'r', encoding="utf8")

    enData = enDataFile.read().split('\n')
    plData = plDataFile.read().split('\n')

    enDataFile.close()
    plDataFile.close()

    if (len(enData) != len(plData)):
        raise Exception("EnData length is not equal to plData length.")

    enDataList = [item.split() for item in enData]
    plDataList = [item.split() for item in plData]

    return {
        "enData": enDataList,
        "plData": plDataList
    }


def run(data):
    plText = data["plData"]
    enText = data["enData"]
    probs = Probs(plText, enText)

    bestAlignments = {idx: [] for idx in range(0, len(plText))}

    maxSteps = 100

    prevBestProb = 0
    prevRatio = -1

    # this two functions need to be run in loop until some condition is met

    for i in range(0, maxSteps):

        algorithm.computeAlignments(plText, enText, probs, bestAlignments)

        algorithm.computeProbsFromAlignments(
            plText, enText, probs, bestAlignments)

    #     # convergence condition, not sure how to formulate it best way
        currBestProb = 0
        for idx in range(0, len(plText)):
            currBestProb = max(currBestProb, algorithm.sentProb(
                plText[idx], enText[idx], bestAlignments[idx], probs))

        if currBestProb > 0 and abs(prevBestProb / currBestProb - prevRatio) < 1e-5:
            break
        if (currBestProb == 0):
            break
        prevRatio = prevBestProb / currBestProb
        prevBestProb = currBestProb
    return probs


if __name__ == '__main__':
    configuration = read_configuration()
    data = get_data(configuration)
    probs = run(data)

    f = open("probs_rev.json", "w")
    f.write(probs.toJSON())
    f.close()
