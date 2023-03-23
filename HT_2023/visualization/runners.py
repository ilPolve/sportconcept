import sys
sys.path.append("..")
from def4 import churn_rate
from triple_def import skip_common_excl, sce_lister
from typing import List
from utils import date_to_epoch, in_range_epoch
import datetime
import random
import json
import os


DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

def add_slice(date, slice):
    return date + datetime.timedelta(hours=slice)

# Function for running the churn rate calculator in different slices of equal time
# slice is in hours
def churn_run(source: str, start_date: str, end_date: str, slice: str) -> List[float]:
    start_in_date = datetime.datetime.strptime(start_date, DATE_FORMAT)
    end_in_date = datetime.datetime.strptime(end_date, DATE_FORMAT)
    rates = []
    while add_slice(start_in_date, slice) < add_slice(end_in_date, slice):
        temp_end = add_slice(start_in_date, slice)
        rate, _ = churn_rate(source, start_date, temp_end.strftime(DATE_FORMAT))
        if rate != 0:
            rates.append(1/rate)
        else:
            rates.append(0)
        start_in_date = temp_end
        start_date = start_in_date.strftime(DATE_FORMAT)
    return rates

main_dir = "../../fulltext/NER/flow"
snap_dir = "DE/Spiegel"

in_range = True
start_date = date_to_epoch("2023-03-16 08:00:00")
end_date = date_to_epoch("2023-03-16 20:01:00")

def triple_def_run(in_range = False, start_date = None, end_date = None):
    values = {}
    simil_cache = {}
    for lang in os.listdir(f"{main_dir}"):
        for source in os.listdir(f"{main_dir}/{lang}"):
            # Switch for linux filesystemh
            # values[f"{lang}/{source}"] = {"skipped": 0, "exclusive": 0, "common": 0}
            values[f"{lang}\\{source}"] = {"skipped": 0, "exclusive": 0, "common": 0}
    all_news = all_news_getter(main_dir, in_range=in_range, start_date=start_date, end_date=end_date)
    for to_check in all_news:
        skipped, exclusive, common = sce_lister(to_check, simil_cache, \
                                                in_range=in_range, start_date=start_date, \
                                                end_date=end_date)
        for source in values:
            if source in skipped:
                values[source]["skipped"] += 1
            if source in exclusive:
                values[source]["exclusive"] += 1
            if source in common:
                values[source]["common"] += 1
        print(values)
    with open('triple_def_out.json', 'w', encoding="utf-8") as fp:
        json.dump(values, fp, indent=4)
        fp.write("\n")
    return values

def all_news_getter(dir: str, in_range: bool = False, start_date: str = None, end_date: str = None) -> List[dict]:
    all_snap = []
    title_list = []
    for lang in os.listdir(f"{dir}"):
        for source in os.listdir(f"{dir}/{lang}"):
            for file in os.listdir(f"{dir}/{lang}/{source}"):
                if file.endswith(".json"):
                    if (not in_range) or in_range_epoch(file, start_date, end_date):
                        full_dir = f"{dir}/{lang}/{source}/{file}"
                        all_snap_getter(full_dir, all_snap, title_list)
    return all_snap

def all_snap_getter(full_dir: str, all_snap: List[dict], title_list: List[str]) -> List[dict]:
    for news in json.load(open(full_dir, "r", encoding="utf-8")):
        if not news["title"] in title_list:
            title_list.append(news["title"])
            all_snap.append(news)
    return all_snap

def main_news_getter(dir: str, idx: int) -> dict:
    with open(dir, "r") as f:
        news = json.load(f)
    single_news = news[idx]
    return single_news

def main():
    triple_def_run(in_range, start_date, end_date)

if __name__ == "__main__":
    main()