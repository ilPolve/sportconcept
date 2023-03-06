# 5. Given a news, a outlet (and an environment),
#    is the news being skipped by the outlet?
#    If no, is it exclusive or in common with other outlets?

import json
import random
from typing import Union, List
from utils import snapped_news_by_source, has_similar_in_pool

main_dir = "../fulltext/NER/flow/IT"
snap_dir = "ANSA_Politica"
news_snap = "2022-05-11T17.34.30E1652290470.188478.json"


check_dir = "ANSA_Politica"
ALL_DIRS = ["AGI_Politica", "AGI_Esteri"]

to_check_dir = f"{main_dir}/{snap_dir}/{news_snap}"

def main():
    to_check = main_news_getter(to_check_dir)
    skip_common_excl(to_check, check_dir)

def skip_common_excl(to_check: dict, check_dir: str) -> Union[str, List[str]]:
    main_snapped = snapped_news_by_source(f"{main_dir}/{check_dir}")
    if not has_similar_in_pool(to_check, main_snapped):
        print("skipped")
        print([])
        return "skipped", []
    covering_list = []
    for dir in ALL_DIRS:
        snapped = snapped_news_by_source(f"{main_dir}/{dir}")
        if has_similar_in_pool(to_check, snapped):
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

def main_news_getter(dir: str) -> dict:
    with open(dir, "r") as f:
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