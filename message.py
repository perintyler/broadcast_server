"""crypto_recommendations.broadcast.message.py"""

import json

class Message:

  def __init__(self, jsonStr):
    self.contents = json.loads(jsonStr)

  @property
  def event(self):
    if isinstance(self.contents, list):
      return 'data_message'
    else:
      return self.contents.get('event', 'data_message')

  def is_list(self):
    return isinstance(self.contents, list)

  def stringify(self):
    return json.dumps(self.contents)

  def __add__(self, other_contents: dict):
    return Message.create({**self.contents, **other_contents})

  def __getitem__(self, key):
    return self.contents[key]

  def __str__(self):
    return str(self.contents)

  def __repr__(self):
    return f'<Message event="{self.event}" contents={self.contents}>'

  @classmethod
  def create(cls, **props):
    msg = json.dumps({**props})
    return cls(msg)
