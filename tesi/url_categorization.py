# Analizzando le notizie giorno per giorno, è possibile stabilire una predominanza di argomenti?
# Confrontare il risultato dell'analisi svolta sulle url degli articoli
# con il risultato di uno 0-shot classifier

import sys
sys.path.append('..')
from definitions.utils import snapped_news_by_date, snapped_news_by_source
import os, json, re

counters = dict()
SOURCES = ['cds', 'gds', 'ts']
OUT_FILE = './out/url_categorization.json'

def main():
    counters = {}
    for source in SOURCES:
        counters[source] = {}
        source_news = snapped_news_by_source(f'../news/flow/it/{source}', nlpy=False)
        for day in range(15, 26):
            date = f'2024-05-{day}'
            counters[source][date] = {}
            daily_news = list({item['news_url']: item for item in filter(lambda i: i['scrape_dt'][0:10] == date, source_news)}.values())
            counters[source][date] = parser(daily_news, source)
            counters[source][date]['daily_news_count'] = len(daily_news)
       
    with open(OUT_FILE, 'w') as fd:
        json.dump(counters, fd, indent=4)
        
def parser(news, source):
    if source == 'cds':
        return cds_parser(news)
    elif source == 'gds':
        return gds_parser(news)
    elif source == 'ts':
        return ts_parser(news)

def cds_parser(news_list):
    counter = {
        'non classificabile': []
    }
    
    for url in [item['news_url'] for item in news_list]:
        sport = 'non classificabile'
        if 'corrieredellosport' not in url:
            regex = r"https://www.(inmoto|auto|motosprint).it/(news|foto)/"
            splitted_url = re.sub(regex, '', url).split('/')
            
            sport = splitted_url[0]
            
            if sport in [
                'curiosita',
                'altre-notizie',
                'attualita',
                'approfondimenti',
                'ripartiamo',
                'social',
                'turismo',
                'speciali',
                'anteprime'
            ]:
                sport = 'notizia non sportiva'
            elif sport in ['sbk', 'motomondiale', 'eventi']:
                if sport == 'eventi' and splitted_url[1] != 'gp-catalunya':
                    sport = 'notizia non sportiva'
                else:
                    sport = 'motociclismo'
        else:
            if 'store.corrieredellosport.it' in url:
                sport = 'notizia non sportiva'
            else:
                regex = r"https://.+.corrieredellosport.it/(news|foto|video|live)/"
                splitted_url = re.sub(regex, '', url).split('/')

                sport = splitted_url[0]

                if sport == 'altri-sport' and re.match('[0-9]{4}', splitted_url[1]):
                    sport = 'altri sport'
                elif sport == 'altri-sport':
                    sport = splitted_url[1].lower()
                elif sport in ['formula-1', 'formula1']:
                    sport = 'automobilismo'
                elif sport in ['motomondiale', 'moto']:
                    sport = 'motociclismo'
                elif sport == 'pokersportivo':
                    sport = 'poker'
                elif sport == 'partita':
                    sport = 'calcio'
                elif sport == 'volley':
                    sport = 'pallavolo'
                elif sport == 'ippica':
                    sport == 'equitazione'
                elif sport in [
                    'scommesse', # non parlano strettamente di uno sport
                    'attualit', # notizie di attualità
                    'on-air', # notizie radio
                    'altre-notizie', # altre notizie non correlate allo sport
                    'lifestyle', # notizie di cronaca
                    'motori', # notizie sul mercato auto
                    'social', # notizie dai social
                    'gossip', # notizie di gossip
                    'mondo-racing'
                    ]: 
                    sport = 'notizia non sportiva'

        try:
            counter[re.sub('-', ' ', sport)].append(url)
        except:
            counter[re.sub('-', ' ', sport)] = [url]

    return counter

def gds_parser(news_list):
    counter = {
        'non classificabile': []
    }
    
    for url in [item['news_url'] for item in news_list]:
        
        sport = 'non classificabile'
        if 'gazzetta.it' not in url:
            regex = r'https://.*.(it|info|com)/'
            splitted_url = re.sub(regex, '', url).split('/')
            
            if splitted_url[0] in [
                'calcio-estero',
                'calcio-italiano',
                'notizie-calcio',
                'calciomercato',
                'udinese',
                'calciomercato-as-roma',
                'news-milan',
                'news-napoli',
                'news-as-roma',
                'news-calcio',
                'ultimissime-calcio-napoli'
                ]:
                sport = 'calcio'
        if 'video.gazzetta.it' not in url and 'gazzetta.it' in url:
            if 'questoquello.gazzetta.it' in url or 'chepalle' in url:
                sport = 'notizia non sportiva'
            elif 'questionedistile.gazzetta.it' in url:
                sport = 'nuoto'
            elif '/motori/ferrari/' in url:
                sport = 'automobilismo'
            else:
                regex = r"https://.+.gazzetta.it/"
                splitted_url = re.sub(regex, '', url).split('/')
                
                sport = splitted_url[0].lower()
        
                if sport == 'sport-invernali':
                    if re.match('[a-zA-Z]+', splitted_url[1]):
                        sport = splitted_url[1].lower()
                        if sport == 'sci-alpino':
                            sport = 'sci'
                    else:
                        sport == 'notizia non sportiva'
                elif sport in ['nba', 'eurolega']:
                    sport = 'basket'
                elif sport in ['auto', 'formula-1']:
                    sport = 'automobilismo'
                elif sport == 'sport-usa':
                    sport = 'football americano'
                elif sport == 'fighting':
                    sport = splitted_url[1].lower()
                elif sport == 'moto':
                    sport = 'motociclismo'
                elif sport == 'mare':
                    sport = 'nuoto'
                elif sport == 'giroditalia':
                    sport = 'ciclismo'
                elif sport == 'volley':
                    sport = 'pallavolo'
                elif sport == 'calciomercato':
                    sport = 'calcio'
                elif sport == 'sport-vari':
                    sport = 'altri sport'
                elif sport == 'olimpiadi':
                    sport = splitted_url[2].lower()
                    if sport == 'volley':
                        sport = 'pallavolo'
                    elif sport == 'canottaggio-canoa-kayak':
                        sport = 'canottaggio'
                elif sport in [
                    'olimpiadi-invernali', # categoria usate per notizie di cronaca
                    'montagna', # pubblicità
                    'tv',
                    'scommesse', # non parlano strettamente di uno sport
                    'gossip', # notizie di cronaca
                    'quiz', # quiz interattivi, non classificabili come articoli sportivi
                    'salute', # notizie salutiste, correlate lascamente allo sport
                    'alimentazione', # notizie salutiste, correlate lascamente allo sport
                    'fitness', # notizie salutiste, correlate lascamente allo sport
                    'active', # notizie salutiste, correlate lascamente allo sport
                    'spettacolo', # notizie di spettacolo
                    'stile', # notizie di moda
                    'motori' # notizie sul mercato auto/moto
                ]:
                    sport = 'notizia non sportiva'


        try:
            counter[re.sub('-', ' ', sport)].append(url)
        except:
            counter[re.sub('-', ' ', sport)] = [url]

    return counter

def ts_parser(news_list):
    counter = {
        'non classificabile': []
    }
    
    for url in [item['news_url'] for item in news_list]:
        sport = 'non classificabile'
        if 'tuttosport' not in url:
            if 'corrieredellosport' in url:
                if '/foto/social/' in url:
                    sport = 'notizia non sportiva'
                else:
                    sport = 'automobilismo'
            else:
                regex = r"https://www.(inmoto|auto|motosprint).it/(news|foto)/"
                splitted_url = re.sub(regex, '', url).split('/')

                sport = splitted_url[0]

                if sport in [
                    'curiosita',
                    'altre-notizie',
                    'attualita',
                    'approfondimenti',
                    'ripartiamo',
                    'social',
                    'turismo',
                    'speciali',
                    'anteprime',
                    'green'
                ]:
                    sport = 'notizia non sportiva'
                elif sport in ['mondo-racing', 'formula1']:
                    sport = 'automobilismo'
                elif sport in ['sbk', 'motomondiale', 'eventi']:
                    if sport == 'eventi' and splitted_url[1] != 'gp-catalunya':
                        sport = 'notizia non sportiva'
                    else:
                        sport = 'motociclismo'
        else:
            if 'store.tuttosport.com' in url:
                sport = 'notizia non sportiva'
            else:
                regex = r"https://.+.tuttosport.com/(news|foto|video|live)/"
                splitted_url = re.sub(regex, '', url).split('/')

                sport = splitted_url[0]

                if sport == 'altri-sport' and re.match('[0-9]{4}', splitted_url[1]):
                    sport = 'altri sport'
                elif sport == 'altri-sport':
                    sport = splitted_url[1]
                elif sport in ['formula-1', 'formula1']:
                    sport = 'automobilismo'
                elif sport in ['moto','motomondiale']:
                    sport = 'motociclismo'
                elif sport == 'pokersportivo':
                    sport = 'poker'
                elif sport == 'partita':
                    sport = 'calcio'
                elif sport in [
                    'scommesse',
                    'attualit',
                    'on-air',
                    'altre-notizie',
                    'lifestyle',
                    'motori',
                    'social',
                    'gossip',
                    'mondo-racing'
                    ]: 
                    sport = 'notizia non sportiva'

        try:
            counter[re.sub('-', ' ', sport)].append(url)
        except:
            counter[re.sub('-', ' ', sport)] = [url]

    return counter

if __name__ == "__main__":
    main()

