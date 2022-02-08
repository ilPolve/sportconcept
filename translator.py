import json
import os
from argostranslate import package, translate
import copy
import time
import httpx

mysubdirs= ['edition/DE', 'edition/FR', 'edition/EN', 'edition/IT', 'flow/DE', 'flow/EN', 'flow/IT']
edition_str_len= 15
BASE_DIR = f"../Newscraping/collectedNews/"


subdir_n_to_lang= {'FR': 'fr',
                 'DE': 'de',
                 'IT': 'it',
                 'EN': 'en'}

lang_to_translator= {'fr': 0, 'de': 1, 'it': 2}

def main():
    translators = translators_setup()
    for subdir_n in mysubdirs:
        news_translator(subdir_n, translators)

def translators_setup():
    translators= [{}, {}, {}]
    installed_languages = translate.get_installed_languages()
    for i in range(1, 4):
        translators[i-1]= installed_languages[i].get_translation(installed_languages[0])
    return translators

#A utility function which allows me to print Unicode encoded chars
def unicode_fix(to_fix):
    for news in to_fix:
        for new in news:
            for dict_attr in new:
                try:
                    new[dict_attr]= new[dict_attr].encode("ascii", errors= "ignore").decode("ascii")
                #in case there are ints and not strings
                except:
                    pass
    return to_fix

#function who translates a given string into a given language
#currently not used due to the very slow running of googletrans lib
def to_english(new, lang, translator):
    curr_news_en= copy.deepcopy(new)
    if lang != "en":
        curr_news_en['en_title'] = translator.translate(curr_news_en['title'])
        print(curr_news_en['en_title'])
    else:
        curr_news_en['en_title']= curr_news_en['title']
    try:
        if lang != "en":
            curr_news_en['en_content'] = translator.translate(curr_news_en['content'])
        else:
            curr_news_en['en_content']= curr_news_en['content']
    except:
        pass
    return curr_news_en

#Function which populates arrays of news, based on edition or flow type of news
def news_translator(subdir_n, translators):
    directory=  f"{BASE_DIR}{subdir_n}"
    for subdir in os.scandir(directory):
        newspaper= subdir.name
        for news in os.scandir(subdir):
            if news.name[0:2] != "en" and news.name[0:2] != "co":
                to_trans_dir= f"{directory}/{newspaper}/{news.name}"
                with open(to_trans_dir, "r") as f:  
                    try:     
                        curr_news= json.load(f)
                    except: 
                        continue
                    curr_edit= []
                    #adding new conceptual informations to the news
                    for curr_new in curr_news:
                        if curr_new['title'] != None:
                            subdir_n= subdir_n[(len(subdir_n)-2):(len(subdir_n))]
                            curr_new['language']= subdir_n_to_lang[subdir_n]
                            curr_new['source']= newspaper
                            curr_new['filename']= news.name
                            time.sleep(0.1)
                            #now create a hardcopy in order to have the same new, but in English
                            translator_to_pass= {}
                            if curr_new['language'] != 'en':
                                translator_to_pass = translators[lang_to_translator[curr_new['language']]]
                            curr_news_en= to_english(curr_new, curr_new['language'], translator_to_pass)
                            curr_edit.append(curr_news_en)
                #replacing the old news-file with a new one with english content added
                print(to_trans_dir)
                os.remove(to_trans_dir)
                translated_dir = f"{directory}/{newspaper}/en_{news.name}"
                with open(translated_dir, "w") as f:
                    json.dump(curr_edit, f, indent= 4, ensure_ascii= False)
                    f.write("\n")


if __name__ == "__main__":
    main()