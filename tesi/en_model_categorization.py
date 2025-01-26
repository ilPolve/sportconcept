# Analizzando le notizie giorno per giorno, è possibile stabilire una predominanza di argomenti?
# Confrontare il risultato dell'analisi svolta sulle url degli articoli
# con il risultato di uno 0-shot classifier

import sys
sys.path.append('..')
from definitions.utils import snapped_news_by_source
import os, json, re

counters = dict()
SOURCES = ['cds', 'gds', 'ts']
SOURCES_NAME = ['corrieredellosport', 'gazzetta', 'tuttosport']
OUT_FILE = './out/en_model_categorization.json'

SPORT_LABELS = [
    'other sports', 'martial arts',
    'athletics', 'motor racing',
    'basketball', 'football',
    'rowing', 'cycling',
    'horse riding', 'esports',
    'American football',
    'golf', 'horse racing',
    'motorcycling', 'non-sports news', 
    'swimming', 'padel',
    'water polo', 'volleyball',
    'poker', 'boxing',
    'rugby', 'running',
    'skiing', 'winter sports',
    'tennis', 'sailing']

from transformers import pipeline, AutoModelForSequenceClassification, AutoTokenizer
tokenizer = AutoTokenizer.from_pretrained("facebook/bart-large-mnli")
model = AutoModelForSequenceClassification.from_pretrained("facebook/bart-large-mnli")
        
def main():
    counters = {}
    for source in SOURCES:
        counters[source] = {}
        source_news = snapped_news_by_source(f'../news/flow/it/{source}', nlpy=False)
        for day in range(15, 16):
            date = f'2024-05-{day}'
            counters[source][date] = {}
            daily_news = list({item['news_url']: item for item in filter(lambda i: i['scrape_dt'][0:10] == date, source_news)}.values())
            counters[source][date] = parser(daily_news, source)
            counters[source][date]['daily_news_count'] = len(daily_news)
       
    with open(OUT_FILE, 'w') as fd:
        json.dump(counters, fd, indent=4)

def parser(news, source):
    global SPORT_LABELS
    counter = {}
    
    classifier = pipeline("zero-shot-classification", tokenizer=tokenizer, model=model, device=0)
    for article in news:
        try:
            text = (article['title'] or '') + (article['subtitle'] or '') + (article['content'] or '')
            sport = classifier(text, SPORT_LABELS)
            sport = sport['labels'][0]
        except:
            sport = 'not classifiable'
            
        try:
            counter[sport].append(article['news_url'])
        except:
            counter[sport] = [article['news_url']]
    
    return counter

if __name__ == "__main__":
    main()