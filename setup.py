#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:copyright: (c) 2017 by Lev Lazinskiy
:license: MIT, see LICENSE for more details.
"""
import os
import sys

from setuptools import setup
from setuptools.command.install import install

# circleci.py version
VERSION = "2.0.0"


def readme():
    """print long description"""
    with open('README.md', encoding="utf-8") as f:
        return f.read()


class VerifyVersionCommand(install):
    """Custom command to verify that the git tag matches our version"""
    description = 'verify that the git tag matches our version'

    def run(self):
        tag = os.getenv('CIRCLE_TAG')

        if tag != VERSION:
            info = "Git tag: {0} does not match the version of this app: {1}".format(
                tag, VERSION
            )
            sys.exit(info)


setup(
    name="SQLAlchemy_wrap",
    version=VERSION,
    description="Python wrapper for the CircleCI API",
    long_description=readme(),
    author="jefung",
    author_email="865424525@qq.com",
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Build Tools",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3 :: Only",
    ],
    keywords='circleci ci cd api sdk',
    packages=[],
    install_requires=[
        'requests==2.18.4',
    ],
    python_requires='>=3',
    cmdclass={
        'verify': VerifyVersionCommand,
    }
)
