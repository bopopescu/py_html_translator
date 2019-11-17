import configparser
from PyQt5              import QtWidgets, uic, QtCore, QtGui
from PyQt5.QtWidgets import (QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QApplication, QLabel, QGridLayout, QDialog)
from PyQt5.QtCore import *
from time               import sleep
from googletrans        import Translator
from subprocess         import check_output
from bs4                import BeautifulSoup
from pathlib            import Path
import sys
import laravel
import os
import json
import codecs
import re
from gui import GUI
import Laravel
import Vocabulary
### Multi threads
import traceback, sys

class WorkerSignals(QObject):
    '''
    Defines the signals available from a running worker thread.

    Supported signals are:

    finished
        No data

    error
        `tuple` (exctype, value, traceback.format_exc() )

    result
        `object` data returned from processing, anything

    '''
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    progress = pyqtSignal(int)

class Worker(QRunnable):
    '''
    Worker thread

    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.

    :param callback: The function callback to run on this worker thread. Supplied args and
                     kwargs will be passed through to the runner.
    :type callback: function
    :param args: Arguments to pass to the callback function
    :param kwargs: Keywords to pass to the callback function

    '''

    def __init__(self, fn, *args, **kwargs):

        super(Worker, self).__init__()
        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

        # Add the callback to our kwargs
        self.kwargs['progress_callback'] = self.signals.progress

    @pyqtSlot()
    def run(self):
        '''
        Initialise the runner function with passed args, kwargs.
        '''

        # Retrieve args/kwargs here; and fire processing using them
        try:
            result = self.fn(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)  # Return the result of the processing
        finally:
            self.signals.finished.emit()  # Done
### Multi threads




class HtmlTranslator(QtWidgets.QMainWindow, laravel.Ui_MainWindow):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле tabs_design.py
        super().__init__()

        self.threadpool = QThreadPool()

        self.appTmpDir = os.path.expanduser('~') + '/.pyLaravelTranslate/'

        if (os.path.exists(self.appTmpDir) == False):
            os.mkdir(self.appTmpDir)

        self.setupUi(self)  # Это нужно для инициализации нашего дизайна

        # Информационное окно
        self.msg = QtWidgets.QMessageBox()

        #Инициализация входной и выходной строки
        self.input = ''
        self.output = ''

        #Загрузка настроек из файла
        self.load_settings()

        # Длина строки перевода (отображение в словаре)
        self.translateLen = 25

        #Языки
        self.default_lang = self.setting_main_lang
        self.langs = self.setting_langs.split('|')
        self.langs.insert(0, self.default_lang)

        #Типы кнопок (удалить, редактировать)
        self.editType = 'edit'
        self.deleteType = 'delete'

        #Загрузка словаря
        self.vocabularyFileName = 'vocabulary'
        self.vocabularyLayout = self.scrollArea

        #Загрузка  данных словаря
        try:
            self.initDataVocabulary = Vocabulary.loadJson(self.vocabularyFileName)
        except FileNotFoundError:
            Vocabulary.writeJson(self.vocabularyFileName, {})
            self.initDataVocabulary = Vocabulary.loadJson(self.vocabularyFileName)

        #Функции инициализации
        if (self.initDataVocabulary is not None and len(self.initDataVocabulary) > 0):
            Vocabulary.indexVocabulary()
            Vocabulary.initTableHeader(self.tableHeaderLayout)
            self.initVocabulary()


        #Обработчики нажатия кнопок
        self.btn_save_settings.clicked.connect(self.click_btn_save_settings)
        self.addTranslate.clicked.connect(self.clickBtnAddTranslate)
        #Laravel
        self.btnLaravelRoot.clicked.connect(self.clickBtnLaravelRoot)
        self.btnLaravelRootLang.clicked.connect(self.clickBtnLaravelRootLang)
        self.btnRunLaravel.clicked.connect(self.clickBtnRunLaravel)

    def load_settings(self):
        # Читаем настройки из файла
        self.settings_path = self.appTmpDir + 'settings.ini'
        if os.path.exists(self.settings_path):
            settings = configparser.ConfigParser()
            settings.read(self.settings_path)
            # GENERAL
            self.setting_langs                      = settings.get('GENERAL', 'LANGS')
            self.setting_main_lang                  = settings.get('GENERAL', 'MAIN_LANG')

            #LARAVEl
            self.settingsLeftLaravelPlaceholder     = settings.get('LARAVEL', 'LEFT_LARAVEL_PLACEHOLDER')
            self.settingsRightLaravelPlaceholder    = settings.get('LARAVEL', 'RIGHT_LARAVEL_PLACEHOLDER')
            self.settingsLaravelRootDir             = settings.get('LARAVEL', 'ROOT_DIR')
            self.settingsLaravelRootDirLang         = settings.get('LARAVEL', 'ROOT_DIR_LANG')

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

            #Laravel
            self.laravelRootDir.setText(self.settingsLaravelRootDir)
            self.laravelRootDirLang.setText(self.settingsLaravelRootDirLang)
            self.leftLaravelPlaceholder.setText(self.settingsLeftLaravelPlaceholder)
            self.rightLaravelPlaceholder.setText(self.settingsRightLaravelPlaceholder)

    ################------------------------####################
    #######****Выбор корневой директории шаблонов****###########
    ################------------------------####################
    def clickBtnLaravelRoot(self):
        dirName = QtWidgets.QFileDialog.getExistingDirectory(self, 'Выберите директорию', '/home')
        self.laravelRootDir.setText(dirName)

    ################------------------------####################
    #######***Выбор корневой директории переводов****###########
    ################------------------------####################
    def clickBtnLaravelRootLang(self):
        dirName = QtWidgets.QFileDialog.getExistingDirectory(self, 'Выберите директорию', '/home')
        self.laravelRootDirLang.setText(dirName)

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

        #Корневая директория шаблонов Laravel
        laravelRootDir      = self.laravelRootDir.text()
        laravelRootDirLang  = self.laravelRootDirLang.text()

        #Плейсхолдеры
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

            settings['LARAVEL'] = {
                'LEFT_LARAVEL_PLACEHOLDER': leftLaravelPlaceholder,
                'RIGHT_LARAVEL_PLACEHOLDER': rightLaravelPlaceholder,
                'ROOT_DIR': laravelRootDir,
                'ROOT_DIR_LANG': laravelRootDirLang,
            }

            with open(self.settings_path, "w") as config_file:
                settings.write(config_file)
            self.load_settings()
            self.initVocabulary()
            Vocabulary.initTableHeader(self.tableHeaderLayout)





##########-------------LARAVEL----------------###############

    ################------------------------####################
    #############****Инициализация словаря****##################
    ################------------------------####################
    def initVocabulary(self):
        layout = QGridLayout()
        initData = self.initDataVocabulary
        widget = QWidget()
        # Виджет в скролл области
        self.scrollArea.setWidget(widget)
        self.vocabularyLayout = QVBoxLayout(widget)

        # Рендер переводов
        for key in initData:
            horizontal = GUI.setRow(self, self.langs, initData[key], key, self.vocabularyLayout)
            # Установка обработчиков нажатия кнопок
            for itemInRow in range(horizontal.itemAt(0).count()) :
                widgetType = horizontal.itemAt(0).itemAt(itemInRow).widget().property('type')
                if(widgetType == 'edit'):
                    horizontal.itemAt(0).itemAt(itemInRow).widget().clicked.connect(self.editClick)
                if (widgetType == 'delete'):
                    horizontal.itemAt(0).itemAt(itemInRow).widget().clicked.connect(self.deleteClick)
            self.vocabularyLayout.addLayout(horizontal)
        # Устанавливаем основной (вертикальный шаблон) в окне приложения
        self.vocabularyLayout.addStretch(1)

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

            del self.initDataVocabulary[keyAttr]
            with open(self.vocabularyFileName + '.json', 'w') as f:
                json.dump(self.initDataVocabulary, f)
            Vocabulary.indexVocabulary()

    def editClick(self):
        self.dialog = QDialog(self)
        self.dialog.ui = uic.loadUi('editTranslateDialog.ui', self.dialog)
        translateKey = self.sender().property('key')
        self.renderDialog(self.initDataVocabulary[translateKey], key=translateKey, type = 'edit')

    def clickBtnAddTranslate(self, values = None) :
        #инициализация диалогового окна и установка дизайна (пустой layout)
        self.dialog = QDialog(self)
        self.dialog.ui = uic.loadUi('addTranslateDialog.ui', self.dialog)
        self.renderDialog()

    def renderDialog(self, values = None, key = None, type = 'save'):
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
                try:
                    lngInput = QtWidgets.QLineEdit(values[lang], objectName='inputField')
                except KeyError:
                    lngInput = QtWidgets.QLineEdit('', objectName='inputField')
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
        saveButton = QPushButton('Сохранить', objectName= 'saveButton' if type == 'save' else 'editButton')
        cancelButton = QPushButton('Отмена', objectName='cancelButton')
        # Обработчик нажатия  кнопок (отмена и сохранить)
        cancelButton.clicked.connect(self.cancelDialogClick)
        saveButton.clicked.connect(self.saveTranslateClick if type == 'save' else self.updateTranslateClick)
        buttonsRow.addWidget(cancelButton)
        buttonsRow.addWidget(saveButton)

        # Информационный текст
        infoRow = QHBoxLayout()
        info = QLabel('Внимание! При редактировании ключа будет создана новая запись в словаре!', objectName='dangerLabel')
        infoRow.addWidget(info)

        layout.addLayout(infoRow)
        layout.addStretch(1)
        layout.addLayout(buttonsRow)
        # Устанавливаем стили диалогового окна
        self.dialog.setStyleSheet(open("styles/qLineEdit.qss", "r").read())
        self.dialog.setLayout(layout)
        # Показываем диалоговое окно
        self.dialog.show()

    # Обновляем  перевод в файлы (словари)
    def updateTranslateClick(self):
        dialogData = {}
        # Собираем данные с формы (диалоговое окно)
        emptyInputError = False
        for dialogInput in range(self.dialog.layout().count()):
            if (self.dialog.layout().itemAt(dialogInput).__class__.__name__ == 'QHBoxLayout'):
                dialogItem = self.dialog.layout().itemAt(dialogInput)
                if (dialogItem.itemAt(1) is not None and dialogItem.itemAt(1).widget().property('name') != None):
                    # Ключ
                    name = self.dialog.layout().itemAt(dialogInput).itemAt(1).widget().property('name')
                    # Значение
                    value = self.dialog.layout().itemAt(dialogInput).itemAt(1).widget().text()
                    # Проверяем на наличие пустых полей
                    if (len(value) < 2):
                        emptyInputError = True
                    dialogData[name] = value
        # В случае пустоты хотя бы в одном из полей информируем пользователя
        if (emptyInputError):
            self.showMessage('Ошибка!', 'Не заполнены все поля', 'warning')
        else:
            newItem = {}
            langValueItem = {}
            # Записываем переводы в файлы локализаций
            for lang in self.langs:
                langValueItem[lang] = dialogData[lang]
            self.initDataVocabulary[dialogData['key']] = langValueItem


            # self.writeJson(self.vocabularyFileName, self.initDataVocabulary)
            Vocabulary.writeJson(self.vocabularyFileName, self.initDataVocabulary)

            self.showMessage('Обновлено', 'Перевод успешно обновлен!', 'info')
            # Очищаем поля ввода в диалоговом окне
            for dialogInput in range(self.dialog.layout().count()):
                if (self.dialog.layout().itemAt(dialogInput).__class__.__name__ == 'QHBoxLayout'):
                    dialogItem = self.dialog.layout().itemAt(dialogInput)
                    if (dialogItem.itemAt(1) is not None and dialogItem.itemAt(1).widget().property('name') != None):
                        self.dialog.layout().itemAt(dialogInput).itemAt(1).widget().setText('')
            horizontal = GUI.setRow(self, self.langs, dialogData, dialogData['key'], self.vocabularyLayout)
            self.initVocabulary()
            Vocabulary.indexVocabulary()

    # Сохраняем перевод в файлы (словари)
    def saveTranslateClick(self):
        dialogData = {}
        #Собираем данные с формы (диалоговое окно)
        emptyInputError = False
        for dialogInput in range(self.dialog.layout().count()):
            if(self.dialog.layout().itemAt(dialogInput).__class__.__name__ == 'QHBoxLayout') :
                dialogItem = self.dialog.layout().itemAt(dialogInput)
                if(dialogItem.itemAt(1) is not None and dialogItem.itemAt(1).widget().property('name') != None) :
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
            if (self.initDataVocabulary is None or len(self.initDataVocabulary) < 1):
                self.initDataVocabulary = {}
                self.initDataVocabulary[dialogData['key']] = langValueItem
                Vocabulary.initTableHeader(self.tableHeaderLayout)
                self.initVocabulary()
            else:
                self.initDataVocabulary[dialogData['key']] = langValueItem


            # self.writeJson(self.vocabularyFileName, self.initDataVocabulary)
            Vocabulary.writeJson(self.vocabularyFileName, self.initDataVocabulary)

            self.showMessage('Сохранено', 'Перевод успешно добавлен!', 'info')
            # Очищаем поля ввода в диалоговом окне
            for dialogInput in range(self.dialog.layout().count()):
                if(self.dialog.layout().itemAt(dialogInput).__class__.__name__ == 'QHBoxLayout') :
                    dialogItem = self.dialog.layout().itemAt(dialogInput)
                    if(dialogItem.itemAt(1) is not None and dialogItem.itemAt(1).widget().property('name') != None) :
                        self.dialog.layout().itemAt(dialogInput).itemAt(1).widget().setText('')
            horizontal = GUI.setRow(self, self.langs, dialogData, dialogData['key'], self.vocabularyLayout)
            self.initVocabulary()
            Vocabulary.indexVocabulary()

    # Закрываем диалоговое окно
    def cancelDialogClick(self):
        self.dialog.close()

    def to_json(self, inputJson):
        try:
            json_object = json.load(inputJson)
        except ValueError as e:
            return None
        return json_object

    ################------------------------####################
    ########****Запускаем работу скрипта(Laravel)****################
    ################------------------------####################
    def clickBtnRunLaravel(self):
        # try:
        #     print(os.path.expanduser('~'))
        #     sys.exit(0)
            functionArgs = {
                'lang': self.setting_main_lang,
                'progress_bar_item' : self.progressBarLaravel,
            }
            worker = Worker(Laravel.run, self.settingsLaravelRootDir, **functionArgs)
            worker.signals.progress.connect(Laravel.progressBar)
            # Execute
            self.threadpool.start(worker)
            # Laravel.run(self.settingsLaravelRootDir, self.setting_main_lang)
        # except FileNotFoundError as f:
        #     self.showMessage('Ошибка!', 'Не верно указан путь к файлу!', 'critical')


    def filter_values(self, x):
        if (re.findall(r'^{{.+}}$|^{!!.+!!}$|^@|^{{\s.+}}|^:{{.+}}$|^\+{{.+}}$', x)):
            return 0
        return 1

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