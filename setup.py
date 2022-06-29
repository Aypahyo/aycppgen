from importlib.metadata import entry_points
from setuptools import find_packages
from setuptools import setup

setup(
   name='aycppgen',
   version='1.0.0',
   description='aycppgen generates my cpp projects',
   author='Aypahyo',
   author_email='Aypahyo@github.com',
   url='https://github.com/Aypahyo/ayTempler',
   packages=['aycppgen_core'],
   py_modules=['aycppgen'],
   entry_points={
    'console_scripts' : [
      'aycppgen = aycppgen:main'
    ],
   }
)
