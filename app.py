import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
from utils_scraper import *
from utils_app import *
import os

wordref_req = requester(requests.session())
wordref_req.update_headers()

path_file = input("Enter the file path wich contain the word to lookup: ")

lang = input('Enter the languages (en and es supported): ')

############
words = pd.read_excel(path_file).iloc[:,0].values

result_list = scrape_batch(requester = wordref_req, words = words, lang = lang)

############
df = process_list(result_list)

path_save = os.path.dirname(path_file) + '/results.xlsx'

df.to_excel(path_save, index = False, encoding = 'latin-1')

print('Saved')
