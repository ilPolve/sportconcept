#!/usr/bin/env python

import os

from newsComparer import full_comparer

BASE_URL = f"flow/"

TO_DO = [[["IT/ANSA_Cronaca", "IT/ANSA_Politica"], ["IT/AGI_Cronaca", "IT/AGI_Politica"]],
         [["IT/ANSA_Esteri", "IT/ANSA_Politica"], ["IT/AGI_Politica", "IT/AGI_Esteri"]]]
    
PATHS = [["IT/ANSA_CrPo", "IT/AGI_CrPo"],
         ["IT/ANSA_EsPo", "IT/AGI_EsPo"]]

DATES = ["2022-05-11", "2022-05-12"]

START_HOUR = 16

DONE = []

def main():
    z= 0
    for couple in TO_DO:
        for i in range(0, len(couple)):
            for j in range(i+1, len(couple)):
                if f"{BASE_URL}{couple[i]} - {BASE_URL}{couple[j]}" not in DONE:
                    print(f"{couple[i]} - {couple[j]}")
                    #np_comparer(TO_DO[i], TO_DO[j])
                    fullday_comparer(couple[i], couple[j], PATHS[z][0], PATHS[z][1], 8)
    z+=1

def np_comparer(newsp_A, newsp_B):
    curr_date = DATES[0]
    for curr_hour in range(0, 24):
        full_comparer(f"{BASE_URL}{newsp_A}", f"{BASE_URL}{newsp_B}", curr_date, str(curr_hour), cosine=True)
        full_comparer(f"{BASE_URL}{newsp_A}", f"{BASE_URL}{newsp_B}", curr_date, str(curr_hour))
        if curr_hour == START_HOUR-1:
            curr_date = DATES[1]

def fullday_comparer(newsp_A, newsp_B, pa, pb, sl):
    full_comparer([f"{BASE_URL}{newsps_A}" for newsps_A in newsp_A], [f"{BASE_URL}{newsps_B}" for newsps_B in newsp_B], DATES[1], str(START_HOUR), cosine=True, PATH_A= pa, PATH_B=pb, curr_slice= sl)
    full_comparer([f"{BASE_URL}{newsps_A}" for newsps_A in newsp_A], [f"{BASE_URL}{newsps_B}" for newsps_B in newsp_B], DATES[1], str(START_HOUR), cosine=False, PATH_A= pa, PATH_B=pb, curr_slice= sl)

if __name__ == "__main__":
    main()
