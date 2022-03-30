#!/usr/bin/env python

import json
import sys
import os
import errno
import spacy
import torch
import numpy as np 
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from sentiment_analysis_spanish import sentiment_analysis
from spacytextblob.spacytextblob import SpacyTextBlob


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
    if len(sys.argv) > 2 and sys.argv[2] == '-s':
        full_recognizer(sys.argv[1], 1)
    full_recognizer(sys.argv[1])

def full_recognizer(subdir, sentiment= 0):
    to_recognize = news_getter(subdir)
    nlp = spacy_setup(to_recognize[0]['language'])
    if sentiment and to_recognize[0]['language'] == 'EN':
        nlp.add_pipe('spacytextblob')
    recognized = news_recognizer(to_recognize, nlp, sentiment)
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


def news_recognizer(to_reco, nlp, sentiment= 0):
    tokenizer= None
    model= None
    if sentiment and to_reco[0]['language'] == 'IT':
        tokenizer, model = load_italian_sentiment()
    if sentiment and to_reco[0]['language'] == 'DE':
        tokenizer, model = load_german_sentiment()
    for article in to_reco:
        article = article_recognizer(article, nlp, sentiment, tokenizer, model)
    return to_reco


def article_recognizer(article, nlp, sentiment= 0, tokenizer= None, model= None):
    field_lang = ""

    if sentiment:
        article['overall_polarity']= 0

    for field_to_nlp in FIELDS_TO_NLP:
        article = field_nlpier(article, f"{field_lang}{field_to_nlp}", nlp, sentiment, tokenizer, model)
        if sentiment:
            article['overall_polarity']+= article[sent_field_creator(f"{field_lang}{field_to_nlp}", "polarity")]
    
    if sentiment:
        article['overall_polarity']/= len(FIELDS_TO_NLP)

    return article


def field_nlpier(article, field, nlp, sentiment= 0, tokenizer= None, model= None):
    nlpied = nlp(article[field])
    if sentiment:
        if article['language'] == 'ES':
            sentiment_an = sentiment_analysis.SentimentAnalysisSpanish()
            article[sent_field_creator(field, "polarity")]= sentiment_an.sentiment(article[field])
        if article['language'] == 'IT':
            article[sent_field_creator(field, "polarity")]= italian_analyze(article[field], tokenizer, model)
        if  article['language'] == 'DE':
            article[sent_field_creator(field, "polarity")]= italian_analyze(article[field], tokenizer, model, german=1)
            print(article[sent_field_creator(field, "polarity")])
        if article['language'] == 'EN':
            article[sent_field_creator(field, "polarity")]= nlpied._.blob.polarity
            article[sent_field_creator(field, "subjectivity")]= nlpied._.blob.subjectivity
    if nlpied.ents:
        article[ner_field_creator(field)]= []
        for ent in nlpied.ents:
            ner_object= ner_object_creator(ent)
            #It is possibile to add a control to avoid appending the same entities many times
            article[ner_field_creator(field)].append(ner_object)
    print(article)
    return article

    
def ner_field_creator(field):
    return (f"{field}_NER")

def sent_field_creator(field, type):
    return (f"{field}_{type}")

def ner_object_creator(info):
    to_ret = {}

    to_ret['word'] = info.text
    to_ret['start_char'] = info.start_char
    to_ret['end_char'] = info.end_char
    to_ret['label'] = info.label_
    to_ret['info'] = spacy.explain(info.label_)

    return to_ret

def load_italian_sentiment():
    tokenizer = AutoTokenizer.from_pretrained("MilaNLProc/feel-it-italian-sentiment")
    model = AutoModelForSequenceClassification.from_pretrained("MilaNLProc/feel-it-italian-sentiment")
    return (tokenizer, model)

def load_german_sentiment():
    tokenizer = AutoTokenizer.from_pretrained("oliverguhr/german-sentiment-bert")
    model = AutoModelForSequenceClassification.from_pretrained("oliverguhr/german-sentiment-bert")
    return (tokenizer, model)


#Function found on https://huggingface.co/MilaNLProc/feel-it-italian-sentiment?text=Mi+piaci.+Ti+amo.+Coglione.
def italian_analyze(to_analyze, tokenizer, model, german= 0):
    #try:
        if len(to_analyze) > 512:
            to_analyze = to_analyze[:512]
        sentence = to_analyze
        inputs = tokenizer(sentence, return_tensors="pt")

        # Call the model and get the logits
        labels = torch.tensor(1).unsqueeze(-1)  # Batch size 1
        outputs = model(**inputs, labels=labels)
        loss, logits = outputs[:2]
        logits = logits.squeeze(0)

        # Extract probabilities
        proba = torch.nn.functional.softmax(logits, dim=0)
        # Unpack the tensor to obtain negative and positive probabilities
        if german:
            positive, negative, neutral = proba
        else:
            negative, positive = proba
        print(f"Negative: {negative.item()} - Positive: {positive.item()}")
        toRet = np.round(positive.item(), 4) - np.round(negative.item(), 4)
        print(toRet)
        return toRet 
    #except:
        #return 0
    


def jsonizer(analyzed, subdir):
    to_json_dir= f"{NER_DIR}/{subdir}"
    if not os.path.exists(os.path.dirname(to_json_dir)):
        try:
            os.makedirs(os.path.dirname(to_json_dir))
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise
    with open(to_json_dir, "w") as f:
        json.dump(analyzed, f, indent= 4, ensure_ascii= False)
        f.write("\n")

if __name__ == "__main__":
    main()