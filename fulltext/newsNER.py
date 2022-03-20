#!/usr/bin/env python

import json
import sys
import os
import errno
import spacy

#The translated news base directory
BASE_DIR = f"./translated"

#The output base directory
NER_DIR = f"./NER"

#The fields' name we want to NER
FIELDS_TO_NLP = ['title',
                 'subtitle',
                 'content'
                ]

#The english-to translated fields' prefix
ENGLISH_PREFIX = "en_"            


def main():
    if len(sys.argv) < 2:
        raise Exception("Too few arguments.")
    full_recognizer(sys.argv[1])

def full_recognizer(subdir):
    to_recognize = news_getter(subdir)
    nlp = spacy_setup()
    recognized = news_recognizer(to_recognize, nlp)
    jsonizer(recognized, subdir)

def spacy_setup():
    return spacy.load('en_core_web_sm')

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
        if article['language'] == 'EN' or f"{ENGLISH_PREFIX}title" in article:
            article = article_recognizer(article, nlp)
    return to_reco


def article_recognizer(article, nlp):
    field_lang = ""

    if article['language'] != 'EN':
        field_lang = ENGLISH_PREFIX

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
    return (f"{field}_NER").replace(ENGLISH_PREFIX, "")

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