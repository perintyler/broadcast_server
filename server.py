"""crypto_recommendations.server"""

import _thread
import threading
import gevent

from .. import logs

__broadcasters__ = []

def add_broadcaster(broadcaster): __broadcasters__.append(broadcaster)
def remove_broadcaster(broadcaster): __broadcasters__.remove(broadcaster)

def listen_to(websocket):
  for broadcaster in __broadcasters__:
    broadcaster.listen_to(websocket)

  while not websocket.closed:
    message = websocket.receive()
    logs.client_event('recieved message', websocket.origin, message=message)
     # Sleep to prevent constant context-switches. This does
     # not affect update speed, which happens on another thread
    gevent.sleep(0.1)

  logs.client_event('client disconnected', websocket.origin)
  for broadcaster in __broadcasters__:
    broadcaster.remove_client(ws)

  if num_clients() == 0:
    for broadcaster in __broadcasters__:
      broadcaster.close()

def num_clients():
  return 0 if not __broadcasters__ else __broadcasters__[0].num_clients()

def start_broadcasting():
  """called when the first connection is made"""
  # logs.application_event('start listening')
  for websocket in __broadcasters__:
    if not websocket.is_idle(): continue
    def thread(*args): websocket.run_forever()
    _thread.start_new_thread(thread, ())
    gevent.sleep(0.1)

def stop_broadcasting():
  """called when all connections are closed"""
  # logs.application_event('stop listening')
  for websocket in __broadcasters__:
    if websocket.is_idle(): continue
    logs.client_event('closing connection', websocket.origin)
    websocket.close()
    # else:
    #   logs.warn('tried closing an already closed client', origin=websocket.origin)

  logs.application_event(f'{threading.active_count()} threads after stopping broadcast')
  for thread in threading.enumerate(): 
    logs.application_event(f'{thread} is still open')
