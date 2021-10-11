import json
import datetime
import os
from googletrans import Translator
import copy
import time


nations= ['CH', 'DE', 'FR', 'IT', 'UK', 'US']
edition_str_len= 15

nation_to_lang= {'CH': 'fr',
                 'DE': 'de',
                 'FR': 'fr',
                 'IT': 'it',
                 'UK': 'en',
                 'US': 'en'}

editions= []
flow= []
editions_en= []
flow_en= []
#A utility function which allow me to print Unicode encoded chars
def unicode_fix(to_fix):
    for news in to_fix:
        for new in news:
            for dict_attr in new:
                try:
                    new[dict_attr]= new[dict_attr].encode("ascii", errors= "ignore").decode("ascii")
                #in case there are ints and not strings
                except:
                    pass
    return to_fix


def to_english(new, lang):
    curr_news_en= copy.deepcopy(new)
    service_urls=['translate.google.com']
    translator = Translator(service_urls= service_urls)
    translator.raise_Exception = True
    print("aaaa")
    curr_news_en['title']= translator.translate(new['title'], src= lang, dest= "en").text
    print(curr_news_en)
    try:
        curr_news_en['content']= translator.translate(new['content'], dest= "en").text
    except:
        pass
    return curr_news_en

#Function which populates arrays of news, based on eidition or flow type of news
def news_finder(nation):
    directory= "..\\D_Coll\\collectedNews\\" + nation
    for subdir in os.scandir(directory):
        newspaper= subdir.name
        for news in os.scandir(subdir):
            f= open(directory + "\\" + newspaper + "\\" + news.name, "r+")
            curr_news= json.load(f)
            #adding new conceptual informations to the news
            for curr_new in curr_news:
                curr_new['nation']= nation
                curr_new['source']= newspaper
                curr_new['filename']= news.name
            lang= nation_to_lang[nation]
            if lang != 'en':
                #now create a hardcopy in order to have the same new, but in English
                curr_news_en= to_english(curr_new, lang)
            if len(news.name) == edition_str_len:
                editions.append(curr_news)
                editions.append(curr_news_en)
                print(curr_news_en)
            else:
                flow.append(curr_news)
                flow.append(curr_news_en)
 

print("aaaaassss")
for nation in nations:
    news_finder(nation)
flow= unicode_fix(flow)
print(editions_en)
print(flow_en)
