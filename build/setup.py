#!/usr/bin/env sage-system-python

from distutils.core import setup
from distutils.cmd import Command
from distutils.command.install import install as distutils_install
from distutils.errors import (DistutilsSetupError, DistutilsModuleError,
                              DistutilsOptionError)

class install(distutils_install):

    def run(self):
        import os
        import sys
        import shutil
        distutils_install.run(self)

        DOT_SAGE = os.environ.get('DOT_SAGE', os.path.join(os.environ.get('HOME'), '.sage'))
        # config.status and other configure output has to be writable.
        SAGE_ROOT = os.path.join(DOT_SAGE, 'sage-{}'.format(self.distribution.version))
        SAGE_LOCAL = os.path.join(SAGE_ROOT, 'local')
        if os.path.exists(os.path.join(SAGE_ROOT, 'config.status')):
            print('Reusing {}'.format(SAGE_ROOT))
        else:
            shutil.copytree('sage_root', SAGE_ROOT)  # will fail if already exists
            cmd = "cd {} && ./configure --prefix={} PYTHON3={}".format(SAGE_ROOT, SAGE_LOCAL, sys.executable)
            print("Running {}".format(cmd))
            if os.system(cmd) != 0:
                raise DistutilsSetupError("configure failed")
        # TODO: Store SAGE_LOCAL in a module sage_bootstrap.config

setup(
    name='sage_bootstrap',
    description='',
    author='Volker Braun',
    author_email='vbraun.name@gmail.com',
    packages=[
        'sage_bootstrap',
        'sage_bootstrap.download',
        'sage_bootstrap.compat',
    ],
    scripts=['bin/sage-package', 'bin/sage-download-file', 'bin/sage-system-python'],
    package_data = {
        'sage_bootstrap': ['sage_root']
    },
    version='1.0',
    url='https://www.sagemath.org',
    cmdclass=dict(install=install)
)
