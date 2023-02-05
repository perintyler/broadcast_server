from setuptools import setup
from pathlib import Path

PACKAGE_NAME = 'broadcast_server'

setup(
  name=PACKAGE_NAME,
  package_dir={PACKAGE_NAME: './src'}, # source files are in the repos's root directory
)