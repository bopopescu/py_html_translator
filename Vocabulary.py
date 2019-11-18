from PyQt5.QtWidgets    import (QPushButton, QHBoxLayout, QVBoxLayout, QApplication, QLabel, QGridLayout, QDialog)
from PyQt5              import QtWidgets, uic, QtCore, QtGui
from PyQt5.QtCore       import QSize
from PyQt5.QtGui        import QIcon
import json
import sys
import os
from os.path import isdir, join, isfile
import Parser
import configparser
import re
import GTranslate
from gui import GUI

# Временная директория приложения
appTmpDir = os.path.expanduser('~') + '/.pyLaravelTranslate/'

# Читаем настройки из файла
settings_path = appTmpDir +'settings.ini'

viewDirNameLaravel = 'views'
vocabularyLaraName = 'vocabulary_lara'
vocabularyFileName = 'vocabulary'
if os.path.exists(settings_path):
    settings = configparser.ConfigParser()
    settings.read(settings_path)
    main_lang = settings.get('GENERAL', 'MAIN_LANG')
    langs = settings.get('GENERAL', 'LANGS').split('|')
    langs.insert(0, main_lang)

_ALLOWED_DIRS = {'backend', 'frontend', 'mails'}


def initTableHeader(headerLayout):
    # Шапка таблицы
    GUI.setTableHeader(langs, headerLayout)

################------------------------####################
#############**Создаем индексы переводов**##################
################------------------------####################
def indexVocabulary():
    initData = loadJson(vocabularyFileName)
    # Инициализация списков для дальнейшего наполнения
    data = {}
    for lang in langs:
        data[lang] = {}
    # Формируем необходимую структуру данных для записи в индексные файлы
    for key in initData :
        for lang in langs:
            try:
                data[lang].update({initData[key][lang]: key})
            except KeyError:
                continue
    # Пишем в файл json данные формата "значение : ключ" (с учетом локализации)
    for lng in data:
        writeJson(vocabularyFileName + '_' + lng, data[lng])

# Сохранить перевод из googleApi translate в локальное хранилище
# return key || None
def saveFromGtranslateApi (gTransApiRes) :
    vocabularyData =  loadJson(vocabularyFileName)
    try:
        key = makeKey(gTransApiRes['en'])
    except KeyError :
        langs = []
        langs.append('en')
        cyrValue = GTranslate.getGTranslateApi(gTransApiRes[main_lang], main_lang, langs)
        key = makeKey(cyrValue['en'])
    if vocabularyData is None:
        vocabularyData = {}
    vocabularyData[key] = gTransApiRes

    # Записываем в файл
    writeJson(vocabularyFileName, vocabularyData)
    return key

# Проверка наличия слова в переводах фреймворка (resourses/lang/...)
# return key || None
def checkTranslateInFramework(bladeFilename, item, lang):
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
    return None

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
        lang = lang_field_connector(lang)
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
    with open(appTmpDir + fileName + '.json', 'w', encoding='utf8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# Получить содержимое файла json
def loadJson(vocabularyFileName):
    with open(appTmpDir + vocabularyFileName + '.json', 'r') as inputData:
        try :
            return json.load(inputData)
        except :
            return None


# Проверка наличия слова в переводах приложения
# return key || None
def checkIndex(indexVocabulary, item):
    try :
        return indexVocabulary[item]
    except (KeyError):
        return None

# Генерация ключа из слова (удаляется все кроме букв и цифр)
# return key
def makeKey(input):
    # В нижний регистр
    inputToLower            = input.lower()
    # Удаляем весь мусор (кроме букв и цифр)
    clearBadCharsStr        = re.sub(r'[^A-Za-z0-9\s]', '', inputToLower)
    # Удаляем повторяющиеся пробелы
    clearRepeatSpacesStr    = re.sub(r'\s+', ' ', clearBadCharsStr).strip()
    # Заменяем пробелы на нижнее подчеркивание
    replSpaceToUnderscore   = clearRepeatSpacesStr.replace(' ', '_')
    return replSpaceToUnderscore

################------------------------####################
#############******Коррекция языков*******##################
################------------------------####################
def lang_field_connector(lang_str):
    langs_correct = {
        'uk': 'ua'
    }
    if (len(lang_str) > 0):
        if lang_str in langs_correct:
            return langs_correct[lang_str]
        else:
            return lang_str

################------------------------####################
#############****Инициализация словаря****##################
################------------------------####################
# def initVocabulary(self):
#     layout = QGridLayout()
#     initData = self.initDataVocabulary
#     widget = QWidget()
#     # Виджет в скролл области
#     self.scrollArea.setWidget(widget)
#     self.vocabularyLayout = QVBoxLayout(widget)
#
#     # Рендер переводов
#     for key in initData:
#         horizontal = GUI.setRow(self, self.langs, initData[key], key, self.vocabularyLayout)
#         # Установка обработчиков нажатия кнопок
#         for itemInRow in range(horizontal.itemAt(0).count()) :
#             widgetType = horizontal.itemAt(0).itemAt(itemInRow).widget().property('type')
#             if(widgetType == 'edit'):
#                 horizontal.itemAt(0).itemAt(itemInRow).widget().clicked.connect(self.editClick)
#             if (widgetType == 'delete'):
#                 horizontal.itemAt(0).itemAt(itemInRow).widget().clicked.connect(self.deleteClick)
#         self.vocabularyLayout.addLayout(horizontal)
#     # Устанавливаем основной (вертикальный шаблон) в окне приложения
#     self.vocabularyLayout.addStretch(1)