# coding=utf8

import os
import sys

import websocket

from dog import FileEventHandler
from event import StrackEvent
from watchdog.observers import Observer
from watchdog.events import *

WATCH_DIR = os.path.join(os.path.dirname(__file__), 'actions')
sys.path.append(WATCH_DIR)


class Main(object):
    def __init__(self, host):
        self.ws = StrackEvent(host)
        self.dog = Observer()
        self.event_handler = FileEventHandler(self.ws)
        self.dog.schedule(self.event_handler, WATCH_DIR, True)

    def start(self):

        self.dog.start()
        self.ws.start()
        self.dog.join()


if __name__ == "__main__":
    websocket.enableTrace(True)
    if len(sys.argv) < 2:
        host = "wss://log.cgspread.com/wss?sign=da369a36c40e11caabcdfbd66ef63f79"
    else:
        host = sys.argv[1]
    ws = Main(host)
    ws.start()
