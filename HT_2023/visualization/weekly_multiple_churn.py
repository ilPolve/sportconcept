import matplotlib.pyplot as plt
import pandas as pd
import sys
sys.path.append("..")
from utils import date_to_epoch
from runners import churn_run
from typing import List
import datetime

sources = ["ANSA_Politica", "ANSA_Esteri", "AGI_Politica", "AGI_Esteri"]
start_date = "2022-05-11 10:00:00"

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# this should be 7, but we only have 3 days now
duration = 4

HOURS_PER_SLICE = 12

def main():
    weekly_churn_visualizer(sources, start_date)

def weekly_churn_visualizer(sources: List[str], start_date: str) -> None:
    start_in_date = datetime.datetime.strptime(start_date, DATE_FORMAT)

    end_date = start_in_date + datetime.timedelta(hours=duration*HOURS_PER_SLICE)
    end_date = end_date.strftime(DATE_FORMAT)
    all_churn_rates = []
    for source in sources:
        all_churn_rates.append(churn_run(source, start_date, end_date, HOURS_PER_SLICE))

    columns = [start_date]
    for i in range(1, duration):
        temp = start_in_date + datetime.timedelta(hours=i*HOURS_PER_SLICE)
        columns.append(temp.strftime(DATE_FORMAT))

    plt.title(f"{sources} churn rate during time")
    for churn_rates in all_churn_rates:
        plt.plot(columns, churn_rates)
    plt.legend(sources)
    plt.show()
    return

if __name__ == "__main__":
    main()