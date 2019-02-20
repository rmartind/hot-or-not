
from setuptools import setup, find_packages
from os import path


here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='hot-or-not',
    version='0.1',
    description='A Discord Hot or Not bot',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/rmartind/hot-or-not',
    author='rmartind',
    author_email='davis@protonmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Communications',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='discord hotornot bot',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    python_requires='!=2.7, >=3.0, !=3.6, !=3.7',
    install_requires=[
      'aiohttp==1.0.5',
      'asyncio==3.4.3',
      'uvloop==0.11.0',
      'discord.py==0.16.12',
      'websockets==3.4'
    ],
    project_urls={
        'Bug Reports': 'https://github.com/rmartind/hot-or-not/issues',
        'Source': 'https://github.com/rmartind/hot-or-not/',
    },
)