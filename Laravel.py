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
import Vocabulary
import configparser

# Читаем настройки из файла
settings_path = 'settings.ini'
viewDirNameLaravel = 'views'
if os.path.exists(settings_path):
    settings = configparser.ConfigParser()
    settings.read(settings_path)

vocabularyFileName = 'vocabulary'

def run(bladeDir, lang):

    indexVocabulary = Vocabulary.loadJson(vocabularyFileName + '_' + lang)
    Vocabulary.indexLaraTranslate()
    initDataVocabulary = Vocabulary.loadJson(vocabularyFileName)

    for filename in Path(bladeDir).glob('**/*.blade.php'):
        # bladeHtml       = ''
        bladeHtml       = Parser.getFileContent(filename)
        items           =  Parser.getFromHtml(bladeHtml)
        filterItems     = list(filter(Parser.filterValuesLaravel, items))
        for item in filterItems:
            indexLaraTranslate = Vocabulary.checkIndexLaraTranslate(filename, item, lang)
            # Если перевод присутствует в файле переводов фреймворка, используем его.
            # Также проверяем наличие его в словаре, если нет - добавляем (TODO)
            if (indexLaraTranslate is not None):
                itemIndex = indexLaraTranslate
            else :
                # if (indexLaraTranslate in initDataVocabulary):
                #     sys.exit(0)
                # else :
                indexAppVocabulary = Vocabulary.checkIndex(indexVocabulary, item)
                itemIndex = indexAppVocabulary

            if(itemIndex is not None) :
                bladeHtml = bladeHtml.replace(item, settings.get('LARAVEL', 'LEFT_LARAVEL_PLACEHOLDER') + str(itemIndex) + settings.get('LARAVEL', 'RIGHT_LARAVEL_PLACEHOLDER'))
        with open(filename, 'w') as file_handler:
            file_handler.write(bladeHtml)
        print(filename)
        sys.exit(0)
# chunks = filter(self.filter_values, chunks)
# for v in chunks:
#     print(v)
# sys.exit(0)
