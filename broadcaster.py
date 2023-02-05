"""crypto_recommendations.broadcast.broadcaster.py"""

from inflection import underscore
import websocket

from .message import Message

def enable_trace(): websocket.enableTrace(True)
def disable_trace(): websocket.enableTrace(False)

class Broadcaster(websocket.WebSocketApp):
  """Listens to other websockets and repackages the data for its clients

  A Client Websocket App that connects to an external websocket
  server to forward messages through this server. To create an
  event callback for event 'eventName', define a function named
  on_event_name, and it will automatically be called.
  """

  def __init__(self, wss, **kwargs):
    self.clients = {}
    super().__init__(wss,
        on_message = self.on_message,
        on_error   = self.on_error,
        on_close   = lambda ws: print('closing', ws),
        **kwargs
    )

  def on_close(self, ws):
    print('closing', ws)

  def connect(self, client):
    self.clients[client.origin] = client

  def remove_client(self, client):
    self.clients.pop(client.origin)

  def num_clients(self):
    return len(self.clients)

  def broadcast(self, **data):
    """Sends data to server clients"""
    message = Message.create(**data).stringify()
    for client in self.clients.values():
      client.send(message)

  def respond(self, **data):
    """Sends data back to the external websocket"""
    message = Message.create(**data)
    self.send(message.stringify())

  def message_filter(self, msg):
    """Returns true if a recieved message should be ignored. This function
    designed to be overriden""" 
    return False

  def on_message(self, msg):
    """Calls event handler if defined"""
    msg = Message(msg)
    if not self.message_filter(msg):
      callbackName = f'on_{underscore(msg.event)}' # 'eventName' -> 'on_event_name'
      event_handler = getattr(self, callbackName, None)
      if callable(event_handler):
        event_handler(msg.contents)

  def on_error(self, *args, **kwargs):
    """TODO"""
    print('handle_error', args, kwargs)

  def on_shutdown(self, *args, **kwargs):
    """TODO"""
    print('handle_shutdown', args, kwargs)
  
  def is_idle(self):
    return not self.sock

