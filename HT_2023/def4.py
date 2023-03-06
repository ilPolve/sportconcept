# 4. How much does a newspaper "churn"?

from os import path
from typing import Union
from utils import date_to_epoch, snapped_news_in_range, remove_duplicates, has_similar_in_pool, SNAP_RATE

start_time = "2022-05-11 01:55:20"
end_time = "2022-05-12 12:55:20"
sources = []


FILE_DIR = path.dirname(__file__)

main_dir = f"{FILE_DIR}/../fulltext/NER/flow/IT"
source = "AGI_Politica"

def main():
    churn_rate(source, start_time, end_time)

def churn_rate(source: str, start_time: str, end_time: str) -> Union[float,  dict]:
    start_epoch = date_to_epoch(start_time)
    end_epoch = date_to_epoch(end_time)
    news_list, snap_list = snapped_news_in_range(f"{main_dir}/{source}", start_epoch, end_epoch)
    news_list = remove_duplicates(news_list)
    
    found = {}

    for article in news_list:
        for snapshot in snap_list:
            if has_similar_in_pool(article, snapshot):
                if article["en_title"] in found:
                    found[article["en_title"]] += 1
                else:
                    found[article["en_title"]] = 1
    
    durations = found.values()
    if len(found) == 0:
        return 0, {}
    max_key = max(found, key=found.get)
    max_value = max(found.values())
    min_key = min(found, key=found.get)
    min_value = min(found.values())
    avg_churn = sum(durations) / len(durations)
    avg_churn_in_mins = avg_churn * SNAP_RATE
    print(f"{source} churns for a mean of {avg_churn:.2f} snapshots ({avg_churn_in_mins} minutes)")
    print(f"Max duration: {max_key} ({max_value} snapshots) ({max_value * SNAP_RATE} minutes)")
    print(f"Min duration: {min_key} ({min_value} snapshots) ({min_value * SNAP_RATE} minutes)")
    return avg_churn, found


if __name__ == "__main__":
    main()

# Example output:
# AGI_Politica churns for a mean of 63.00 snapshots (945.00 minutes)
# Max duration: Press and Palace: Draghi in the US and the clash in the centerright (78 snapshots) (1170 minutes)
# Min duration: Petrocelli is attacking: "No sending weapons and taking away the trust in Draghi" (18 snapshots) (270 minutes)
# return: 63.00
#         {"article_title": snapshots_duration}
