#!/usr/bin/env python

import json, sys, os, errno, spacy, torch, numpy as np
from globals import NER_IN_DIR, NER_OUT_DIR
from transformers import AutoTokenizer, AutoModelForSequenceClassification, TFAutoModelForSequenceClassification, pipeline

#The fields' name we want to NER
FIELDS_TO_NLP = [
    'title',
    'subtitle',
    'content'
]

def main():
    if len(sys.argv) < 2:
        raise Exception("Too few arguments.")
    if len(sys.argv) > 2 and sys.argv[2] == '-s':
        full_recognizer(sys.argv[1], 1)
    else:
        full_recognizer(sys.argv[1])

def full_recognizer(subdir, sentiment=0):
    to_recognize = news_getter(subdir)
    nlp = spacy_setup()
    recognized = news_recognizer(to_recognize, nlp, sentiment)
    jsonizer(recognized, subdir)

def spacy_setup():
    return spacy.load("it_core_news_lg")

def news_getter(subdir):
    to_get_dir= f"{NER_IN_DIR}/{subdir}"
    print("ANALYZING: ", to_get_dir)
    with open(to_get_dir, "r") as f:
        try:
            return json.load(f)
        except:
            raise Exception("Could not read file from the given directory: " + to_get_dir + ".")

def news_recognizer(to_reco, nlp, sentiment=0):
    tokenizer= None
    model= None
    
    if sentiment:
        tokenizer, model = load_italian_sentiment()
    
    for article in to_reco:
        article_recognizer(article, nlp, sentiment, tokenizer, model)

    return to_reco


def article_recognizer(article, nlp, sentiment=0, tokenizer=None, model=None):
    if sentiment:
        article['overall_polarity'] = 0

    for field_to_nlp in FIELDS_TO_NLP:
        article = field_nlpier(article, field_to_nlp, nlp, sentiment, tokenizer, model)
        if sentiment:
            try:
                article['overall_polarity'] += article[sent_field_creator(field_to_nlp, "polarity")] or 0
            except:
                pass
    
    if sentiment:
        article['overall_polarity'] /= len(FIELDS_TO_NLP)

    return article


def field_nlpier(article, field, nlp, sentiment=0, tokenizer=None, model=None):
    if (article[field] is not None and len(article[field]) > 0):    
        nlpied = nlp(article[field])
        if sentiment:
            article[sent_field_creator(field, "polarity")]= italian_analyze(article[field], tokenizer, model)

        if nlpied.ents:
            article[ner_field_creator(field)] = []
            for ent in nlpied.ents:
                ner_object = ner_object_creator(ent)
                #It is possibile to add a control to avoid appending the same entities many times
                article[ner_field_creator(field)].append(ner_object)
    
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

#Function found on https://huggingface.co/MilaNLProc/feel-it-italian-sentiment?text=Mi+piaci.+Ti+amo.+Coglione.
def italian_analyze(to_analyze, tokenizer, model):
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
    negative, positive = proba
    toRet = np.round(positive.item(), 4) - np.round(negative.item(), 4)
    
    return toRet
    


def jsonizer(analyzed, subdir):
    to_json_dir= f"{NER_OUT_DIR}/{subdir}"
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