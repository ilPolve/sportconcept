# 5. Given a news, a outlet (and an environment),
#    is the news being skipped by the outlet?
#    If no, is it exclusive or in common with other outlets?

import json
import os
import random
from typing import Optional, Union, List, Tuple
from utils import snapped_news_by_source, has_similar_in_snapshot, snapped_news_in_range, Snapshot, similar_in_snapshot_linked, similar_in_snapshot_spacy

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# For fast example:
repo_dir = "../fulltext/NER/flow/IT"
snap_dir = "ANSA_Politica"
news_snap = "2022-05-11T17.34.30E1652290470.188478.json"

ALL_NEWS_OUTLETS = ["AGI_Politica", "AGI_Esteri"]

check_dir = "ANSA_Politica"
to_check_dir = f"{repo_dir}/{snap_dir}/{news_snap}"

# For real example:
repo_dir = f"{BASE_DIR}\\..\\fulltext\\translated"
ALL_NEWS_OUTLETS = ["IT\\ilPost", "ES\\ABC", "FR\\France24", "EN\\BBC", "DE\\Spiegel", "IT\\ANSA_Esteri"]


# Trying Swissinfo
# repo_dir = f"{BASE_DIR}\\..\\..\\SwissScrape\\scraped_items"
# snap_dir = "ITA"
# news_snap = "2023-09-23T18.16.42E1695493002.188904.json"
# check_dir = "ITA"
# to_check_dir = f"{repo_dir}\\{snap_dir}\\{news_snap}"
# ALL_NEWS_OUTLETS = ["GER", "FRE", "ENG", "SPA"]

NLPY = True

SIMIL_FUN = similar_in_snapshot_linked
if NLPY:
    SIMIL_FUN = similar_in_snapshot_spacy


def main():
    to_check = main_news_getter(to_check_dir)
    skip_common_excl(to_check, check_dir)

def skip_common_excl(to_check: dict, check_dir: str, simil_cache: dict = {}, in_range: bool = False, start_date: str = None, end_date: str = None) -> Union[str, List[str]]:
    main_snapped = []
    if in_range:
        main_snapped, _ = snapped_news_in_range(f"{repo_dir}/{check_dir}", start_date, end_date, nlpy=NLPY)
    else:
        main_snapped = snapped_news_by_source(f"{repo_dir}/{check_dir}", nlpy = NLPY)
    if not has_similar_in_snapshot(to_check, main_snapped, simil_fun=SIMIL_FUN):
        print("skipped")
        print([])
        return "skipped", []
    covering_list = []
    for dir in ALL_NEWS_OUTLETS:
        snapped = snapped_news_by_source(f"{repo_dir}/{dir}", nlpy = NLPY)
        if has_similar_in_snapshot(to_check, snapped, simil_cache, simil_fun=SIMIL_FUN):
            covering_list.append(dir)

    covering_list.append(check_dir)
    if len(covering_list) == 1:
        print("exclusive")
        print(covering_list)
        return "exclusive", covering_list
    else:
        print("common")
        print(covering_list)
        return "common", covering_list


def snapshots_in_range(
    in_range: bool,
    start_date: int,
    end_date: int,
    nlpy: bool = NLPY,
) -> dict[str, Snapshot]:
    snapshots = {}
    for news_outlet in ALL_NEWS_OUTLETS:
        if in_range:
            snapshot, _ = snapped_news_in_range(f"{repo_dir}/{news_outlet}", start_date, end_date, nlpy=nlpy)
        else:
            snapshot = snapped_news_by_source(f"{repo_dir}/{news_outlet}", nlpy = nlpy)

        snapshots[news_outlet] = snapshot

    return snapshots


def sce_classify(
    news_item_to_check: dict,
    simil_cache: dict,
    snapshots: dict[str, Snapshot],
) -> tuple[list[str], list[str], list[str]]:
    sce_list = []
    for news_outlet, snapshot in snapshots.items():
        if has_similar_in_snapshot(news_item_to_check, snapshot, simil_cache, simil_fun=SIMIL_FUN):
            sce_list.append(news_outlet)

    skipped = []
    exclusive = []
    common = []
    for news_outlet in ALL_NEWS_OUTLETS:
        if len(sce_list) == 1:
            if news_outlet == sce_list[0]:
                exclusive.append(news_outlet)
            else:
                skipped.append(news_outlet)
        else:
            if news_outlet in sce_list:
                common.append(news_outlet)
            else:
                skipped.append(news_outlet)

    return skipped, exclusive, common


def main_news_getter(dir: str) -> dict:
    with open(dir, "r", encoding="utf-8") as f:
        news = json.load(f)
    n_new = random.randint(0, len(news)-1)
    n_new = 0
    single_news = news[n_new]
    return single_news

if __name__ == "__main__":
    main()

# Example output:
# return: "skipped", []
#         "exclusive", ["ANSA_Politica"]
#         "common", ["AGI_Politica", "ANSA_Politica"]