from setuptools import setup, find_packages
import os

VERSION = "0.0.1"

DESCRIPTION = "EmailReport is a package"

LICENSE = "BSD"

DESCRIPTION = "a"

LONG_DESCRIPTION = "i"

setup(name='emailreport',
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
