from __future__ import absolute_import

import logging
import os
import sys
import time

from functools import partial

from sage.env import SAGE_DOC_SRC

from .. import get_builder
from .. import build_options as opts


logger = logging.getLogger('docbuild')


def _build_other_doc(args):
    """Target for parallel doc builds."""

    document = args[0]
    name = args[1]
    kwds = args[2]
    args = args[3:]
    logger.warning("\nBuilding %s.\n" % document)
    getattr(get_builder(document), name)(*args, **kwds)


class Builder(object):
    """
    Base class for all documentation builders (including the 'meta builder'
    class AllBuilder, which builds all documents.

    Currently just a placeholder.
    """

    priority = 0

    @classmethod
    def match(cls, name):
        """
        Checks whether this Builder class can build the document of the given
        name, and if so returns an instance of that class configured to build
        that document, and returns None otherwise.

        Builders are searched by order of priority, with document names matched
        against the Builders with highest priority first, but in general it is
        best to make matches as unambiguous as possible.
        """

        raise NotImplementedError('must be implemented by subclasses')

    @classmethod
    def output_formats(self):
        """
        Returns a list of the possible output formats.

        EXAMPLES::

            sage: from sage_setup.docbuild.builders.docbuilder import DocBuilder
            sage: DocBuilder.output_formats()
            ['changes', 'html', 'htmlhelp', 'inventory', 'json', 'latex', 'linkcheck', 'pdf', 'pickle', 'web']

        """
        # Go through all the attributes of self and check to see which ones
        # have an 'is_output_format' attribute.  These are the ones created
        # with output_formatter.
        output_formats = []
        for attr in dir(self):
            if hasattr(getattr(self, attr), 'is_output_format'):
                output_formats.append(attr)
        output_formats.sort()
        return output_formats


class AllBuilder(Builder):
    """
    A class used to build all of the documentation.
    """

    priority = 100

    def __getattr__(self, attr):
        """
        For any attributes not explicitly defined, we just go through
        all of the documents and call their attr.  For example,
        'AllBuilder().json()' will go through all of the documents
        and call the json() method on their builders.
        """
        return partial(self._wrapper, attr)

    @classmethod
    def match(cls, name):
        if name == 'all':
            return cls()

    def _wrapper(self, name, *args, **kwds):
        """
        This is the function which goes through all of the documents
        and does the actual building.
        """
        start = time.time()
        docs = self.get_all_documents()
        refs = [x for x in docs if x.endswith('reference')]
        others = [x for x in docs if not x.endswith('reference')]

        # Build the reference manual twice to resolve references.  That is,
        # build once with the inventory builder to construct the intersphinx
        # inventory files, and then build the second time for real.  So the
        # first build should be as fast as possible;
        logger.warning("\nBuilding reference manual, first pass.\n")
        for document in refs:
            getattr(get_builder(document), 'inventory')(*args, **kwds)

        logger.warning("Building reference manual, second pass.\n")
        for document in refs:
            getattr(get_builder(document), name)(*args, **kwds)

        # build the other documents in parallel
        L = [(doc, name, kwds) + args for doc in others]
        build_many(_build_other_doc, L)
        logger.warning("Elapsed time: %.1f seconds."%(time.time()-start))
        logger.warning("Done building the documentation!")

    def get_all_documents(self, default_lang=None):
        """
        Returns a list of all of the documents. A document is a directory within one of
        the language subdirectories of SAGE_DOC_SRC specified by the global LANGUAGES
        variable.

        If default_lang is given matching one of the documentation language
        codes, that code is stripped from all results (e.g. 'tutorial' is
        returned instead of 'en/tutorial').

        EXAMPLES::

            sage: from sage_setup.docbuild.builders import AllBuilder
            sage: documents = AllBuilder().get_all_documents()
            sage: 'en/tutorial' in documents
            True
            sage: documents[0] == 'en/reference'
            True
            sage: documents = AllBuilder().get_all_documents(default_lang='en')
            sage: 'tutorial' in documents
            True
        """

        documents = []
        for lang in opts.LANGUAGES:
            for document in os.listdir(os.path.join(SAGE_DOC_SRC, lang)):
                if (document not in opts.OMIT
                    and os.path.isdir(os.path.join(SAGE_DOC_SRC, lang, document))):
                    if lang == default_lang:
                        documents.append(document)
                    else:
                        documents.append(os.path.join(lang, document))

        # Ensure that the reference guide is compiled first so that links from
        # the other documents to it are correctly resolved.
        if default_lang == 'en':
            ref = 'reference'
        else:
            ref = os.path.join('en', 'reference')

        if ref in documents:
            documents.remove(ref)
        documents.insert(0, ref)

        return documents


if opts.NUM_THREADS > 1:
    def build_many(target, args):
        from multiprocessing import Pool
        pool = Pool(opts.NUM_THREADS, maxtasksperchild=1)
        # map_async handles KeyboardInterrupt correctly. Plain map and
        # apply_async does not, so don't use it.
        x = pool.map_async(target, args, 1)
        try:
            ret = x.get(99999)
            pool.close()
            pool.join()
        except Exception:
            pool.terminate()
            if opts.ABORT_ON_ERROR:
                raise
        return ret
else:
    def build_many(target, args):
        results = []

        for arg in args:
            try:
                results.append(target(arg))
            except Exception:
                if opts.ABORT_ON_ERROR:
                    raise

        return results


def output_formatter(type):
    """
    Returns a function which builds the documentation for
    output type type.
    """

    if isinstance(type, str):
        def formatter(self, *args, **kwds):
            output_dir = self._output_dir(type)

            options = opts.ALLSPHINXOPTS

            if self.name == 'website':
                # WEBSITESPHINXOPTS is either empty or " -A hide_pdf_links=1 "
                options += opts.WEBSITESPHINXOPTS

            if kwds.get('use_multidoc_inventory', True):
                options += ' -D multidoc_first_pass=0'
            else:
                options += ' -D multidoc_first_pass=1'

            build_command = '-b %s -d %s %s %s %s'%(type, self._doctrees_dir(),
                                                      options, self.dir,
                                                      output_dir)
            logger.debug(build_command)

            # Run Sphinx with Sage's special logger
            from ..sphinxbuild import runsphinx
            old_argv = sys.argv[:]
            sys.argv = ["sphinx-build"] + build_command.split()
            try:
                runsphinx()
            except Exception:
                if opts.ABORT_ON_ERROR:
                    raise
            finally:
                sys.argv = old_argv

            if "/latex" in output_dir:
                logger.warning("LaTeX file written to {}".format(output_dir))
            else:
                logger.warning(
                    "Build finished.  The built documents can be found in {}".
                    format(output_dir))
    else:
        # In case of use as a decorator
        formatter = type

    formatter.is_output_format = True
    return formatter
