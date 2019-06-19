import configparser
from PyQt5 import QtWidgets, uic, QtCore
import sys
import html_design
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

class HtmlTranslator(QtWidgets.QMainWindow, html_design.Ui_MainWindow):
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

        #Обработчики нажатия кнопок
        self.btn_run.clicked.connect(self.click_btn_run)
        self.btn_save_settings.clicked.connect(self.click_btn_save_settings)
        self.btn_translate_file.clicked.connect(self.click_btn_translate_file)

        #Обработчик события изменение позиции курсора
        #self.main_input.cursorPositionChanged.connect(self.changeInput)

    def load_settings(self):
        # Читаем настройки из файла
        self.settings_path = 'settings.ini'
        if os.path.exists(self.settings_path):
            settings = configparser.ConfigParser()
            settings.read(self.settings_path)
            # GENERAL
            self.setting_langs = settings.get('GENERAL', 'LANGS')
            self.setting_main_lang = settings.get('GENERAL', 'MAIN_LANG')
            self.setting_file_translates = settings.get('GENERAL', 'FILE_TRANSLATES')
            self.setting_l_placeholder = settings.get('GENERAL', 'LEFT_PLACEHOLDER')
            self.setting_r_placeholder = settings.get('GENERAL', 'RIGHT_PLACEHOLDER')
            # DB
            self.setting_db_user = settings.get('DB', 'DB_USER')
            self.setting_db_name = settings.get('DB', 'DB_NAME')
            self.setting_db_pass = settings.get('DB', 'DB_PASS')

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
        #Плейсхолдеры
        l_placeholder = self.l_placeholder.text()
        r_placeholder = self.r_placeholder.text()

        #Подтверждение сохранения настроек
        buttonReply = QtWidgets.QMessageBox.question(self, 'Изменение настроек', "Сохранить выбранные настройки?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if buttonReply == QtWidgets.QMessageBox.Yes:
            settings = configparser.ConfigParser()

            settings['GENERAL'] = {
                'LANGS':                '|'.join(langs),
                'MAIN_LANG':            m_lang,
                'FILE_TRANSLATES':      file_translates,
                'LEFT_PLACEHOLDER':     l_placeholder,
                'RIGHT_PLACEHOLDER':    r_placeholder,
            }

            settings['DB'] = {
                'DB_USER': db_user,
                'DB_NAME': db_name,
                'DB_PASS': db_pass,
            }
            with open(self.settings_path, "w") as config_file:
                settings.write(config_file)
            self.load_settings()

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

    ################------------------------####################
    ############****Запускаем работу скрипта****################
    ################------------------------####################
    def click_btn_run(self):
        # mb = QtWidgets.QMessageBox()
        # mb.setIcon(QtWidgets.QMessageBox.Information)
        # mb.setWindowTitle('Job done!')
        # mb.setText('Copy and past content from input to template.')
        # mb.setStandardButtons(QtWidgets.QMessageBox.Ok)
        # mb.show()
        # Получаем все переводы из файла
        translate_file_content = check_output(['php', '-r', 'include "' + self.setting_file_translates + '"; echo json_encode($l);'])
        translate_file_content = json.loads(translate_file_content)
        # print(translate_file_content)
        # sys.exit(0)

        #Введенный фрагмент
        self.input = self.output = self.main_input.toPlainText()
        soup = BeautifulSoup(self.input, 'html.parser')
        for script in soup(["script", "style"]):
            script.extract()  # rip it out
        text = soup.get_text()
        # break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # break multi-headlines into a line each
        chunks = [c for c in filter(None, lines)]

        #Массив с переводами которые уже есть в БД (и которые не нужно будет переводить)
        exist_translates = DB.check_translates(self.setting_db_name, self.setting_db_user, self.setting_db_pass, self.setting_main_lang, chunks)

        #Подставляем ID существующих переводов, и удаляем эти элементы из списка (chunks)
        if(len(exist_translates) > 0) :
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
        langs       = self.setting_langs.split('|')
        for item in chunks:
            translate_file_string = []
            translate_dic = {}
            translate_dic[self.setting_main_lang] = item

            #строка для файла переводов
            translate_file_string = []
            for lang in langs:
                new_translate = translator.translate(item, src=self.setting_main_lang, dest=lang).text
                translate_dic[lang] = new_translate                # Пауза для гугла
                sleep(3)

            # для запроса в базу (корректировка языков)
            correct_lang_sql = []
            #значения для записи в базу
            string_sql_values = []
            for item in translate_dic.items() :
                print(item[0] + '--------' + item[1])
                correct_lang_sql.append(DB.lang_field_connector(item[0]))
                string_sql_values.append("'" + item[1] + "'")
                # Строка для записи в файл переводов
                translate_file_string.append('"' + item[0] + '": "' + item[1] + '"')
            langs_sql = ','.join(correct_lang_sql)
            string_sql_values = ','.join(string_sql_values)

            # Запись в БД
            sql = "INSERT INTO modx_a_lang (" + langs_sql + ") VALUES (" + string_sql_values + ");"
            #values = (translate_dic["uk"], translate_dic["ru"], translate_dic["en"]);
            last_id = DB.add_translate(self.setting_db_name, self.setting_db_user, self.setting_db_pass, sql)

            # Запись в файл переводов
            translate_file_string = '{' + ','.join(translate_file_string) + '}'
            translate_file_string = json.loads(translate_file_string)

            # Добавление нового перевода в строку json переводов
            translate_file_content[last_id] = translate_file_string
            self.output = self.output.replace(translate_dic[self.setting_main_lang], "[#" + str(last_id) + "#]")

        self.write_to_file(translate_file_content, self.setting_file_translates)
        #subprocess.call(['chmod', '0777', '"' + self.setting_file_translates + '"'])
        self.main_input.setPlainText(self.output)


#Основная функция приложения
def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    win = HtmlTranslator()  # Создаём объект класса HtmlTranslator
    win.show()  # Показываем окно
    sys.exit(app.exec())
#Если запуск из скрипта (не импорт) выполняем функцию
if __name__ == '__main__' :
    main()