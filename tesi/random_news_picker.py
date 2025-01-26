# Generare un sotto insieme casuale di notizie, 100 per ciascuna sorgente 

import os, json, sys, random
sys.path.append('..')
from definitions.utils import snapped_news_by_source

SOURCES = ['cds', 'gds', 'ts']

def main():
    selected_news = []
    for source in SOURCES:
        source_news = snapped_news_by_source(f'../news/flow/it/{source}', False)
        selected_news = selected_news + random.choices(source_news, k=50)
        
    with open(f'./out/random_news.json', 'w') as fd:
        json.dump(selected_news, fd, indent=4)
    
    with open(f'./out/random_news_task.json', 'w') as fd:
        task = []
        for index, news in enumerate(selected_news):
            task_object = {}
            task_object['id'] = index
            task_object['data'] = {}
            task_object['data']['text'] = f'{news['news_url']}\n\n{news['title'] or ''}\n\n{news['subtitle'] or ''}\n\n{news['content'] or ''}'
            
            task.append(task_object)
        
        json.dump(task, fd, indent=4)

if __name__ == "__main__":
    if not os.path.exists('./out'):
        os.mkdir('./out')
            
    main()

# LABEL_STUDIO_LOCAL_FILES_SERVING_ENABLED=true LABEL_STUDIO_LOCAL_FILES_DOCUMENT_ROOT=/home/ilpolve label-studio start