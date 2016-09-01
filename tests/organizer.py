import argparse
import csv
import os
from bs4 import BeautifulSoup


parser = argparse.ArgumentParser(description='Inspect project code')
path = '.'
counter = 0
for (dirpath, dirnames, filenames) in os.walk(path):
    if filename == 'views.py':
        pass
    for filename in filenames:
        print(dirpath+'\\'+filename)
        # if filename.endswith(".html"):     counter += 1
