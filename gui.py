from PyQt5.QtWidgets    import (QPushButton, QHBoxLayout, QVBoxLayout, QApplication, QLabel, QGridLayout, QDialog)
from PyQt5              import QtWidgets, uic, QtCore, QtGui
from PyQt5.QtCore       import QSize
from PyQt5.QtGui        import QIcon
import json
import sys
import laravel
from laravel import Ui_MainWindow

class GUI (QtWidgets.QMainWindow, laravel.Ui_MainWindow) :
    def __init__(self):
        # Типы кнопок (удалить, редактировать)
        self.editType = 'edit'
        self.deleteType = 'delete'
        self.processedItemCounter = 0

        super().__init__()
        self.setupUi(self)

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
        shortKey = key
        # Ограничиваем длину
        if (len(key) > self.translateLen):
            shortKey = key[:self.translateLen] + '...'

        rowKey = QLabel(shortKey)
        rowKey.setToolTip(key)
        horizontalRowGrid.addWidget(rowKey, 0, 0)
        i = 1
        for lang in langs:
            wordItem = QLabel()
            try:
                text = data[lang]
                if (len(data[lang]) > self.translateLen):
                    text = data[lang][:self.translateLen] + '...'
            except KeyError:
                text = ''
            wordItem.setText(text)
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

    def clearLayout(layout):
        if layout is not None:
            for itemIndex in range(layout.count()):
                if (layout.itemAt(itemIndex).__class__.__name__ == "QHBoxLayout"):
                    qGridItems = layout.itemAt(itemIndex).itemAt(0)
                    print(qGridItems.count())
                    for qGridItemIndex in range(qGridItems.count()) :
                        print(qGridItems.itemAt(qGridItemIndex).widget())
                        # print(qGridItems.itemAt(2).widget().setParent(None))

    def progressBar(progressData):
        gui                                 = progressData['gui_elements']
        current_file_str                    = str(progressData['current_file'])
        current_file_total_item_str         = str(progressData['current_file_total_item'])
        current_file_current_item_str       = str(progressData['current_file_current_item'])

        if (progressData['current_file'] is not None):
            gui['current_file'].setText(current_file_str)
        if (progressData['current_file_total_item'] is not None):
            gui['current_file_total_item'].setText(current_file_total_item_str)
            gui['items_count_current_file'].setText(current_file_total_item_str)
            gui['progress_bar_item'].setMaximum(progressData['current_file_total_item'])
        gui['current_file_current_item'].setText(current_file_current_item_str)
        gui['progress_bar_item'].setValue(progressData['current_file_current_item'])