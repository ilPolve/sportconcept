#!/usr/bin/env python

import sys
import os

from newsTranslator import full_translator
from newsNER import full_recognizer

ESTENSION_CHECK = ".json"

GET_DIR = "../../Newscraping/collectedNews"

CHECK_DIR = "./translated"

def main():
    if len(sys.argv) < 2:
        raise Exception("Too few arguments.")
    dir_translator(sys.argv[1])

def dir_translator(dir):
    for subdir in os.scandir(f"{GET_DIR}/{dir}"):
        print(subdir.name[len(subdir.name)-5:])
        if new_trans_check(dir, subdir.name):
            if "2022" in subdir.name and "04" in subdir.name:
                print(subdir.name)
                full_translator(f"{dir}/{subdir.name}")
                full_recognizer(f"{dir}/{subdir.name}", sentiment=1)
    
def new_trans_check(dir, to_check):
    for subdir in os.scandir(f"{CHECK_DIR}/{dir}"):
        if subdir.name == to_check or subdir.name[len(subdir.name)-5:] != ESTENSION_CHECK:
            return False
    return True

if __name__ == "__main__":
    main()