# 2. Given a newspaper, how much does it skip usually?

import json
import os

from utils import snapped_news_by_source, snapped_news_by_date, has_similar_in_pool

sources_dir = ["ANSA_Politica", "ANSA_Cronaca", "ANSA_Esteri"]
main_dir = "../fulltext/NER/flow/IT"

check_date = "2022-05-11"


def main():
    skip_usually(sources_dir, check_date)

def skip_usually(source, day):
    skipped = 0
    published_in_date_by_source = []
    for source in sources_dir:
        temp = snapped_news_by_source(f"{main_dir}/{source}")
        for article in temp:
            if article["date"] == day:
                published_in_date_by_source.append(article)
    published_in_date = snapped_news_by_date(check_date, "ANSA")

    for article in published_in_date_by_source:
        if not has_similar_in_pool(article, published_in_date):
            skipped += 1
    skipped_percentage = (skipped / len(published_in_date_by_source))*100
    print(f"{sources_dir} skips a mean of {skipped_percentage:.2f}% news")
    return skipped_percentage


if __name__ == "__main__":
    main()

# Example output:
# ['ANSA_Politica', 'ANSA_Cronaca', 'ANSA_Esteri'] skips a mean of 76.19% news
# return: 76.19