import configparser
from PyQt5 import QtWidgets, uic, QtCore
import sys
import start_activity
import index
import os
from subprocess         import check_output
from bs4 import BeautifulSoup
from mysql.connector    import MySQLConnection, Error
import DB
import json
from time               import sleep
from googletrans        import Translator
import codecs
import subprocess
import re

class StartWindow(QtWidgets.QMainWindow, start_activity.Ui_MainWindow):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле html.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна

        # Обработчики нажатия кнопок
        self.select_proect.clicked.connect(self.click_select_proect)

    #Выбор типа проекта
    def click_select_proect(self):
        laravel     = self.laravel.isChecked()
        modx        = self.modx.isChecked()
        if (laravel) :
            type_project = 'laravel'

        if (modx) :
            type_project = 'modx'

        laravel_app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
        win = index.main()  # Создаём объект класса StartWindow
        win.show()  # Показываем окно
        sys.exit(laravel_app.exec())


#Основная функция приложения
def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    win = StartWindow()  # Создаём объект класса StartWindow
    win.show()  # Показываем окно
    sys.exit(app.exec())
#Если запуск из скрипта (не импорт) выполняем функцию
if __name__ == '__main__' :
    main()