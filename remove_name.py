
import requests
import json
import time
import datetime
import pytz
from loguru import logger
from date2timestamp import date2timestamp
from read_name import read_name_ms, read_name_th
from nickname2uid import nickname2uid
from tenhou import ptth

def del_name_ms(group, name):
    uids, nicknames = read_name_ms(group)
    if name not in nicknames:
        return f'{name}不在关注列表中'
    with open(f'data/groups/{group}/uids_ms', 'w', encoding='utf-8') as out:
        for uid, nickname in zip(uids, nicknames):
            if name == nickname:
                continue
            out.write(f'{uid}\t{nickname}\n')
    return f'删除成功{nickname}'

def del_name_th(group, name):
    nicknames = read_name_th(group)
    if name not in nicknames:
        return f'{name}不在关注列表中'
    with open(f'data/groups/{group}/names_th', 'w', encoding='utf-8') as out:
        for nickname in nicknames:
            if name == nickname:
                continue
            out.write(f'{nickname}\n')
    return f'删除成功{nickname}'

if __name__ == '__main__':
    print(del_name_th(1, '天才麻将杏杏'))