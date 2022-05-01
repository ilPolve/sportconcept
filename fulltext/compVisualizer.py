#!/usr/bin/env python

import json
import os
import sys
import errno

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

BASE_URL = f"full_compared/"

TO_DO = ["ANSA", "AGI"]


DATES = ["2022-04-28", "2022-04-29"]

START_HOUR = 22

def main():
    plt.close()
    for i in range(0, len(TO_DO)):
        for j in range(i+1, len(TO_DO)):
            two_visualizer(f"{BASE_URL}{max(TO_DO[i], TO_DO[j])}/{min(TO_DO[i], TO_DO[j])}/", max(TO_DO[i], TO_DO[j]), min(TO_DO[i], TO_DO[j]))

def two_visualizer(path, newsp_A, newsp_B):
    both_cov_standard = []
    both_cov_cos = []

    cov_A_st = []
    cov_A_cos = []
    sent_A = []
    sub_A = []

    cov_B_st = []
    cov_B_cos = []
    sent_B = []
    sub_B = []

    hours = []
    curr_date = DATES[0]

    curr_hour = START_HOUR


    while curr_hour != START_HOUR or curr_date != DATES[1]:
        
        if curr_hour == 24:
            curr_date = DATES[1]
            curr_hour= 0

        pathname = f"./{path}/{curr_date}/cos_{curr_hour}-{str(curr_hour+1)}.json"
        curr_comp = file_open(pathname)
        both_cov_cos.append(curr_comp["covered_both_percent"])
        cov_A_cos.append(curr_comp["covered_A_percent"])
        cov_B_cos.append(curr_comp["covered_B_percent"])

        pathname = pathname.replace("cos_", "")
        curr_comp = file_open(pathname)
        both_cov_standard.append(curr_comp["covered_both_percent"])
        cov_A_st.append(curr_comp["covered_A_percent"])
        cov_B_st.append(curr_comp["covered_B_percent"])

        sent_sub = get_sent_sub_avg(curr_comp)
        sent_A.append(sent_sub["sent_A"])
        sub_A.append(sent_sub["sub_A"])
        sent_B.append(sent_sub["sent_B"])
        sub_B.append(sent_sub["sub_B"])

        hours.append(curr_hour)
        curr_hour+=1
        
    print(hours)
    avg_A_st = sum(cov_A_st) / len(cov_A_st)
    avg_A_cos = sum(cov_A_cos) / len(cov_A_cos)

    avg_B_st = sum(cov_B_st) / len(cov_B_st)
    avg_B_cos = sum(cov_B_cos) / len(cov_B_cos)

    avg_both_st = sum(both_cov_standard) / len(both_cov_standard)
    avg_both_cos = sum(both_cov_cos) / len(both_cov_cos)
    
    df = pd.DataFrame(np.array([both_cov_standard, both_cov_cos]).transpose(), index=range(0, 24), columns= ["standard", "cosine"])

    df2 = pd.DataFrame(np.array([cov_A_st, cov_A_cos, cov_B_st, cov_B_cos]).transpose(), index=range(0, 24), columns= [f"{newsp_A} standard", f"{newsp_A} cosine", f"{newsp_B} standard", f"{newsp_B} cosine"])

    df3 = pd.DataFrame(np.array([sent_A, sent_B]).transpose(), index=range(0, 24), columns= [f"{newsp_A}", f"{newsp_B}"])
    df4 = pd.DataFrame(np.array([sub_A, sub_B]).transpose(), index=range(0, 24), columns= [f"{newsp_A} ", f"{newsp_B}"])

    df5 = pd.DataFrame({'standard': [avg_A_st, avg_B_st, avg_both_st], 'cosine': [avg_A_cos, avg_B_cos, avg_both_cos]}, index=[newsp_A, newsp_B, "Both"])

    plt.figure()

    df.plot(title=f"Comparison Graph")
    plt.xticks(df.index, hours)
    df2.plot(title=f"Coverage Graph")
    plt.xticks(df.index, hours)
    df3.plot(title=f"Average Sentiment Graph")
    plt.xticks(df.index, hours)
    df4.plot(title=f"Average Subjectivity Graph")
    plt.xticks(df.index, hours)

    df5.plot.pie(subplots=True, figsize=(11, 6), title=f"Average Coverage", autopct='%1.0f%%')


    plt.show()

def file_open(path):
    with open(path, "r") as f:
        try:
            curr_comp = json.load(f)
        except:
            raise Exception("Could not read file from the given directory: " + path + ".")
    return curr_comp

def get_sent_sub_avg(news):
    sentiment_A = []
    subject_A = []

    sentiment_B = []
    subject_B = []
    for new_A in dict(list(news.items())[9:]):
        for new_B in news[new_A]:
            if news[new_A][new_B]["are_similar"]:
                sentiment_A.append(news[new_A][new_B]["polarity_X"])
                subject_A.append(news[new_A][new_B]["subjectivity_X"])

                sentiment_B.append(news[new_A][new_B]["polarity_Y"])
                subject_B.append(news[new_A][new_B]["subjectivity_Y"])
    
    to_ret= {}
    if len(sentiment_A) > 0:
        to_ret["sent_A"] = sum(sentiment_A) / len(sentiment_A)
        to_ret["sub_A"] = sum(subject_A) / len(subject_A)
        to_ret["sent_B"] = sum(sentiment_B) / len(sentiment_B)
        to_ret["sub_B"] = sum(subject_B) / len(subject_B)
    else:
        to_ret["sent_A"] = 0
        to_ret["sub_A"] = 0
        to_ret["sent_B"] = 0
        to_ret["sub_B"] = 0

    return to_ret

            

if __name__ == "__main__":
    main()
