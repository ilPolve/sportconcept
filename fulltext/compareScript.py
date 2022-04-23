#!/usr/bin/env python

import os

from newsComparer import full_comparer

BASE_URL = f"flow/"

TO_DO = ["EN/CNN", "FR/France24", "DE/Spiegel", "IT/ilPost", "IT/Televideo", "ES/ABC", "EN/BBC"]

DATES = ["2022-04-22", "2022-04-21"]

START_HOUR = 18

DONE = [f"{BASE_URL}EN/CNN - {BASE_URL}FR/France24", f"{BASE_URL}EN/CNN - {BASE_URL}DE/Spiegel", f"{BASE_URL}EN/CNN - {BASE_URL}IT/ilPost"]

def main():
    for i in range(0, len(TO_DO)):
        for j in range(i+1, len(TO_DO)):
            if f"{BASE_URL}{TO_DO[i]} - {BASE_URL}{TO_DO[j]}" not in DONE:
                print(TO_DO[i] + " " + TO_DO[j])
                np_comparer(TO_DO[i], TO_DO[j])

def np_comparer(newsp_A, newsp_B):
    curr_date = DATES[0]
    for curr_hour in range(0, 24):
        full_comparer(f"{BASE_URL}{newsp_A}", f"{BASE_URL}{newsp_B}", curr_date, str(curr_hour))
        full_comparer(f"{BASE_URL}{newsp_A}", f"{BASE_URL}{newsp_B}", curr_date, str(curr_hour), cosine=True)
        if curr_hour == START_HOUR-1:
            curr_date = DATES[1]

if __name__ == "__main__":
    main()