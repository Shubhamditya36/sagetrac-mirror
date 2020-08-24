#!/usr/bin/env python

from __future__ import print_function

import os
import sys
import time
from distutils import log
from setuptools import setup, find_namespace_packages
from Cython.Build.Dependencies import default_create_extension

#########################################################
### Set source directory
#########################################################

import sage.env
sage.env.SAGE_SRC = os.getcwd()
from sage.env import *

from sage_setup.excepthook import excepthook
sys.excepthook = excepthook

#########################################################
### Configuration
#########################################################

if len(sys.argv) > 1 and sys.argv[1] == "sdist":
    sdist = True
else:
    sdist = False

#########################################################
### Testing related stuff
#########################################################

# Remove (potentially invalid) star import caches
import sage.misc.lazy_import_cache
if os.path.exists(sage.misc.lazy_import_cache.get_cache_file()):
    os.unlink(sage.misc.lazy_import_cache.get_cache_file())

from Cython.Build import cythonize
from sage.env import cython_aliases, sage_include_directories


#########################################################
### Discovering Sources
#########################################################

log.info("Discovering Python/Cython source code....")
t = time.time()

# Exclude a few files if the corresponding distribution is not loaded
from sage_setup.optional_extension import is_package_installed_and_updated
from sage_setup.find import find_sources_by_distribution

optional_packages = ['mcqd', 'bliss', 'tdlib', 'primecount',
                     'coxeter3', 'fes', 'sirocco', 'meataxe']
not_installed_packages = [package for package in optional_packages
                          if not is_package_installed_and_updated(package)]

distributions_to_exclude = ['sage-{}'.format(pkg)
                            for pkg in not_installed_packages]
files_to_exclude = find_sources_by_distribution(SAGE_SRC, distributions_to_exclude)

log.warn('files_to_exclude = {0}'.format(files_to_exclude))


# TODO: Fails with 
# src/sage/rings/padics/padic_capped_absolute_element.c:32285:233: note: expected ‘__mpz_struct *’ {aka ‘struct <anonymous> *’} but argument is of type ‘mpz_srcptr’ {aka ‘const struct <anonymous> *’}
files_to_exclude += ['src/sage/rings/padics/padic_capped_absolute_element.pyx', 'src/sage/rings/padics/padic_capped_relative_element.pyx', 'src/sage/rings/padics/padic_fixed_mod_element.pyx', 'src/sage/rings/padics/padic_floating_point_element.pyx']

python_packages = find_namespace_packages(where=SAGE_SRC)
log.warn('python_packages = {0}'.format(python_packages))
cython_modules = ["src/**/*.pyx"]
log.warn('cython_modules = {0}'.format(cython_modules))

include_directories = sage_include_directories(use_sources=True)
log.warn('include_directories = {0}'.format(include_directories))

aliases = cython_aliases()
log.warn('aliases = {0}'.format(aliases))

log.info("Discovered Python/Cython sources, time: %.2f seconds." % (time.time() - t))

import numpy
def my_create_extension(template, kwds):
    # Add numpy and source folder to the include search path used by the compiler
    # This is a workaround for https://github.com/cython/cython/issues/1480

    include_dirs = kwds.get('include_dirs', []) + [numpy.get_include(), 'src', 'src/sage/ext']
    kwds['include_dirs'] = include_dirs
    return default_create_extension(template, kwds)

#########################################################
### Distutils
#########################################################
compile_time_env = dict(
            PY_VERSION_HEX=sys.hexversion,
            PY_MAJOR_VERSION=sys.version_info[0],
            PY_PLATFORM=sys.platform
        )
cython_directives = dict(
            language_level="3str",
            cdivision=True,
        )

code = setup(name = 'sage',
      version     =  SAGE_VERSION,
      description = 'Sage: Open Source Mathematics Software',
      license     = 'GNU Public License (GPL)',
      author      = 'William Stein et al.',
      author_email= 'https://groups.google.com/group/sage-support',
      url         = 'https://www.sagemath.org',
      packages    = python_packages,
      package_dir = {"": "src"},
      package_data = {
          'sage.libs.gap': ['sage.gaprc'],
          'sage.interfaces': ['sage-maxima.lisp'],
          'sage.doctest':  ['tests/*'],
          'sage': ['ext_data/*',
                   'ext_data/kenzo/*',
                   'ext_data/singular/*',
                   'ext_data/singular/function_field/*',
                   'ext_data/images/*',
                   'ext_data/doctest/*',
                   'ext_data/doctest/invalid/*',
                   'ext_data/doctest/rich_output/*',
                   'ext_data/doctest/rich_output/example_wavefront/*',
                   'ext_data/gap/*',
                   'ext_data/gap/joyner/*',
                   'ext_data/mwrank/*',
                   'ext_data/notebook-ipython/*',
                   'ext_data/nbconvert/*',
                   'ext_data/graphs/*',
                   'ext_data/pari/*',
                   'ext_data/pari/dokchitser/*',
                   'ext_data/pari/buzzard/*',
                   'ext_data/pari/simon/*',
                   'ext_data/magma/*',
                   'ext_data/magma/latex/*',
                   'ext_data/magma/sage/*',
                   'ext_data/valgrind/*',
                   'ext_data/threejs/*']
      },
      scripts = [## The sage script
                 'bin/sage',
                 ## Other scripts that should be in the path also for OS packaging of sage:
                 'bin/sage-eval',
                 'bin/sage-runtests',          # because it is useful for doctesting user scripts too
                 'bin/sage-fixdoctests',       # likewise
                 'bin/sage-coverage',          # because it is useful for coverage-testing user scripts too
                 'bin/sage-coverageall',       # likewise
                 'bin/sage-cython',            # deprecated, might be used in user package install scripts
                 ## Helper scripts invoked by sage script
                 ## (they would actually belong to something like libexec)
                 'bin/sage-cachegrind',
                 'bin/sage-callgrind',
                 'bin/sage-massif',
                 'bin/sage-omega',
                 'bin/sage-valgrind',
                 'bin/sage-version.sh',
                 'bin/sage-cleaner',
                 ## Only makes sense in sage-the-distribution. TODO: Move to another installation script.
                 'bin/sage-list-packages',
                 'bin/sage-download-upstream',
                 'bin/sage-location',
                 ## Uncategorized scripts in alphabetical order
                 'bin/math-readline',
                 'bin/sage-env',
                 'bin/sage-env-config',
                 # sage-env-config.in -- not to be installed',
                 'bin/sage-gdb-commands',
                 'bin/sage-grep',
                 'bin/sage-grepdoc',
                 'bin/sage-inline-fortran',
                 'bin/sage-ipynb2rst',
                 'bin/sage-ipython',
                 'bin/sage-native-execute',
                 'bin/sage-notebook',
                 'bin/sage-num-threads.py',
                 'bin/sage-open',
                 'bin/sage-preparse',
                 'bin/sage-pypkg-location',
                 'bin/sage-python',
                 'bin/sage-rebase.bat',
                 'bin/sage-rebase.sh',
                 'bin/sage-rebaseall.bat',
                 'bin/sage-rebaseall.sh',
                 'bin/sage-rst2txt',
                 'bin/sage-run',
                 'bin/sage-run-cython',
                 'bin/sage-startuptime.py',
                 'bin/sage-update-src',
                 'bin/sage-update-version',
                 'bin/sage-upgrade',
                 ],
        ext_modules = cythonize(cython_modules,
                                exclude=files_to_exclude,
                                include_path=include_directories,
                                compile_time_env=compile_time_env,
                                compiler_directives=cython_directives,
                                aliases=aliases,
                                create_extension=my_create_extension))
