from sdk.send_message import send_group_message
from sdk.message import text_message
from core.plugin import Plugin
from config import QQ
from typing import List
import random

async def handler(seesion: str,group_id: int,sender_id: int,message:List):
    list = message[1].split('还是')
    list.append('杂鱼～我才不回答你的问题呢')
    if ('打胶' in message[1]) or ('打搅' in message[1]) or ('月抛' in message[1]):
        await send_group_message(seesion, group_id, [text_message('戒了吧，对身体不好')])
    else:
        await send_group_message(seesion, group_id, [text_message(random.choice(list))])
def checker(group_id: int,sender_id: int,message: List):
    return message[0] == QQ and '还是' in message[1]

choosing_helper = Plugin('choosing_helper')
choosing_helper.register_callback('group.@P',handler,checker)
