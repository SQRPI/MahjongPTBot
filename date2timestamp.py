import time, datetime

def date2timestamp(date, millisecond=True):
    str_time = f'{date} 00:00:00'
    return int(time.mktime(time.strptime(str_time, "%Y%m%d %H:%M:%S"))*(1000 if millisecond else 1))