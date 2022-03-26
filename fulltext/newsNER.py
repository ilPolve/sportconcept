#!/usr/bin/env python

import json
import sys
import os
import errno
import spacy
from spacytextblob.spacytextblob import SpacyTextBlob

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
    if len(sys.argv) > 2 and sys.argv[2] == '-s':
        full_recognizer(sys.argv[1], 1)
    else:
        full_recognizer(sys.argv[1])

def full_recognizer(subdir, sentiment= 0):
    to_recognize = news_getter(subdir)
    nlp = spacy_setup()
    if sentiment:
        nlp.add_pipe('spacytextblob')
    recognized = news_recognizer(to_recognize, nlp, sentiment)
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


def news_recognizer(to_reco, nlp, sentiment= 0):
    for article in to_reco:
        if article['language'] == 'EN' or f"{ENGLISH_PREFIX}title" in article:
            article = article_recognizer(article, nlp, sentiment)
    return to_reco


def article_recognizer(article, nlp, sentiment= 0):
    field_lang = ""

    if article['language'] != 'EN':
        field_lang = ENGLISH_PREFIX

    if sentiment:
        article['overall_polarity']= 0
        article['overall_subjectivity']= 0

    for field_to_nlp in FIELDS_TO_NLP:
        article = field_nlpier(article, f"{field_lang}{field_to_nlp}", nlp, sentiment)
        if sentiment:
            article['overall_polarity']+= article[sent_field_creator(f"{field_lang}{field_to_nlp}", "polarity")]
            article['overall_subjectivity']+= article[sent_field_creator(f"{field_lang}{field_to_nlp}", "subjectivity")]
    
    if sentiment:
        article['overall_polarity']/= len(FIELDS_TO_NLP)
        article['overall_subjectivity']/= len(FIELDS_TO_NLP)

    return article


def field_nlpier(article, field, nlp, sentiment= 0):
    nlpied = nlp(article[field])
    if sentiment:
            article[sent_field_creator(field, "polarity")]= nlpied._.blob.polarity
            article[sent_field_creator(field, "subjectivity")]= nlpied._.blob.subjectivity
    if nlpied.ents:
        article[ner_field_creator(field)]= []
        for ent in nlpied.ents:
            ner_object= ner_object_creator(ent)
            #It is possibile to add a control to avoid appending the same entities many times
            article[ner_field_creator(field)].append(ner_object)
    
    return article

    
def ner_field_creator(field):
    return (f"{field}_NER").replace(ENGLISH_PREFIX, "")

def sent_field_creator(field, type):
    return (f"{field}_{type}").replace(ENGLISH_PREFIX, "")

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