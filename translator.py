import json
import os
from googletrans import Translator
import copy
import time
import httpx

nations= ['CH', 'DE', 'FR', 'IT', 'UK', 'US']
edition_str_len= 15


nation_to_lang= {'CH': 'fr',
                 'DE': 'de',
                 'FR': 'en',
                 'IT': 'it',
                 'UK': 'en',
                 'US': 'en'}

#A utility function which allows me to print Unicode encoded chars
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

#function who translates a given string into a given language
#currently not used due to the very slow running of googletrans lib
def to_english(new, lang):
    curr_news_en= copy.deepcopy(new)
    service_urls=['translate.google.com']
    timeout = httpx.Timeout(5)
    translator = Translator(service_urls= service_urls, timeout= timeout)
    translator.raise_Exception = True
    if lang != "en":
        curr_news_en['en_title']= translator.translate(new['title'], src= lang, dest= "en").text
    else:
        curr_news_en['en_title']= curr_news_en['title']
    print(curr_news_en)
    try:
        if lang != "en":
            curr_news_en['en_content']= translator.translate(new['content'], dest= "en").text
        else:
            curr_news_en['en_content']= curr_news_en['content']
    except:
        pass
    return curr_news_en

#Function which populates arrays of news, based on eidition or flow type of news
def news_translator(nation):
    directory= "../newScraping/collectedNews/" + nation
    for subdir in os.scandir(directory):
        newspaper= subdir.name
        for news in os.scandir(subdir):
            print(news.name)
            if news.name[0:2] != "en" and news.name[0:2] != "co":
                f= open(directory + "/" + newspaper + "/" + news.name, "r+", encoding= "latin-1")            
                curr_news= json.load(f)
                curr_edit= []
                #adding new conceptual informations to the news
                for curr_new in curr_news:
                    if curr_new['title'] != None:
                        curr_new['language']= nation_to_lang[nation]
                        curr_new['source']= newspaper
                        curr_new['filename']= news.name
                        lang= nation_to_lang[nation]
                        time.sleep(0.1)
                        #now create a hardcopy in order to have the same new, but in English
                        curr_news_en= to_english(curr_new, lang)
                        curr_edit.append(curr_news_en)
                f.close()
                #replacing the old news-file with a new one with english content added
                os.remove(directory + "/" + newspaper + "/" + news.name)
                f= open(directory + "/" + newspaper + "/en_" + news.name, "w")
                json.dump(curr_edit, f, indent= 4, ensure_ascii= False)
                f.close()

for nation in nations:
    news_translator(nation)