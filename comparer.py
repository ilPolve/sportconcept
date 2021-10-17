import json
import os

nations= ['CH', 'DE', 'FR', 'IT', 'UK', 'US']

ed_type= ["RTS", "Tagesschau", "Zdf", "France24", "GR1", "PBS"]
flow_type= ["Zeit", "Televideo", "ilPost", "BBC", "NYT"]

source_conv= {'RTS': 0, 'Tagesschau': 1, 'Zdf': 2, 'France24': 3, 'GR1': 4, 'PBS': 5,
              'Zeit': 0, 'Televideo': 1, 'ilPost': 2, 'BBC': 3, 'NYT': 4}

editions_by_source= [[], [], [], [], [], []]
flows_by_source= [[], [],[], [], []]


#Semlice funzione che dato un file .json ne restituisce un oggetto sse contiene il campo "concepts"
def jsonizer(directory):
    f= open(directory, "r+")
    to_ret= json.load(f)
    f.close()
    to_append= False
    if 'concepts' in to_ret[0]:
        to_append= True
    return to_append, to_ret

#Funzione ausiliaria che data una nazione e un giornale, aggiunge le sue edizioni (o i suoi flussi) al relativo array
def news_getter(nation, source):
    directory= "../newScraping/collectedNews/" + nation + "/" + source
    if source in ed_type:
        for to_append in os.scandir(directory):
            should_i, to_append= jsonizer(directory + "/" + to_append.name)
            if should_i:
                editions_by_source[source_conv[source]].append(to_append)
    elif source in flow_type:
            for to_append in os.scandir(directory):
                should_i, to_append= jsonizer(directory + "/" + to_append.name)
                if should_i:
                    flows_by_source[source_conv[source]].append(to_append)
    else:
        print("Source not recognized")


#Funzione naif che compara due news e restituisce grado di similarità e parole uguali
def compare(news_a, news_b):
    is_simil= 0
    to_ret= []
    for concept_a in news_a['concepts']:
        for concept_b in news_b['concepts']:
            if concept_a['word'] == concept_b['word']:
                to_ret.append(concept_a)
                is_simil+= 0.5
    return is_simil, to_ret

#Funzione che dato un array di giornali, restituisce una lista di notizie simili con concatenati i concetti simili
def news_comparing(sources):
    simil= []
    for i in range(0, len(sources)):
        for j in range(i+1, len(sources)):
            for edition_a in sources[i]:
                for edition_b in sources[j]:
                    for news_a in edition_a:
                        for news_b in edition_b:
                            rate, concepts= compare(news_a, news_b)
                            if rate >= 1:
                                to_app= []
                                to_app.append(news_a)
                                to_app.append(news_b)
                                to_ret= {'concepts': concepts, 'news': to_app}
                                simil.append(to_ret)
    return simil
    


for nation in nations:
    dir= "../newScraping/collectedNews/" + nation
    for source_dir in os.scandir(dir):
        source= source_dir.name
        news_getter(nation, source)
f= open("editions_simils.txt", "w")
simil_ed = news_comparing(editions_by_source)
json.dump(simil_ed, f, indent= 4, ensure_ascii= False)
f.close()
f= open("flows_simils.txt", "w")
simil_fl = news_comparing(flows_by_source)
json.dump(simil_fl, f, indent= 4, ensure_ascii= False)
f.close()