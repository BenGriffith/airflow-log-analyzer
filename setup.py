# -*- coding: utf-8 -*-
from setuptools import setup

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='Apache Airflow Mini-Project 1',
    version='0.1.0',
    description='Created a data pipeline to extract online stock market data and deliver analytical results',
    long_description=readme,
    author='Ben Griffith',
    author_email='bengriffith@outlook.com',
    url='https://github.com/bengriffith/airflow-stock-market',
    license=license
)

