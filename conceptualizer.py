import json
import datetime
import os
from googletrans import Translator
import copy
import time
import httpx
import spacy

nations= ['CH', 'DE', 'FR', 'IT', 'UK', 'US']
edition_str_len= 15


nation_to_lang= {'CH': 'fr',
                 'DE': 'de',
                 'FR': 'fr',
                 'IT': 'it',
                 'UK': 'en',
                 'US': 'en'}


fr_nlp= spacy.load("fr_core_news_sm")
de_nlp= spacy.load("fr_core_news_sm")
it_nlp= spacy.load("it_core_news_sm")
en_nlp= spacy.load("en_core_web_sm")

nlp_dict= {'CH': fr_nlp,
           'FR': fr_nlp,
           'DE': de_nlp,
           'UK': en_nlp,
           'US': en_nlp,
           'IT': it_nlp}

editions= []
flow= []
editions_en= []
flow_en= []
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


def create_concept(word, meaning, pos):
    concept= {'word': word, 'meaning': meaning, 'pos': pos}
    return concept

#function who translates a given string into a given language
#currently not used due to the very slow running of googletrans lib
def to_english(new, lang):
    curr_news_en= copy.deepcopy(new)
    service_urls=['translate.google.com']
    timeout = httpx.Timeout(5)
    translator = Translator(service_urls= service_urls, timeout= timeout)
    translator.raise_Exception = True
    curr_news_en['title']= translator.translate(new['title'], src= lang, dest= "en").text
    print(curr_news_en)
    try:
        curr_news_en['content']= translator.translate(new['content'], dest= "en").text
    except:
        pass
    return curr_news_en

#Function which populates arrays of news, based on eidition or flow type of news
def news_finder(nation):
    directory= "../newScraping/collectedNews/" + nation
    for subdir in os.scandir(directory):
        newspaper= subdir.name
        for news in os.scandir(subdir):
            f= open(directory + "/" + newspaper + "/" + news.name, "r+", encoding= "latin-1")
            curr_news= json.load(f)
            #adding new conceptual informations to the news
            for curr_new in curr_news:
                curr_new['nation']= nation
                curr_new['source']= newspaper
                curr_new['filename']= news.name
            lang= nation_to_lang[nation]
            #time.sleep(0.1)
            ##if lang != 'en':
                #now create a hardcopy in order to have the same new, but in English
                #curr_news_en= to_english(curr_new, lang)
            if len(news.name) == edition_str_len:
                editions.append(curr_news)
                #editions_en.append(curr_news_en)
            else:
                flow.append(curr_news)
                #flow_en.append(curr_news_en)


def pos_tagger(editions):
    to_ret= []
    for edition in editions:
        c_edit= []
        nlp= de_nlp
        for new in edition:
            concepts= []
            #if new['nation']== "CH" or new['nation']=="FR":
                #nlp= fr_nlp
            #elif new['nation']== "UK" or new['nation']=="US":
                #nlp= en_nlp
            #elif new['nation']== "IT":
                #nlp= it_nlp
            #Choosing the right nlp-parser due to the news languages
            nlp= nlp_dict[new['nation']]
            #NLP-ing the title
            doc_title= nlp(new['title'])
            for t_token in doc_title:
                #print(t_token.text, t_token.dep_, t_token.head.pos_)
                if t_token.dep_ == "nsubj" or t_token.dep_ == "dobj" or t_token.dep_ == "pobj" or t_token.dep_ == "csubj":
                    concepts.append(create_concept(t_token.text, t_token.dep_, t_token.head.pos_))
            #this s a try only because some news may not have a content field, in that case just skip
            #currently not using it because it tends to analyze "sentence-per-sentence", going out of the project target
            #try:
                #doc_content= nlp(new['content'])
                #for c_token in doc_content:
                    #print(c_token.text, c_token.dep_, c_token.head.pos_)
                    #if c_token.head.pos_ == "NOUN" or  c_token.dep_ == "nsubj":
                        #concepts.append(create_concept(c_token.text, c_token.dep_, c_token.head.pos_))
            #except:
                #pass
            conceptitle={'title': new['title'],
                        'date': new['date'],
                        'nation': new['nation'],
                        'source': new['source'],
                        'concepts': concepts}
            #print(json.dumps(conceptitle, indent= 4))
            c_edit.append(conceptitle)
        to_ret.append(c_edit)
    return to_ret
        

for nation in nations:
    news_finder(nation)
flow= unicode_fix(flow)
#print(editions_en)
#print(flow_en)
c_flows= []
c_editions= []
c_flows = pos_tagger(flow)
c_editions= pos_tagger(editions)
print(json.dumps(c_editions, indent= 4))
print(json.dumps(c_flows, indent= 4))