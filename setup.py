from setuptools import setup, find_packages
import os

DISTNAME = 'reporty'

VERSION = '0.1.0'

DESCRIPTION = 'Reporty is a python library that contains useful functions for organizing and distributing visual data'

LONG_DESCRIPTION = ""

LICENSE = 'BSD'

AUTHOR = 'Andrew Boyer and Ben Tengleson'

EMAIL = 'reportylib@gmail.com'

URL = 'https://github.com/asboyer2/email_report'

KEYWORDS = ['report', 'email', 'plot', 'graph', 'embed']

REQUIREMENTS = ['pyaml']

setup(name=DISTNAME,
      packages=['reporty'],
      package_dir={'reporty': 'module/reporty'},
      package_data={'reporty': ['templates/*.yaml']},
      version=VERSION,
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      license=LICENSE,
      author=AUTHOR,
      author_email=EMAIL,
      url= URL,
      project_urls=PROJECT_URLS,
      keywords=KEYWORDS,
      install_requires=REQUIREMENTS,
      include_package_data=True
      )
