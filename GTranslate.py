from googletrans        import Translator
import sys
from time               import sleep
import re


def getGTranslateApi(item, currLang, langs):
    translator = Translator()
    translator.session.proxies['http'] = '125.26.109.83:8141'
    translator.session.proxies['http'] = '98.221.88.193:64312'
    translator.session.proxies['http'] = '188.244.35.162:10801'
    translator.session.proxies['http'] = '185.162.0.110:10801'
    translate_dic = {}
    result = {}
    translate_dic[currLang] = item
    for lang in langs:
        new_translate = translator.translate(item, src=currLang, dest=lang).text
        translate_dic[lang] = new_translate  # Пауза для гугла
        sleep(3)
    return translate_dic