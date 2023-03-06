# 2. Given a newspaper, how much does it skip usually?

import json
import os

from utils import snapped_news_by_source, snapped_news_by_date, has_similar_in_pool, remove_duplicates

sources_dir = ["ANSA_Politica", "ANSA_Cronaca", "ANSA_Esteri"]
main_dir = "../fulltext/NER/flow/IT"

check_date = "2022-05-11"


def main():
    skip_usually(sources_dir, check_date)

def skip_usually(source: str, day: str) -> float:
    skipped = 0
    published_in_date_by_source = []
    for source in sources_dir:
        temp = snapped_news_by_source(f"{main_dir}/{source}")
        # To use only in this case, in general we should use all news
        for article in temp:
            if article["date"] == day:
                published_in_date_by_source.append(article)
    # Also here, in general we get all news by all sources every day
    published_in_date = snapped_news_by_date(check_date)

    published_in_date = remove_duplicates(published_in_date)

    for article in published_in_date:
        if not has_similar_in_pool(article, published_in_date_by_source):
            skipped += 1
    skipped_percentage = (skipped / len(published_in_date))*100
    print(f"{sources_dir} skips a mean of {skipped_percentage:.2f}% news")
    return skipped_percentage


if __name__ == "__main__":
    main()

# Example output:
# ['ANSA_Politica', 'ANSA_Cronaca', 'ANSA_Esteri'] skips a mean of 39.08% news
# return: 39.08