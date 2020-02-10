from bs4 import BeautifulSoup
import re
from os.path import isfile
import sys

def getFromHtml(input):
    soup = BeautifulSoup(input, 'html.parser')
    for script in soup(["script", "style"]):
        script.extract()  # rip it out
    text = soup.get_text()
    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = [c for c in filter(None, lines)]
    return chunks

def getFileContent(pathAndFileName):
    with open(pathAndFileName, 'r') as theFile:
        data = theFile.read()
        return data

def filterValuesLaravel(x):
    if (re.findall(r'{{.+}}|->|=>|\]\)|{!!.+|.+!!}|{!!.+!!}|@|{{\s.+}}|:{{.+}}|\+{{.+}}', x)):
        return 0
    if len(x) < 2:
        return 0
    return 1

################------------------------####################
###*****Парсинг файла переводов Laravel (PHP массив)****####
################------------------------####################
def parseLaravelLangFile(filePath):
    if isfile(filePath):
        # Получаем содержимое файла
        fContent = getFileContent(filePath)
        # Разбираем его на строки
        regExpInputs = re.findall(r'\'.+,|\".+,', fContent)
        # Парсим непосредственно сами переводы и помещаем в словарь (key : value)
        fContentDict = prepareLaravelLangFileData(regExpInputs)
        print(fContentDict)
        sys.exit(0)

################------------------------####################
#**Формирование словаря (python) из файла переводов (PHP)**#
################------------------------####################
def prepareLaravelLangFileData(regExpInputs):
    data = {}
    if (len(regExpInputs) > 0):
        for reItem in regExpInputs:
            reItemSplit = reItem.split('=>')
            key = re.search(r'\'.+\'|\".+\"', reItemSplit[0]).group(0).replace("'", '').replace('"', '')
            value = re.search(r'\'.+\'|\".+\"', reItemSplit[1]).group(0).replace("'", '').replace('"', '')
            data.update({key: value})
        return data
    return None