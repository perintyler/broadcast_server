from setuptools import setup
from pathlib import Path

PACKAGE_NAME = 'broadcast_server'

requirements_file = Path(__file__).parent.joinpath('requirements.txt')

with open(requirements_file.resolve()) as f:
  requirements = f.read().splitlines()

setup(
  name=PACKAGE_NAME,
  package_dir={PACKAGE_NAME: './src'}, # source files are in the repos's root directory
  install_requires=requirements # requirements outlined in `requirements.txt`
)