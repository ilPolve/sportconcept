#!/usr/bin/env python

import os
from datetime import datetime
from newsTranslator import full_translator
from globals import TRANSL_IN_DIR, TRANSL_OUT_DIR, NEWS_SOURCES

def main():
    print("LAUNCHED AT: ", datetime.now().strftime("%H:%M:%S"))
    dir_check(TRANSL_IN_DIR, TRANSL_OUT_DIR)
    
    for source_dir in NEWS_SOURCES:
        dir_translator(source_dir)
    print("ENDED AT: ", datetime.now().strftime("%H:%M:%S"))

def dir_check(in_dir, out_dir):
    if not os.path.exists(in_dir):
        raise FileNotFoundError(f"Directory not found: {in_dir}")
    
    if not os.path.exists(out_dir):
        try:
            os.makedirs(out_dir)
            for source in NEWS_SOURCES:
                os.makedirs(f"{out_dir}/flow/{source}")
        except:
            raise Exception(f"Directory {out_dir} does not exist and could not be created")
        
def dir_translator(dir):
    for entry in os.listdir(f"{TRANSL_IN_DIR}/{dir}"):
        if not os.path.exists(f"{TRANSL_OUT_DIR}/{dir}/{entry}"):
            full_translator(f"{dir}/{entry}")
            # full_recognizer(f"{dir}/{subdir.name}", sentiment=1)

if __name__ == "__main__":
    main()
