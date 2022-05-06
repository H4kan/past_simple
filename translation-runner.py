import configparser
import translation


def read_configuration():
    Config = configparser.ConfigParser()
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
    probs = translation.Probs(plText, enText)

    bestAlignments = {idx: [] for idx in range(0, len(plText))}

    translation.computeAlignments(plText, enText, probs, bestAlignments)

    translation.computeProbsFromAlignments(
        plText, enText, probs, bestAlignments)


if __name__ == '__main__':
    configuration = read_configuration()
    data = get_data(configuration)
    run(data)
