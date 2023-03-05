import os
import json
import spacy
import warnings
from datetime import datetime
warnings.filterwarnings("ignore")

nlp = spacy.load("en_core_web_sm")
main_dir = f"../fulltext/NER/flow/IT"

COSINE_THRESHOLD = 0.90

SNAP_RATE = 15

def snapped_news_by_source(dir):
    title_list = []
    news_list = []
    for file in os.listdir(dir):
        if file.endswith(".json"):
            with open(f"{dir}/{file}", "r") as f:
                news = json.load(f)
                for new in news:
                    if new["title"] not in title_list:
                        title_list.append(new["title"])
                        news_list.append(new)
    return news_list

def snapped_news_by_date(date, exclude):
    title_list = []
    news_list = []
    for subdir in os.listdir(main_dir):
        if not subdir.startswith(exclude):
            for file in os.listdir(f"{main_dir}/{subdir}"):
                if file.endswith(".json") and file.startswith(date):
                    with open(f"{main_dir}/{subdir}/{file}", "r") as f:
                        news = json.load(f)
                        for new in news:
                            if new["title"] not in title_list:
                                title_list.append(new["title"])
                                news_list.append(new)
    return news_list

def snapped_news_in_range(dir, start_epoch, end_epoch, nlpy = False):
    snap_list = []
    news_list = []
    for file in os.listdir(dir):
        if file.endswith(".json"):
            if in_range_epoch(file, start_epoch, end_epoch):
                with open(f"{dir}/{file}", "r") as f:
                    news = json.load(f)
                    if nlpy:
                        for new in news:
                            new["cont_nlp"] = nlp(new["en_content"])
                    snap_list.append(news)
                    for new in news:
                        news_list.append(new)
    return news_list, snap_list

def has_similar_in_pool(main_news, news_pool):
    for news in news_pool:
        if is_similar(main_news, news, nlp, COSINE_THRESHOLD):
            return True
    return False

def has_similar_in_pool_nlpied(main_news, news_pool):
    for news in news_pool:
        if is_similar_nlpied(main_news, news, nlp, COSINE_THRESHOLD):
            return True
    return False

def is_similar(news_A, news_B, nlp=nlp, COSINE_THRESHOLD=COSINE_THRESHOLD):
    content_A = news_A["en_content"]
    content_B = news_B["en_content"]

    corpus = [nlp(content_A), nlp(content_B)]
    similarity = corpus[0].similarity(corpus[1])

    #Sklearn Vectorizer
    # corpus = [content_A, content_B]
    # vectorizer = TfidfVectorizer(stop_words="english")
    # sparse_matrix = vectorizer.fit_transform(corpus)
    # doc_term_matrix = sparse_matrix.todense()
    # df = pd.DataFrame(doc_term_matrix, columns=vectorizer.get_feature_names_out(), index=['news_A', 'news_B'])
    # similarity = cosine_similarity(df, df)[0][1]


    if similarity > COSINE_THRESHOLD:
        # print(news_A["title"])
        # print(news_B["title"])
        return True
    else:
        return False

def is_similar_nlpied(cont_A, cont_B, nlp=nlp, COSINE_THRESHOLD=COSINE_THRESHOLD):
    corpus = [cont_A["cont_nlp"], cont_B["cont_nlp"]]
    similarity = corpus[0].similarity(corpus[1])
    if similarity > COSINE_THRESHOLD:
        return True
    else:
        return False

def date_to_epoch(date):
    date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    epoch = datetime.utcfromtimestamp(0)
    return (date - epoch).total_seconds()

def in_range_epoch(filename, start_epoch, end_epoch):
    return int(start_epoch) <= int(filename.split("E")[1].split(".")[0]) <= int(end_epoch)

def remove_duplicates(news, nlpied=False):
    # Removing same article
    title_list = []
    news_list = []
    for new in news:
        if new["title"] not in title_list:
            title_list.append(new["title"])
            news_list.append(new)
    
    # Removing similar articles
    to_ret = []
    for i in range(len(news_list)):
        article_A = news_list[i]
        if i < len(news_list)-1:
            if nlpied:
                if not has_similar_in_pool_nlpied(article_A, news_list[i+1:]):
                    to_ret.append(article_A)
            else:
                if not has_similar_in_pool(article_A, news_list[i+1:]):
                    to_ret.append(article_A)
    
    return to_ret