from setuptools import setup, find_packages
from datuma.version import __version__

setup(
    name='datuma',
    version=__version__,
    description='A Tool to migrate data between database instances with JSON configuration files.',
    entry_points={"console_scripts": ['datuma = datuma.cli:main']},
    author='André Freitas',
    author_email='andre.freitas@ndrive.com',
    url='https://github.com/ndrive/datuma',
    license='MIT',
    packages=find_packages('.'),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
    ],
    install_requires=[
        "rdbtools==0.1.10"
    ]
)
