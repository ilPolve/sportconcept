#!/usr/bin/env python

import json
from argostranslate import package, translate
import sys
import os
import errno

#The scraped news base directory
BASE_DIR= f"../../Newscraping/collectedNews"

#The output base directory
TRANSLATED_DIR= f"./translated"

#The translators indexes based on the source language
LANG_TO_TRANS = {'FR': 0,
                 'DE': 1,
                 'IT': 2,
                 'ES': 3,
                 'en': 0,
                 'EN': 0}

def main():
    if len(sys.argv) < 2:
        raise Exception("Too few arguments.")
    full_translator(sys.argv[1])

def full_translator(subdir):
    translators = translators_setup()
    to_translate= news_getter(subdir)
    translated = news_translator(to_translate, translators)
    jsonizer(translated, subdir)

#Starting from the 1-st because of the 0-index english translator
def translators_setup():
    translators= [{}, {}, {}, {}]
    installed_languages = translate.get_installed_languages()
    for i in range(1, 5):
        translators[i-1]= installed_languages[i].get_translation(installed_languages[0])
    return translators

def news_getter(subdir):
    to_get_dir= f"{BASE_DIR}/{subdir}"
    to_get= {}
    with open(to_get_dir, "r") as f:
        try:
            to_get = json.load(f)
        except:
            raise Exception("Could not read file from the given directory: " + to_get_dir + ".")
    return to_get

def news_translator(to_trans, translators):
    for article in to_trans:
        if article['title'] != None:
            try:
                article = article_translator(article, translators[LANG_TO_TRANS[article['language']]])
            except:
                article = article_translator(article, translators[LANG_TO_TRANS["EN"]], True)
    return to_trans

def article_translator(article, translator, isEn= False):
    if not isEn and article['language'] != "EN" and article['language'] != "en":
        article['en_title']= translator.translate(article['title'])
        print(article['title'] + "   " + article['en_title'])

        try:
            article['en_content']= translator.translate(article['content'])
        except:
            raise Exception("Could not translate content of an article.")

        try: 
            article['en_subtitle']= translator.translate(article['subtitle'])
        except:
            pass
    else:
        article['en_title'] = article['title']
        
        article['en_content'] = article['content']

        try:
            article['en_subtitle']  = article['subtitle']
        except:
            pass

    return article

def jsonizer(translated, subdir):
    to_json_dir= f"{TRANSLATED_DIR}/{subdir}"
    if not os.path.exists(os.path.dirname(to_json_dir)):
        try:
            os.makedirs(os.path.dirname(to_json_dir))
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise
    with open(to_json_dir, "w") as f:
        json.dump(translated, f, indent= 4, ensure_ascii= False)
        f.write("\n")


if __name__ == "__main__":
    main()