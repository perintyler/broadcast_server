"""broadcast_server.server"""

import _thread
import threading
import gevent
from werkzeug.routing import WebsocketMismatch

from .. import logs

__broadcasters__ = []

def add_broadcaster(broadcaster):
  __broadcasters__.append(broadcaster)
  def thread(*args): broadcaster.run_forever()
  _thread.start_new_thread(thread, ())
  gevent.sleep(0.1)
  broadcaster.start()

def remove_broadcaster(broadcaster):
  if broadcaster.is_broadcasting(): 
    broadcaster.close()
  __broadcasters__.remove(broadcaster)

def has_broadcaster(): 
  return len(__broadcasters__) != 0

def num_clients():
  return 0 if not __broadcasters__ else __broadcasters__[0].num_clients()

def start_broadcasting():
  for broadcaster in __broadcasters__:
    broadcaster.start()

def stop_broadcasting():
  """called when all connections are closed"""
  for broadcaster in __broadcasters__:
    broadcaster.stop()

def connect_client(websocket):
  while not websocket.closed and websocket.origin is not None:
    try: 
      message = websocket.receive()
    except WebsocketMismatch: 
      logs.application_event('caught WebsocketMismatch error', websocket=str(websocket))
      break

    logs.application_event('recieved client message', message=message, client=websocket.origin)

    if message == 'subscribe':
      for broadcaster in __broadcasters__:
        broadcaster.add_client(websocket)
    elif message == 'unsubscribe':
      for broadcaster in __broadcasters__:
        broadcaster.remove_client(websocket)
        break;

     # Sleep to prevent constant context-switches. This does
     # not affect update speed, which happens on another thread
    gevent.sleep(0.1)

  logs.application_event('closed client', websocket=str(websocket))

  for broadcaster in __broadcasters__:
    broadcaster.remove_client(websocket)

if __name__ == "__main__":
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler
    server = pywsgi.WSGIServer(('', 5000), app, handler_class=WebSocketHandler)
    server.serve_forever()

