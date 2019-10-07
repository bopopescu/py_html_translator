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


class Vocabulary () :

    def loadIndexFile(lang, vocabularyFileName):
        with open(vocabularyFileName + '_' + lang + '.json', 'r') as inputData:
            return json.load(inputData)

    def checkIndex(indexVocabulary, item):
        try :
            return indexVocabulary[item]
        except (KeyError):
            return False