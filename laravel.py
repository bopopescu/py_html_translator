# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'laravel.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1043, 876)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.laravel = QtWidgets.QWidget()
        self.laravel.setObjectName("laravel")
        self.btnRunLaravel = QtWidgets.QPushButton(self.laravel)
        self.btnRunLaravel.setGeometry(QtCore.QRect(15, 195, 111, 35))
        self.btnRunLaravel.setStyleSheet("border-radius: 5px; \n"
"background-color: black;\n"
"color: white;")
        self.btnRunLaravel.setObjectName("btnRunLaravel")
        self.progressBarLaravel = QtWidgets.QProgressBar(self.laravel)
        self.progressBarLaravel.setGeometry(QtCore.QRect(140, 195, 856, 36))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 128, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 128, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 128, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Highlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255, 128))
        brush.setStyle(QtCore.Qt.NoBrush)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.PlaceholderText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 128, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 128, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 128, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Highlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 128, 0, 128))
        brush.setStyle(QtCore.Qt.NoBrush)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.PlaceholderText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 128, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 128, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 128, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(145, 145, 145))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Highlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255, 128))
        brush.setStyle(QtCore.Qt.NoBrush)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.PlaceholderText, brush)
        self.progressBarLaravel.setPalette(palette)
        self.progressBarLaravel.setStyleSheet("color: green;")
        self.progressBarLaravel.setMaximum(100)
        self.progressBarLaravel.setProperty("value", 0)
        self.progressBarLaravel.setObjectName("progressBarLaravel")
        self.translated = QtWidgets.QLabel(self.laravel)
        self.translated.setGeometry(QtCore.QRect(25, 25, 196, 17))
        self.translated.setObjectName("translated")
        self.translated_2 = QtWidgets.QLabel(self.laravel)
        self.translated_2.setGeometry(QtCore.QRect(25, 110, 86, 17))
        self.translated_2.setObjectName("translated_2")
        self.current_file = QtWidgets.QLabel(self.laravel)
        self.current_file.setGeometry(QtCore.QRect(125, 110, 866, 17))
        self.current_file.setText("")
        self.current_file.setObjectName("current_file")
        self.translated_3 = QtWidgets.QLabel(self.laravel)
        self.translated_3.setGeometry(QtCore.QRect(25, 150, 231, 17))
        self.translated_3.setObjectName("translated_3")
        self.total_items_count = QtWidgets.QLabel(self.laravel)
        self.total_items_count.setGeometry(QtCore.QRect(235, 25, 46, 17))
        self.total_items_count.setText("")
        self.total_items_count.setObjectName("total_items_count")
        self.translated_4 = QtWidgets.QLabel(self.laravel)
        self.translated_4.setGeometry(QtCore.QRect(25, 65, 186, 17))
        self.translated_4.setObjectName("translated_4")
        self.items_count_current_file = QtWidgets.QLabel(self.laravel)
        self.items_count_current_file.setGeometry(QtCore.QRect(230, 60, 46, 17))
        self.items_count_current_file.setText("")
        self.items_count_current_file.setObjectName("items_count_current_file")
        self.current_file_current_item = QtWidgets.QLabel(self.laravel)
        self.current_file_current_item.setGeometry(QtCore.QRect(265, 150, 46, 17))
        self.current_file_current_item.setText("")
        self.current_file_current_item.setObjectName("current_file_current_item")
        self.translated_5 = QtWidgets.QLabel(self.laravel)
        self.translated_5.setGeometry(QtCore.QRect(335, 150, 21, 17))
        self.translated_5.setObjectName("translated_5")
        self.current_file_total_item = QtWidgets.QLabel(self.laravel)
        self.current_file_total_item.setGeometry(QtCore.QRect(380, 150, 46, 17))
        self.current_file_total_item.setText("")
        self.current_file_total_item.setObjectName("current_file_total_item")
        self.tabWidget.addTab(self.laravel, "")
        self.settings = QtWidgets.QWidget()
        self.settings.setObjectName("settings")
        self.de_l = QtWidgets.QLabel(self.settings)
        self.de_l.setGeometry(QtCore.QRect(100, 130, 16, 17))
        self.de_l.setObjectName("de_l")
        self.btn_save_settings = QtWidgets.QPushButton(self.settings)
        self.btn_save_settings.setGeometry(QtCore.QRect(830, 445, 171, 35))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255, 128))
        brush.setStyle(QtCore.Qt.NoBrush)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.PlaceholderText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255, 128))
        brush.setStyle(QtCore.Qt.NoBrush)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.PlaceholderText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255, 128))
        brush.setStyle(QtCore.Qt.NoBrush)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.PlaceholderText, brush)
        self.btn_save_settings.setPalette(palette)
        self.btn_save_settings.setStyleSheet("border-radius: 5px; \n"
"background-color: black;\n"
"color: white;")
        self.btn_save_settings.setObjectName("btn_save_settings")
        self.en_l = QtWidgets.QLabel(self.settings)
        self.en_l.setGeometry(QtCore.QRect(100, 90, 16, 17))
        self.en_l.setObjectName("en_l")
        self.main_lang = QtWidgets.QComboBox(self.settings)
        self.main_lang.setGeometry(QtCore.QRect(290, 70, 86, 35))
        self.main_lang.setStyleSheet("border-radius: 5px; \n"
"background-color: #FCE94F;\n"
"color: black;")
        self.main_lang.setObjectName("main_lang")
        self.main_lang.addItem("")
        self.main_lang.addItem("")
        self.main_lang.addItem("")
        self.main_lang.addItem("")
        self.label_5 = QtWidgets.QLabel(self.settings)
        self.label_5.setGeometry(QtCore.QRect(160, 75, 121, 21))
        font = QtGui.QFont()
        font.setFamily("KacstTitle")
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.ru_l = QtWidgets.QLabel(self.settings)
        self.ru_l.setGeometry(QtCore.QRect(100, 70, 16, 17))
        self.ru_l.setObjectName("ru_l")
        self.uk = QtWidgets.QCheckBox(self.settings)
        self.uk.setGeometry(QtCore.QRect(80, 110, 16, 23))
        self.uk.setText("")
        self.uk.setObjectName("uk")
        self.label_4 = QtWidgets.QLabel(self.settings)
        self.label_4.setGeometry(QtCore.QRect(20, 70, 51, 21))
        font = QtGui.QFont()
        font.setFamily("KacstTitle")
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.ua_l = QtWidgets.QLabel(self.settings)
        self.ua_l.setGeometry(QtCore.QRect(100, 110, 16, 17))
        self.ua_l.setObjectName("ua_l")
        self.en = QtWidgets.QCheckBox(self.settings)
        self.en.setGeometry(QtCore.QRect(80, 90, 16, 23))
        self.en.setText("")
        self.en.setObjectName("en")
        self.de = QtWidgets.QCheckBox(self.settings)
        self.de.setGeometry(QtCore.QRect(80, 130, 16, 23))
        self.de.setText("")
        self.de.setObjectName("de")
        self.ru = QtWidgets.QCheckBox(self.settings)
        self.ru.setGeometry(QtCore.QRect(80, 70, 16, 23))
        self.ru.setText("")
        self.ru.setObjectName("ru")
        self.label_10 = QtWidgets.QLabel(self.settings)
        self.label_10.setGeometry(QtCore.QRect(20, 170, 66, 17))
        font = QtGui.QFont()
        font.setFamily("KacstTitle")
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.line_2 = QtWidgets.QFrame(self.settings)
        self.line_2.setGeometry(QtCore.QRect(20, 180, 971, 16))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.laravelRootDir = QtWidgets.QLineEdit(self.settings)
        self.laravelRootDir.setGeometry(QtCore.QRect(230, 295, 761, 35))
        self.laravelRootDir.setStyleSheet("border-radius: 5px; \n"
"background-color: #FCE94F;\n"
"color: black;\n"
"padding-left: 5px;\n"
"padding-right: 5px;")
        self.laravelRootDir.setObjectName("laravelRootDir")
        self.btnLaravelRoot = QtWidgets.QPushButton(self.settings)
        self.btnLaravelRoot.setGeometry(QtCore.QRect(20, 295, 191, 35))
        self.btnLaravelRoot.setStyleSheet("border-radius: 5px; \n"
"background-color: black;\n"
"color: white;")
        self.btnLaravelRoot.setFlat(False)
        self.btnLaravelRoot.setObjectName("btnLaravelRoot")
        self.line_3 = QtWidgets.QFrame(self.settings)
        self.line_3.setGeometry(QtCore.QRect(20, 30, 971, 16))
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.label_11 = QtWidgets.QLabel(self.settings)
        self.label_11.setGeometry(QtCore.QRect(20, 20, 66, 17))
        font = QtGui.QFont()
        font.setFamily("KacstTitle")
        self.label_11.setFont(font)
        self.label_11.setObjectName("label_11")
        self.leftLaravelPlaceholder = QtWidgets.QLineEdit(self.settings)
        self.leftLaravelPlaceholder.setGeometry(QtCore.QRect(205, 215, 113, 35))
        self.leftLaravelPlaceholder.setStyleSheet("border-radius: 5px; \n"
"background-color: #FCE94F;\n"
"color: black;\n"
"padding-left: 5px;\n"
"padding-right: 5px;")
        self.leftLaravelPlaceholder.setObjectName("leftLaravelPlaceholder")
        self.label_12 = QtWidgets.QLabel(self.settings)
        self.label_12.setGeometry(QtCore.QRect(20, 225, 171, 21))
        font = QtGui.QFont()
        font.setFamily("KacstTitle")
        self.label_12.setFont(font)
        self.label_12.setObjectName("label_12")
        self.label_13 = QtWidgets.QLabel(self.settings)
        self.label_13.setGeometry(QtCore.QRect(345, 225, 176, 21))
        font = QtGui.QFont()
        font.setFamily("KacstTitle")
        self.label_13.setFont(font)
        self.label_13.setObjectName("label_13")
        self.rightLaravelPlaceholder = QtWidgets.QLineEdit(self.settings)
        self.rightLaravelPlaceholder.setGeometry(QtCore.QRect(530, 215, 113, 35))
        self.rightLaravelPlaceholder.setStyleSheet("border-radius: 5px; \n"
"background-color: #FCE94F;\n"
"color: black;\n"
"padding-left: 5px;\n"
"padding-right: 5px;")
        self.rightLaravelPlaceholder.setObjectName("rightLaravelPlaceholder")
        self.laravelRootDirLang = QtWidgets.QLineEdit(self.settings)
        self.laravelRootDirLang.setGeometry(QtCore.QRect(230, 370, 761, 35))
        self.laravelRootDirLang.setStyleSheet("border-radius: 5px; \n"
"background-color: #FCE94F;\n"
"color: black;\n"
"padding-left: 5px;\n"
"padding-right: 5px;")
        self.laravelRootDirLang.setObjectName("laravelRootDirLang")
        self.btnLaravelRootLang = QtWidgets.QPushButton(self.settings)
        self.btnLaravelRootLang.setGeometry(QtCore.QRect(20, 370, 191, 35))
        self.btnLaravelRootLang.setStyleSheet("border-radius: 5px; \n"
"background-color: black;\n"
"color: white;")
        self.btnLaravelRootLang.setFlat(False)
        self.btnLaravelRootLang.setObjectName("btnLaravelRootLang")
        self.label_14 = QtWidgets.QLabel(self.settings)
        self.label_14.setGeometry(QtCore.QRect(425, 265, 266, 21))
        font = QtGui.QFont()
        font.setFamily("KacstTitle")
        self.label_14.setFont(font)
        self.label_14.setObjectName("label_14")
        self.label_15 = QtWidgets.QLabel(self.settings)
        self.label_15.setGeometry(QtCore.QRect(425, 345, 266, 21))
        font = QtGui.QFont()
        font.setFamily("KacstTitle")
        self.label_15.setFont(font)
        self.label_15.setObjectName("label_15")
        self.tabWidget.addTab(self.settings, "")
        self.vocabulary = QtWidgets.QWidget()
        self.vocabulary.setObjectName("vocabulary")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.vocabulary)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(5, 60, 1006, 41))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.tableHeaderLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.tableHeaderLayout.setContentsMargins(0, 0, 0, 0)
        self.tableHeaderLayout.setObjectName("tableHeaderLayout")
        self.addTranslate = QtWidgets.QPushButton(self.vocabulary)
        self.addTranslate.setGeometry(QtCore.QRect(905, 10, 111, 35))
        self.addTranslate.setStyleSheet("border-radius: 5px; \n"
"background-color: black;\n"
"color: white;")
        self.addTranslate.setObjectName("addTranslate")
        self.scrollArea = QtWidgets.QScrollArea(self.vocabulary)
        self.scrollArea.setGeometry(QtCore.QRect(5, 110, 1006, 631))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 1004, 629))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents_2)
        self.verticalLayoutWidget_3 = QtWidgets.QWidget(self.vocabulary)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(5, 750, 1006, 26))
        self.verticalLayoutWidget_3.setObjectName("verticalLayoutWidget_3")
        self.vocabularyLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_3)
        self.vocabularyLayout.setContentsMargins(0, 0, 0, 0)
        self.vocabularyLayout.setObjectName("vocabularyLayout")
        self.tabWidget.addTab(self.vocabulary, "")
        self.verticalLayout.addWidget(self.tabWidget)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1043, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "PyHtmlTranslate"))
        self.btnRunLaravel.setText(_translate("MainWindow", "Начать"))
        self.translated.setText(_translate("MainWindow", "Общее кол-во элементов :"))
        self.translated_2.setText(_translate("MainWindow", "Перевожу :"))
        self.translated_3.setText(_translate("MainWindow", "Переведено (в текущем файле)"))
        self.translated_4.setText(_translate("MainWindow", "Кол-во в текущем файле :"))
        self.translated_5.setText(_translate("MainWindow", "из"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.laravel), _translate("MainWindow", "Laravel"))
        self.de_l.setText(_translate("MainWindow", "de"))
        self.btn_save_settings.setText(_translate("MainWindow", "Сохранить настройки"))
        self.en_l.setText(_translate("MainWindow", "en"))
        self.main_lang.setItemText(0, _translate("MainWindow", "ru"))
        self.main_lang.setItemText(1, _translate("MainWindow", "en"))
        self.main_lang.setItemText(2, _translate("MainWindow", "ua"))
        self.main_lang.setItemText(3, _translate("MainWindow", "de"))
        self.label_5.setText(_translate("MainWindow", "Основной язык"))
        self.ru_l.setText(_translate("MainWindow", "ru"))
        self.label_4.setText(_translate("MainWindow", "Языки"))
        self.ua_l.setText(_translate("MainWindow", "ua"))
        self.label_10.setText(_translate("MainWindow", "Laravel"))
        self.btnLaravelRoot.setText(_translate("MainWindow", "Выбрать директорию"))
        self.label_11.setText(_translate("MainWindow", "Общие"))
        self.label_12.setText(_translate("MainWindow", "Левый плейсхолдер"))
        self.label_13.setText(_translate("MainWindow", "Правый плейсхолдер"))
        self.btnLaravelRootLang.setText(_translate("MainWindow", "Выбрать директорию"))
        self.label_14.setText(_translate("MainWindow", "Корневая директория шаблонов"))
        self.label_15.setText(_translate("MainWindow", "Корневая директория переводов"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.settings), _translate("MainWindow", "Настройки"))
        self.addTranslate.setText(_translate("MainWindow", "Добавить"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.vocabulary), _translate("MainWindow", "Словарь"))
