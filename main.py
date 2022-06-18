import asyncio

from graia.broadcast import Broadcast
from graia.ariadne.app import Ariadne
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import Plain
from graia.ariadne.model import Friend, MiraiSession, Group
from loguru import logger

import time, datetime
import calendar
from ptday import ptday
from read_name import ptls
from add_name import add_name_th, add_name_ms
from remove_name import del_name_th, del_name_ms
from help_msg import help_msg
from pt_single import ptsingle


loop = asyncio.new_event_loop()

broadcast = Broadcast(loop=loop)
app = Ariadne(
    broadcast=broadcast,
    connect_info=MiraiSession(
        host="http://localhost:8080",  # 填入 HTTP API 服务运行的地址
        verify_key="INITKEYhbxytn1Q",  # 填入 verifyKey
        account=2790639145,  # 你的机器人的 qq 号
    )
)

@broadcast.receiver("GroupMessage")
async def friend_message_listener(app: Ariadne, group: Group, message: MessageChain):
    match str(message).split(' '):
        case ['ptls']:
            await app.sendMessage(group, MessageChain.create([Plain(f"{ptls(group.id)}")]))
        case ['ptmsadd', x] | ['msadd', x]:
            await app.sendMessage(group, MessageChain.create([Plain(f"{add_name_ms(group.id, x)}")]))
        case ['ptthadd', x] | ['thadd', x]:
            await app.sendMessage(group, MessageChain.create([Plain(f"{add_name_th(group.id, x)}")]))
        case ['ptmsdel', x] | ['msdel', x]:
            await app.sendMessage(group, MessageChain.create([Plain(f"{del_name_ms(group.id, x)}")]))
        case ['ptthdel', x] | ['thdel', x]:
            await app.sendMessage(group, MessageChain.create([Plain(f"{del_name_th(group.id, x)}")]))
        case ['pthelp']:
            await app.sendMessage(group, MessageChain.create([Plain(help_msg)]))

        case ['ptday']:
            today = datetime.date.today() - datetime.timedelta(days=1)
            await app.sendMessage(group, MessageChain.create([Plain(ptday(group.id, today, today))]))        
        case ['ptday', x, y]:
            start = datetime.datetime.strptime(x, "%Y%m%d")
            end = datetime.datetime.strptime(y, "%Y%m%d")
            await app.sendMessage(group, MessageChain.create([Plain(ptday(group.id, start, end))]))

        case ['pttoday']:
            today = datetime.date.today()
            await app.sendMessage(group, MessageChain.create([Plain(ptday(group.id, today, today))]))

        case ['ptweek']:
            today = datetime.date.today() - datetime.timedelta(days=1)
            await app.sendMessage(group, MessageChain.create([Plain(ptday(group.id, today - datetime.timedelta(days=6), today))]))
        case ['ptmonth', x]:
            logger.info(f'ptmoth {x}')
            try:
                year, month = int(x[:4]), int(x[4:])
                s, e = calendar.monthrange(year, month)
                start = datetime.datetime.strptime(f'{x}01 00:00:00', "%Y%m%d %H:%M:%S")
                end = datetime.datetime.strptime(f'{x}{e} 00:00:00', "%Y%m%d %H:%M:%S")
                await app.sendMessage(group, MessageChain.create([Plain(ptday(group.id, start, end))]))
            except Exception as e:
                await app.sendMessage(group, MessageChain.create([Plain(f"{e}")]))

        case ['msday', name, x, y]:
            start = datetime.datetime.strptime(x, "%Y%m%d")
            end = datetime.datetime.strptime(y, "%Y%m%d")
            await app.sendMessage(group, MessageChain.create([Plain(ptsingle(name, start, end, 'majsoul'))]))
        case ['thday', name, x, y]:
            start = datetime.datetime.strptime(x, "%Y%m%d")
            end = datetime.datetime.strptime(y, "%Y%m%d")
            await app.sendMessage(group, MessageChain.create([Plain(ptsingle(name, start, end, 'tenhou'))]))

        case ['msday', name]:
            today = datetime.date.today() - datetime.timedelta(days=1)
            await app.sendMessage(group, MessageChain.create([Plain(ptsingle(name, today, today, 'majsoul'))]))
        case ['thday', name]:
            today = datetime.date.today() - datetime.timedelta(days=1)
            await app.sendMessage(group, MessageChain.create([Plain(ptsingle(name, today, today, 'tenhou'))]))

        case ['mstoday', name]:
            today = datetime.date.today()
            await app.sendMessage(group, MessageChain.create([Plain(ptsingle(name, today, today, 'majsoul'))]))
        case ['thtoday', name]:
            today = datetime.date.today()
            await app.sendMessage(group, MessageChain.create([Plain(ptsingle(name, today, today, 'tenhou'))]))

        case ['msmonth', name, x]:
            logger.info(f'ptmoth {x}')
            try:
                year, month = int(x[:4]), int(x[4:])
                s, e = calendar.monthrange(year, month)
                start = datetime.datetime.strptime(f'{x}01 00:00:00', "%Y%m%d %H:%M:%S")
                end = datetime.datetime.strptime(f'{x}{e} 00:00:00', "%Y%m%d %H:%M:%S")
                await app.sendMessage(group, MessageChain.create([Plain(ptsingle(name, start, end, 'majsoul'))]))
            except Exception as e:
                await app.sendMessage(group, MessageChain.create([Plain(f"{e}")]))
        case ['thmonth', name, x]:
            logger.info(f'ptmoth {x}')
            try:
                year, month = int(x[:4]), int(x[4:])
                s, e = calendar.monthrange(year, month)
                start = datetime.datetime.strptime(f'{x}01 00:00:00', "%Y%m%d %H:%M:%S")
                end = datetime.datetime.strptime(f'{x}{e} 00:00:00', "%Y%m%d %H:%M:%S")
                await app.sendMessage(group, MessageChain.create([Plain(ptsingle(name, start, end, 'tenhou'))]))
            except Exception as e:
                await app.sendMessage(group, MessageChain.create([Plain(f"{e}")]))

loop.run_until_complete(app.lifecycle())