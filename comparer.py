import json
import os

my_subdirs= ['edition/DE', 'edition/FR', 'edition/EN', 'edition/IT', 'flow/DE', 'flow/EN', 'flow/IT']

ed_type= ["RTS", "Tagesschau", "Zdf", "France24", "GR1", "PBS"]
flow_type= ["Zeit", "Televideo", "ilPost", "BBC", "NYT"]

source_conv= {'RTS': 0, 'Tagesschau': 1, 'Zdf': 2, 'France24': 3, 'GR1': 4, 'PBS': 5,
              'Zeit': 0, 'Televideo': 1, 'ilPost': 2, 'BBC': 3, 'NYT': 4}

editions_by_source= [[], [], [], [], [], []]
flows_by_source= [[], [],[], [], []]

simil_clean = []

def main():
    for my_subdir in my_subdirs:
        dir= "../newScraping/collectedNews/" + my_subdir
        for source_dir in os.scandir(dir):
            source= source_dir.name
            news_getter(my_subdir, source)
    f= open("editions_simils.txt", "w")
    simil_ed = source_comparing(editions_by_source)
    #next three lines are for a simpler visualization of the simil_file
    global simil_clean
    simil_ed = simil_clean
    simil_clean = []
    json.dump(simil_ed, f, indent= 4, ensure_ascii= False)
    f.close()
    f= open("flows_simils.txt", "w")
    simil_fl = source_comparing(flows_by_source)
    #next two lines are for a simpler visualization of the simil_file
    simil_fl = simil_clean
    simil_clean =[]
    json.dump(simil_fl, f, indent= 4, ensure_ascii= False)
    f.close()

#Semlice funzione che dato un file .json ne restituisce un oggetto sse contiene il campo "concepts"
def jsonizer(directory):
    f= open(directory, "r+")
    #print(directory)
    to_ret= json.load(f, encoding='mac_roman')
    f.close()
    to_append= False
    if 'concepts' in to_ret[0]:
        to_append= True
    return to_append, to_ret

#Funzione ausiliaria che data una nazione e un giornale, aggiunge le sue edizioni (o i suoi flussi) al relativo array
def news_getter(my_subdir, source):
    directory= "../newScraping/collectedNews/" + my_subdir + "/" + source
    if source in ed_type:
        for to_append in os.scandir(directory):
            should_i, to_append= jsonizer(directory + "/" + to_append.name)
            if should_i:
                global editions_by_source
                editions_by_source[source_conv[source]].append(to_append)
    elif source in flow_type:
            for to_append in os.scandir(directory):
                should_i, to_append= jsonizer(directory + "/" + to_append.name)
                if should_i:
                    global flows_by_source
                    flows_by_source[source_conv[source]].append(to_append)
    else:
        print("Source not recognized")


#Funzione naif che compara due news e restituisce grado di similarità e parole uguali
def compare_naif(news_a, news_b):
    to_ret= {}
    conc_to_ret= []
    n_A= 0
    n_B= 0
    couples= 0
    for concept_a in news_a['concepts']:
        n_A+=1
        n_B= 0
        for concept_b in news_b['concepts']:
            n_B+=1
            if concept_a['word'] == concept_b['word']:
                couples+=1
                conc_to_ret.append(concept_a)
    if couples > 1:
        similar= True
    else:
        similar= False
    to_ret['similar']= similar
    to_ret['n_found']= couples
    to_ret['n_newA']= n_A
    to_ret['n_newB']= n_B
    to_ret['n_possible']= n_A*n_B
    to_ret['concepts_found']= conc_to_ret
    return similar, to_ret

#Funzione che dato un array di sources di notizie, restituisce le coppie di notizie dello stesso giorno simili
def source_comparing(sources):
    to_ret= []
    for i in range(0, len(sources)):
        for j in range(i+1, len(sources)):
            temp = edition_comparing(sources[i], sources[j])
            if len(temp) > 0:
                to_ret.append(temp)
    return to_ret

#Funzione che dati due array di edizioni, restituisce le coppie di notizie dello stesso giorno simili
def edition_comparing(editions_a, editions_b):
    to_ret = []
    for edition_a in editions_a:
        for edition_b in editions_b:
            try:
                date_a = edition_a[0]['date']
                date_b = edition_b[0]['date']
            except:
                date_a = edition_a[0]['date_raw']
                date_b = edition_b[0]['date_raw']
            if date_a == date_b:
                temp = news_comparing(edition_a, edition_b)
                if len(temp) > 0:
                    to_ret.append(temp)
    return to_ret

#Funzione che dati due array di notizie, restituisce una lista di notizie simili con concatenati i concetti simili
def news_comparing(edition_a, edition_b):
    simil= []
    for news_a in edition_a:
        #max = 2
        for news_b in edition_b:
            #if max <= 0:
                 #break
            are_similar, concepts= compare_naif(news_a, news_b)
            if are_similar:
                to_app= []
                to_app.append(news_a)
                to_app.append(news_b)
                to_ret= {'concepts': concepts, 'news': to_app}
                global simil_clean
                simil_clean.append(to_ret)
                simil.append(to_ret)
                #max-=1
    return simil

if __name__ == "__main__":
    main()