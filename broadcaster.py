"""crypto_recommendations.broadcast.broadcaster.py"""

from inflection import underscore
import websocket

from .message import Message

from .. import logs

def enable_trace(): websocket.enableTrace(True)
def disable_trace(): websocket.enableTrace(False)

class Broadcaster(websocket.WebSocketApp):
  """Listens to other websockets and broadcasts the data to its clients

  To create an event callback for event 'eventName', subclass `Broadcaster`
  and define an instance function named `on_event_name`.
  """

  def __init__(self, wss, **kwargs):
    self.clients = {}
    super().__init__(wss,
        on_message = self.on_message,
        on_error   = self.on_error,
        on_close   = self.on_close,
        **kwargs
    )

  def add_client(self, client):
    self.clients[client.origin] = client

  def remove_client(self, client):
    logs.application_event('removing client', client=client.origin)
    if client in self.clients:
      self.clients.pop(client.origin)

  def num_clients(self):
    return len(self.clients)

  def is_broadcasting(self):
    return self.sock is not None

  def broadcast(self, **data):
    """Sends data to server clients"""
    message = Message.create(**data).stringify()
    for client in self.clients.values():
      try:
        client.send(message)
      except Exception as error:
        if str(error) == 'Socket is dead':
          logs.application_event('removing client', client=client.__dict__)
          self.remove_client(client)

  def respond(self, **data):
    """Sends data back to the external websocket"""
    if not self.sock: return
    message = Message.create(**data)
    self.send(message.stringify())

  def message_filter(self, msg):
    """Returns true if a recieved message should be ignored. This function
    designed to be overriden""" 
    return False

  def on_message(self, msg):
    """Calls event handler if defined"""
    logs.application_event('recieved message', message=msg)
    msg = Message(msg)
    if not self.message_filter(msg):
      callbackName = f'on_{underscore(msg.event)}' # 'eventName' -> 'on_event_name'
      event_handler = getattr(self, callbackName, None)
      if callable(event_handler):
        event_handler(msg.contents)

  def start(self):
    pass

  def stop(self):
    pass

  def on_close(self, *args, **kwargs):
    pass

  def on_error(self, *args, **kwargs):
    pass

  def on_shutdown(self, *args, **kwargs):
    pass
  
