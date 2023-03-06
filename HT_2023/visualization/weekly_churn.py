import matplotlib.pyplot as plt
import pandas as pd
import sys
sys.path.append("..")
from utils import date_to_epoch
from runners import churn_run
import datetime

source = "ANSA_Politica"
start_date = "2022-05-11 10:00:00"

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# this should be 7, but we only have 3 days now
duration = 5

HOURS_PER_SLICE = 12

def main():
    weekly_churn_visualizer(source, start_date)

def weekly_churn_visualizer(source: str, start_date: str) -> None:
    start_in_date = datetime.datetime.strptime(start_date, DATE_FORMAT)

    end_date = start_in_date + datetime.timedelta(hours=duration*HOURS_PER_SLICE)
    end_date = end_date.strftime(DATE_FORMAT)
    churn_rates = churn_run(source, start_date, end_date, HOURS_PER_SLICE)

    columns = [start_date]
    for i in range(1, duration):
        temp = start_in_date + datetime.timedelta(hours=i*HOURS_PER_SLICE)
        columns.append(temp.strftime(DATE_FORMAT))

    plt.title(f"{source} churn rate during time")
    plt.plot(columns, churn_rates)
    plt.show()
    return

if __name__ == "__main__":
    main()