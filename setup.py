"""broadcast_server.setup"""

from setuptools import setup

PACKAGE_NAME = 'broadcast_server'

with open('./requirements.txt') as f:
  requirements = f.read().splitlines()

setup(
  name=PACKAGE_NAME,
  package_dir={PACKAGE_NAME: '.'}, # source files in root folder of repo
  install_requires=requirements # requirements outlined in `requirements.txt`
)
