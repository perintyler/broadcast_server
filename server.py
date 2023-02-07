"""broadcast_server.server"""

import _thread
import threading
import gevent

from .. import logs

__broadcasters__ = []

def add_broadcaster(broadcaster):
  __broadcasters__.append(broadcaster)

def remove_broadcaster(broadcaster):
  if not broadcaster.is_broadcasting(): broadcaster.close()
  __broadcasters__.remove(broadcaster)

def has_broadcaster(): 
  return len(__broadcasters__) != 0

def num_clients():
  return 0 if not __broadcasters__ else __broadcasters__[0].num_clients()

def start_broadcasting():
  """called when the first connection is made"""
  logs.application_event('start listening')
  for broadcaster in __broadcasters__:
    if not broadcaster.is_broadcasting(): continue
    def thread(*args): broadcaster.run_forever()
    _thread.start_new_thread(thread, ())
    gevent.sleep(0.1)

def stop_broadcasting():
  """called when all connections are closed"""
  logs.application_event('stop listening')
  for broadcaster in __broadcasters__:
    if broadcaster.is_broadcasting(): continue
    logs.client_event('closing connection', broadcaster.origin)
    broadcaster.close()

  logs.application_event(f'{threading.active_count()} threads after stopping broadcast')
  for thread in threading.enumerate(): 
    logs.application_event(f'{thread} is still open')

def connect_client(websocket):
  for broadcaster in __broadcasters__:
    broadcaster.add_client(websocket)
  
  start_broadcasting()

  while not websocket.closed:
    message = websocket.receive()
    logs.application_event('recieved msg', message=message)
     # Sleep to prevent constant context-switches. This does
     # not affect update speed, which happens on another thread
    gevent.sleep(0.1)

  for broadcaster in __broadcasters__:
    broadcaster.remove_client(ws)

  if num_clients() == 0:
    stop_broadcasting()

