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
IN_FILE = './out/random_news.json'
OUT_FILE = './out/it_model_task_news_categorization.json'

SPORT_LABELS = [
    'altri sport', 'arti marziali',
    'atletica', 'automobilismo',
    'basket', 'calcio',
    'canottaggio', 'ciclismo',
    'equitazione', 'esports',
    'football americano',
    'golf', 'ippica',
    'motociclismo', 'notizia non sportiva', 
    'nuoto', 'padel',
    'pallanuoto', 'pallavolo',
    'poker', 'pugilato',
    'rugby', 'running',
    'sci', 'sport invernali',
    'tennis', 'vela'
    ]

from transformers import pipeline, AutoModelForSequenceClassification, AutoTokenizer
tokenizer = AutoTokenizer.from_pretrained("knowledgator/comprehend_it-base")
model = AutoModelForSequenceClassification.from_pretrained("knowledgator/comprehend_it-base")
        
def main():
    counters = {}
    with open(IN_FILE, 'r') as fd:
        data = json.load(fd)
        counters = parser(data)
       
    with open(OUT_FILE, 'w') as fd:
        json.dump(counters, fd, indent=4)

def parser(news):
    global SPORT_LABELS
    counter = {}
    
    classifier = pipeline("zero-shot-classification", tokenizer=tokenizer, model=model, device=0)
    for article in news:
        try:
            text = (article['title'] or '') + (article['subtitle'] or '') + (article['content'] or '')
            sport = classifier(text, SPORT_LABELS)
            sport = sport['labels'][0]
        except:
            sport = 'non classificabile'
            
        try:
            counter[sport].append(article['news_url'])
        except:
            counter[sport] = [article['news_url']]
    
    return counter

if __name__ == "__main__":
    main()