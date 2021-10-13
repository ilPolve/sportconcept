import json
import datetime
import os
from googletrans import Translator
import copy
import time
import httpx
import spacy

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