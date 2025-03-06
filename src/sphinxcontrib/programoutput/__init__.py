# -*- coding: utf-8 -*-
# Copyright (c) 2010, 2011, 2012, Sebastian Wiesner <lunaryorn@gmail.com>
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

"""
    sphinxcontrib.programoutput
    ===========================

    This extension provides a directive to include the output of commands as
    literal block while building the docs.

    .. moduleauthor::  Sebastian Wiesner  <lunaryorn@gmail.com>
"""

from __future__ import print_function, division, absolute_import

import sys
import os
import shlex
from subprocess import Popen, PIPE, STDOUT
from collections import defaultdict, namedtuple

from docutils import nodes
from docutils.parsers import rst
from docutils.parsers.rst.directives import flag, unchanged, nonnegative_int
from docutils.statemachine import StringList

from sphinx.util import logging as sphinx_logging

__version__ = '0.19.dev0'

logger = sphinx_logging.getLogger('contrib.programoutput')

class program_output(nodes.Element):
    pass


def _container_wrapper(directive, literal_node, caption):
    container_node = nodes.container('', literal_block=True,
                                     classes=['literal-block-wrapper'])
    parsed = nodes.Element()
    directive.state.nested_parse(StringList([caption], source=''),
                                 directive.content_offset, parsed)
    if isinstance(parsed[0], nodes.system_message): # pragma: no cover
        # TODO: Figure out if this is really possible and how to produce
        # it in a test case.
        msg = 'Invalid caption: %s' % parsed[0].astext()
        raise ValueError(msg)
    assert isinstance(parsed[0], nodes.Element)
    caption_node = nodes.caption(parsed[0].rawsource, '',
                                 *parsed[0].children)
    caption_node.source = literal_node.source
    caption_node.line = literal_node.line
    container_node += caption_node
    container_node += literal_node
    return container_node


def wrap_with_caption(node, caption, source='', line=0):
    """
    Wrap the given node in a container with a caption.
    This mimics a figure-like construct.
    """
    container = nodes.container('', classes=['literal-block-wrapper'])
    caption_node = nodes.caption(caption, caption)
    caption_node.source = source
    caption_node.line = line
    container += caption_node
    container += node
    return container



def _slice(value):
    parts = [int(v.strip()) for v in value.split(',')]
    if len(parts) > 2:
        raise ValueError('too many slice parts')
    return tuple((parts + [None] * 2)[:2])


class ProgramOutputDirective(rst.Directive):
    has_content = False
    final_argument_whitespace = True
    required_arguments = 1

    option_spec = dict(
        shell=flag,
        prompt=flag,
        nostderr=flag,
        ellipsis=_slice,
        extraargs=unchanged,
        returncode=nonnegative_int,
        cwd=unchanged,
        caption=unchanged,
        name=unchanged,
        language=unchanged,
        rich=flag            # When provided, enable rich SVG output.
    )

    def run(self):
        env = self.state.document.settings.env

        node = program_output()
        node.line = self.lineno
        node['command'] = self.arguments[0]

        if self.name == 'command-output':
            node['show_prompt'] = True
        else:
            node['show_prompt'] = 'prompt' in self.options

        node['hide_standard_error'] = 'nostderr' in self.options
        node['extraargs'] = self.options.get('extraargs', '')
        _, cwd = env.relfn2path(self.options.get('cwd', '/'))
        node['working_directory'] = cwd
        node['use_shell'] = 'shell' in self.options
        node['returncode'] = self.options.get('returncode', 0)
        node['language'] = self.options.get('language', 'text')
        node['rich'] = 'rich' in self.options:
        
        # Store the caption (if provided) regardless of the output mode.
        if 'caption' in self.options:
            node['caption'] = self.options['caption'] or self.arguments[0]
        
        if 'ellipsis' in self.options:
            node['strip_lines'] = self.options['ellipsis']
        self.add_name(node)
        return [node]



_Command = namedtuple(
    'Command', 'command shell hide_standard_error working_directory')


class Command(_Command):
    """
    A command to be executed.
    """

    def __new__(cls, command, shell=False, hide_standard_error=False,
                working_directory='/'):
        # `chdir()` resolves symlinks, so we need to resolve them too for
        # caching to make sure that different symlinks to the same directory
        # don't result in different cache keys.  Also normalize paths to make
        # sure that identical paths are also equal as strings.
        working_directory = os.path.normpath(os.path.realpath(
            working_directory))
        # Likewise, normalize the command now for better caching, and so
        # that we can present *exactly* what we run to the user.
        command = cls.__normalize_command(command, shell)
        return _Command.__new__(cls, command, shell, hide_standard_error,
                                working_directory)

    @staticmethod
    def __normalize_command(command, shell): # pylint:disable=unused-private-member
        # Returns either a native string, to a tuple.
        if (bytes is str
                and not isinstance(command, str)
                and hasattr(command, 'encode')):
            # Python 2, given a unicode string
            command = command.encode(sys.getfilesystemencoding())
            assert isinstance(command, str)

        if not shell and isinstance(command, str):
            command = shlex.split(command)

        if isinstance(command, list):
            command = tuple(command)

        assert isinstance(command, (str, tuple)), command

        return command

    @classmethod
    def from_program_output_node(cls, node):
        """
        Create a command from a :class:`program_output` node.
        """
        extraargs = node.get('extraargs', '')
        command = (node['command'] + ' ' + extraargs).strip()
        return cls(command, node['use_shell'],
                   node['hide_standard_error'], node['working_directory'])

    def execute(self):
        """
        Execute this command.

        Return the :class:`~subprocess.Popen` object representing the running
        command.
        """
        command = self.command

        # Popen is a context manager only in Python 3, and we'd have to restructure
        # the code to work with it anyway.
        # pylint:disable=consider-using-with
        return Popen(command, shell=self.shell, stdout=PIPE,
                     stderr=PIPE if self.hide_standard_error else STDOUT,
                     cwd=self.working_directory, 
                     )

    def get_output(self):
        """
        Get the output of this command.

        Return a tuple ``(returncode, output)``.  ``returncode`` is the
        integral return code of the process, ``output`` is the output as
        unicode string, with final trailing spaces and new lines stripped.
        """
        process = self.execute()
        output = process.communicate()[0].decode(
            sys.getfilesystemencoding(), 'replace').rstrip()
        return process.returncode, output

    def __str__(self):
        command = self.command
        command = list(command) if isinstance(command, tuple) else command
        return repr(command)


class ProgramOutputCache(defaultdict):
    """
    Execute command and cache their output.

    This class is a mapping.  Its keys are :class:`Command` objects represeting
    command invocations.  Its values are tuples of the form ``(returncode,
    output)``, where ``returncode`` is the integral return code of the command,
    and ``output`` is the output as unicode string.

    The first time, a key is retrieved from this object, the command is
    invoked, and its result is cached.  Subsequent access to the same key
    returns the cached value.
    """

    def __missing__(self, command):
        """
        Called, if a command was not found in the cache.

        ``command`` is an instance of :class:`Command`.
        """
        result = command.get_output()
        self[command] = result
        return result


def _prompt_template_as_unicode(app):
    tmpl = app.config.programoutput_prompt_template
    if isinstance(tmpl, bytes):
        for enc in 'utf-8', sys.getfilesystemencoding():
            try:
                tmpl = tmpl.decode(enc)
            except UnicodeError: # pragma: no cover
                pass
            else:
                app.config.programoutput_prompt_template = tmpl
                break
    return tmpl


def run_programs(app, doctree):
    """
    Execute all commands represented by `program_output` nodes in the doctree.
    Each node is replaced with the output of the executed command.

    If the 'rich' option is enabled on the node, the output is rendered as a styled SVG
    using Rich's Console. The console width is configurable via the
    'programoutput_rich_width' setting in conf.py. An optional title (':title:') can be provided
    for the rich SVG output. In both rich and literal modes, if a ':caption:' is provided,
    the output will be wrapped in a container with a caption.
    """
    cache = app.env.programoutput_cache

    for node in doctree.findall(program_output):
        # Create a Command instance from the node's attributes.
        command = Command.from_program_output_node(node)
        try:
            # Retrieve the command output from the cache (execute the command if not cached).
            returncode, output = cache[command]
        except EnvironmentError as error:
            # Log error and replace the node with an error message if command execution fails.
            error_message = 'Command {0} failed: {1}'.format(command, error)
            error_node = doctree.reporter.error(error_message, base_node=node)
            error_node['level'] = 6  # Set high severity to ensure visibility.
            node.replace_self(error_node)
            continue
        else:
            # Log a warning if the return code does not match the expected value.
            if returncode != node['returncode']:
                logger.warning(
                    'Unexpected return code %s from command %r (output=%r)',
                    returncode, command, output
                )

            # If the 'ellipsis' option is specified, replace the indicated lines with an ellipsis.
            if 'strip_lines' in node:
                start, stop = node['strip_lines']
                lines = output.splitlines()
                lines[start:stop] = ['...']
                output = '\n'.join(lines)

            # Format output with a prompt if 'show_prompt' is enabled.
            if node['show_prompt']:
                prompt_template = _prompt_template_as_unicode(app)
                output = prompt_template.format(
                    command=node['command'],
                    output=output,
                    returncode=returncode
                )

            # Check if the 'rich' option is enabled to render output as a Rich SVG.
            rich_flow = node.get('rich', False)
            if rich_flow:
                try:
                    # Import Rich's Console for rendering.
                    from rich.console import Console
                    from rich.text import Text
                except ImportError:
                    rich_flow = False
                    logger.warning("Rich is not installed; using a plain literal block instead.")
            
                else:
                    # Get the console width from configuration (default: 80).
                    rich_width = app.config.programoutput_rich_width
                    # Create a Console instance in record mode with the configured width.
                    console = Console(record=True, width=rich_width)
                    console.print(Text.from_ansi(output))
                    # Export the captured console output to an SVG string with inline styles.
                    svg_output = console.export_svg()
                    # Create a raw node with the SVG content for HTML output.
                    new_node = nodes.raw('', svg_output, format='html')
            
            if not rich_flow:
                # For non-rich output, simply create a literal block with the command output.
                new_node = nodes.literal_block(output, output)
                new_node['language'] = node['language']

            # If a caption is provided, wrap the output node in a container with a caption.
            if 'caption' in node:
                new_node = wrap_with_caption(new_node, node['caption'], node.get('source', ''), node.line)
            # Replace the original node with the new node.
            node.replace_self(new_node)



def init_cache(app):
    """
    Initialize the cache for program output at
    ``app.env.programoutput_cache``, if not already present (e.g. being
    loaded from a pickled environment).

    The cache is of type :class:`ProgramOutputCache`.
    """
    if not hasattr(app.env, 'programoutput_cache'):
        app.env.programoutput_cache = ProgramOutputCache()


def setup(app):
    app.add_config_value('programoutput_prompt_template', '$ {command}\n{output}', 'env')
    # Add a configuration value for the Rich console width (default: 80)
    app.add_config_value('programoutput_rich_width', 100, 'env')
    app.add_directive('program-output', ProgramOutputDirective)
    app.add_directive('command-output', ProgramOutputDirective)
    app.connect('builder-inited', init_cache)
    app.connect('doctree-read', run_programs)
    metadata = {
        'parallel_read_safe': True
    }
    return metadata
