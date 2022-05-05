import configparser


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

    enDataList = [item.split() for item in enData]
    plDataList = [item.split() for item in plData]

    return {
        "enData": enDataList,
        "plData": plDataList
    }


if __name__ == '__main__':
    configuration = read_configuration()

    data = get_data(configuration)
