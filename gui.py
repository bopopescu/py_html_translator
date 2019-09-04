from PyQt5.QtWidgets    import (QPushButton, QHBoxLayout, QVBoxLayout, QApplication, QLabel, QGridLayout, QDialog)
from PyQt5              import QtWidgets, uic, QtCore, QtGui
from PyQt5.QtCore       import QSize
from PyQt5.QtGui        import QIcon
import json

class GUI () :
    def __init__(self):
        # Типы кнопок (удалить, редактировать)
        self.editType = 'edit'
        self.deleteType = 'delete'

    def setTableHeader(langs, layout):
        # Шапка таблицы
        tableHeaderRow = QHBoxLayout()
        tableHeaderGrid = QGridLayout()
        keyLabel = QLabel('ключ', objectName='headerRowKey')
        keyLabel.setStyleSheet(open("styles/qLineEdit.qss", "r").read())
        keyLabel.setFixedWidth(230)
        tableHeaderGrid.addWidget(keyLabel, 0, 0)
        j = 1;
        for lang in langs:
            j += 1;
            keyLangLabel = QLabel(lang, objectName='headerRowKey')
            keyLangLabel.setStyleSheet(open("styles/qLineEdit.qss", "r").read())
            keyLangLabel.setFixedWidth(230)
            tableHeaderGrid.addWidget(keyLangLabel, 0, j)
        tableHeaderRow.addLayout(tableHeaderGrid)
        tableHeaderRow.addStretch(1)
        layout.addLayout(tableHeaderRow)


    def setRow(self, langs, data, key, layout) :
        horizontal = QHBoxLayout()
        horizontalRowGrid = QGridLayout()
        # Ключ перевода
        rowKey = QLabel(key)
        horizontalRowGrid.addWidget(rowKey, 0, 0)
        i = 1
        for lang in langs:
            wordItem = QLabel()
            wordItem.setText(data[lang])
            horizontalRowGrid.addWidget(wordItem, 0, i)
            i += 1
        # Иконки для кнопок, размер кнопок
        editButton = QPushButton()
        deleteButton = QPushButton()
        editButton.setIcon(QIcon('edit-icon-image-9.png'))
        deleteButton.setIcon(QIcon('delete-icon-16x16-29 .png'))
        editButton.setIconSize(QSize(16, 20))
        deleteButton.setIconSize(QSize(16, 20))
        deleteButton.setFixedHeight(24)
        deleteButton.setFixedWidth(24)
        editButton.setFixedHeight(24)
        editButton.setFixedWidth(24)
        # Итератор шаблонов (горизонтальных в вертикальном)
        iterate = layout.count()
        # ID-ки и ключи кнопок (для удаления и редактирования)
        # ID-ки кнопок должны совпадать и итератором шаблонов (горизонтальных в вертикальном - номер строки перевода(индекс))
        editButton.setProperty('key', key)
        editButton.setProperty('id', iterate)
        editButton.setProperty('type', self.editType)
        deleteButton.setProperty('key', key)
        deleteButton.setProperty('id', iterate)
        deleteButton.setProperty('type', self.deleteType)
        # Обработчик нажатия  кнопок (редактировать и удалить)
        # Добавляем в каждый горизонтальный шаблон (строку) кнопки удаления и редактирования
        horizontalRowGrid.addWidget(editButton, 0, i)
        i += 1
        horizontalRowGrid.addWidget(deleteButton, 0, i)
        i += 1
        # Добавляем горизонтальный шаблон (с переводами и кнопками) во "внешний вертикальный" (проще говоря добавляем строку в ячейку)
        horizontal.addLayout(horizontalRowGrid)
        return horizontal