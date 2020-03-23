import os
import os.path
import shutil
import tempfile

from docutils import nodes
from docutils.parsers.rst import directives
from docutils.parsers.rst import roles
from sphinx.application import Sphinx

from functools import update_wrapper

# pylint:disable=no-self-use,protected-access,too-few-public-methods
# useless-object-inheritance is version specific
# pylint:disable=bad-option-value,useless-object-inheritance

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

def _find_duplicate_default_nodes():
    from sphinx import addnodes # pylint:disable=import-outside-toplevel

    class App(object):

        def __init__(self):
            self.nodes = set()

        def add_node(self, node):
            self.nodes.add(node.__name__)


    app = App()
    try:
        addnodes.setup(app)
    except AttributeError:
        # Sphinx 1 doesn't have this
        pass

    return app.nodes

class AppMixin(object):

    #: The contents of the main 'doc.rst' document.
    #:
    #: This will be written as a bytestring to the document, allowing for
    #: the document to be in an arbitrary encoding.
    #:
    #: If this object is not a bytestring, it will first be encoded using
    #: the encoding named in `self.document_encoding`.
    document_content = '=============\ndummy content\n=============\n'

    document_encoding = 'utf-8'

    duplicate_nodes_to_remove = _find_duplicate_default_nodes()

    def setUp(self):
        # Avoid "WARNING: while setting up extension
        # sphinxcontrib.programoutput: directive u'program-output' is
        # already registered, it will be overridden".
        # This may only be needed for Sphinx 1.
        self.directives = directives._directives.copy()
        # Likewise for 'eq'
        self.roles = roles._roles.copy()

        # Avoid "node class 'toctree' is already registered, its visitors will be overridden"
        # By default this class has *no* `visit_` methods
        for node in self.duplicate_nodes_to_remove:
            if hasattr(nodes.GenericNodeVisitor, 'visit_' + node):
                delattr(nodes.GenericNodeVisitor, 'visit_' + node)

    def tearDown(self):
        directives._directives = self.directives
        roles._roles = self.roles

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
        contents = self.document_content
        if not isinstance(contents, bytes):
            contents = contents.encode(self.document_encoding)

        with open(content_document, 'wb') as f:
            f.write(b"=====\n")
            f.write(b"Title\n")
            f.write(b"=====\n\n")

            f.write(contents)

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
    def build_app(self): # pylint:disable=method-hidden
        return False

    @Lazy
    def ignore_warnings(self):
        return True

    @Lazy
    def doctree(self):
        getattr(self, 'build_app')
        self.build_app = True
        app = self.app
        return app.env.get_doctree('content/doc')

assert isinstance(AppMixin.app, Lazy) # coverage
