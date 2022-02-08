#!/usr/bin/env python

import json
import os
import spacy

my_subdirs= ['edition/DE', 'edition/FR', 'edition/EN', 'edition/IT', 'flow/DE', 'flow/EN', 'flow/IT']

nlp= spacy.load("en_core_web_sm")

BASE_DIR = "../Newscraping/collectedNews/" 

def main():
    for my_subdir in my_subdirs:
        pos_tagger(getting_news(my_subdir), my_subdir)  

def create_concept(word, meaning, pos):
    concept= {'word': word, 'meaning': meaning, 'pos': pos}
    return concept

def pos_tagger(editions, my_subdir):
    to_ret= []
    for nat_ed in editions:
        for edition in nat_ed:
            c_edit= []
            for new in edition:
                conceptitle = conceptualize(new)
                c_edit.append(conceptitle)
            to_ret.append(c_edit)
            if len(edition) > 0:
                filepath= f"{BASE_DIR}{my_subdir}/{edition[0]['source']}/conc_{edition[0]['filename'][5:]}"
                to_remove= filepath.replace("conc_", "")
                os.remove(to_remove)
                with open(filepath, "w") as f:
                    json.dump(edition, f, ensure_ascii = False, indent= 4)
                    f.write("\n")
    return to_ret

def conceptualize(new):
    concepts= []
    #nlp-ing the title
    doc_title= nlp(new['en_title'])
    for t_token in doc_title:
        if t_token.pos_ == "NOUN" or t_token.pos_ == "PROPN":
            concepts.append(create_concept(t_token.text, t_token.dep_, t_token.head.pos_))
    try:
        act_date = new['date']
    except:
        act_date = new['date_raw']
    conceptitle={'title': new['title'],
                            'en_title': new['en_title'],
                            'date': act_date,
                            'language': new['language'],
                            'source': new['source'],
                            'concepts': concepts}
    new['concepts']= concepts
    return conceptitle
        

def getting_news(my_subdir):
    directory= f"{BASE_DIR}{my_subdir}"
    nat_ed= []
    for subdir in os.scandir(directory):
        newspaper= subdir.name
        editions= []
        for news in os.scandir(subdir):
            if(news.name[0:2] == "en"):
                filepath= f"{directory}/{newspaper}/{news.name}"
                with open(filepath, "r+") as f:    
                    curr_news= json.load(f)
                edition= []
                for new in curr_news:
                    new['filename'] = "conc_" + news.name
                    edition.append(new)
                editions.append(edition)
        nat_ed.append(editions)
    return nat_ed 

if __name__ == "__main__":
    main()