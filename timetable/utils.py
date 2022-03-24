import datetime

def get_duration_in_seconds(start_time, end_time):
    start_time = datetime.datetime.combine(
        datetime.date(2022, 3, 17), start_time)
    end_time = datetime.datetime.combine(
        datetime.date(2022, 3, 17), end_time)
    return (end_time - start_time).total_seconds()