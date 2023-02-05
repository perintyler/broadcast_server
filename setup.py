from setuptools import setup
from pathlib import Path

PACKAGE_NAME = 'broadcast_server'

requirements = '''bidict==0.22.1
cachetools==5.3.0
certifi==2022.12.7
charset-normalizer==3.0.1
click==7.1.2
Flask==1.1.4
Flask-SocketIO==4.3.1
Flask-Sockets==0.2.1
gevent==20.6.2
gevent-websocket==0.10.1
google-api-core==2.11.0
google-auth==2.16.0
google-cloud-appengine-logging==1.3.0
google-cloud-audit-log==0.2.5
google-cloud-core==2.3.2
google-cloud-logging==3.5.0
googleapis-common-protos==1.58.0
greenlet==0.4.16
grpc-google-iam-v1==0.12.6
grpcio==1.51.1
grpcio-status==1.51.1
gunicorn==20.0.4
idna==3.4
inflection==0.5.0
itsdangerous==1.1.0
Jinja2==2.11.3
MarkupSafe==2.0.1
proto-plus==1.22.2
protobuf==4.21.12
pyasn1==0.4.8
pyasn1-modules==0.2.8
python-engineio==4.3.4
python-socketio==5.7.2
requests==2.28.2
rsa==4.9
six==1.16.0
urllib3==1.26.14
websocket-client==0.57.0
Werkzeug==1.0.1
zope.event==4.6
zope.interface==5.5.2
'''.splitlines()

setup(
  name=PACKAGE_NAME,
  package_dir={PACKAGE_NAME: './src'}, # source files are in the repos's root directory
  install_requires=requirements # requirements outlined in `requirements.txt`
)