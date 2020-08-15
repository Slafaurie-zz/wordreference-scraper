from bs4 import BeautifulSoup

def remove_dup(lista):

    unique = []
    
    for i in lista:
        
        if i not in unique:
            
            unique.append(i)
            
    return unique


def get_definitions_cells(table):
        
   return table.find_all(lambda tag: tag.name =='tr' and  tag.has_attr('id'))


def get_parents(r):
    
    table =  BeautifulSoup(r.text, 'lxml').find("table", class_='WRD')
    
    definitions = get_definitions_cells(table)
    
    return definitions


def get_siblings(parent):

    class_check = parent.get('class')

    class_i = class_check

    ejemplos = []

    for sibling in parent.next_siblings:
        
        "when class changes, break form the loop"

        if class_i != class_check:

            break

        try:
            
            " Avoid \n, only append .tag"

            class_i = sibling.get('class')

            ejemplos.append(sibling)

        except:

            pass
        
    return ejemplos

    
def get_FrWord(parent):
    
    text = parent.find('strong').text
    
    if text[-1] == '⇒':
        
        return text[:-1]
    
    else: 
        
        return text


def get_nuance(parent):
    
    raw = parent.find_all('td')[1].text
    
    left,right = raw.find("("), raw.find(")")
    
    return raw[left+1:right]


def get_ToWord(parent):
    
    return parent.find_all('td')[2].find(text = True)


def get_pos(parent):
    
    return parent.find('i').text


def get_pos_ToWord(parent):
    return parent.find_all('i')[-1].text
    

def get_FrEx(siblings):

    ex_list = [x.find('td', class_ = 'FrEx') for x in siblings if x.find('td', class_ = 'FrEx')]

    return [x.text for x in ex_list]


def get_ToEx(siblings):

    ex_list = [x.find('td', class_ = 'ToEx') for x in siblings if x.find('td', class_ = 'ToEx')]

    return [x.text for x in ex_list]


def scrape_word_info(r):
    
    dict_word = {}

    parents = get_parents(r)

    siblings= [get_siblings(x) for x in parents ]

    dict_word['FrWord'] = [get_FrWord(x) for x in parents]
    
    dict_word['pos_FrWord'] = [get_pos(x) for x in parents]

    dict_word['nuance'] = [get_nuance(x) for x in parents]

    dict_word['ToWord'] = [get_ToWord(x) for x in parents]
    
    dict_word['pos_ToWord'] = [get_pos_ToWord(x) for x in parents]
    
    dict_word['FrEx'] = [get_FrEx(x) for x in siblings]

    dict_word['ToEx'] = [get_ToEx(x) for x in siblings]
    
    return dict_word
