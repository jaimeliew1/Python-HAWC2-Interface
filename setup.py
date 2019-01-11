# https://python-packaging.readthedocs.io
from setuptools import setup

setup(name                 = 'python-HAWC2 Interface',
      version              = '0.1',
      description          = 'Runs custom python functions in HAWC2 in realtime.',
      url                  = 'https://github.com/jaimeliew1/Python-HAWC2-Interface.git',
      author               = 'Jaime Liew',
      author_email         = 'jaimeliew1@gmail.com',
      license              = 'MIT',
      packages             = ['HAWC2_TCP'],
      install_requires     = ['numpy', 'click'],
      zip_safe             = False,
      include_package_date = True,
)
