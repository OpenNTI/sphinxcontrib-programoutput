# -*- coding: utf-8 -*-
# Copyright (c) 2011, 2012, Sebastian Wiesner <lunaryorn@gmail.com>
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:

# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import os
import re
from setuptools import setup
from setuptools import find_namespace_packages

def read_desc():
    with open('README.rst', encoding='utf-8') as stream:
        readme = stream.read()
    # CHANGES.rst includes sphinx-specific markup, so
    # it can't be in the long description without some processing
    # that we're not doing -- its invalid ReST

    return readme

def read_version_number():
    VERSION_PATTERN = re.compile(r"__version__ = '([^']+)'")
    with open(os.path.join('src', 'sphinxcontrib', 'programoutput', '__init__.py'),
              encoding='utf-8') as stream:
        for line in stream:
            match = VERSION_PATTERN.search(line)
            if match:
                return match.group(1)

        raise ValueError('Could not extract version number')

tests_require = [
    # Sphinx 8.1 stopped raising SphinxWarning when the ``logger.warning``
    # method is invoked. So we now have to test side effects.
    # That's OK, and the same side effect test works on older
    # versions as well.
]

setup(
    name='sphinxcontrib-programoutput',
    version=read_version_number(),
    url='https://sphinxcontrib-programoutput.readthedocs.org/',
    license='BSD',
    author='Sebastian Wiesner',
    author_email='lunaryorn@gmail.com',
    maintainer="Jason Madden",
    maintainer_email='jason@seecoresoftware.com',
    description='Sphinx extension to include program output',
    long_description=read_desc(),
    keywords="sphinx cli command output program example",
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        'Topic :: Documentation',
        'Topic :: Utilities',
        'Framework :: Sphinx',
        'Framework :: Sphinx :: Extension',
    ],
    platforms='any',
    packages=find_namespace_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    install_requires=[
        'Sphinx>=5.0.0',
    ],
    extras_require={
        'test': tests_require,
        'docs': [
            'furo',
        ],
    },
    python_requires=">=3.8",
)
