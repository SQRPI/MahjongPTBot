import requests
import json
import time, datetime
import os
import logging
from date2timestamp import date2timestamp
from pttime import ptms
from tenhou import ptth
from loguru import logger
from levels import levels

def align(text, target_len=20):
    _str_len = len(text)
    for char in text:
        if u'\u4e00' <= char <= u'\u9fa5':
            _str_len += 1
    return text + ' '*(target_len-_str_len)


def ptdiff(prev, curr, mode='majsoul'):
    prev_rank, prev_score = prev
    curr_rank, curr_score = curr
    levelmap = levels[mode]
    if prev_rank not in levelmap or curr_rank not in levelmap:
        return -99999999
    if prev_rank == curr_rank:
        return curr_score - prev_score
    if levelmap[prev_rank] > levelmap[curr_rank]:   # 掉段
        # 掉分 = -prev_sc + (curr_sc - half_cur_max)
        res = -prev_score
        for l, s in levelmap.items():
            if levelmap[curr_rank] < s < levelmap[prev_rank]:
                res -= s // 2
        return res + curr_score - levelmap[curr_rank] // 2
    if levelmap[prev_rank] < levelmap[curr_rank]:   # 升段
        # 上分 = prev_max-prev_sc + (curr_sc - half_cur_max)
        res = levelmap[prev_rank]-prev_score
        for l, s in levelmap.items():
            if levelmap[prev_rank] < s < levelmap[curr_rank]:
                res += s // 2
        return res + curr_score - levelmap[curr_rank] // 2


def ptday(group, start=None, end=None):
    today = datetime.date.today() - datetime.timedelta(days=1)
    if start is None:
        start = today
    if end is None:
        end = today
    try:
        res = f'统计时间: {start:%Y%m%d}-{end:%Y%m%d}\n'
    except ValueError as e:
        logger.info(str(e))
        return f'时间格式错误, 正确格式为YYYYMMDD, 例: ptday 20140514 20190810\n{e}'
    start, end = f'{start:%Y%m%d}', f'{end + datetime.timedelta(days=1):%Y%m%d}'
    if not os.path.exists(f'data/groups/{group}'):
        return '群未注册, 请先使用ptadd添加关注id'

    if not os.path.exists(f'data/groups/{group}/uids_ms') and not os.path.exists(f'data/groups/{group}/names_th') :
        return '还没有关注任何id, 请先使用ptadd添加关注id'

    output = {4: [], 3: []}
    with open(f'data/groups/{group}/uids_ms', 'r', encoding='utf-8') as f:
        for line in f:
            uid, nickname = line.strip().split('\t')
            logger.info(f'读取雀魂[{uid}]{nickname}')
            response = ptms(uid, start, end)
            for i in [3, 4]:
                if not response[i]['success']: continue
                if sum(response[i]['results']) == 0: continue
                rank = ptdiff(
                    (response[i]['last_level'], response[i]['last_score']),
                    (response[i]['cur_level'], response[i]['cur_score']),
                    'majsoul')
                regular_results = '-'.join([f'{x}' for x in response[i]['results']])
                output[i].append((rank, f'{nickname} \n\t {regular_results} {response[i]["score_change"]}'))
    res += '\n雀魂四麻: \n'
    res += '\n'.join([x[1] for x in sorted(output[4], reverse=True)])
    
    if output[3]:
        res += '\n三麻: \n'
        res += '\n'.join([x[1] for x in sorted(output[3], reverse=True)])
    output = {4: [], 3: []}
    with open(f'data/groups/{group}/names_th', 'r', encoding='utf-8') as f:
        for line in f:
            nickname = line.strip()
            logger.info(f'读取天凤{nickname}')
            response = ptth(nickname, start, end)
            for i in [3, 4]:
                if not response[i]['success']: continue
                if sum(response[i]['results']) == 0: continue
                rank = ptdiff(
                    (response[i]['last_level'], response[i]['last_score']),
                    (response[i]['cur_level'], response[i]['cur_score']),
                    'tenhou')
                regular_results = '-'.join([f'{x}' for x in response[i]['results']])
                output[i].append((rank, f'{nickname} \n\t {regular_results} {response[i]["score_change"]}'))
    res += '\n天凤四麻: \n'
    res += '\n'.join([x[1] for x in sorted(output[4], reverse=True)])
    if output[3]:
        res += '\n三麻: \n'
        res += '\n'.join([x[1] for x in sorted(output[3], reverse=True)])
    return res
    
if __name__ == '__main__':
    print(ptday(1, datetime.date.today(), datetime.date.today()))
