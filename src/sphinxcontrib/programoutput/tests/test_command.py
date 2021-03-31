# -*- coding: utf-8 -*-
# Copyright (c) 2011, Sebastian Wiesner <lunaryorn@gmail.com>
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

import sys
import unittest
import tempfile
import shutil
import os.path

from sphinxcontrib.programoutput import Command, program_output

class TestCommand(unittest.TestCase):

    def test_new_with_string_command(self):
        cmd = 'echo "spam with eggs"'
        parsed_cmd = ('echo', 'spam with eggs')
        self.assertEqual(Command(cmd).command, parsed_cmd)
        self.assertEqual(Command(cmd, shell=True).command, cmd)


    def test_new_with_list(self):
        cmd = Command(['echo', 'spam'])
        self.assertEqual(cmd.command, ('echo', 'spam'))


    def test_new_with_list_hashable(self):
        # Test that Command objects are hashable even when passed a non-hashable
        # list.  Important for caching!
        hash(Command(['echo', 'spam']))


    def test_from_programoutput_node(self):
        node = program_output()
        node['command'] = 'echo spam'
        node['use_shell'] = False
        node['hide_standard_error'] = False
        node['working_directory'] = '/spam/with/eggs'
        command = Command.from_program_output_node(node)
        parsed_command = ('echo', 'spam')
        self.assertEqual(command.command, parsed_command)
        self.assertEqual(command.working_directory, '/spam/with/eggs')
        self.assertFalse(command.shell)
        self.assertFalse(command.hide_standard_error)
        node['use_shell'] = True
        self.assertTrue(Command.from_program_output_node(node).shell)
        self.assertFalse(Command.from_program_output_node(node).hide_standard_error)
        node['hide_standard_error'] = True
        self.assertTrue(Command.from_program_output_node(node).hide_standard_error)


    def test_from_programoutput_node_extraargs(self):
        node = program_output()
        node['command'] = 'echo spam'
        node['use_shell'] = False
        node['hide_standard_error'] = False
        node['extraargs'] = 'with eggs'
        node['working_directory'] = '/'
        command = Command.from_program_output_node(node)
        parsed_command = ('echo', 'spam', 'with', 'eggs')
        self.assertEqual(command.command, parsed_command)


    def test_execute(self, **kwargs):
        process = Command('echo spam', **kwargs).execute()
        self.assertIsNone(process.stderr)
        self.assertFalse(process.stdout.closed)
        self.assertEqual(process.wait(), 0)
        process.stdout.close()


    def test_execute_with_shell(self):
        self.test_execute(shell=True)

    def test_execute_with_hidden_standard_error(self):
        process = Command('echo spam', hide_standard_error=True).execute()
        self.assertFalse(process.stdout.closed)
        self.assertFalse(process.stderr.closed)
        self.assertEqual(process.wait(), 0)
        process.stdout.close()
        process.stderr.close()


    def test_get_output(self):
        returncode, output = Command('echo spam').get_output()
        self.assertEqual(returncode, 0)
        self.assertEqual(output, 'spam')


    def test_get_output_non_zero(self):
        returncode, output = Command(
            sys.executable + ' -c "import sys; print(\'spam\'); sys.exit(1)"').get_output()
        self.assertEqual(returncode, 1)
        self.assertEqual(output, 'spam')


    def test_get_output_with_hidden_standard_error(self):
        returncode, output = Command(
            sys.executable + ' -c "import sys; sys.stderr.write(\'spam\')"',
            hide_standard_error=True).get_output()
        self.assertEqual(returncode, 0)
        self.assertEqual(output, '')


    def test_get_output_with_working_directory(self):
        tmpdir = tempfile.mkdtemp()
        cwd = os.path.realpath(str(tmpdir))
        returncode, output = Command(
            sys.executable + ' -c "import sys, os; sys.stdout.write(os.getcwd())"',
            working_directory=cwd).get_output()
        self.assertEqual(returncode, 0)
        self.assertEqual(output, cwd)
        shutil.rmtree(tmpdir)

def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
