from bs4 import BeautifulSoup
import re

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
    if (re.findall(r'{{.+}}|->|{!!.+|.+!!}|{!!.+!!}|@|{{\s.+}}|:{{.+}}|\+{{.+}}', x)):
        return 0
    if len(x) < 2:
        return 0
    return 1