import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
from utils_scraper import *
from utils_app import *
import os

###########
headers = {
    'accept': '*/*',
'accept-encoding': 'gzip, deflate, br',
'accept-language': 'es-ES,es;q=0.9,en;q=0.8,it;q=0.7',
'sec-fetch-dest': 'empty',
'sec-fetch-mode': 'cors',
'sec-fetch-site': 'same-origin',
'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
    }


s = init_session(requests, headers)

path_file = input("Enter the file path wich contain the word to lookup: ")

languages = input('Enter the languages (esen and enes supported): ')


############
words = pd.read_excel(path_file).iloc[:,0].values

result_list = scrape_batch(s = s, words = words, languages = languages)

############
net_list = [ pd.DataFrame(x) for x in result_list]

df = pd.concat(net_list, sort = False)\
.reset_index(drop = True)\
.apply(pd.Series.explode)\
.assign(FrEx=  lambda col: col['FrEx'].apply(lambda x: x[0] if len(x) > 0 else None),
       ToEx = lambda col: col['ToEx'].apply(lambda x: x[0] if len(x) > 0 else None),
        FrEx_len = lambda col: col['FrEx'].apply(lambda x: len(x.split()) if isinstance(x, str) else 0)
                                           )

path_save = os.path.dirname(path_file) + '/results.xlsx'

df.to_excel(path_save, index = False, encoding = 'latin-1')

print('Saved')

