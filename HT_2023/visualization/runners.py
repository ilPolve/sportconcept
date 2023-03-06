import sys
sys.path.append("..")
from def4 import churn_rate
from typing import List
import datetime

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

def add_slice(date, slice):
    return date + datetime.timedelta(hours=slice)

# slice is in days
def churn_run(source: str, start_date: str, end_date: str, slice: str) -> List[float]:
    start_in_date = datetime.datetime.strptime(start_date, DATE_FORMAT)
    end_in_date = datetime.datetime.strptime(end_date, DATE_FORMAT)
    rates = []
    while add_slice(start_in_date, slice) < add_slice(end_in_date, slice):
        temp_end = add_slice(start_in_date, slice)
        rate, _ = churn_rate(source, start_date, temp_end.strftime(DATE_FORMAT))
        rates.append(rate)
        start_in_date = temp_end
        start_date = start_in_date.strftime(DATE_FORMAT)
    return rates