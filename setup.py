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
from setuptools import setup, find_packages

def read_desc():
    with open('README.rst') as stream:
        readme = stream.read()
    with open('CHANGES.rst') as stream:
        changes = stream.read()

    return readme + '\n\n' + changes

def read_version_number():
    VERSION_PATTERN = re.compile(r"__version__ = '([^']+)'")
    with open(os.path.join('src', 'sphinxcontrib', 'programoutput', '__init__.py')) as stream:
        for line in stream:
            match = VERSION_PATTERN.search(line)
            if match:
                return match.group(1)

        raise ValueError('Could not extract version number')

tests_require = [
]

setup(
    name='sphinxcontrib-programoutput',
    version=read_version_number(),
    url='https://sphinxcontrib-programoutput.readthedocs.org/',
    license='BSD',
    author='Sebastian Wiesner',
    author_email='lunaryorn@gmail.com',
    maintainer="Jason Madden",
    maintainer_email='jason@nextthought.com',
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
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        'Topic :: Documentation',
        'Topic :: Utilities',
        'Framework :: Sphinx',
        'Framework :: Sphinx :: Extension',
    ],
    platforms='any',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['sphinxcontrib'],
    include_package_data=True,
    install_requires=[
        'Sphinx>=1.7.0',
    ],
    tests_require=tests_require,
    extras_require={
        'test': tests_require,
    },
    python_requires=">=2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*,!=3.4.*",
    test_suite='sphinxcontrib.programoutput.tests',
)
