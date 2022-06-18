import requests
import json
import os, sys
import time
import datetime
import pytz
from loguru import logger
from date2timestamp import date2timestamp

def read_name_ms(group):
    uids, nicknames = [], []
    if not os.path.exists(f'data/groups/{group}'):
        os.mkdir(f'data/groups/{group}')

    if not os.path.exists(f'data/groups/{group}/uids_ms'):
        return []

    with open(f'data/groups/{group}/uids_ms', 'r', encoding='utf-8') as f:
        for line in f:
            uid, nickname = line.strip().split('\t')
            uids.append(uid)
            nicknames.append(nickname)
    return uids, nicknames


def read_name_th(group):
    uids, nicknames = [], []
    if not os.path.exists(f'data/groups/{group}'):
        os.mkdir(f'data/groups/{group}')

    if not os.path.exists(f'data/groups/{group}/names_th'):
        return []

    with open(f'data/groups/{group}/names_th', 'r', encoding='utf-8') as f:
        for line in f:
            nickname = line.strip()
            nicknames.append(nickname)
    return nicknames

def ptls(group):
    ms = read_name_ms(group)
    th = read_name_th(group)
    res = '雀魂:\n'
    for u, n in zip(*ms):
        res += f'{n}[{u}]\n'
    res += '天凤:\n'
    for n in th:
        res += f'{n}\n'
    return res


if __name__ == '__main__':
    # print(read_name_ms(452173056))
    # print(read_name_th(452173056))
    print(ptls(452173056))