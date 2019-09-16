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

from __future__ import print_function, division, absolute_import

import os
import pickle
import sys
import unittest

from sphinxcontrib.programoutput import ProgramOutputCache, Command

from . import AppMixin


class TestCache(AppMixin,
                unittest.TestCase):

    def assert_cache(self, cache, cmd, output, returncode=0):
        result = (returncode, output)
        self.assertFalse(cache)
        self.assertEqual(cache[cmd], result)
        self.assertEqual(cache, {cmd: result})

    def test_simple(self):
        cache = ProgramOutputCache()
        self.assert_cache(cache, Command([u'echo', u'blök']), u'blök')


    def test_shell(self):
        cache = ProgramOutputCache()
        self.assert_cache(cache, Command(u'echo blök', shell=True), u'blök')


    def test_working_directory(self):
        cache = ProgramOutputCache()
        cwd = os.path.join(self.tmpdir, 'wd')
        os.mkdir(cwd)
        cwd = os.path.realpath(os.path.normpath(str(cwd)))
        cmd = [sys.executable, '-c', 'import sys, os; sys.stdout.write(os.getcwd())']
        self.assert_cache(cache, Command(cmd, working_directory=cwd), cwd)


    def test_working_directory_shell(self):
        cache = ProgramOutputCache()
        cwd = os.path.join(self.tmpdir, 'wd')
        os.mkdir(cwd)
        cwd = os.path.realpath(os.path.normpath(str(cwd)))
        cmd = Command('echo $PWD', working_directory=cwd, shell=True)
        self.assert_cache(cache, cmd, cwd)


    def test_hidden_standard_error(self):
        cache = ProgramOutputCache()
        cmd = [sys.executable, '-c', 'import sys; sys.stderr.write("spam")']
        self.assert_cache(cache, Command(cmd, hide_standard_error=True), '')


    def test_nonzero_return_code(self):
        cache = ProgramOutputCache()
        cmd = [sys.executable, '-c', 'import sys; sys.exit(1)']
        self.assert_cache(cache, Command(cmd), '', returncode=1)


    def test_nonzero_return_code_shell(self):
        cache = ProgramOutputCache()
        cmd = sys.executable + " -c 'import sys; sys.exit(1)'"
        self.assert_cache(cache, Command(cmd, shell=True), '', returncode=1)

    def test_cache_pickled(self):
        doctreedir = self.doctreedir
        app = self.app
        cmd = Command(['echo', 'spam'])
        result = (0, 'spam')
        assert app.env.programoutput_cache[cmd] == result
        app.build()
        pickled_env_path = os.path.join(doctreedir, 'environment.pickle')
        with open(pickled_env_path, 'rb') as f:
            pickled_env = pickle.load(f)
        assert pickled_env.programoutput_cache == {cmd: result}

def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
