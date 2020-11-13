"""
Setup file for reporty library
"""

from setuptools import setup

DISTNAME = 'reporty'

VERSION = '0.1.9'

DESCRIPTION = 'Reporty is a python library that contains useful functions for organizing and distributing visual data'

LONG_DESCRIPTION = """
**Reporty** is a python library that contains useful 
functions for organizing and distributing visual data

All features available using gmail

Limited features available using outlook

Support for other mail providers coming soon

Templates:
* Basic
* Green
* Red Stripes
* Red

More templates **coming soon**

Report any bugs or email us with questions: reportylib@gmail.com
"""

LICENSE = 'BSD'

AUTHOR = 'Andrew Boyer & Ben Tengelsen'

EMAIL = 'reportylib@gmail.com'

URL = 'https://github.com/asboyer2/reporty'

KEYWORDS = ['report', 'email', 'plot', 'graph', 'embed']

REQUIREMENTS = ['pyaml']

PYTHON = ">=3.5"

setup(name=DISTNAME,
      packages=['reporty'],
      package_dir={'reporty': 'module/reporty'},
      package_data={'reporty': ['templates/*.yaml']},
      version=VERSION,
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      long_description_content_type='text/markdown',
      license=LICENSE,
      author=AUTHOR,
      author_email=EMAIL,
      url=URL,
      keywords=KEYWORDS,
      install_requires=REQUIREMENTS,
      python_requires=PYTHON,
      include_package_data=True
      )
