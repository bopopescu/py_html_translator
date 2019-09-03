import sys
from PyQt5.QtWidgets import (QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QApplication, QLabel)
from PyQt5.QtCore import QSize
from PyQt5 import QtGui
from PyQt5.QtGui import QIcon


class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):

        #okButton = QPushButton("OK")
        #cancelButton = QPushButton("Cancel")
        vertical    = self.vertical =  QVBoxLayout()

        initData = {}
        initData = {
            'hello': {'en': 'Hello', 'ru': 'Привет', 'ua': 'Доброго дня'},
            'phone': {'en': 'Phone', 'ru': 'Телефон', 'ua': 'Телефон'},
            'product': {'en': 'Product', 'ru': 'Товар', 'ua': 'Продукт'},
        }

        langs = ['ru', 'en', 'ua']

        for key in initData:
            self.horizontal = QHBoxLayout()
            horizontal = self.horizontal
            for lang in langs :
                wordItem = QLabel()
                wordItem.setText(initData[key][lang])
                horizontal.addWidget(wordItem)

            #Иконки для кнопок, размер кнопок
            editButton = QPushButton()
            deleteButton = QPushButton()
            editButton.setIcon(QIcon('edit-icon-image-9.png'))
            deleteButton.setIcon(QIcon('delete-icon-16x16-29 .png'))
            editButton.setIconSize(QSize(16, 20))
            deleteButton.setIconSize(QSize(16, 20))

            # Итератор шаблонов (горизонтальных в вертикальном)
            iterate = self.vertical.count()

            # ID-ки и ключи кнопок (для удаления и редактирования)
            # ID-ки кнопок должны совпадать и итератором шаблонов (горизонтальных в вертикальном - номер строки перевода(индекс))
            editButton.setProperty('key', key)
            deleteButton.setProperty('key', key)
            deleteButton.setProperty('id', iterate)
            editButton.setProperty('id', iterate)
            # Обработчик нажатия  кнопок (редактировать и удалить)
            editButton.clicked.connect(self.editClick)
            deleteButton.clicked.connect(self.deleteClick)
            # Добавляем в каждый горизонтальный шаблон (строку) кнопки удаления и редактирования
            horizontal.addWidget(editButton)
            horizontal.addWidget(deleteButton)
            # Добавляем горизонтальный шаблон (с переводами и кнопками) во "внешний вертикальный" (проще говоря добавляем строку в ячейку)
            self.vertical.addLayout(horizontal)
        # Устанавливаем основной (вертикальный шаблон) в окне приложения
        self.setLayout(vertical)



        self.setGeometry(300, 300, 500, 150)
        self.setWindowTitle('Buttons')
        self.show()
    def editClick(self) :
        print(self.sender().objectName())
    def deleteClick(self) :
        #vlayout = QHBoxLayout(self.horizontal)

        # for i in range(self.vertical.count()):
        #     layout_item = self.vertical.itemAt(i)
        #     print(layout_item)

        #print(self.vertical.count())
        while self.vertical.itemAt(1):
            child = self.vertical.itemAt(1).takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        self.vertical.removeItem(self.vertical.itemAt(1))
        #print(self.sender().objectName())
        print(self.sender().property('id'))

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())