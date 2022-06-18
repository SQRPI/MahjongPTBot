import requests
import json

def nickname2uid(nickname):
    url_list = [f'https://ak-data-2.sapk.ch/api/v2/pl4/search_player/{nickname}?limit=20',
                f'https://ak-data-2.sapk.ch/api/v2/pl3/search_player/{nickname}?limit=20']

    for url in url_list:
        try:
            r = json.loads(requests.get(url, timeout=10).text)
            if r and r[0]['nickname'] == nickname:
                uid = r[0]['id']
                return uid, f'已添加{nickname}[{uid}]'
        except requests.exceptions.ReadTimeout:
            return -1, f'{nickname}雀魂牌谱屋超时'
    else:
        return -1, f'未找到{nickname}'

def transName():
    with open('nicknames.txt', 'r', encoding='utf-8') as inp, open('data/groups/452173056/uids', 'w', encoding='utf-8') as out:
        for line in inp:
            nickname = line.strip()
            uid, response = nickname2uid(nickname)
            if uid != -1:
                out.write(f'{uid}\t{nickname}\n')
            print(f'{response}')

if __name__ == '__main__':
    print(nickname2uid('放铳无役振听'))