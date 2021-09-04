# pip install websocket-client

import websocket
import json
import sys
import uuid
import loop_timer


def on_message(ws, message):
    print(json.loads(message))


def on_error(ws, error):
    print(error)


def on_close(ws):
    print("### closed ###")


def on_open(ws):
    uid = str(uuid.uuid4())
    bind_data = {'method': 'bind', 'data': {'uid': uid, "group": "eventlog"}}
    ws.send(json.dumps(bind_data))
    # t = loop_timer.LoopTimer(10, check_heartbeat, ws)
    # t.start()

def check_heartbeat(ws):
    ws.send(json.dumps({'method':  'heartbeat'}))

if __name__ == "__main__":
    websocket.enableTrace(True)
    if len(sys.argv) < 2:
        host = "ws://192.168.31.108:9083?sign=7dc70a53a6cc0fff5b02c47c070c471f"
    else:
        host = sys.argv[1]
    ws = websocket.WebSocketApp(host,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever(ping_interval=5, ping_timeout=3)

