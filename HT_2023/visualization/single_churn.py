import sys
sys.path.append("..")
import datetime
import json
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from utils import date_to_epoch
from runners import churn_run
from typing import List

source = "IT/ilPost"
start_dates = ["2023-03-16 00:00:00", "2023-03-17 00:00:00", "2023-03-18 00:00:00"]

sources = ["ES/ABC", "FR/France24", "DE/Spiegel", "IT/ANSA_Esteri", "IT_AGI_Esteri"]

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

duration = 12

HOURS_PER_SLICE = 2

def main():
    for source in sources:
        single_week_churn(source, start_dates)

def single_week_churn(source: str, start_dates: List[str]) -> None:
    start_in_dates = [datetime.datetime.strptime(start_date, DATE_FORMAT) for start_date in start_dates]
    real_dates = [start_date[:11] for start_date in start_dates]

    end_dates = [start_in_date + datetime.timedelta(hours=duration*HOURS_PER_SLICE) for start_in_date in start_in_dates]
    end_dates = [end_date.strftime(DATE_FORMAT) for end_date in end_dates]

    all_rates = []
    for i in range(len(start_in_dates)):
        all_rates.append(churn_run(source, start_dates[i], end_dates[i], HOURS_PER_SLICE))
    
    columns = [start_dates[0][11:]]
    for i in range(1, duration):
        temp = start_in_dates[0] + datetime.timedelta(hours=i*HOURS_PER_SLICE)
        columns.append(temp.strftime(DATE_FORMAT)[11:])


    width = 0.1
    i= 0
    ind = np.arange(len(all_rates[0]))
    bars = []

    plt.title(f"Churn rate of {source} in {len(all_rates)} different days")
    for churn_rates in all_rates:
        bars.append(plt.bar(ind+(width*i), churn_rates, width=width))
        i+=1

    plt.xlabel("Time")
    plt.ylabel("Average churn rate (1/news_lifespan)")
    plt.xticks(ind+width, columns)
    plt.legend(bars, real_dates)
    plt.show()

    i = 0
    avg_rate = []
    for i in range(len(all_rates[0])):
        avg_rate.append(0)
        for j in range(len(all_rates)):
            avg_rate[i] += all_rates[j][i]
        avg_rate[i] = avg_rate[i]/len(all_rates)
    
    plt.title(f"Average churn rate of {source} in {len(all_rates)} different days")
    plt.bar(ind, avg_rate)
    plt.xlabel("Time")
    plt.ylabel("Average churn rate (1/news_lifespan)")
    plt.xticks(ind, columns)
    plt.show()

    return

if __name__ == "__main__":
    main()