"""broadcast_server.tests"""

import json
import asyncio
import pytest
import pytest_asyncio

from . import server
from .broadcaster import Broadcaster
from .message import Message

import threading

class FakeClient:

  def __init__(self, name):
    self.origin = name
    self.messages = []
    self.closed = False

  def close(self):
    self.closed = True

  def receive(self):
    pass

  def send(self, msg):
    # print('fake client msg', msg)
    self.messages.append(msg)

  def has_message(self):
    return len(self.messages) > 0

  def get_message(self, index=0):
    return json.loads(self.messages[index])

broadcaster = Broadcaster(None)
clients = (
  client1,
  client2,
  client3
) = [ FakeClient(f'client{index}') for index in range(3) ]

def test_message():
  message1 = Message.create(event='some-event', prop1='prop1', prop2='prop2')
  assert message1.event == 'some-event'
  assert message1['prop1'] == 'prop1'
  assert message1.stringify() \
      == '{"event": "some-event", "prop1": "prop1", "prop2": "prop2"}'
  message2 = Message('[1, 2, 3]')
  assert message2.event == 'data_message'
  assert message2.stringify() == '[1, 2, 3]'

def test_add_broadcaster():
  server.add_broadcaster(broadcaster)
  assert server.has_broadcaster()

def test_remove_broadcaster():
  server.remove_broadcaster(broadcaster)
  assert not broadcaster.is_broadcasting()
  assert not server.has_broadcaster()

def test_broadcast():
  server.add_broadcaster(broadcaster)
  for client in clients: 
    broadcaster.add_client(client)
  test_msg = 'this is a test'
  broadcaster.broadcast(test_message=test_msg)
  for client in clients:
    assert client.has_message()
    recieved_msg = client.get_message()
    assert len(recieved_msg.keys()) == 1
    assert 'test_message' in recieved_msg
    assert recieved_msg['test_message'] == test_msg
