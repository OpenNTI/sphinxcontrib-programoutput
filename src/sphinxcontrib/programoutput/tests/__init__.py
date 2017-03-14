import os
import os.path
import shutil
import tempfile

from docutils.parsers.rst import directives
from sphinx.application import Sphinx

from functools import update_wrapper

class Lazy(object):

    def __init__(self, func, name=None):
        if name is None:
            name = func.__name__
        self.data = (func, name)
        update_wrapper(self, func)

    def __get__(self, inst, class_):
        if inst is None:
            return self


        func, name = self.data
        value = func(inst)
        inst.__dict__[name] = value
        inst.addCleanup(delattr, inst, name)
        return value

#: conf.py for tests
CONF_PY = """\
extensions = ['sphinxcontrib.programoutput']

source_suffix = '.rst'

master_doc = 'index'

project = u'epydoc-test'
copyright = u'2011, foo'

version = '1'
release = '1'

exclude_patterns = []

pygments_style = 'sphinx'
html_theme = 'default'
"""


class AppMixin(object):

    document_content = '=============\ndummy content\n=============\n'

    def setUp(self):
        # Avoid "WARNING: while setting up extension
        # sphinxcontrib.programoutput: directive u'program-output' is
        # already registered, it will be overridden".
        self.directives = directives._directives.copy()

    def tearDown(self):
        directives._directives = self.directives

    @Lazy
    def tmpdir(self):
        d = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, d)
        return d

    @Lazy
    def srcdir(self):
        """
        Generated source directory for test Sphinx application.
        """
        tmpdir = self.tmpdir
        srcdir = os.path.join(tmpdir, 'src')
        os.mkdir(srcdir)
        confpy = os.path.join(srcdir, 'conf.py')
        with open(confpy, 'w') as f:
            f.write(CONF_PY)
        index_document = os.path.join(srcdir, 'index.rst')
        with open(index_document, 'w') as f:
            f.write("""\
    .. toctree::

       content/doc""")
        content_directory = os.path.join(srcdir, 'content')
        os.mkdir(content_directory)
        content_document = os.path.join(content_directory, 'doc.rst')
        with open(content_document, 'w') as f:
            f.write("=====\n")
            f.write("Title\n")
            f.write("=====\n\n")
            f.write(self.document_content)

        return srcdir

    @Lazy
    def outdir(self):
        return os.path.join(self.tmpdir, 'html')

    @Lazy
    def doctreedir(self):
        return os.path.join(self.tmpdir, 'doctrees')

    @Lazy
    def confoverrides(self):
        return {}


    @Lazy
    def app(self):
        """
        Sphinx application for the current test.
        """
        srcdir = self.srcdir
        outdir = self.outdir
        doctreedir = self.doctreedir
        confoverrides = self.confoverrides
        warningiserror = not self.ignore_warnings

        app = Sphinx(str(srcdir), str(srcdir), str(outdir), str(doctreedir), 'html',
                     status=None, warning=None, freshenv=None,
                     warningiserror=warningiserror, confoverrides=confoverrides)
        if self.build_app:
            app.build()
        return app

    @Lazy
    def build_app(self):
        return False

    @Lazy
    def ignore_warnings(self):
        return False

    @Lazy
    def doctree(self):
        getattr(self, 'build_app')
        self.build_app = True
        app = self.app
        return app.env.get_doctree('content/doc')

def with_content(content, **kwargs):
    def factory(f):
        def w(self):
            self.document_content = content
            if kwargs:
                if 'ignore_warnings' in kwargs:
                    getattr(self, 'ignore_warnings')
                    self.ignore_warnings = kwargs.pop("ignore_warnings")
                getattr(self, 'confoverrides')
                self.confoverrides = kwargs
            f(self)
        return w
    return factory
