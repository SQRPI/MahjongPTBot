import requests
import json
import time, datetime
import os
import logging
from date2timestamp import date2timestamp
from pttime import ptms
from tenhou import ptth
from loguru import logger
from nickname2uid import nickname2uid

def ptsingle(name, start=None, end=None, mode='majsoul'):
    today = datetime.date.today()
    if start is None:
        start = today
    if end is None:
        end = today
    try:
        res = f'统计时间: {start:%Y%m%d}-{end:%Y%m%d}\n'
    except ValueError as e:
        logger.info(str(e))
        return f'时间格式错误, 正确格式为YYYYMMDD, 例: ptday 三色双龙会 20140514 20190810\n{e}'
    res = f'{name} {start:%Y%m%d}-{end:%Y%m%d} 战绩\n'
    start, end = f'{start:%Y%m%d}', f'{end + datetime.timedelta(days=1):%Y%m%d}'
    output = {4: [], 3: []}
    if mode == 'majsoul':
        uid, r = nickname2uid(name)
        if uid == -1: return r
        response = ptms(uid, start, end) 
    elif mode == 'tenhou':
        response = ptth(name, start, end)
    for i in [3, 4]:
        if not response[i]['success']: continue
        if sum(response[i]['results']) == 0: continue

        regular_results = '-'.join([f'{x}' for x in response[i]['results']])
        res += "麻" * i + '\n'
        res += f'{regular_results} {response[i]["score_change"]}'
    return res

if __name__  == '__main__':
    print(ptsingle('天才麻将杏杏'))