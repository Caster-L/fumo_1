import sdk.api as api
import time
import asyncio
from sdk.temp_data import dump

last_send = time.time()

async def time_block():
    global last_send
    while time.time() - last_send < 1:
        await asyncio.sleep(1)
    last_send = time.time()

async def send_group_message(session: str, group_id: int, *message_chain):
    dump(f'repeat_{group_id}')
    await time_block()
    api.post('/sendGroupMessage', {
        "sessionKey": session,
        "target": group_id,
        "messageChain": message_chain
    })

async def send_friend_message(session: str, user_id: int, *message_chain):
    await time_block()
    api.post('/sendFriendMessage', {
        "sessionKey": session,
        "target": user_id,
        "messageChain": message_chain
    })
