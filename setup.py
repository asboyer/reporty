from setuptools import setup, find_packages
import os

VERSION = "0.0.3"

DESCRIPTION = "Reporty is a package"

LICENSE = "BSD"

DESCRIPTION = "This python library contains functions that help with sending formatted data"

LONG_DESCRIPTION = "Coming soon"

setup(name='reporty',
      packages=find_packages(),
      version=VERSION,
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      license=LICENSE,
      #classifiers=CLASSIFIERS,
      author='Andrew S. Boyer and Ben Tengleson',
      author_email='asboyer@gmail.com',
      url='https://github.com/asboyer2/email_report',  # URL to the repo
      keywords=['report', 'email'],
      install_requires=[
          ],
      include_package_data=False
      )
