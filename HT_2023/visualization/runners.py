import sys
sys.path.append("..")

import datetime
import json
import os

from def4 import churn_rate
from triple_def import sce_classify, snapshots_in_range
from utils import date_to_epoch, in_range_epoch

<<<<<<< HEAD
from typing import List
=======
>>>>>>> 5b2fd248146083d8c86068e65eebc492a59022f1

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def add_slice(date, my_slice):
    return date + datetime.timedelta(hours=my_slice)


# Function for running the churn rate calculator in different slices of equal time
# slice is in hours
<<<<<<< HEAD
def churn_run(source: str, start_date: str, end_date: str, my_slice: str) -> List[float]:
=======
def churn_run(source: str, start_date: str, end_date: str, my_slice: str) -> list[float]:
>>>>>>> 5b2fd248146083d8c86068e65eebc492a59022f1
    start_in_date = datetime.datetime.strptime(start_date, DATE_FORMAT)
    end_in_date = datetime.datetime.strptime(end_date, DATE_FORMAT)
    rates = []
    while add_slice(start_in_date, my_slice) < add_slice(end_in_date, my_slice):
        temp_end = add_slice(start_in_date, my_slice)
        rate, _ = churn_rate(source, start_date, temp_end.strftime(DATE_FORMAT))
        if rate != 0:
            rates.append(1/rate)
        else:
            rates.append(0)
        start_in_date = temp_end
        start_date = start_in_date.strftime(DATE_FORMAT)
    return rates


<<<<<<< HEAD
BASE_DIR = os.path.join(os.path.dirname(__file__))

main_dir = f"../../fulltext/translated"
=======
main_dir = "../../fulltext/translated"
>>>>>>> 5b2fd248146083d8c86068e65eebc492a59022f1
snap_dir = "DE/Spiegel"

in_range = True

<<<<<<< HEAD
# Now we consider between 13-03 and 18-03
start_date = int(date_to_epoch("2023-03-11 08:00:00"))
end_date = int(date_to_epoch("2023-03-12 08:01:00"))
=======
start_date = int(date_to_epoch("2023-03-15 00:01:00"))
end_date = int(date_to_epoch("2023-03-15 23:59:00"))
>>>>>>> 5b2fd248146083d8c86068e65eebc492a59022f1


def triple_def_run(in_range: bool = False, start_date: int = None, end_date: int = None):
    sce: dict[str, dict[str, int]] = {}
    for lang in os.listdir(f"{main_dir}"):
        news_outlets = os.listdir(f"{main_dir}/{lang}")
        for news_outlet in news_outlets:
            # Switch for linux filesystem
<<<<<<< HEAD
            sce[f"{lang}/{news_outlet}"] = {"skipped": 0, "exclusive": 0, "common": 0}
            # idx = lang
            # # if "SwissScrape" not in main_dir:
            # #     idx = f"{lang}\\{news_outlet}"
            # sce[idx] = {"skipped": 0, "exclusive": 0, "common": 0}
=======
            # sce[f"{lang}/{news_outlet}"] = {"skipped": 0, "exclusive": 0, "common": 0}
            idx = lang
            if "SwissScrape" not in main_dir:
                idx = f"{lang}\\{news_outlet}"
            sce[idx] = {"skipped": 0, "exclusive": 0, "common": 0}
>>>>>>> 5b2fd248146083d8c86068e65eebc492a59022f1

    simil_cache = {}
    snapshots = snapshots_in_range(in_range, start_date, end_date, nlpy=True)

    # nlp_all_the_things!
    news_items = get_all_news_items(main_dir, in_range=in_range, start_date=start_date, end_date=end_date)
<<<<<<< HEAD
    # print(snapshots)
=======
    print(snapshots)
>>>>>>> 5b2fd248146083d8c86068e65eebc492a59022f1

    for news_item in news_items:
        skipped, exclusive, common = sce_classify(news_item, simil_cache, snapshots)
        for news_outlet in sce:
            if news_outlet in skipped:
                sce[news_outlet]["skipped"] += 1
            if news_outlet in exclusive:
                sce[news_outlet]["exclusive"] += 1
            if news_outlet in common:
                sce[news_outlet]["common"] += 1
    print(sce)

<<<<<<< HEAD
    with open('special_issue/triple_def_out_11_24hours.json', 'w', encoding="utf-8") as fp:
=======
    with open('special_issue\\triple_def_out_15_3.json', 'w', encoding="utf-8") as fp:
>>>>>>> 5b2fd248146083d8c86068e65eebc492a59022f1
        json.dump(sce, fp, indent=4)
        fp.write("\n")

    return sce


<<<<<<< HEAD
def get_all_news_items(dir: str, in_range: bool = False, start_date: int = None, end_date: int = None) -> List[dict]:
=======
def get_all_news_items(dir: str, in_range: bool = False, start_date: int = None, end_date: int = None) -> list[dict]:
>>>>>>> 5b2fd248146083d8c86068e65eebc492a59022f1
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


<<<<<<< HEAD
def all_snap_getter(full_dir: str, all_snap: List[dict], title_list: List[str]) -> List[dict]:
=======
def all_snap_getter(full_dir: str, all_snap: list[dict], title_list: list[str]) -> list[dict]:
>>>>>>> 5b2fd248146083d8c86068e65eebc492a59022f1
    for news in json.load(open(full_dir, "r", encoding="utf-8")):
        if not news["title"] in title_list:
            title_list.append(news["title"])
            all_snap.append(news)
    return all_snap


def main_news_getter(check_dir: str, idx: int) -> dict:
    with open(check_dir, "r") as f:
        news = json.load(f)
    single_news = news[idx]
    return single_news


def main():
    triple_def_run(in_range, start_date, end_date)


if __name__ == "__main__":
    main()
