import requests
from utils_scraper import *
import time
import pandas as pd 

class requester():
    
    url = 'https://www.wordreference.com'
    
    path = {
        'en': '/es/translation.asp',
        'es': '/es/en/translation.asp'
    }
    
    languages = {
    'en':'tranword',
    'es':'spen'
    }
    
    headers = {
    'accept': '*/*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'es-ES,es;q=0.9,en;q=0.8,it;q=0.7',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
    }
    
    def __init__(self, s):
        self.s = s
        
    def update_headers(self):
        self.s.headers.update(requester.headers)
        
    def make_request(self, word, lang = 'en'):
        url2get = requester.url + requester.path[lang]
        param = requester.languages[lang]
        payload = {param:word}
        r = self.s.get(url2get, params = payload)
        return r


def search_word(requester, word, lang):
    r = requester.make_request(word = word, lang = lang)
    dict_word = scrape_word_info(r = r)
    dict_word['word'] = [word]
    return dict_word


def scrape_words(requester, words, lang):
    lista_words = []
    # i_error = 0
    # i_len = 0
    # len_list = len(words)
    for word in words:
        try:
            word_def = search_word(requester = requester, word = word, lang = lang)
            lista_words.append(word_def)
            print(f'{word} success!')
        except Exception as e:
            print(e)
#             print(f'{word} failed!')
        time.sleep(0.5)
    return lista_words


def scrape_batch(requester, words, lang, step = 100):
    result_list = []
    len_word = len(words)  
    while True:
        print(f'{len(result_list)} of {len_word}')
        words_it = words[:step]
        try:
            result_list.append(scrape_words(requester = requester, words = words_it, lang = lang))
            words = words[step:]
        except Exception as e:
            print(e)
            break
        if len(words) == 0:
            break
    return result_list

def process_list(result_list):
    net_list = [ pd.DataFrame(x) for x in result_list]
    df = pd.concat(net_list, sort = False)\
            .reset_index(drop = True)\
            .apply(pd.Series.explode)\
            .assign(FrEx=  lambda col: col['FrEx'].apply(lambda x: x[0] if len(x) > 0 else None),
                   ToEx = lambda col: col['ToEx'].apply(lambda x: x[0] if len(x) > 0 else None),
                    FrEx_len = lambda col: col['FrEx'].apply(lambda x: len(x.split()) if isinstance(x, str) else 0)
                    )
    return df