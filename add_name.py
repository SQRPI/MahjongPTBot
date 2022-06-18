
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

def add_name_ms(group, name):
    uids, nicknames = read_name_ms(group)
    uid, _ = nickname2uid(name)
    if uid == -1:
        return '添加失败, 未找到用户'
    if name in nicknames:
        return '用户已存在'
    uids.append(uid)
    nicknames.append(name)
    with open(f'data/groups/{group}/uids_ms', 'w', encoding='utf-8') as out:
        for uid, nickname in zip(uids, nicknames):
            out.write(f'{uid}\t{nickname}\n')
    return f'添加成功{nickname}[{uid}]'

def add_name_th(group, name):
    nicknames = read_name_th(group)
    if (t := ptth(name, 20010101, 20991231)) == ({3: None, 4: None}, {3: None, 4: None}, {3: None, 4: None}):
        return '添加失败, 未找到用户'
    if name in nicknames:
        return '用户已存在'
    nicknames.append(name)
    with open(f'data/groups/{group}/names_th', 'w', encoding='utf-8') as out:
        for nickname in nicknames:
            out.write(f'{nickname}\n')
    return f'添加成功{nickname}'

if __name__ == '__main__':
    print(add_name_th(1, '天才麻将杏杏'))