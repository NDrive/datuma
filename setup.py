from setuptools import setup, find_packages
from migrator.version import __version__

setup(name='Migrator',
      version=__version__,
      description='Migrates databases instances data.',
      entry_points={"console_scripts": ['migrate = migrator.cli:main']},
      author='André Freitas',
      author_email='andre.freitas@ndrive.com',
      url='https://github.com/ndrive/migrator',
      license='MIT',
      packages=find_packages('.'))
