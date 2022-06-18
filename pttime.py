
import requests
import json
import time
import datetime
import pytz
from loguru import logger
from date2timestamp import date2timestamp
from collections import defaultdict


TIMEOUT = 10
mspt_site = {4: 'https://ak-data-3.sapk.ch/api/v2/pl4/player_stats',
             3: 'https://ak-data-1.sapk.ch/api/v2/pl3/player_stats'}
default_start_time = 1262304000000

max_score = {
    301: 1200,
    302: 1400,
    303: 2000,
    401: 2800,
    402: 3200,
    403: 3600,
    501: 4000,
    502: 6000,
    503: 9000
}

def int2str(i):
    match i:
        case 1:
            return '一'
        case 2:
            return '二'
        case 3:
            return '三'

def level2name(level):
    match level:
        case level if 101 <= level <= 103:
            return f'初{int2str(level%10)}'
        case level if 201 <= level <= 203:
            return f'士{int2str(level%10)}'
        case level if 301 <= level <= 303:
            return f'杰{int2str(level%10)}'
        case level if 401 <= level <= 403:
            return f'豪{int2str(level%10)}'
        case level if 501 <= level <= 503:
            return f'圣{int2str(level%10)}'
        case level if 700 < level <= 800:
            return f'魂天{level%100}'
        case _:
            return '未知'

def convert_score(score, level):
    if level in max_score and score >= max_score[level]:
        level += 1
        if level % 10 > 3:
            level += 97
        return level2name(level), max_score[level] // 2 if level != 10701 else 10.0
    if score < 0:
        level -= 1
        if level % 10 == 0:
            level -= 97
        return level2name(level), max_score[level] // 2
    return level2name(level), score

def ptms(uid, starttime, endtime, mode={3: '26.24.22.25.23.21', 4: '16.12.9.11.8'}):
    starttime, endtime = date2timestamp(starttime), date2timestamp(endtime)
    # sc, res, rk = dict(), dict(), dict()
    res = defaultdict(dict)
    res['platform'] = 'majsoul'
    for i in [3, 4]:
        url = f'{mspt_site[i]}/{uid}/{starttime}/{endtime}?mode={mode[i]}'
        try:
            r = json.loads(requests.get(url, timeout=TIMEOUT).text)
        except requests.exceptions.ReadTimeout:
            logger.info(f'{uid} 雀魂超时')
            res[i]['success'] = False
            continue

        if r == {'error': 'id_not_found'}:
            logger.info(f'{uid} Not Found')
            res[i]['success'] = False
            continue

        cur_level, cur_score = convert_score(r['level']['score'] + r['level']['delta'], r['level']['id'] % 1000)

        count = r['count']
        results = [round(x*count) for x in r['rank_rates']]

        url = f'{mspt_site[i]}/{uid}/{default_start_time}/{starttime}?mode={mode[i]}'

        try:
            r = json.loads(requests.get(url, timeout=TIMEOUT).text)
        except requests.exceptions.ReadTimeout:
            logger.info(f'{uid} 雀魂超时')
            res[i]['success'] = False
            continue        
        if r == {'error': 'id_not_found'}:
            res[i]['success'] = False
            continue
        last_level, last_score = convert_score(r['level']['score'] + r['level']['delta'], r['level']['id'] % 1000)


        if cur_level == last_level:
            score_change = f'({cur_score - last_score:+4d}) {cur_level} {last_score:4d} -> {cur_score:4d}'
        else:
            score_change = f'{last_level} {last_score:4d} -> {cur_level} {cur_score:4d}'
        res[i]['success'] = True
        res[i]['last_level'] = last_level
        res[i]['score_change'] = score_change
        res[i]['results'] = results
        res[i]['cur_level'] = cur_level
        res[i]['last_score'] = last_score
        res[i]['cur_score'] = cur_score
        # sc[i], res[i], rk[i] = score_change, results, cur_score - last_score
    return res

if __name__ == '__main__':
    print(ptms(8594042, 20220529, 20220530))