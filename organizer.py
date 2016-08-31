from os import walk
from html.parser import HTMLParser
import csv
from bs4 import BeautifulSoup


def write_out(result):
    with open('html.csv', 'w') as f:
        w = csv.DictWriter(f, result.keys())
        # w.writeheader()
        w.writerow(result)


class MyHTMLParser(HTMLParser):
    """docstring for MyHTMLParser"""
    def handle_starttag(self, tag, attrs):
        for name, value in attrs:
            if name == 'class':
                print(value, 'in', tag)

    # def handle_endtag(self, tag):
    #     print("Encountered an end tag :", tag)

    # def handle_data(self, data):
    #     print("Encountered some data  :", data)

try:
    f = open(r"C:\Users\Arvind\Documents\GitHub\industryo\templates\base.html")
    print(f)
finally:
    f.close()

with open(r"C:\Users\Arvind\Documents\GitHub\industryo\templates\base.html") as f:
    data = f.read().replace('\n', '')

parser = MyHTMLParser()
parser.feed(data)
path = '.'
counter = 0
for (dirpath, dirnames, filenames) in walk(path):
    if filename == 'views.py':
        pass
    for filename in filenames:
        print(dirpath+'\\'+filename)
        # if filename.endswith(".html"):     counter += 1
