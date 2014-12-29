from setuptools import setup, find_packages
import os

def read(file_name):
    with open(os.path.join(os.path.dirname(__file__), file_name), 'r') as f:
        return f.read()

setup(
    name="olin-biofilm-study",
    version="0.1",
    packages=find_packages(),
    setup_requires=read('pip-required')
)
