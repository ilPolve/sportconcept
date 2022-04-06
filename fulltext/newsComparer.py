#!/usr/bin/env python

import json
import os
import sys
import errno

#The analyzed news base directory
BASE_DIR = f"./NER"

#The output base directory
COMPARED = f"./compared"

#The fields name we want to compare
TO_COMPARE = ['title']

#The english-to translated fields' prefix
ENGLISH_PREFIX = "en_"

#Scraped hour range for comparison (in hour)
HOUR_RANGE = 2


#Called with arguments like: path_newspaper_A path_newspaper_B date hour
def main():
    if len(sys.argv) < 5:
        raise Exception("Too few arguments.")
    else:
        full_comparer(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])

def full_comparer(newsp_A, newsp_B, date, hour):
    news_A = multi_news_getter(newsp_A, int(hour), date)
    news_B = multi_news_getter(newsp_B, int(hour), date)
    comparison = news_comparer(news_A, news_B)
    jsonizer(comparison, path_formatter(newsp_A, newsp_B, date, hour))


def multi_news_getter(newsp, start_hour, date):
    final_hour = start_hour + HOUR_RANGE

    multi_path = []

    for subdir in os.scandir(f"{BASE_DIR}/{newsp}"):
        filename = subdir.name
        scrape_date = filename.split("T")[0]
        scrape_time = filename.split("T")[1].split("E")[0]
        scrape_hour = int(scrape_time.split(".")[0])

        if scrape_date == date:
            if scrape_hour >= start_hour and scrape_hour <= final_hour:
                multi_path.append(filename)
        
    to_ret = []
    for single_path in multi_path:
        to_ret.append(news_getter(f"{newsp}/{single_path}"))
    return to_ret

def news_getter(subdir):
    to_get_dir = f"{BASE_DIR}/{subdir}"
    to_get = {}
    with open(to_get_dir, "r") as f:
        try:
            to_get = json.load(f)
        except:
            raise Exception("Could not read file from the given directory: " + to_get_dir + ".")
    return to_get


def news_comparer(news_A, news_B):
    


def jsonizer(comparison, path_A, path_B):
    to_json_dir = f"{comparison.nameA}/{comparison.nameB}/{comparison.hour}"
    if not os.path.exists(os.path.dirname(to_json_dir)):
        try:
            os.makedirs(os.path.dirname(to_json_dir))
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise
    with open(to_json_dir, "w") as f:
        json.dump(comparison, f, indent= 4, ensure_ascii= False)
        f.write("\n")

def path_formatter(path_A, path_B, date, hour):
    newsp_A = path_A.split("/")
    newsp_B = path_B.split("/")
    newsp_A = newsp_A[len(newsp_A)-1]
    newsp_B = newsp_B[len(newsp_B)-1]
    final_hour = str(int(hour) + HOUR_RANGE)
    to_ret = f"{max(newsp_A, newsp_B)}/{min(newsp_A, newsp_B)}/{date}/{hour}-{final_hour}.json"
    return to_ret

if __name__ == "__main__":
    main()