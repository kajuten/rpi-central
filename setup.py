#!/usr/bin/python

from setuptools import setup, find_packages

setup(name='Rpi-Central',
      version='0.0.1',
      description='Python project for Raspberry Pi',
      author='Julian Kaltenhofer',
      author_email='julian.kaltenhofer@gmail.com',
      url='https://github.com/kajuten/rpi-central',
      license='MIT',
      packages=find_packages(),
      long_description=open('README.md').read(),
      install_requires: ['nose'],
     )

setup(**config)
