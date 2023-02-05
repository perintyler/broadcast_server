"""crypto_recommendations.server"""

import _thread
import threading
import gevent

from .. import logs

all_broadcasters = []

def add_broadcaster(broadcaster): all_broadcasters.append(broadcaster)
def remove_broadcaster(broadcaster): all_broadcasters.remove(broadcaster)

def listen_to(websocket):
  for broadcaster in all_broadcasters:
    broadcaster.listen_to(websocket)

  broadcast.server.start_broadcasting()

  while not websocket.closed:
    message = websocket.receive()
    logs.client_event('recieved message', websocket.origin, message=message)
     # Sleep to prevent constant context-switches. This does
     # not affect update speed, which happens on another thread
    gevent.sleep(0.1)

  logs.client_event('client disconnected', websocket.origin)
  for broadcaster in all_broadcasters:
    broadcaster.remove_client(ws)

  if num_clients() == 0:
    broadcast.server.stop_broadcasting()

def num_clients():
  return 0 if not all_broadcasters else all_broadcasters[0].num_clients()

def start_broadcasting():
  """called when the first connection is made"""
  # logs.application_event('start listening')
  for websocket in all_broadcasters:
    if not websocket.is_idle(): continue
    def thread(*args): websocket.run_forever()
    _thread.start_new_thread(thread, ())
    gevent.sleep(0.1)

def stop_broadcasting():
  """called when all connections are closed"""
  # logs.application_event('stop listening')
  for websocket in all_broadcasters:
    if websocket.is_idle(): continue
    logs.client_event('closing connection', websocket.origin)
    websocket.close()
    # else:
    #   logs.warn('tried closing an already closed client', origin=websocket.origin)

  logs.application_event(f'{threading.active_count()} threads after stopping broadcast')
  for thread in threading.enumerate(): 
    logs.application_event(f'{thread} is still open')
