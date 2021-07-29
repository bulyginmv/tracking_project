from setuptools import setup

setup(
   name='tracking',
   version='1.0',
   description='A module for tracking motion',
   author='Team Carrots',
   author_email='foomail@foo.com',
   packages=['tracking'],  #same as name
   install_requires=['opencv-python','numpy'], #external packages as dependencies
)