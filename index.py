import configparser
from PyQt5              import QtWidgets, uic, QtCore, QtGui
from PyQt5.QtWidgets import (QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QApplication, QLabel, QGridLayout, QDialog)
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from time               import sleep
from googletrans        import Translator
from subprocess         import check_output
from bs4                import BeautifulSoup
from mysql.connector    import MySQLConnection, Error
from pathlib            import Path
import sys
# import html_design
#import restore_update
import tabs_design
import os
import DB
import json
import codecs
import subprocess
import re
import numpy as np
import io
from gui import GUI

#Laravel
from os import listdir
from os.path import isdir, join, isfile

class HtmlTranslator(QtWidgets.QMainWindow, tabs_design.Ui_MainWindow):

    def tinitVocabulary(self):
        initData = {}
        initData = {
            'hello': {'en': 'Hello', 'ru': 'Привет', 'ua': 'Доброго дня'},
            'phone': {'en': 'Phone', 'ru': 'Телефон', 'ua': 'Телефон'},
            'product': {'en': 'Product', 'ru': 'Товар', 'ua': 'Продукт'},
        }

        langs = ['ru', 'en', 'ua']

        i = 1

        for key in initData:
            j = 0
            #self.vocabylaryGridLayout.setColumnStretch(i, 1)
            for lang in langs:
                wordItem = QLabel()
                wordItem.setText(initData[key][lang])
                self.vocabylaryGridLayout.setColumnStretch(j, 1)
                self.vocabylaryGridLayout.addWidget(wordItem, i, j)
                j = j + 1
            # Иконки для кнопок, размер кнопок
            editButton = QPushButton()
            deleteButton = QPushButton()
            editButton.setIcon(QIcon('edit-icon-image-9.png'))
            deleteButton.setIcon(QIcon('delete-icon-16x16-29 .png'))
            editButton.setIconSize(QSize(16, 20))
            deleteButton.setIconSize(QSize(16, 20))

            # Итератор шаблонов (горизонтальных в вертикальном)
            iterate = self.vocabylaryGridLayout.count()

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
            #horizontal.addStretch(1)
            self.vocabylaryGridLayout.addWidget(editButton, i, j)
            j = j + 1
            self.vocabylaryGridLayout.addWidget(deleteButton, i, j)
            j = j + 1
            # Добавляем горизонтальный шаблон (с переводами и кнопками) во "внешний вертикальный" (проще говоря добавляем строку в ячейку)
            #self.vocabularyLayout.addLayout(horizontal)
            i = i + 1
        # Устанавливаем основной (вертикальный шаблон) в окне приложения
        #self.vocabylaryLayout.addStretch(1)
        #self.vocabylaryGridLayout.addLayout(horizontal)

    def initVocabulary(self):
        layout = QGridLayout()
        initData = self.initData
        # if (os.path.isfile('vocabulary.json') == False) :
        #     with open('vocabulary.json', 'w') as f:
        #         json.dump(initData, f)

        # Шапка таблицы
        GUI.setTableHeader(self.langs, self.vocabularyLayout)
        # Рендер переводов
        for key in initData:
            horizontal = GUI.setRow(self, self.langs, initData[key], key, self.vocabularyLayout)
            for itemInRow in range(horizontal.itemAt(0).count()) :
                widgetType = horizontal.itemAt(0).itemAt(itemInRow).widget().property('type')
                if(widgetType == 'edit'):
                    horizontal.itemAt(0).itemAt(itemInRow).widget().clicked.connect(self.editClick)
                if (widgetType == 'delete'):
                    horizontal.itemAt(0).itemAt(itemInRow).widget().clicked.connect(self.deleteClick)
            self.vocabularyLayout.addLayout(horizontal)
        # Устанавливаем основной (вертикальный шаблон) в окне приложения
        self.vocabularyLayout.addStretch(1)

    def editClick(self) :
        self.dialog = QDialog(self)
        self.dialog.ui = uic.loadUi('editTranslateDialog.ui', self.dialog)
        translateKey = self.sender().property('key')
        self.renderDialog(self.initData[translateKey], key = translateKey)
    def deleteClick(self) :
        # Подтверждение удаления записи
        confirmDelete = QtWidgets.QMessageBox.critical(None, 'Подтверждение удаления', 'Вы действительно желаете удалить данную запись?', QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if confirmDelete == QtWidgets.QMessageBox.Yes:
            # Получаем индекс горизонтального шаблона по аттрибуту кнопки (ID)
            horizontalRowLayoutId = self.sender().property('id')
            keyAttr = self.sender().property('key')
            horizontalRowLayout = self.vocabularyLayout.itemAt(horizontalRowLayoutId)

            # Шаблон сетки в горизонтальном шаблоне (QGridLayoiut в шаблоне QHLayout)
            innerRowGridLayout = horizontalRowLayout.itemAt(0) #Немного костыль, если будет боолее одного layout-та не сработает
            widgetCount = innerRowGridLayout.count()

            # Удаляем все виджеты в шаблоне (layuot-e)
            for i in reversed(range(widgetCount)):
                innerRowGridLayout.itemAt(i).widget().setParent(None)
            # Удаляем шаблон сетки (QGridLayout) из горизонтального шаблона
            horizontalRowLayout.removeItem(horizontalRowLayout.itemAt(0))
            self.vocabularyLayout.removeItem(self.vocabularyLayout.itemAt(horizontalRowLayoutId))

            #Обновление аттрибутов ID у кнопок редактирования и удаления (чтобы индексы слоев GUI соответствовали индексам записей из словаря)
            i = 0
            for horizontalRow in range(self.vocabularyLayout.count() - 1) : # count()-1 Убираем из общего количества объектов последний добавляющий растяжение макету (self.vocabularyLayout.addStretch(1))
                if(self.vocabularyLayout.itemAt(horizontalRow).itemAt(0) != None) :
                    for itemInRow in range(self.vocabularyLayout.itemAt(horizontalRow).itemAt(0).count()) :
                        #Тип элемента GUI (если это тип удалить или редактировать (кнопки), то обновляем их ID-ки после удаления перевода)
                        rowItemWidgetType = self.vocabularyLayout.itemAt(horizontalRow).itemAt(0).itemAt(itemInRow).widget().property('type')
                        if(rowItemWidgetType == self.editType or rowItemWidgetType == self.deleteType) :
                            self.vocabularyLayout.itemAt(horizontalRow).itemAt(0).itemAt(itemInRow).widget().setProperty('id', i)
                i += 1
            del self.initData[keyAttr]
            with open(self.vocabularyFileName + '.json', 'w') as f:
                json.dump(self.initData, f)

    def clickBtnAddTranslate(self, values = None) :
        #инициализация диалогового окна и установка дизайна (пустой layout)
        self.dialog = QDialog(self)
        self.dialog.ui = uic.loadUi('addTranslateDialog.ui', self.dialog)
        self.renderDialog()
    def renderDialog(self, values = None, key = None):
        layout = QVBoxLayout()
        # Ключ перевода (добавляем на layout метку и инпут)
        keyRow = QHBoxLayout()
        keyRow.addWidget(QLabel('Ключ', objectName='textLabel'))
        if key is not None :
            keyInput = QtWidgets.QLineEdit(key, objectName='inputField')
        else:
            keyInput = QtWidgets.QLineEdit(objectName='inputField')
        keyInput.setProperty('name', 'key')
        keyRow.addWidget(keyInput)
        layout.addLayout(keyRow)
        layout.addStretch(1)
        # Локализованные значения (сами переводы)
        for lang in self.langs:
            langRowHorizontal = QHBoxLayout()
            lng = QLabel(lang, objectName='textLabel')
            if values is not None:
                lngInput = QtWidgets.QLineEdit(values[lang], objectName='inputField')
            else:
                lngInput = QtWidgets.QLineEdit(objectName='inputField')
            lngInput.setProperty('name', lang)
            langRowHorizontal.addWidget(lng)
            langRowHorizontal.addWidget(lngInput)
            layout.addLayout(langRowHorizontal)
            layout.addStretch(1)
        layout.addStretch(1)
        # Кнопки взаимодействия с диалоговым окном (сохранить и отмена - закрыть диалог)
        buttonsRow = QHBoxLayout()
        saveButton = QPushButton('Сохранить', objectName='saveButton')
        cancelButton = QPushButton('Отмена', objectName='cancelButton')
        # Обработчик нажатия  кнопок (отмена и сохранить)
        cancelButton.clicked.connect(self.cancelDialogClick)
        saveButton.clicked.connect(self.saveTranslateClick)
        buttonsRow.addWidget(cancelButton)
        buttonsRow.addWidget(saveButton)
        layout.addLayout(buttonsRow)
        # Устанавливаем стили диалогового окна
        self.dialog.setStyleSheet(open("styles/qLineEdit.qss", "r").read())
        self.dialog.setLayout(layout)
        # Показываем диалоговое окно
        self.dialog.show()
    # Закрываем диалоговое окно
    def cancelDialogClick(self):
        self.dialog.close()
    # Сохраняем перевод в файлы (словари)
    def saveTranslateClick(self):
        dialogData = {}
        #Собираем данные с формы (диалоговое окно)
        emptyInputError = False
        for dialogInput in range(self.dialog.layout().count()):
            if(self.dialog.layout().itemAt(dialogInput).__class__.__name__ == 'QHBoxLayout') :
                if(self.dialog.layout().itemAt(dialogInput).itemAt(1).widget().property('name') != None) :
                    #Ключ
                    name = self.dialog.layout().itemAt(dialogInput).itemAt(1).widget().property('name')
                    #Значение
                    value = self.dialog.layout().itemAt(dialogInput).itemAt(1).widget().text()
                    # Проверяем на наличие пустых полей
                    if(len(value) < 2) :
                        emptyInputError = True
                    dialogData[name] = value
        # В случае пустоты хотя бы в одном из полей информируем пользователя
        if(emptyInputError) :
            self.showMessage('Ошибка!', 'Не заполнены все поля', 'warning')
        else :
            newItem = {}
            langValueItem = {}
            #Записываем переводы в файлы локализаций
            for lang in self.langs :
                langValueItem[lang] = dialogData[lang]
            self.initData[dialogData['key']] = langValueItem
            with open(self.vocabularyFileName + '.json', 'w') as f:
                json.dump(self.initData, f)
            print(dialogData)
            self.showMessage('Сохранено', 'Перевод успешно добавлен!', 'info')
            # Очищаем поля ввода в диалоговом окне
            for dialogInput in range(self.dialog.layout().count()):
                if(self.dialog.layout().itemAt(dialogInput).__class__.__name__ == 'QHBoxLayout') :
                    if(self.dialog.layout().itemAt(dialogInput).itemAt(1).widget().property('name') != None) :
                        self.dialog.layout().itemAt(dialogInput).itemAt(1).widget().setText('')


    def getInputs(self):
        return (self.first.text(), self.second.text())
    # def getFiles(self, dir = ''):
    #     if(len(dir) > 0) :
    #         return [f for f in listdir(dir) if isfile(join(dir, f))]
    #
    # def getDirs(self, dir=''):
    #     if (len(dir) > 0):
    #         return [f for f in listdir(dir) if isdir(join(dir, f))]

    ################------------------------####################
    ############****Запускаем работу скрипта****################
    ################------------------------####################
    def clickBtnRunLaravel(self):
        # Save
        dictionary = {'hello': 'world'}
        np.save('my_file.npy', dictionary)

        # Получаем все переводы из файла
        # translate_path = Path(self.setting_file_translates)
        try:
            # translate_path.owner()
            # translate_file_content = check_output(
            #    ['php', '-r', 'include "' + self.setting_file_translates + '"; echo json_encode($l);'])
            # translate_file_content = json.loads(translate_file_content)

            dirDirectories  = [f for f in listdir(self.settingsLaravelRootDir) if isdir(join(self.settingsLaravelRootDir, f))]
            dirFiles        = [f for f in listdir(self.settingsLaravelRootDir) if isfile(join(self.settingsLaravelRootDir, f))]

            if(len(dirDirectories) > 0) :
                for tDir in dirDirectories :




                    #templateDirectories = [f for f in listdir(self.settingsLaravelRootDir) if isdir(join(self.settingsLaravelRootDir, f))]
                    if(tDir == 'errors') :
                        print(tDir)
            sys.exit(0)

            # Введенный фрагмент
            self.input = self.output = self.main_input.toPlainText()
            soup = BeautifulSoup(self.input, 'html.parser')
            for script in soup(["script", "style"]):
                script.extract()  # rip it out
            text = soup.get_text()
            # break into lines and remove leading and trailing space on each
            lines = (line.strip() for line in text.splitlines())
            # break multi-headlines into a line each
            chunks = [c for c in filter(None, lines)]

            chunks = filter(self.filter_values, chunks)
            for v in chunks:
                print(v)
            sys.exit(0)

            # Массив с переводами которые уже есть в БД (и которые не нужно будет переводить)
            exist_translates = DB.check_translates(self.setting_db_name, self.setting_db_user, self.setting_db_pass,
                                                   self.setting_main_lang, chunks)

            # Подставляем ID существующих переводов, и удаляем эти элементы из списка (chunks)
            if (len(exist_translates) > 0):
                for translate in exist_translates:
                    self.output = self.output.replace(translate[self.setting_main_lang],
                                                      str(self.setting_l_placeholder) + str(
                                                          translate['lang_id']) + str(self.setting_r_placeholder))
                    chunks.pop(chunks.index(translate[self.setting_main_lang]))

            # Перебираем оставщиеся строки, требующие перевода
            translator = Translator()
            translator.session.proxies['http'] = '125.26.109.83:8141'
            translator.session.proxies['http'] = '98.221.88.193:64312'
            translator.session.proxies['http'] = '188.244.35.162:10801'
            translator.session.proxies['http'] = '185.162.0.110:10801'

            # языки
            langs = self.setting_langs.split('|')

            # Прогресс бар
            i = 0
            self.progressBar.setMaximum(len(chunks) + 1)
            # Прогресс бар

            for item in chunks:

                # Прогресс бар
                i += 1
                self.progressBar.setValue(i)
                # Прогресс бар

                translate_file_string = []
                translate_dic = {}
                translate_dic[self.setting_main_lang] = item

                # строка для файла переводов
                translate_file_string = []
                for lang in langs:
                    new_translate = translator.translate(item, src=self.setting_main_lang, dest=lang).text
                    translate_dic[lang] = new_translate  # Пауза для гугла
                    sleep(3)

                # для запроса в базу (корректировка языков)
                correct_lang_sql = []
                # значения для записи в базу
                string_sql_values = []
                for item in translate_dic.items():
                    print(item[0] + '--------' + item[1])
                    correct_lang_sql.append(DB.lang_field_connector(item[0]))
                    string_sql_values.append("'" + item[1] + "'")
                    # Строка для записи в файл переводов
                    translate_file_string.append('"' + item[0] + '": "' + item[1] + '"')
                langs_sql = ','.join(correct_lang_sql)
                string_sql_values = ','.join(string_sql_values)

                # Запись в БД
                sql = "INSERT INTO modx_a_lang (" + langs_sql + ") VALUES (" + string_sql_values + ");"
                # values = (translate_dic["uk"], translate_dic["ru"], translate_dic["en"]);
                last_id = DB.add_translate(self.setting_db_name, self.setting_db_user, self.setting_db_pass, sql)

                # Запись в файл переводов
                translate_file_string = '{' + ','.join(translate_file_string) + '}'
                translate_file_string = json.loads(translate_file_string)

                # Добавление нового перевода в строку json переводов
                translate_file_content[last_id] = translate_file_string
                self.output = self.output.replace(translate_dic[self.setting_main_lang], "[#" + str(last_id) + "#]")

            self.write_to_file(translate_file_content, self.setting_file_translates)
            # subprocess.call(['chmod', '0777', '"' + self.setting_file_translates + '"'])
            self.main_input.setPlainText(self.output)
            # Информационное сообщение о завершении работы
            self.showMessage("Перевод завершен!",
                             "Перевод фрагмента html выполнен. Теперь вы можете его скопировать и добавить в свой шаблон!",
                             'info')
        except FileNotFoundError as f:
            self.showMessage('Ошибка!', 'Не верно указан путь к файлу!', 'critical')


    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле html.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна

        #Инициализация входной и выходной строки
        self.input = ''
        self.output = ''

        #Загрузка настроек из файла
        self.load_settings()

        #Языки
        self.langs = self.setting_langs.split('|')
        self.default_lang = self.setting_main_lang

        #Типы кнопок (удалить, редактировать)
        self.editType = 'edit'
        self.deleteType = 'delete'

        #Загрузка словаря
        self.vocabularyFileName = 'vocabulary'
        with open(self.vocabularyFileName + '.json', 'r') as inputData:
            self.initData = json.load(inputData)
        self.initVocabulary()

        #Обработчики нажатия кнопок
        self.btn_run.clicked.connect(self.click_btn_run)
        self.btn_save_settings.clicked.connect(self.click_btn_save_settings)
        self.btn_translate_file.clicked.connect(self.click_btn_translate_file)
        self.addTranslate.clicked.connect(self.clickBtnAddTranslate)
        #Laravel
        self.btnLaravelRoot.clicked.connect(self.clickBtnLaravelRoot)
        self.btnRunLaravel.clicked.connect(self.clickBtnRunLaravel)

        #Информационное окно
        self.msg = QtWidgets.QMessageBox()

        #Обработчик события изменение позиции курсора
        #self.main_input.cursorPositionChanged.connect(self.changeInput)

    def load_settings(self):
        # Читаем настройки из файла
        self.settings_path = 'settings.ini'
        if os.path.exists(self.settings_path):
            settings = configparser.ConfigParser()
            settings.read(self.settings_path)
            # GENERAL
            self.setting_langs                      = settings.get('GENERAL', 'LANGS')
            self.setting_main_lang                  = settings.get('GENERAL', 'MAIN_LANG')
            self.setting_file_translates            = settings.get('MODX', 'FILE_TRANSLATES')
            self.setting_l_placeholder              = settings.get('MODX', 'LEFT_PLACEHOLDER')
            self.setting_r_placeholder              = settings.get('MODX', 'RIGHT_PLACEHOLDER')
            #LARAVEl
            self.settingsLeftLaravelPlaceholder     = settings.get('LARAVEL', 'LEFT_LARAVEL_PLACEHOLDER')
            self.settingsRightLaravelPlaceholder    = settings.get('LARAVEL', 'RIGHT_LARAVEL_PLACEHOLDER')
            self.settingsLaravelRootDir             = settings.get('LARAVEL', 'ROOT_DIR')
            # DB
            self.setting_db_user                    = settings.get('DB', 'DB_USER')
            self.setting_db_name                    = settings.get('DB', 'DB_NAME')
            self.setting_db_pass                    = settings.get('DB', 'DB_PASS')

            # Установка значений настроек из файла на форму
            if len(self.setting_langs) > 0:
                langs_arr = self.setting_langs.split('|')
                if 'ru' in langs_arr:
                    self.ru.setChecked(True)
                if 'en' in langs_arr:
                    self.en.setChecked(True)
                if 'uk' in langs_arr:
                    self.uk.setChecked(True)
                if 'de' in langs_arr:
                    self.de.setChecked(True)
            main_lang = self.main_lang.findText(self.setting_main_lang, QtCore.Qt.MatchFixedString)
            if main_lang >= 0:
                self.main_lang.setCurrentIndex(main_lang)
            self.file_path.setText(self.setting_file_translates)
            self.l_placeholder.setText(self.setting_l_placeholder)
            self.r_placeholder.setText(self.setting_r_placeholder)
            self.db_user.setText(self.setting_db_user)
            self.db_name.setText(self.setting_db_name)
            self.db_pass.setText(self.setting_db_pass)

            #Laravel
            self.laravelRootDir.setText(self.settingsLaravelRootDir)
            self.leftLaravelPlaceholder.setText(self.settingsLeftLaravelPlaceholder)
            self.rightLaravelPlaceholder.setText(self.settingsRightLaravelPlaceholder)

    # def changeInput (self):
    #     input = self.main_input
    #     #self.input = self.main_input.toPlainText()
    #     #str_output = self.input.replace('<div>', "[#" + str(exist_id) + "#]")
    #     input.setText("<div></div>")
    #     #print(self.input)

    ################------------------------####################
    #############****Выбор файла переводов****##################
    ################------------------------####################
    def click_btn_translate_file(self):
        fname, _filter = QtWidgets.QFileDialog.getOpenFileName(self, 'Выберите файл')
        self.file_path.setText(fname)

    ################------------------------####################
    #######****Выбор корневой директории шаблонов****###########
    ################------------------------####################
    def clickBtnLaravelRoot(self):
        dirName = QtWidgets.QFileDialog.getExistingDirectory(self, 'Выберите директорию', '/home')
        self.laravelRootDir.setText(dirName)

    ################------------------------####################
    #############****Обновление настроек****####################
    ################------------------------####################
    def click_btn_save_settings (self):
        # языки для переводов
        langs = []
        if self.ru.isChecked():
            langs.append('ru')
        if self.en.isChecked():
            langs.append('en')
        if self.uk.isChecked():
            langs.append('uk')
        if self.de.isChecked():
            langs.append('de')
        # Основной язык
        m_lang = self.main_lang.currentText()
        #База данных
        db_user = self.db_user.text()
        db_pass = self.db_pass.text()
        db_name = self.db_name.text()

        # Путь к файлу переводов
        file_translates = self.file_path.text()

        #Корневая директория шаблонов Laravel
        laravelRootDir  = self.laravelRootDir.text()

        #Плейсхолдеры
        l_placeholder               = self.l_placeholder.text()
        r_placeholder               = self.r_placeholder.text()
        leftLaravelPlaceholder      = self.leftLaravelPlaceholder.text()
        rightLaravelPlaceholder     = self.rightLaravelPlaceholder.text()

        #Подтверждение сохранения настроек
        buttonReply = QtWidgets.QMessageBox.question(self, 'Изменение настроек', "Сохранить выбранные настройки?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if buttonReply == QtWidgets.QMessageBox.Yes:
            settings = configparser.ConfigParser()

            settings['GENERAL'] = {
                'LANGS':                '|'.join(langs),
                'MAIN_LANG':            m_lang,
            }

            settings['MODX'] = {
                'FILE_TRANSLATES': file_translates,
                'LEFT_PLACEHOLDER': l_placeholder,
                'RIGHT_PLACEHOLDER': r_placeholder,
            }

            settings['LARAVEL'] = {
                'LEFT_LARAVEL_PLACEHOLDER': leftLaravelPlaceholder,
                'RIGHT_LARAVEL_PLACEHOLDER': rightLaravelPlaceholder,
                'ROOT_DIR': laravelRootDir,
            }

            settings['DB'] = {
                'DB_USER': db_user,
                'DB_NAME': db_name,
                'DB_PASS': db_pass,
            }
            with open(self.settings_path, "w") as config_file:
                settings.write(config_file)
            self.load_settings()

    def filter_values(self, x):
        if (re.findall(r'^{{.+}}$|^{!!.+!!}$|^@|^{{\s.+}}|^:{{.+}}$|^\+{{.+}}$', x)):
            return 0
        return 1

    ################------------------------####################
    ############****Запускаем работу скрипта****################
    ################------------------------####################
    def click_btn_run(self):
        # Получаем все переводы из файла
        translate_path = Path(self.setting_file_translates)
        try:
            translate_path.owner()
            translate_file_content = check_output(['php', '-r', 'include "' + self.setting_file_translates + '"; echo json_encode($l);'])
            translate_file_content = json.loads(translate_file_content)

            # Введенный фрагмент
            self.input = self.output = self.main_input.toPlainText()
            soup = BeautifulSoup(self.input, 'html.parser')
            for script in soup(["script", "style"]):
                script.extract()  # rip it out
            text = soup.get_text()
            # break into lines and remove leading and trailing space on each
            lines = (line.strip() for line in text.splitlines())
            # break multi-headlines into a line each
            chunks = [c for c in filter(None, lines)]

            chunks = filter(self.filter_values, chunks)
            for v in chunks :
                print(v)
            sys.exit(0)

            # Массив с переводами которые уже есть в БД (и которые не нужно будет переводить)
            exist_translates = DB.check_translates(self.setting_db_name, self.setting_db_user, self.setting_db_pass, self.setting_main_lang, chunks)

            # Подставляем ID существующих переводов, и удаляем эти элементы из списка (chunks)
            if (len(exist_translates) > 0):
                for translate in exist_translates:
                    self.output = self.output.replace(translate[self.setting_main_lang], str(self.setting_l_placeholder) + str(translate['lang_id']) + str(self.setting_r_placeholder))
                    chunks.pop(chunks.index(translate[self.setting_main_lang]))

            # Перебираем оставщиеся строки, требующие перевода
            translator = Translator()
            translator.session.proxies['http'] = '125.26.109.83:8141'
            translator.session.proxies['http'] = '98.221.88.193:64312'
            translator.session.proxies['http'] = '188.244.35.162:10801'
            translator.session.proxies['http'] = '185.162.0.110:10801'

            # языки
            langs = self.setting_langs.split('|')

            # Прогресс бар
            i = 0
            self.progressBar.setMaximum(len(chunks) + 1)
            # Прогресс бар

            for item in chunks:

                # Прогресс бар
                i += 1
                self.progressBar.setValue(i)
                # Прогресс бар

                translate_file_string = []
                translate_dic = {}
                translate_dic[self.setting_main_lang] = item

                # строка для файла переводов
                translate_file_string = []
                for lang in langs:
                    new_translate = translator.translate(item, src=self.setting_main_lang, dest=lang).text
                    translate_dic[lang] = new_translate  # Пауза для гугла
                    sleep(3)

                # для запроса в базу (корректировка языков)
                correct_lang_sql = []
                # значения для записи в базу
                string_sql_values = []
                for item in translate_dic.items():
                    print(item[0] + '--------' + item[1])
                    correct_lang_sql.append(DB.lang_field_connector(item[0]))
                    string_sql_values.append("'" + item[1] + "'")
                    # Строка для записи в файл переводов
                    translate_file_string.append('"' + item[0] + '": "' + item[1] + '"')
                langs_sql = ','.join(correct_lang_sql)
                string_sql_values = ','.join(string_sql_values)

                # Запись в БД
                sql = "INSERT INTO modx_a_lang (" + langs_sql + ") VALUES (" + string_sql_values + ");"
                # values = (translate_dic["uk"], translate_dic["ru"], translate_dic["en"]);
                last_id = DB.add_translate(self.setting_db_name, self.setting_db_user, self.setting_db_pass, sql)

                # Запись в файл переводов
                translate_file_string = '{' + ','.join(translate_file_string) + '}'
                translate_file_string = json.loads(translate_file_string)

                # Добавление нового перевода в строку json переводов
                translate_file_content[last_id] = translate_file_string
                self.output = self.output.replace(translate_dic[self.setting_main_lang], "[#" + str(last_id) + "#]")

            self.write_to_file(translate_file_content, self.setting_file_translates)
            # subprocess.call(['chmod', '0777', '"' + self.setting_file_translates + '"'])
            self.main_input.setPlainText(self.output)
            # Информационное сообщение о завершении работы
            self.showMessage("Перевод завершен!", "Перевод фрагмента html выполнен. Теперь вы можете его скопировать и добавить в свой шаблон!", 'info')
        except FileNotFoundError as f:
            self.showMessage('Ошибка!', 'Не верно указан путь к файлу!', 'critical')


    ################------------------------####################
    ############**********Запись в файл*********################
    ################------------------------####################
    def write_to_file(self, json_string, path="D:\OSPanel\domains\shop.loc\dump.php"):
        f = codecs.open(path, "w+", "utf-8")
        f.write('<?php \n $l=[')
        tr_strings = []
        for l_id, value in json_string.items():
            single_tr = str(l_id) + "=>["
            # Массив переводов одного слова(предложения)
            tr_langs = []
            for lang, v in value.items():
                tr_langs.append("'" + lang + "'=>'" + v + "'")
            # Массив переводов строк
            single_tr += ','.join(tr_langs) + "],";
            f.write(single_tr)
        f.write('];')
        f.close()
        return True;

    #########****************************************###########
    #########****Показать сообщение пользователю*****###########
    #########****************************************###########
    def showMessage (self, title, message, icon) :
        icons = {
            'info': QtWidgets.QMessageBox.Information,
            'warning': QtWidgets.QMessageBox.Warning,
            'critical': QtWidgets.QMessageBox.Critical,
        }
        self.msg.setIcon(icons[icon])
        self.msg.setWindowTitle(title)
        self.msg.setText(message)
        self.msg.exec_()

#Основная функция приложения
def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    win = HtmlTranslator()  # Создаём объект класса HtmlTranslator
    win.show()  # Показываем окно
    sys.exit(app.exec())
#Если запуск из скрипта (не импорт) выполняем функцию
if __name__ == '__main__' :
    main()