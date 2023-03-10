# 5. Given a news, a outlet (and an environment),
#    is the news being skipped by the outlet?
#    If no, is it exclusive or in common with other outlets?

import json
import random
from typing import Union, List, Tuple
from utils import snapped_news_by_source, has_similar_in_pool, snapped_news_in_range

# For fast example:
main_dir = "../fulltext/NER/flow/IT"
snap_dir = "ANSA_Politica"
news_snap = "2022-05-11T17.34.30E1652290470.188478.json"

ALL_DIRS = ["AGI_Politica", "AGI_Esteri"]

check_dir = "ANSA_Politica"
to_check_dir = f"{main_dir}/{snap_dir}/{news_snap}"

# For real example:
main_dir = "../../../All_News/ConcepTitle/fulltext/NER/flow"
ALL_DIRS = ["EN/CNN", "ES/ABC", "FR/France24", "EN/BBC", "DE/Spiegel"]



def main():
    to_check = main_news_getter(to_check_dir)
    skip_common_excl(to_check, check_dir)

def skip_common_excl(to_check: dict, check_dir: str, simil_cache: dict = {}, in_range: bool = False, start_date: str = None, end_date: str = None) -> Union[str, List[str]]:
    main_snapped = []
    if in_range:
        main_snapped, _ = snapped_news_in_range(f"{main_dir}/{check_dir}", start_date, end_date)
    else:
        main_snapped = snapped_news_by_source(f"{main_dir}/{check_dir}")
    if not has_similar_in_pool(to_check, main_snapped):
        print("skipped")
        print([])
        return "skipped", []
    covering_list = []
    for dir in ALL_DIRS:
        snapped = snapped_news_by_source(f"{main_dir}/{dir}")
        if has_similar_in_pool(to_check, snapped, simil_cache):
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

def sce_lister(to_check: dict, simil_cache: dict = {}, in_range: bool = False, start_date: str = None, end_date: str = None) -> Tuple[List[str]]:
    sce_list = []
    for dir in ALL_DIRS:
        snapped = []
        if in_range:
            snapped, _ = snapped_news_in_range(f"{main_dir}/{dir}", start_date, end_date)
        else:
            snapped = snapped_news_by_source(f"{main_dir}/{dir}")
        if has_similar_in_pool(to_check, snapped, simil_cache):
            sce_list.append(dir)
    skipped = []
    exclusive = []
    common = []
    for dir in ALL_DIRS:
        if len(sce_list) == 1:
            if dir == sce_list[0]:
                exclusive.append(dir)
            else:
                skipped.append(dir)
        else:
            if dir in sce_list:
                common.append(dir)
            else:
                skipped.append(dir)
    return (skipped, exclusive, common)

def main_news_getter(dir: str) -> dict:
    with open(dir, "r") as f:
        news = json.load(f)
    n_new = random.randint(0, len(news)-1)
    single_news = news[n_new]
    return single_news

if __name__ == "__main__":
    main()

# Example output:
# return: "skipped", []
#         "exclusive", ["ANSA_Politica"]
#         "common", ["AGI_Politica", "ANSA_Politica"]