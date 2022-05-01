#!/usr/bin/env python

import os

from newsComparer import full_comparer

BASE_URL = f"flow/"

TO_DO = ["IT/ANSA_ITA", "IT/AGI_ITA"]

DATES = ["2022-04-29", "2022-04-28"]

START_HOUR = 22

DONE = []

def main():
    for i in range(0, len(TO_DO)):
        for j in range(i+1, len(TO_DO)):
            if f"{BASE_URL}{TO_DO[i]} - {BASE_URL}{TO_DO[j]}" not in DONE:
                print(TO_DO[i] + " " + TO_DO[j])
                np_comparer(TO_DO[i], TO_DO[j])
                #fullday_comparer(TO_DO[i], TO_DO[j])

def np_comparer(newsp_A, newsp_B):
    curr_date = DATES[0]
    for curr_hour in range(0, 24):
        full_comparer(f"{BASE_URL}{newsp_A}", f"{BASE_URL}{newsp_B}", curr_date, str(curr_hour), cosine=True)
        full_comparer(f"{BASE_URL}{newsp_A}", f"{BASE_URL}{newsp_B}", curr_date, str(curr_hour))
        if curr_hour == START_HOUR-1:
            curr_date = DATES[1]

def fullday_comparer(newsp_A, newsp_B):
    full_comparer(f"{BASE_URL}{newsp_A}", f"{BASE_URL}{newsp_B}", DATES[1], str(START_HOUR))
    full_comparer(f"{BASE_URL}{newsp_A}", f"{BASE_URL}{newsp_B}", DATES[1], str(START_HOUR), cosine=True)

if __name__ == "__main__":
    main()
