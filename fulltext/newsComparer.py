#!/usr/bin/env python

import json
import os
import sys
import errno
import spacy
from collections import defaultdict

#The nlp pipeline used in order to get nouns
NLP = spacy.load("en_core_web_sm")

#The output base directory
OUT_DIR = f"./compared"

#The analyzed news base directory
BASE_DIR = f"./NER"

#The output base directory
COMPARED = f"./compared"

#The fields name we want to compare
TO_COMPARE = ['title']

#The english-to translated fields' prefix
ENGLISH_PREFIX = "en_"

#Scraped hour range for comparison (in hour)
HOUR_RANGE = 2

#Field to conceptualize before comparison
FIELDS_TO_NLP = ["en_title", "en_subtitle", "en_content"]

#Pos-Tagging right positions for comparison
COMP_POS = ["NOUN", "PROPN"]

#Number of similar concepts two news must have in order to be considered similar
SIMIL_LOWER_BOUND = 25

#Called with arguments like: path_newspaper_A path_newspaper_B date hour
def main():
    if len(sys.argv) < 5:
        raise Exception("Too few arguments.")
    else:
        full_comparer(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])

def full_comparer(newsp_A, newsp_B, date, hour):
    news_A = multi_news_getter(newsp_A, int(hour), date)
    news_B = multi_news_getter(newsp_B, int(hour), date)
    comparison = news_comparer(news_A, news_B)
    jsonizer(comparison, path_formatter(newsp_A, newsp_B, date, hour))


def multi_news_getter(newsp, start_hour, date):
    final_hour = start_hour + HOUR_RANGE

    multi_path = []

    for subdir in os.scandir(f"{BASE_DIR}/{newsp}"):
        filename = subdir.name
        scrape_date = filename.split("T")[0]
        scrape_time = filename.split("T")[1].split("E")[0]
        scrape_hour = int(scrape_time.split(".")[0])

        if scrape_date == date:
            if scrape_hour in range(start_hour, final_hour):
                multi_path.append(filename)
        
    to_ret = []
    for single_path in multi_path:
        to_ret = news_getter(f"{newsp}/{single_path}", to_ret)
    return to_ret

def news_getter(subdir, to_append):
    to_get_dir = f"{BASE_DIR}/{subdir}"
    to_get = {}
    with open(to_get_dir, "r") as f:
        try:
            to_get = json.load(f)
        except:
            raise Exception("Could not read file from the given directory: " + to_get_dir + ".")
    for single_news in to_get:
        to_append.append(single_news)
    return to_append


def news_comparer(news_A, news_B):
    to_ret = defaultdict(dict)
    for i in range(len(news_A)):
        concepts_A = get_concepts(news_A[i])
        for j in range(len(news_B)):
            concepts_B = get_concepts(news_B[j])
            to_ret[news_A[i]["en_title"]][news_B[j]["en_title"]] = single_comparer(news_A[i], news_B[j], concepts_A, concepts_B)
    return to_ret

def single_comparer(news_A, news_B, concepts_A, concepts_B):
    return concepts_comparison(concepts_A, news_A['overall_polarity'], news_A['overall_subjectivity'], concepts_B, news_B['overall_polarity'], news_B['overall_subjectivity'])

def get_concepts(news):
    to_ret = []
    for field in FIELDS_TO_NLP:
        doc_title = NLP(news[field])
        for t_token in doc_title:
            if t_token.pos_ in COMP_POS and t_token.text:
                to_ret.append(t_token.text)
    return to_ret


def concepts_comparison(concepts_A, polarity_A, subjectivity_A, concepts_B, polarity_B, subjectivity_B):
    simil_concepts= []
    for concept_A in concepts_A:
        for concept_B in concepts_B:
            if concept_A == concept_B and concept_A not in simil_concepts:
                simil_concepts.append(concept_A)
    
    return comparison_object_constructor(polarity_A, subjectivity_A, polarity_B, subjectivity_B, simil_concepts)


def comparison_object_constructor(polarity_A, subjectivity_A, polarity_B, subjectivity_B, simil_concepts):
    to_ret= {}

    to_ret["are_similar"] = True if (len(simil_concepts) >= SIMIL_LOWER_BOUND) else False
    to_ret["similar_concepts_number"] = len(simil_concepts)
    to_ret["polarity_X"] = polarity_A
    to_ret["subjectivity_X"] = subjectivity_A
    to_ret["polarity_Y"] = polarity_B
    to_ret["subjectivity_Y"] = subjectivity_B
    to_ret["simil_concepts"] = simil_concepts

    return to_ret


def jsonizer(comparison, to_json_dir):
    if not os.path.exists(os.path.dirname(to_json_dir)):
        try:
            os.makedirs(os.path.dirname(to_json_dir))
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise
    with open(to_json_dir, "w") as f:
        json.dump(comparison, f, indent= 4, ensure_ascii= False)
        f.write("\n")

def path_formatter(path_A, path_B, date, hour):
    newsp_A = path_A.split("/")
    newsp_B = path_B.split("/")
    newsp_A = newsp_A[len(newsp_A)-1]
    newsp_B = newsp_B[len(newsp_B)-1]
    final_hour = str(int(hour) + HOUR_RANGE)
    to_ret = f"{OUT_DIR}/{max(newsp_A, newsp_B)}/{min(newsp_A, newsp_B)}/{date}/{hour}-{final_hour}.json"
    return to_ret

if __name__ == "__main__":
    main()
