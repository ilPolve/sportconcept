import json
import os
import spacy

nations= ['CH', 'DE', 'FR', 'IT', 'UK', 'US']

nlp= spacy.load("en_core_web_sm")

basedir = "../newScraping/collectedNews/" 

def create_concept(word, meaning, pos):
    concept= {'word': word, 'meaning': meaning, 'pos': pos}
    return concept

def pos_tagger(editions):
    to_ret= []
    for nat_ed in editions:
        for edition in nat_ed:
            c_edit= []
            for new in edition:
                concepts= []
                #if new['nation']== "CH" or new['nation']=="FR":
                    #nlp= fr_nlp
                #elif new['nation']== "UK" or new['nation']=="US":
                    #nlp= en_nlp
                #elif new['nation']== "IT":
                    #nlp= it_nlp
                #Choosing the right nlp-parser due to the news languages
                #nlp-ing the title
                doc_title= nlp(new['en_title'])
                for t_token in doc_title:
                    #print(t_token.text, t_token.dep_, t_token.head.pos_)
                    if t_token.pos_ == "NOUN" or t_token.pos_ == "PROPN":
                        concepts.append(create_concept(t_token.text, t_token.dep_, t_token.head.pos_))
                #this s a try only because some news may not have a content field, in that case just skip
                #currently not using it because it tends to analyze "sentence-per-sentence", going out of the project target
                #try:
                    #doc_content= nlp(new['en_content'])
                    #for c_token in doc_content:
                        #print(c_token.text, c_token.dep_, c_token.head.pos_)
                        #if c_token.head.pos_ == "NOUN" or  c_token.dep_ == "nsubj":
                            #concepts.append(create_concept(c_token.text, c_token.dep_, c_token.head.pos_))
                #except:
                    #pass
                conceptitle={'title': new['title'],
                            'en_title': new['en_title'],
                            'date': new['date'],
                            'language': new['language'],
                            'source': new['source'],
                            'concepts': concepts}
                new['concepts']= concepts
                #print(json.dumps(conceptitle, indent= 4))
                c_edit.append(conceptitle)
            to_ret.append(c_edit)
            if len(edition) > 0:
                os.remove(basedir + nation + "/" + edition[0]['source'] + "/" + edition[0]['filename'])
                f= open(basedir + nation + "/" + edition[0]['source'] + "/conc_" + edition[0]['filename'], "w")
                json.dump(edition, f, ensure_ascii = False, indent= 4)
                f.close()
    return to_ret
        

def getting_news(nation):
    directory= basedir + nation
    nat_ed= []
    for subdir in os.scandir(directory):
        newspaper= subdir.name
        editions= []
        for news in os.scandir(subdir):
            if(news.name[0:2] == "en"):
                f= open(directory + "/" + newspaper + "/" + news.name, "r+", encoding= "latin-1")            
                curr_news= json.load(f)
                edition= []
                for new in curr_news:
                    new['filename'] = news.name
                    edition.append(new)
                f.close()
                editions.append(edition)
        nat_ed.append(editions)
    return nat_ed 

for nation in nations:
    pos_tagger(getting_news(nation))