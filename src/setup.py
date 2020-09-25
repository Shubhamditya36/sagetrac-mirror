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

# TODO: Fails because sage/ext/interpreters/ is empty
files_to_exclude += ['sage/calculus/integration.pyx', 'sage/plot/plot3d/parametric_surface.pyx']

# TODO: Fails due to missing Singular lib
files_to_exclude += [
    'sage/algebras/letterplace/free_algebra_element_letterplace.pyx',
    'sage/algebras/letterplace/free_algebra_letterplace.pyx',
    'sage/algebras/letterplace/letterplace_ideal.pyx',
    'sage/libs/pynac/constant.pyx',
    'sage/libs/pynac/pynac.pyx',
    'sage/libs/singular/function.pyx',
    'sage/libs/singular/groebner_strategy.pyx',
    'sage/libs/singular/option.pyx',
    'sage/libs/singular/polynomial.pyx',
    'sage/libs/singular/ring.pyx',
    'sage/libs/singular/singular.pyx',
    'sage/matrix/matrix_mpolynomial_dense.pyx',
    'sage/rings/polynomial/multi_polynomial_ideal_libsingular.pyx',
    'sage/rings/polynomial/multi_polynomial_libsingular.pyx',
    'sage/rings/polynomial/plural.pyx',
    'sage/symbolic/comparison.pyx',
    'sage/symbolic/constants_c.pyx',
    'sage/symbolic/expression.pyx',
    'sage/symbolic/function.pyx',
    'sage/symbolic/getitem.pyx',
    'sage/symbolic/ring.pyx',
    'sage/symbolic/series.pyx',
    'sage/symbolic/substitution_map.pyx',
]

# TODO: Fails due to missing GAP lib
files_to_exclude += [
    'sage/coding/codecan/codecan.pyx',
    'sage/combinat/enumeration_mod_permgroup.pyx',
    'sage/combinat/root_system/reflection_group_c.pyx',
    'sage/combinat/root_system/reflection_group_element.pyx',
    'sage/graphs/spanning_tree.pyx',
    'sage/groups/libgap_wrapper.pyx',
    'sage/groups/matrix_gps/group_element.pyx',
    'sage/groups/perm_gps/permgroup_element.pyx',
    'sage/groups/perm_gps/partn_ref/automorphism_group_canonical_label.pyx',
    'sage/groups/perm_gps/partn_ref/canonical_augmentation.pyx',
    'sage/groups/perm_gps/partn_ref/data_structures.pyx',
    'sage/groups/perm_gps/partn_ref/double_coset.pyx',
    'sage/groups/perm_gps/partn_ref/refinement_binary.pyx',
    'sage/groups/perm_gps/partn_ref/refinement_graphs.pyx',
    'sage/groups/perm_gps/partn_ref/refinement_lists.pyx',
    'sage/groups/perm_gps/partn_ref/refinement_matrices.pyx',
    'sage/groups/perm_gps/partn_ref/refinement_python.pyx',
    'sage/groups/perm_gps/partn_ref/refinement_sets.pyx',
    'sage/groups/perm_gps/partn_ref2/refinement_generic.pyx',
    'sage/libs/gap/element.pyx',
    'sage/libs/gap/libgap.pyx',
    'sage/libs/gap/util.pyx',
    'sage/matrix/matrix_gap.pyx',
    'sage/sets/disjoint_set.pyx'
]

# TODO: Fails due to missing Arb lib
files_to_exclude += [
    'sage/libs/arb/arith.pyx',
    'sage/matrix/matrix_complex_ball_dense.pyx',
    'sage/rings/complex_arb.pyx',
    'sage/rings/number_field/number_field_element_quadratic.pyx',
    'sage/rings/polynomial/polynomial_complex_arb.pyx',
    'sage/rings/real_arb.pyx'
]

# TODO: Fails due to missing ecl lib
files_to_exclude += ['sage/libs/ecl.pyx']

# TODO: Fails due to missing giac lib
files_to_exclude += ['sage/libs/giac/giac.pyx']

# TODO: Fails due to missing homfly lib
files_to_exclude += ['sage/libs/homfly.pyx']

# TODO: Fails due to problem in cysignals (missing cysigs)
files_to_exclude += [
    'sage/rings/padics/padic_capped_absolute_element.pyx',
    'sage/rings/padics/padic_capped_relative_element.pyx',
    'sage/rings/padics/padic_fixed_mod_element.pyx',
    'sage/rings/padics/padic_floating_point_element.pyx'
]

# TODO: Fails due to missing CCObject
files_to_exclude += ['sage/rings/padics/pow_computer_ext.pyx']

# TODO: Fails due to missing linbox lib
files_to_exclude += [
    'sage/libs/linbox/linbox_flint_interface.pyx',
    'sage/matrix/matrix_integer_sparse.pyx',
    'sage/matrix/matrix_modn_dense_double.pyx',
    'sage/matrix/matrix_modn_dense_float.pyx',
    'sage/matrix/matrix_modn_sparse.pyx'
]

# TODO: Fails due to missing ratpoints lib
files_to_exclude += ['sage/libs/ratpoints.pyx', 'sage/schemes/elliptic_curves/descent_two_isogeny.pyx']

# TODO: Fails due to missing zn_poly lib
files_to_exclude += [
    'sage/modular/modsym/p1list.pyx',
    'sage/modular/pollack_stevens/dist.pyx',
    'sage/rings/fraction_field_FpT.pyx',
    'sage/rings/polynomial/polynomial_zmod_flint.pyx',
    'sage/schemes/hyperelliptic_curves/hypellfrob.pyx',
]

# TODO: Fails due to missing mari lib
files_to_exclude += [
    'sage/matrix/matrix_gf2e_dense.pyx',
    'sage/matrix/matrix_integer_dense.pyx',
    'sage/matrix/matrix_mod2_dense.pyx',
    'sage/matrix/matrix_rational_dense.pyx',
    'sage/modules/vector_mod2_dense.pyx',
    'sage/rings/polynomial/pbori.pyx',
    'sage/rings/polynomial/polynomial_gf2x.pyx'
]

python_packages = find_namespace_packages(where=SAGE_SRC)
log.warn('python_packages = {0}'.format(python_packages))
cython_modules = ["**/*.pyx"]
log.warn('cython_modules = {0}'.format(cython_modules))

include_directories = sage_include_directories(use_sources=True)
include_directories += ['.']
# for gmpy2 support
#include_directories += sys.path
log.warn('include_directories = {0}'.format(include_directories))

aliases = cython_aliases()
log.warn('aliases = {0}'.format(aliases))

log.info("Discovered Python/Cython sources, time: %.2f seconds." % (time.time() - t))

import numpy
def my_create_extension(template, kwds):
    # Add numpy and source folder to the include search path used by the compiler
    # This is a workaround for https://github.com/cython/cython/issues/1480

    include_dirs = kwds.get('include_dirs', []) + [numpy.get_include(), 'src', 'src/sage/ext', '.']
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
