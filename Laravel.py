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
from Parser import Parser
from Vocabulary import Vocabulary


class Laravel () :
    # Список файлов (шаблоны blage)
    bladeFiles = []

    def run(bladeDir, lang):

        indexVocabulary = Vocabulary.loadIndexFile(lang, vocabularyFileName = 'vocabulary')

        for filename in Path(bladeDir).glob('**/*.blade.php'):
            # bladeHtml       = ''
            bladeHtml       = Parser.getFileContent(filename)
            items           =  Parser.getFromHtml(bladeHtml)
            filterItems     = list(filter(Parser.filterValuesLaravel, items))
            for item in filterItems:
                index = Vocabulary.checkIndex(indexVocabulary, item)
                if(index) :
                    bladeHtml = bladeHtml.replace(item, "@lang('" + str(index) + "')")
            with open(filename, 'w') as file_handler:
                file_handler.write(bladeHtml)
            sys.exit(0)
    # chunks = filter(self.filter_values, chunks)
    # for v in chunks:
    #     print(v)
    # sys.exit(0)
