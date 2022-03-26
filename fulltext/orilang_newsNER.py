#!/usr/bin/env python

import json
import sys
import os
import errno
import spacy

#The scraped news base directory
BASE_DIR = f"../../Newscraping/collectedNews"

#The output base directory
NER_DIR = f"./multilang_NER"

#The fields' name we want to NER
FIELDS_TO_NLP = ['title',
                 'subtitle',
                 'content'
                ]     

LANG_TO_SPACY = {'EN': "en_core_web_sm",
                 'IT': "it_core_news_md",
                 'ES': "es_core_news_md",
                 'DE': "de_core_news_md",
                 'FR': "fr_core_news_md"}

def main():
    if len(sys.argv) < 2:
        raise Exception("Too few arguments.")
    full_recognizer(sys.argv[1])

def full_recognizer(subdir):
    to_recognize = news_getter(subdir)
    nlp = spacy_setup(to_recognize[0]['language'])
    recognized = news_recognizer(to_recognize, nlp)
    jsonizer(recognized, subdir)

def spacy_setup(lang):
    spacy_module = ""
    if lang in LANG_TO_SPACY:
        spacy_module = LANG_TO_SPACY[lang]
    else:
        raise Exception("Language not analyzable.")
    return spacy.load(spacy_module)

def news_getter(subdir):
    to_get_dir = f"{BASE_DIR}/{subdir}"
    to_get = {}
    with open(to_get_dir, "r") as f:
        try:
            to_get = json.load(f)
        except:
            raise Exception("Could not read file from the given directory: " + to_get_dir + ".")
    return to_get


def news_recognizer(to_reco, nlp):
    for article in to_reco:
        article = article_recognizer(article, nlp)
    return to_reco


def article_recognizer(article, nlp):
    field_lang = ""

    for field_to_nlp in FIELDS_TO_NLP:
        article = field_nlpier(article, f"{field_lang}{field_to_nlp}", nlp)
    
    return article


def field_nlpier(article, field, nlp):
    nlpied = nlp(article[field])
    if nlpied.ents:
        article[ner_field_creator(field)]= []
        for ent in nlpied.ents:
            ner_object= ner_object_creator(ent)
            #It is possibile to add a control to avoid appending the same entities many times
            article[ner_field_creator(field)].append(ner_object)
    return article

    
def ner_field_creator(field):
    return (f"{field}_NER")

def ner_object_creator(info):
    to_ret = {}

    to_ret['word'] = info.text
    to_ret['start_char'] = info.start_char
    to_ret['end_char'] = info.end_char
    to_ret['label'] = info.label_
    to_ret['info'] = spacy.explain(info.label_)

    return to_ret

def jsonizer(translated, subdir):
    to_json_dir= f"{NER_DIR}/{subdir}"
    if not os.path.exists(os.path.dirname(to_json_dir)):
        try:
            os.makedirs(os.path.dirname(to_json_dir))
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise
    with open(to_json_dir, "w") as f:
        json.dump(translated, f, indent= 4, ensure_ascii= False)
        f.write("\n")

if __name__ == "__main__":
    main()