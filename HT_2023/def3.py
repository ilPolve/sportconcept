# 3. Given two newspapers A and B, how much does A skip with regards to B?

data_days = ["2022-05-11", "2022-05-12"]
sources_dir_A = ["ANSA_Politica"]
sources_dir_B = ["AGI_Politica"]

def main1():
    skip_between(sources_dir_A, sources_dir_B)

def skip_between(source_A, source_B):
    skip_means = []
    for day in data_days:
        skip_means.append(skip_between_day(source_A, source_B, day))
    print(f"{source_A} skips a mean of {sum(skip_means)/len(skip_means):.2f}% news of {source_B}")
    return skip_means

# 3b. Given two newspapers A and B, how much does A skip with regards to B, in a given day(/hour/temporal frame)?

from utils import snapped_news_by_source, has_similar_in_pool

main_dir = "../fulltext/NER/flow/IT"

def main2():
    skip_between_day(sources_dir_A, sources_dir_B, "2022-05-11")

def skip_between_day(source_A, source_B, day):
    skipped = 0
    published_in_date_by_source_A = []
    for source in source_A:
        temp = snapped_news_by_source(f"{main_dir}/{source}")
        for article in temp:
            if article["date"] == day:
                published_in_date_by_source_A.append(article)
    published_in_date_by_source_B = []
    for source in source_B:
        temp = snapped_news_by_source(f"{main_dir}/{source}")
        for article in temp:
            if article["date"] == day:
                published_in_date_by_source_B.append(article)

    for article in published_in_date_by_source_A:
        if not has_similar_in_pool(article, published_in_date_by_source_B):
            skipped += 1
    skipped_percentage = -1 if len(published_in_date_by_source_A) == 0 else (skipped / len(published_in_date_by_source_A))*100
    print(f"{source_A} skipped a mean of {skipped_percentage:.2f}% news of {source_B} on {day}")
    return skipped_percentage

if __name__ == "__main__":
    main1()
    main2()

# Example output:
# 3
# ['ANSA_Politica'] skipped a mean of 63.19% news of ['AGI_Politica']
# return: [57.14, 69.24] 
#
# 3b
# ['ANSA_Politica'] skipped a mean of 57.14% news of ['AGI_Politica'] on 2022-05-11
# return: 57.14