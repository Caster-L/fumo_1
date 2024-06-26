from sdk.send_message import send_group_message
from sdk.message import text_message
from plugins.guess_npc.saying import npc_saying
import random
from core.plugin import Plugin
from sdk.temp_data import alloc, fetch, dump
from sdk.user import user_group_nickname

npc_name = [key for (key, value) in npc_saying.items()]

async def handler(session: str, group_id: int, sender_id: int, message):
    key = f"guess_npc_{group_id}"

    data = fetch(key)
    assert data != None

    if message[0] == "结束游戏":
        await send_group_message(session, group_id, text_message(f"游戏结束，答案是：{data['npc']}"))
        dump(key)
        return
    
    if message[0] == data["npc"]:
        await send_group_message(session, group_id, text_message(f"猜对咯，答案是{data['npc']}！"))
        dump(key)
        return
    else:
        await send_group_message(session, group_id, text_message(f"猜错了，继续猜吧！"))
        return

def checker(group_id: int, sender_id: int, message):
    return message[0] == "结束游戏" or message[0] in npc_name

async def startup_handler(session: str, group_id: int, sender_id: int, message):
    key = f"guess_npc_{group_id}"

    if fetch(key) != None:
        await send_group_message(session, group_id, text_message("请先猜对当前npc，或输入“结束游戏”"))
        return
    
    npc = random.choice(npc_name)
    saying = random.choice(npc_saying[npc])
    saying.replace("__name__", user_group_nickname(session, group_id, sender_id))
    alloc(key, {
        "npc": npc,
        "saying": saying
    })
    await send_group_message(session, group_id, text_message(saying))


def startup_checker(group_id: int, sender_id: int, message):
    return message[1] == "猜npc"

guess_npc = Plugin('guess_npc')
guess_npc.register_callback('group.@fumoP', startup_handler, startup_checker)
guess_npc.register_callback('group.P', handler, checker)