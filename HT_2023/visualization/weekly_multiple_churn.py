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

sources = ["DE/Spiegel", "EN/BBC", "ES/ABC", "FR/France24", "IT/ilPost", "IT/ANSA_Esteri"]
start_date = "2023-03-16 12:00:00"

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

duration = 12

HOURS_PER_SLICE = 2

def main():
    weekly_churn_visualizer(sources, start_date)

def weekly_churn_visualizer(sources: List[str], start_date: str) -> None:
    start_in_date = datetime.datetime.strptime(start_date, DATE_FORMAT)

    end_date = start_in_date + datetime.timedelta(hours=duration*HOURS_PER_SLICE)
    end_date = end_date.strftime(DATE_FORMAT)
    all_churn_rates = []
    for source in sources:
        all_churn_rates.append(churn_run(source, start_date, end_date, HOURS_PER_SLICE))

    columns = [start_date[11:]]
    for i in range(1, duration):
        temp = start_in_date + datetime.timedelta(hours=i*HOURS_PER_SLICE)
        columns.append(temp.strftime(DATE_FORMAT)[11:])

    with open('weekly_churn_out.json', 'w') as fp:
        json.dump(all_churn_rates, fp, indent=4)
        fp.write("\n")

    width = 0.1
    i= 0
    ind = np.arange(len(all_churn_rates[0]))
    bars = []

    plt.title(f"Churn rate during time on {start_date[:11]}")
    for churn_rates in all_churn_rates:
        bars.append(plt.bar(ind+(width*i), churn_rates, width=width))
        i+=1
    
    plt.xlabel("Time")
    plt.ylabel("Average churn rate (1/news_lifespan)")
    plt.xticks(ind+width, columns)
    plt.legend(bars, sources)
    plt.show()
    return

if __name__ == "__main__":
    main()