#!/usr/bin/env python

import json
import os
import sys
import errno
import spacy
from collections import defaultdict
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

#The nlp pipeline used in order to get nouns
NLP = spacy.load("en_core_web_sm")

#The output base directory
OUT_DIR = f"./full_compared"

#The analyzed news base directory
BASE_DIR = f"./NER"

#The output base directory
COMPARED = f"./full_compared"

#The english-to translated fields' prefix
ENGLISH_PREFIX = "en_"

#Scraped hour range for comparison (in hour)
HOUR_RANGE = 1

#Field to conceptualize before comparison
FIELDS_TO_NLP = ["en_title", "en_subtitle", "en_content"]

COSINE_FIELDS_TO_NLP = ["en_content"]

#Pos-Tagging right positions for comparison
COMP_POS = ["NOUN", "PROPN"]

#Percentage of similar concepts two news must have in order to be considered similar
SIMIL_LOWER_BOUND = 10

#Percentage of similarity needed for cosine algorithm to be considered similar
COSINE_SIMIL_LOWER_BOUND = 80

#Words-Count vector
count_vect = CountVectorizer()

#Sklearn Vectorizer
vectorizer = TfidfVectorizer()



#Called with arguments like: path_newspaper_A path_newspaper_B date hour
def main():
    if len(sys.argv) < 5:
        raise Exception("Too few arguments.")
    else:
        if len(sys.argv) > 5 and sys.argv[5] == "-c":
            full_comparer(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], cosine=True)
        else:
            full_comparer(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])

def full_comparer(newsp_A, newsp_B, date, hour, cosine=False):
    news_A = multi_news_getter(newsp_A, int(hour), date)
    news_B = multi_news_getter(newsp_B, int(hour), date)
    comparison = news_comparer(news_A, news_B, cosine)
    jsonizer(comparison, path_formatter(newsp_A, newsp_B, date, hour, cosine))


def multi_news_getter(newsp, start_hour, date):
    got_titles= []
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
        to_ret = news_getter(f"{newsp}/{single_path}", to_ret, got_titles)
    return to_ret

def news_getter(subdir, to_append, got_titles):
    to_get_dir = f"{BASE_DIR}/{subdir}"
    to_get = {}
    with open(to_get_dir, "r") as f:
        try:
            to_get = json.load(f)
        except:
            raise Exception("Could not read file from the given directory: " + to_get_dir + ".")
    for single_news in to_get:
        if not single_news['en_title'] in got_titles:
            got_titles.append(single_news['en_title'])
            to_append.append(single_news)
    return to_append


def news_comparer(news_A, news_B, cosine=False):
    to_ret = defaultdict(dict)
    found_A = [False] * len(news_A)
    found_B = [False] * len(news_B)
    to_ret["len_A"] = len(news_A)
    to_ret["len_B"] = len(news_B)
    to_ret["coupled_A"] = 0
    to_ret["coupled_B"] = 0
    to_ret["covered_A_percent"] = 0
    to_ret["covered_B_percent"] = 0
    to_ret["covered_both_percent"] = 0

    for i in range(len(news_A)):
        if not cosine:
            concepts_A = get_concepts(news_A[i])

        for j in range(len(news_B)):
            if not cosine:
                concepts_B = get_concepts(news_B[j])

            if not cosine:
                to_ret[news_A[i]["en_title"]][news_B[j]["en_title"]] = single_comparer(news_A[i], news_B[j], concepts_A, concepts_B)
            else:
                to_ret[news_A[i]["en_title"]][news_B[j]["en_title"]] = cosine_comparer(news_A[i], news_B[j])

            if to_ret[news_A[i]["en_title"]][news_B[j]["en_title"]]["are_similar"]:
                found_A[i] = found_B[j] = True
    
    to_ret["coupled_A"] = sum(found_A)
    to_ret["coupled_B"] = sum(found_B)
    
    total_news = len(news_A) + len(news_B)
        
    to_ret["covered_A_percent"] = (len(found_A) - to_ret["coupled_A"]) / total_news * 100
    to_ret["covered_B_percent"] = (len(found_B) - to_ret["coupled_B"]) / total_news * 100
    to_ret["covered_both_percent"] = (100 - (to_ret['covered_A_percent'] + to_ret['covered_B_percent']))

    return to_ret

def single_comparer(news_A, news_B, concepts_A, concepts_B):
    return concepts_comparison(concepts_A, news_A['overall_polarity'], news_A['overall_subjectivity'], concepts_B, news_B['overall_polarity'], news_B['overall_subjectivity'])

def cosine_comparer(news_A, news_B):
    total_similarity = []
    for field in COSINE_FIELDS_TO_NLP:
        if news_A[field] != "" and news_B[field] != "":
            field_A = news_A[field]
            field_B = news_B[field]
            corpus = [field_A, field_B]
            X_train_counts = count_vect.fit_transform(corpus)
            pd.DataFrame(X_train_counts.toarray(), columns = count_vect.get_feature_names_out(), index=['field_A', 'field_B'])

            trsfm = vectorizer.fit_transform(corpus)
            pd.DataFrame(trsfm.toarray(), columns = vectorizer.get_feature_names_out(), index=['field_A', 'field_B'])

            similarity = cosine_similarity(trsfm[0:1], trsfm)
            total_similarity.append(similarity[0][1] * 100)
    medium_similarity = 0
    if len(total_similarity) > 0:
        for single_simil in total_similarity:
            medium_similarity += single_simil
        medium_similarity = medium_similarity / len(total_similarity)



    return comparison_object_constructor(news_A["overall_polarity"], news_A["overall_subjectivity"], news_B["overall_polarity"], news_B["overall_subjectivity"], medium_similarity, [], cosine= True)


def get_concepts(news):
    to_ret = []
    for field in FIELDS_TO_NLP:
        if field in news:
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
    
    return comparison_object_constructor(polarity_A, subjectivity_A, polarity_B, subjectivity_B, len(simil_concepts), simil_concepts, cosine=False, max_news_len=(len(concepts_A) + len(concepts_B))/2)


def comparison_object_constructor(polarity_A, subjectivity_A, polarity_B, subjectivity_B, simil_concepts_length, simil_concepts, cosine= False, max_news_len= 0):
    to_ret= {}

    to_ret["are_similar"] = True if ((not cosine and are_similar_naive(simil_concepts_length, max_news_len)) or (cosine and simil_concepts_length >= COSINE_SIMIL_LOWER_BOUND)) else False
    to_ret["similar_concepts_number" if not cosine else "similarity_percentage"] = simil_concepts_length
    to_ret["polarity_X"] = polarity_A
    to_ret["subjectivity_X"] = subjectivity_A
    to_ret["polarity_Y"] = polarity_B
    to_ret["subjectivity_Y"] = subjectivity_B
    to_ret["simil_concepts"] = simil_concepts

    return to_ret


def are_similar_naive(simil_length, news_length):
    if int((news_length*SIMIL_LOWER_BOUND)/100) <= simil_length and int((news_length*SIMIL_LOWER_BOUND)/100) > 0:
        return True
    else:
        return False

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

def path_formatter(path_A, path_B, date, hour, cosine=False):
    newsp_A = path_A.split("/")
    newsp_B = path_B.split("/")
    newsp_A = newsp_A[len(newsp_A)-1]
    newsp_B = newsp_B[len(newsp_B)-1]
    final_hour = str(int(hour) + HOUR_RANGE)
    to_ret = f"{OUT_DIR}/{max(newsp_A, newsp_B)}/{min(newsp_A, newsp_B)}/{date}/{'cos_' if cosine else ''}{hour}-{final_hour}.json"
    return to_ret

if __name__ == "__main__":
    main()
