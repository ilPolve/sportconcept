#!/usr/bin/env python

import json, sys, os, errno
from argostranslate import translate
from globals import TRANSL_IN_DIR, TRANSL_OUT_DIR

def main():
    if len(sys.argv) < 2:
        raise Exception("Too few arguments.")
    full_translator(sys.argv[1])

def full_translator(subdir):
    translator = translator_setup()
    to_translate = news_getter(subdir)
    translated = news_translator(to_translate, translator)
    jsonizer(translated, subdir)

#Starting from the 1-st because of the 0-index english translator
def translator_setup():
    return translate.get_translation_from_codes(from_code="it", to_code="en")

def news_getter(subdir):
    to_get_dir= f"{TRANSL_IN_DIR}/{subdir}"
    print("TRANSLATING: ", to_get_dir)
    with open(to_get_dir, "r") as f:
        try:
            return json.load(f)
        except:
            raise Exception("Could not read file from the given directory: " + to_get_dir + ".")

def news_translator(to_trans, translator):
    for article in to_trans:
        if article['title'] != None:
            article = article_translator(article, translator)
    return to_trans

def article_translator(article, translator):
    article['en_title']= translator.translate(article['title'])
    
    try:
        if article['content'] is not None:
            article['en_content'] = translator.translate(article['content'])
    except:
        raise Exception("Could not translate content of an article.")
    try: 
        if article['subtitle'] is not None:
            article['en_subtitle'] = translator.translate(article['subtitle'])
    except:
        raise Exception("Could not translate subtitle of an article.")

    return article

def jsonizer(translated, subdir):
    to_json_dir= f"{TRANSL_OUT_DIR}/{subdir}"
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