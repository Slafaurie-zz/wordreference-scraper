import requests
from utils_scraper import *
import time

url_dict = {

    'enes': 'https://www.wordreference.com/es/translation.asp?tranword=',
    'esen': 'https://www.wordreference.com/es/en/translation.asp?spen='
    }


def init_session(requests, headers):
    
    s = requests.session()
    
    s.headers.update(headers)
    
    return s

def make_request(s, word, languages):

    url = url_dict[languages] + word

    r = s.get(url)

    print(r)

    return r


def search_word(s, word, languages):

    r = make_request(s = s, word = word, languages = languages)

    dict_word = scrape_word_info(r = r)

    dict_word['word'] = [word]

    return dict_word


def scrape_words(s, words, languages):
    
    lista_words = []

    # i_error = 0
    # i_len = 0
    # len_list = len(words)

    for word in words:

        try:

            word_def = search_word(s = s, word = word, languages = languages)

            lista_words.append(word_def)

            print(f'{word} success!')

        except:

            print(f'{word} failed!')


        time.sleep(1)
        
    return lista_words


def scrape_batch(s, words, languages, step = 100):

    result_list = []

    len_word = len(words)  

    while True:
        
        print(f'{len(result_list)} of {len_word}')

        words_it = words[:step]

        try:
            result_list.append(scrape_words(s = s, words = words_it, languages = languages))
        
            words = words[step:]
        
        except:

            break

        if len(words) == 0:
            
            break

    return result_list