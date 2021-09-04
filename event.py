# coding=utf8

import time
import datetime
import json
import uuid
import sys

import threading
import zmq

import os
import websocket
from log import get_logger
from load import mod_load
from dog import WATCH_DIR

sys.path.append(WATCH_DIR)


class StrackEvent(websocket.WebSocketApp):
    def __init__(self, host, interval=30):
        super(StrackEvent, self).__init__(host, on_message=self.on_message, on_open=self.on_open, on_close=self.on_close)
        self.ping_interval = interval
        self.logger = get_logger()
        self.action_list = {}
        self.mod_list = {}

        self.zmq_context = zmq.Context().socket(zmq.PUSH)
        self.zmq_context.bind("tcp://127.0.0.1:5000")

        self.zmq_threading = threading.Thread(target=self.start_zmq)
        self.zmq_threading.start()

    def add_action(self, name):
        if not name.startswith("__") and name.endswith(".py"):
            name = os.path.basename(name)
            mod, func = mod_load(name)
            self.action_list[name] = func
            self.mod_list[name] = mod

    def reload_action(self, name):
        if not name.startswith("__") and name.endswith(".py"):
            name = os.path.basename(name)
            print(self.mod_list.keys())
            reload(self.mod_list[name])

    def rm_action(self, name):
        if not name.startswith("__") and name.endswith(".py"):
            name = os.path.basename(name)
            try:
                del self.action_list[name]
                del self.mod_list[name]
            except:
                pass

    def load_action(self):
        for f in os.listdir(WATCH_DIR):
            if not f.startswith("__") and f.endswith(".py"):
                mod, func = mod_load(f)
                self.action_list[f] = func
                self.mod_list[f] = mod

    def on_message(self, message):
        # json_msg = json.loads(message)
        # print("22222222222222222")
        # print(json_msg)
        # print(self.action_list)
        # if json_msg['type'] == "built_in":
        self.zmq_context.send(message)
            # map(lambda f: f(json_msg), self.action_list.values())

    def on_error(self, error):
        self.logger.error(str(error))

    def on_close(self):
        self.logger.info(datetime.datetime.now())
        self.logger.info("################################ ws closed ###############################")

    def on_open(self):
        uid = str(uuid.uuid4())

        bind_data = {'method': 'bind', 'data': {'uid': uid, "group": "eventlog"}}
        print(json.dumps(bind_data))
        self.send(json.dumps(bind_data))
        self.logger.info(datetime.datetime.now())
        self.logger.info("################################ ws opened ###############################")
        self.logger.info("###############uuid  %s ################" % uid)

    def start(self):
        self.load_action()
        self.run_forever(ping_interval=self.ping_interval, ping_timeout=10)

    def start_zmq(self):
        context = zmq.Context()
        socket = context.socket(zmq.PULL)
        socket.connect("tcp://127.0.0.1:5000")
        while True:
            message = socket.recv()
            json_msg = json.loads(message)
            map(lambda f: f(self.logger, json_msg), self.action_list.values())
            time.sleep(1)


if __name__ == "__main__":
    websocket.enableTrace(True)
    if len(sys.argv) < 2:
        host = "ws://192.168.31.108:9083?sign=7dc70a53a6cc0fff5b02c47c070c471f"
    else:
        host = sys.argv[1]
    ws = StrackEvent(host)
    ws.start()
