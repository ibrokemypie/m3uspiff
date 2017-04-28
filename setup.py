#!/usr/bin/env python
"""pypi package setup script"""
import os
import pandoc
from setuptools import setup

pandoc.core.PANDOC_PATH = '/usr/local/bin/pandoc'
DOC = pandoc.Document()
DOC.markdown = open('README.md').read()
NEWFILE = open('README.txt', 'w+')
NEWFILE.write(DOC.rst)
NEWFILE.close()

if os.path.exists('README.txt'):
    DESCRIPTION = open('README.txt').read()

setup(name='m3uspiff',
      version='1.0',
      description='An M3U to XSPF playlist converter.',
      long_description=DESCRIPTION,
      author='ibrokemypie',
      author_email='ibrokemypie@bastardi.net',
      url='https://github.com/ibrokemypie/m3uspiff',
      license='GNU General Public License v2.0',
      scripts=['m3uspiff.py'],
      install_requires=['setuptools'],
      entry_points={'console_scripts': ['m3uspiff=m3uspiff:main']}
      )

os.remove('README.txt')
