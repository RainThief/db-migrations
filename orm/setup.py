#!/usr/bin/env python
"""package setup"""

from setuptools import setup, find_packages

setup(
    name='models',
    packages=find_packages(),
    version='0.0.1',
    description='Sqlalchemy models',
    license="Proprietary",
    install_requires=[
        'SQLAlchemy==1.3.19',
        'psycopg2==2.8.5'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OGL-UK-3.0",
        "Operating System :: OS Independent",
        "Topic :: Database",
    ],
)
