from PyQt5.QtWidgets    import (QPushButton, QHBoxLayout, QVBoxLayout, QApplication, QLabel, QGridLayout, QDialog)
from PyQt5              import QtWidgets, uic, QtCore, QtGui
from PyQt5.QtCore       import QSize
from PyQt5.QtGui        import QIcon
import json
import sys
import os
from os import listdir
from os.path import isdir, join, isfile
from pathlib import Path
import Parser
import configparser
import re
import DB

# Читаем настройки из файла
settings_path = 'settings.ini'
viewDirNameLaravel = 'views'
vocabularyLaraName = 'vocabulary_lara'
if os.path.exists(settings_path):
    settings = configparser.ConfigParser()
    settings.read(settings_path)
    langs = settings.get('GENERAL', 'LANGS').split('|')

_ALLOWED_DIRS = {'backend', 'frontend', 'mails'}

# Получить содержимое файла json
def loadJson(vocabularyFileName):
    with open(vocabularyFileName + '.json', 'r') as inputData:
        return json.load(inputData)

# Проверка наличия слова в переводах приложения
# return key || None
def checkIndex(indexVocabulary, item):
    try :
        return indexVocabulary[item]
    except (KeyError):
        return None

# Проверка наличия слова в переводах фреймворка (resourses/lang/...)
# return key || None
def checkIndexLaraTranslate(bladeFilename, item, lang):
    # Файл переводов во фреймворке (Laravel) [backend, frontend, mails, ...]
    trFile = getTranslateFileName(bladeFilename, lang)
    if (trFile is not None) :
        # Содержимое json файла (для текущей локали) из переводов фреймворка [value => key]
        langJsonLara = loadJson(vocabularyLaraName + '_' + trFile + '_' + lang)
        try :
            indexLaraTr = langJsonLara[item]
        except (KeyError):
            indexLaraTr = None
        return indexLaraTr

################------------------------####################
#*****Получить имя файла перевода по пути файла шаблона****#
##############*****Внутренние соглашения*****###############
################------------------------####################
# return str - [backend, frontend, mails, ...]
def getTranslateFileName(bladeFilename, lang):
    splitPath = str(bladeFilename).split(viewDirNameLaravel)
    firstPartPath = splitPath[0]
    lastPartPath = splitPath[1]
    try :
        fName   = re.match(r'^\/.+\/', lastPartPath).group(0).replace('/', '')
    except(AttributeError):
        return None

    if (fName in _ALLOWED_DIRS) :
        fTrPath = firstPartPath + 'lang/' + DB.lang_field_connector(lang) + '/' + fName + '.php'
        return fName if isfile(fTrPath) else None

################------------------------####################
######*****Индексирование переводов Laravel*****############
################------------------------####################
def indexLaraTranslate() :
    langRoot = settings.get('LARAVEL', 'ROOT_DIR_LANG')
    data = {}
    for lang in langs:
        lang = DB.lang_field_connector(lang)
        data[lang] = {}
        for allowFile in _ALLOWED_DIRS :
            data[lang][allowFile] = {}
            file = langRoot + '/' + lang + '/' + allowFile + '.php'
            if isfile(file) :
                fContent = Parser.getFileContent(file)
                allInputs = re.findall(r'\'.+,', fContent)
                if (len(allInputs) > 0) :
                    for reItem in allInputs :
                        reItemSplit = reItem.split('=>')
                        key     = re.search(r'\'.+\'', reItemSplit[0]).group(0).replace("'", '')
                        value   = re.search(r'\'.+\'', reItemSplit[1]).group(0).replace("'", '')
                        data[lang][allowFile].update({value: key})
            writeJson(vocabularyLaraName + '_' + allowFile + '_' + lang, data[lang][allowFile])

################------------------------####################
#############*****Заппись json в файл*****##################
################------------------------####################
def writeJson(fileName, data):
    with open(fileName + '.json', 'w', encoding='utf8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)