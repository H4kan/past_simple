import configparser
import language


def read_configuration():
    Config = configparser.ConfigParser()

    Config.read("past_simple/config.ini")

    plLangDataPath = Config.get('LanguageModule', 'PlLangData')

    return {
        "plLangDataPath": plLangDataPath
    }


def get_lang_data(configuration):
    plLangDataFile = open(
        configuration["plLangDataPath"], 'r', encoding="utf8")

    plLangData = plLangDataFile.read().split('\n')

    plLangDataFile.close()

    plLangDataList = [item.split() for item in plLangData]

    return {
        "plLangData": plLangDataList
    }


def runlang(data):
    return language.Lang(data["plLangData"])


if __name__ == '__main__':
    configuration = read_configuration()
    data = get_lang_data(configuration)

    lang = runlang(data)

    f = open("lang.json", "w")
    f.write(lang.toJSON())
    f.close()
