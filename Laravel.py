import configparser
from PyQt5.QtWidgets    import (QPushButton, QHBoxLayout, QVBoxLayout, QApplication, QLabel, QGridLayout, QDialog)
from PyQt5              import QtWidgets, uic, QtCore, QtGui
from PyQt5.QtCore       import QSize, pyqtSignal, QObject
from PyQt5.QtGui        import QIcon
import json
import sys
import os
from os import listdir
from os.path import isdir, join, isfile
from pathlib import Path
import Parser
import Vocabulary
import GTranslate
from gui import GUI
from time import sleep

# Временная директория приложения
appTmpDir = os.path.expanduser('~') + '/.pyLaravelTranslate/'

# Читаем настройки из файла
settings_path = appTmpDir + 'settings.ini'

viewDirNameLaravel = 'views'
if os.path.exists(settings_path):
    settings = configparser.ConfigParser()
    settings.read(settings_path)
    langs = settings.get('GENERAL', 'LANGS').split('|')

vocabularyFileName = 'vocabulary'

def run(bladeDir, lang, progress_callback, **guiElements):

    checkVocabularyFileName = Vocabulary.checkFile(vocabularyFileName + '_' + lang)
    if (checkVocabularyFileName is None) :
        Vocabulary.writeJson(vocabularyFileName + '_' + lang, {})

    indexVocabulary = Vocabulary.loadJson(vocabularyFileName + '_' + lang)
    Vocabulary.indexLaraTranslate()

    for filename in Path(bladeDir).glob('**/*.blade.php'):
        bladeHtml       = Parser.getFileContent(filename)
        items           =  Parser.getFromHtml(bladeHtml)
        filterItems     = list(filter(Parser.filterValuesLaravel, items))

        # Количество переведенных элементов
        i = 0

        print('Текущий файл: ' + str(filename))

        # Передача в GUI
        current_file = filename
        current_file_total_item = len(filterItems)

        for item in filterItems:

            print('    Текущее слово: ' + item)

            indexLaraTranslate = Vocabulary.checkTranslateInFramework(filename, item, lang)

            # Если перевод присутствует в файле переводов фреймворка, используем его.
            # Также проверяем наличие его в словаре, если нет - добавляем (TODO)
            if (indexLaraTranslate is not None):
                itemIndex = indexLaraTranslate
            else :
                indexAppVocabulary = Vocabulary.checkIndex(indexVocabulary, item)
                if (indexAppVocabulary is not None):
                    itemIndex = indexAppVocabulary
                else :
                    gTranslateApiResult = GTranslate.getGTranslateApi(item, lang, langs)
                    if gTranslateApiResult is not None :
                        itemIndex = Vocabulary.saveFromGtranslateApi(gTranslateApiResult)
                        Vocabulary.indexVocabulary()
            if(itemIndex is not None) :
                bladeHtml = bladeHtml.replace(item, settings.get('LARAVEL', 'LEFT_LARAVEL_PLACEHOLDER') + str(itemIndex) + settings.get('LARAVEL', 'RIGHT_LARAVEL_PLACEHOLDER'))
            with open(filename, 'w') as file_handler:
                file_handler.write(bladeHtml)
            # Обновляем счетчик количества выполненных переводов
            i += 1

            progressData = {
                'current_file': current_file,
                'current_file_current_item': i,
                'current_file_total_item': current_file_total_item,
                'gui_elements': guiElements,
            }

            current_file = None
            current_file_total_item = None
            sleep(.100)
            progress_callback.emit(progressData)
