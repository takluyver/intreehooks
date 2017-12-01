# Deliberately not using flit packaging, because I want to use this for building
# flit, without a dependency loop.
from setuptools import setup

with open("README.rst", "r") as f:
    readme = f.read()

setup(name='intreehooks',
      version='1.0',
      description='Load a PEP 517 backend from inside the source tree',
      long_description = readme,
      author='Thomas Kluyver',
      author_email='thomas@kluyver.me.uk',
      url='https://github.com/takluyver/intreehooks',
      py_modules=['intreehooks'],
      classifiers=[
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Topic :: Software Development :: Libraries :: Python Modules',
      ],
      install_requires=['pytoml'],
)
