# coding=utf8

import os

from watchdog.observers import Observer
from watchdog.events import *
import time

WATCH_DIR = os.path.join(os.path.dirname(__file__), 'actions')


class FileEventHandler(FileSystemEventHandler):
    def __init__(self, strack_event):
        FileSystemEventHandler.__init__(self)
        self.st_event = strack_event

    def on_created(self, event):
        if not event.is_directory:
            print("file modified:{0}".format(event.src_path))
            path = os.path.normpath(event.src_path)
            self.st_event.add_action(path)

    def on_moved(self, event):
        if not event.is_directory:
            print("file moved from {0} to {1}".format(event.src_path, event.dest_path))
            path = os.path.normpath(event.dest_path)
            if WATCH_DIR in path:
                self.st_event.reload_action(path)
            else:
                self.st_event.rm_action(path)

    def on_deleted(self, event):
        if not event.is_directory:
            print("file deleted:{0}".format(event.src_path))
            path = os.path.normpath(event.src_path)
            self.st_event.rm_action(path)

    def on_modified(self, event):
        if not event.is_directory:
            print("file modified:{0}".format(event.src_path))
            path = os.path.normpath(event.src_path)
            self.st_event.reload_action(path)


if __name__ == "__main__":
    observer = Observer()
    event_handler = FileEventHandler()
    observer.schedule(event_handler, WATCH_DIR, True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
