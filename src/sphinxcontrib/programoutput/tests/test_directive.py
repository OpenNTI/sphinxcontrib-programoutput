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
import sys
import unittest

from sphinx.errors import SphinxWarning
from docutils.nodes import literal_block, system_message

from sphinxcontrib.programoutput import Command

from . import AppMixin
from . import with_content


class TestDirective(AppMixin,
                    unittest.TestCase):

    def assert_output(self, doctree, output):
        __tracebackhide__ = True
        literal = doctree.next_node(literal_block)
        self.assertTrue(literal)
        self.assertEqual(literal.astext(), output)

    def assert_cache(self, app, cmd, output, use_shell=False,
                     hide_standard_error=False, returncode=0,
                     working_directory=None):
        # pylint:disable=too-many-arguments
        cache = app.env.programoutput_cache
        working_directory = working_directory or app.srcdir
        working_directory = os.path.normpath(os.path.realpath(
            working_directory))
        cache_key = Command(cmd, use_shell, hide_standard_error,
                            working_directory)
        self.assertEqual(cache, {cache_key: (returncode, output)})

    @with_content('.. program-output:: echo eggs')
    def test_simple(self):

        self.assert_output(self.doctree, 'eggs')
        self.assert_cache(self.app, 'echo eggs', 'eggs')


    @with_content("""\
    .. program-output:: python -c 'print("spam with eggs")'""")
    def test_with_spaces(self):
        """
        Test for command splitting with spaces involved.  Do *not* use ``echo`` for
        this test, because ``echo`` handles multiple arguments just as well as
        single arguments.
        """

        self.assert_output(self.doctree, 'spam with eggs')
        self.assert_cache(self.app, 'python -c \'print("spam with eggs")\'',
                          'spam with eggs')


    @with_content("""\
    .. program-output:: python -c 'import sys; sys.stderr.write("spam with eggs")'
                              """)
    def test_standard_error(self):
        output = 'spam with eggs'
        self.assert_output(self.doctree, output)
        cmd = 'python -c \'import sys; sys.stderr.write("spam with eggs")\''
        self.assert_cache(self.app, cmd, output)


    @with_content("""\
    .. program-output:: python -V
       :nostderr:""")
    @unittest.skipIf(sys.version_info[0] > 2,
                     reason="Python 3 prints version to stdout, not stderr")
    def test_standard_error_disabled(self):
        self.assert_output(self.doctree, '')
        self.assert_cache(self.app, 'python -V', '', hide_standard_error=True)


    @with_content("""\
    .. program-output:: python -c 'import os; print(os.getcwd())'""")
    def test_working_directory_defaults_to_srcdir(self):
        output = os.path.realpath(self.srcdir)
        self.assert_output(self.doctree, output)
        self.assert_cache(self.app, "python -c 'import os; print(os.getcwd())'", output,
                          working_directory=str(self.srcdir))


    @with_content("""\
    .. program-output:: python -c 'import os; print(os.getcwd())'
       :cwd: /""")
    def test_working_directory_relative_to_srcdir(self):
        output = os.path.realpath(self.srcdir)
        self.assert_output(self.doctree, output)
        self.assert_cache(self.app, "python -c 'import os; print(os.getcwd())'", output,
                          working_directory=str(self.srcdir))


    @with_content("""\
    .. program-output:: python -c 'import os; print(os.getcwd())'
       :cwd: .""")
    def test_working_directory_relative_to_document(self):
        contentdir = os.path.join(self.srcdir, 'content')
        output = os.path.realpath(contentdir)
        self.assert_output(self.doctree, output)
        self.assert_cache(self.app, "python -c 'import os; print(os.getcwd())'", output,
                          working_directory=str(contentdir))


    @with_content("""\
.. program-output:: echo "${PWD}"
       :shell:
       :cwd: .""")
    def test_working_directory_with_shell(self):
        doctree = self.doctree
        contentdir = os.path.join(self.srcdir, 'content')
        output = os.path.realpath(contentdir)
        self.assert_output(doctree, output)
        self.assert_cache(self.app, 'echo "${PWD}"', output, use_shell=True,
                          working_directory=str(contentdir))


    @with_content('.. program-output:: echo "${HOME}"')
    def test_no_expansion_without_shell(self):
        self.assert_output(self.doctree, '${HOME}')
        self.assert_cache(self.app, 'echo "${HOME}"', '${HOME}')


    @with_content("""\
    .. program-output:: echo "${HOME}"
       :shell:""")
    def test_expansion_with_shell(self):
        self.assert_output(self.doctree, os.environ['HOME'])
        self.assert_cache(self.app, 'echo "${HOME}"', os.environ['HOME'], use_shell=True)


    @with_content("""\
    .. program-output:: echo "spam with eggs"
       :prompt:""")
    def test_prompt(self):
        self.assert_output(self.doctree, """\
$ echo "spam with eggs"
spam with eggs""")
        self.assert_cache(self.app, 'echo "spam with eggs"', 'spam with eggs')


    @with_content('.. command-output:: echo "spam with eggs"')
    def test_command(self):
        self.assert_output(self.doctree, """\
$ echo "spam with eggs"
spam with eggs""")
        self.assert_cache(self.app, 'echo "spam with eggs"', 'spam with eggs')


    @with_content('.. command-output:: echo spam',
                  programoutput_prompt_template='>> {command}\n<< {output}')
    def test_command_non_default_prompt(self):
        self.assert_output(self.doctree, '>> echo spam\n<< spam')
        self.assert_cache(self.app, 'echo spam', 'spam')

    @with_content("""\
    .. program-output:: echo spam
       :extraargs: with eggs""")
    def test_extraargs(self):
        self.assert_output(self.doctree, 'spam with eggs')
        self.assert_cache(self.app, 'echo spam with eggs', 'spam with eggs')


    @with_content(u'.. command-output:: echo "U+2264 ≤ LESS-THAN OR EQUAL TO"')
    def test_prompt_with_utf8(self):
        self.assert_output(self.doctree, u"""\
$ echo "U+2264 ≤ LESS-THAN OR EQUAL TO"
U+2264 ≤ LESS-THAN OR EQUAL TO""")
        self.assert_cache(self.app, u'echo "U+2264 ≤ LESS-THAN OR EQUAL TO"', u'U+2264 ≤ LESS-THAN OR EQUAL TO')


    @with_content('''\
    .. program-output:: echo
       :shell:
       :extraargs: "${HOME}"''')
    def test_extraargs_with_shell(self):
        self.assert_output(self.doctree, os.environ['HOME'])
        self.assert_cache(self.app, 'echo "${HOME}"', os.environ['HOME'], use_shell=True)


    @with_content("""\
    .. program-output:: echo spam
       :prompt:
       :extraargs: with eggs""")
    def test_extraargs_with_prompt(self):
        self.assert_output(self.doctree, '$ echo spam\nspam with eggs')
        self.assert_cache(self.app, 'echo spam with eggs', 'spam with eggs')


    @with_content("""\
    .. program-output:: python -c 'print("spam\\nwith\\neggs")'
       :ellipsis: 2""")
    def test_ellipsis_stop_only(self):
        self.assert_output(self.doctree, 'spam\nwith\n...')
        self.assert_cache(self.app, 'python -c \'print("spam\\nwith\\neggs")\'',
                          'spam\nwith\neggs')


    @with_content("""\
    .. program-output:: python -c 'print("spam\\nwith\\neggs")'
       :ellipsis: -2""")
    def test_ellipsis_negative_stop(self):
        self.assert_output(self.doctree, 'spam\n...')
        self.assert_cache(self.app, """python -c 'print("spam\\nwith\\neggs")'""",
                          'spam\nwith\neggs')


    @with_content("""\
    .. program-output:: python -c 'print("spam\\nwith\\neggs")'
       :ellipsis: 1, 2""")
    def test_ellipsis_start_and_stop(self):
        self.assert_output(self.doctree, 'spam\n...\neggs')
        self.assert_cache(self.app, """python -c 'print("spam\\nwith\\neggs")'""",
                          'spam\nwith\neggs')


    @with_content("""\
    .. program-output:: python -c 'print("spam\\nwith\\neggs")'
       :ellipsis: 1, -1""")
    def test_ellipsis_start_and_negative_stop(self):
        self.assert_output(self.doctree, 'spam\n...\neggs')
        self.assert_cache(self.app, """python -c 'print("spam\\nwith\\neggs")'""",
                          'spam\nwith\neggs')


    @with_content("""\
    .. program-output:: python -c 'import sys; sys.exit(1)'""")
    def test_unexpected_return_code(self):
        with self.assertRaises(SphinxWarning) as excinfo:
            self.app.build()
        self.assertIn('Unexpected return code 1 from command',
                      excinfo.exception.args[0])
        self.assertIn("python -c 'import sys; sys.exit(1)'",
                      excinfo.exception.args[0])


    @with_content("""\
    .. program-output:: python -c 'import sys; sys.exit(1)'
       :shell:""")
    def test_shell_with_unexpected_return_code(self):
        with self.assertRaises(SphinxWarning) as excinfo:
            self.app.build()
        self.assertIn('Unexpected return code 1 from command',
                      excinfo.exception.args[0])
        self.assertIn("python -c 'import sys; sys.exit(1)'",
                      excinfo.exception.args[0])



    @with_content("""\
    .. program-output:: python -c 'import sys; print("foo"); sys.exit(1)'
       :returncode: 1""")
    def test_expected_non_zero_return_code(self):
        self.assert_output(self.doctree, 'foo')
        self.assert_cache(self.app, 'python -c \'import sys; print("foo"); sys.exit(1)\'',
                          'foo', returncode=1)


    @with_content("""\
.. command-output:: python -c 'import sys; sys.exit(1)'
   :returncode: 1""",
                  programoutput_prompt_template='> {command}\n{output}\n[{returncode}]>')
    def test_prompt_with_return_code(self):
        doctree = self.doctree
        app = self.app
        self.assert_output(doctree, """\
> python -c 'import sys; sys.exit(1)'

[1]>""")
        self.assert_cache(app, "python -c 'import sys; sys.exit(1)'", '',
                          returncode=1)


    @with_content(u".. program-output:: 'spam with eggs'", ignore_warnings=True)
    def test_non_existing_executable(self):
        # check that a proper error message appears in the document
        message = self.doctree.next_node(system_message)
        self.assertTrue(message)
        srcfile = os.path.join(self.srcdir, 'content', 'doc.rst')
        self.assertEqual(message['source'], srcfile)
        self.assertEqual(message['line'], 5)

        message_text = message.astext()
        self.assertIn(srcfile, message_text)
        self.assertIn('spam with eggs', message_text)
        self.assertIn("Errno", message_text)


    @with_content("""\
    .. program-output:: echo spam
       :cwd: ./subdir""", ignore_warnings=True)
    def test_non_existing_working_directory(self):
        # check that a proper error message appears in the document
        doctree = self.doctree
        srcdir = self.srcdir
        message = doctree.next_node(system_message)
        self.assertTrue(message)
        srcfile = os.path.join(srcdir, 'content', 'doc.rst')
        self.assertEqual(message['source'], srcfile)
        self.assertEqual(message['line'], 5)

        message_text = message.astext()
        self.assertIn(srcfile, message_text)
        self.assertIn('subdir', message_text)
        self.assertIn("No such file or directory", message_text)

def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
