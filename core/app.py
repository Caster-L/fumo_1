from sdk.recv_message import recv_message
from sdk.message import convert_message
import sdk.api as api
from sdk.send_message import send_group_message
from core.plugin import Plugin
from typing import List
import asyncio
from queue import Queue
from threading import Thread

VERIFY_KEY = "1234567890"
QQ = 3793571711

class App:

    plugin: List[Plugin]
    session: str
    message_queue: Queue

    def __init__(self):
        verification = api.post('/verify', {
            "verifyKey": VERIFY_KEY
        })
        self.session = verification["session"]

        api.post('/bind', {
            "sessionKey": self.session,
            "qq": QQ
        })

        self.plugin = []
        self.message_queue = Queue()


    def register_plugin(self, plugin):
        self.plugin.append(plugin)
        plugin.session = self.session # will be modifyed later.

    # async def task(self, result):
    #     msg = await recv_message(self.session)

    #     result.clear()

    #     print("got msg:", msg) # log system......
    #     msg_type, args = convert_message(msg)
    #     print("========", msg_type, args)
    #     for plugin in self.plugin:
    #         for task in plugin.handle(msg_type, **args):
    #             print('get task', task)
    #             result.append(task)

    async def fetch_message(self):
        print("Thread started.")
        while True:
            msg = await recv_message(self.session)
            msg_type, args = convert_message(msg)
            for plugin in self.plugin:
                for task in plugin.handle(msg_type, **args):
                    # print('get task', task)
                    self.message_queue.put(task)

    def handle_task(self, task):
        new_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(new_loop)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(task)
        loop.close()

    def run(self):
        Thread(target=lambda: asyncio.run(self.fetch_message()), name="fetch_message_loop").start()

        while True:
            # task = []
            # while not self.message_queue.empty():
            #     task.append(self.message_queue.get())
            # if task != []:
            #     print("task =", task)
            #     Thread(target=lambda: self.handle_task(task), name="handle_task").start()
            if not self.message_queue.empty():
                Thread(target=lambda: self.handle_task(self.message_queue.get()), name="handle_task").start()

    # async def run(self):
    #     while True:
    #         task = []
            
    #         msg = await recv_message(self.session)
    #         print("got msg:", msg) # log system......
    #         msg_type, args = convert_message(msg)
    #         print("========", msg_type, args)
            
    #         for plugin in self.plugin:
    #             task = [*task, *plugin.handle(msg_type, **args)]
    #         # print(task)
    #         await asyncio.gather(*task)
    #         await asyncio.sleep(0.05)