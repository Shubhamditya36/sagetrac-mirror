# -*- coding: utf-8 -*-
r"""
Testing for features of the environment at runtime

A computation can require a certain package to be installed in the runtime
environment. Abstractly such a package describes a :class`Feature` which can
be tested for at runtime. It can be of various kinds, most prominently an
:class:`Executable` in the PATH or an additional package for some installed
system such as a :class:`GapPackage`.

AUTHORS:

- Julian Rüth (2016-04-07): Initial version

EXAMPLES:

Some generic features are available for common cases. For example, to
test for the existence of a binary, one can use an :class:`Executable`
feature::

    sage: from sage.misc.feature import GapPackage, Executable
    sage: Executable(name="sh", executable="sh").is_present()
    True

Here we test whether the grape GAP package is available::

    sage: GapPackage("grape", spkg="gap_packages").is_present() # optional: gap_packages
    True

When one wants to raise an error if the feature is not available, one
can use the ``require`` method::

    sage: Executable(name="sh", executable="sh").require()

    sage: Executable(name="random", executable="randomOochoz6x", spkg="random", url="http://rand.om").require()
    Traceback (most recent call last):
    ...
    FeatureNotPresentError: random is not available. To use this feature make
    sure that randomOochoz6x is in the PATH. To install random you can try to
    run sage -i random. Further installation instructions might be available at
    http://rand.om.

As can be seen above, features try to produce helpful error messages.
"""
from sage.misc.cachefunc import cached_method

class FeatureNotPresentError(RuntimeError):
    r"""
    A missing feature error.

    EXAMPLES::

        sage: from sage.misc.feature import Feature
        sage: class Missing(Feature):
        ....:     def is_present(self): return False

        sage: Missing(name="missing").require()
        Traceback (most recent call last):
        ...
        FeatureNotPresentError: missing is not available.
    """
    def __init__(self, feature):
        r"""
        TESTS::

            sage: from sage.misc.feature import Feature, FeatureNotPresentError
            sage: class Missing(Feature):
            ....:     def is_present(self): return False

            sage: try:
            ....:     Missing(name="missing").require() # indirect doctest
            ....: except FeatureNotPresentError: pass

        """
        self.feature = feature

    def __str__(self):
        r"""
        Return the error message.

        EXAMPLES::

            sage: from sage.misc.feature import GapPackage
            sage: GapPackage("gapZuHoh8Uu").require()   # indirect doctest
            Traceback (most recent call last):
            ...
            FeatureNotPresentError: GAP package gapZuHoh8Uu is not available.
        """
        return ("%s is not available. %s"%(self.feature.name, self.feature.resolution())).strip()


class Feature(object):
    r"""
    A feature of the runtime environment

    Overwrite :meth:`is_present` to add feature checks.

    EXAMPLES::

        sage: from sage.misc.feature import GapPackage
        sage: GapPackage("grape", spkg="gap_packages") # indirect doctest
        Feature("GAP package grape")
    """
    VERBOSE_LEVEL = 50

    def __init__(self, name, spkg = None):
        r"""
        TESTS::

            sage: from sage.misc.feature import GapPackage, Feature
            sage: isinstance(GapPackage("grape", spkg="gap_packages"), Feature) # indirect doctest
            True
        """
        self.name = name;
        self.spkg = spkg

    def is_present(self):
        r"""
        Return whether the feature is present.

        EXAMPLES::

            sage: from sage.misc.feature import GapPackage
            sage: GapPackage("grape", spkg="gap_packages").is_present() # optional: gap_packages
            True
            sage: GapPackage("NOT_A_PACKAGE", spkg="gap_packages").is_present() # optional: gap_packages
            False
        """
        return True

    def require(self):
        r"""
        Raise a :class:`FeatureNotPresentError` if the feature is not present.

        EXAMPLES::

            sage: from sage.misc.feature import GapPackage
            sage: GapPackage("ve1EeThu").require()
            Traceback (most recent call last):
            ...
            FeatureNotPresentError: GAP package ve1EeThu is not available.
        """
        if not self.is_present():
            raise FeatureNotPresentError(self)

    def resolution(self):
        r"""
        Return a hint on how to enable this feature.

        EXAMPLES::

            sage: from sage.misc.feature import GapPackage
            sage: GapPackage("grape", spkg="gap_packages").resolution()
            'You can try to install this package with sage -i gap_packages.'
        """
        return ""

    def __repr__(self):
        r"""
        Return a printable representation of this object.

        EXAMPLES::

            sage: from sage.misc.feature import GapPackage
            sage: GapPackage("grape") # indirect doctest
            Feature("GAP package grape")
        """
        return 'Feature("%s")'%(self.name,)

class GapPackage(Feature):
    r"""
    A feature describing the presence of a GAP package.

    EXMAPLES::

        sage: from sage.misc.feature import GapPackage
        sage: GapPackage("grape", spkg="gap_packages")
        Feature("GAP package grape")
    """
    def __init__(self, package, spkg=None):
        Feature.__init__(self, "GAP package %s"%package)
        self.package = package
        self.spkg = spkg

    @cached_method
    def is_present(self):
        r"""
        Return whether the package is available in GAP.

        This does not check whether this package is functional.

        EXAMPLES::

            sage: from sage.misc.feature import GapPackage
            sage: GapPackage("grape", spkg="gap_packages").is_present() # optional: gap_packages
            True
        """
        from sage.libs.gap.libgap import libgap
        return bool(libgap.eval('TestPackageAvailability("%s")'%self.package))

    def resolution(self):
        r"""
        Return a hint on how to enable this feature.

        EXAMPLES::

            sage: from sage.misc.feature import GapPackage
            sage: GapPackage("grape", spkg="gap_packages").resolution()
            'You can try to install this package with sage -i gap_packages.'
        """
        if self.spkg:
            return "You can try to install this package with sage -i %s."%(self.spkg,)
        else:
            return ""

class Executable(Feature):
    r"""
    A feature describing an executable in the PATH.

    .. NOTE::

        Overwrite :meth:`is_functional` if you also want to check whether
        the executable shows proper behaviour.

        Calls to :meth:`is_present` are cached. You might want to cache the
        :class:`Executable` object to prevent unnecessary calls to the
        executable.

    EXAMPLES::

        sage: from sage.misc.feature import Executable
        sage: Executable(name="sh", executable="sh").is_present()
        True
    """
    def __init__(self, name, executable, spkg=None, url=None):
        r"""
        TESTS::

            sage: from sage.misc.feature import Executable
            sage: isinstance(Executable(name="sh", executable="sh"), Executable)
            True
        """
        Feature.__init__(self, name=name)
        self.executable = executable
        self.spkg = spkg
        self.url = url

    @cached_method
    def is_present(self):
        r"""
        Test whether the executable is on the current PATH and functional.

        .. SEEALSO:: :meth:`is_functional`

        EXAMPLES::

            sage: from sage.misc.feature import Executable
            sage: Executable(name="sh", executable="sh").is_present()
            True
        """
        from distutils.spawn import find_executable
        if find_executable(self.executable) is None:
            from sage.misc.misc import verbose
            verbose("No %s found on path.`"%(self.executable,), level=Feature.VERBOSE_LEVEL)
            return False
        return self.is_functional()

    def is_functional(self):
        r"""
        Return whether an executable in the path is functional.

        EXAMPLES:

        This default implementation always return ``True``::

            sage: from sage.misc.feature import Executable
            sage: Executable(name="sh", executable="sh").is_functional()
            True
        """
        return True

    def resolution(self):
        r"""
        EXAMPLES::

            sage: from sage.misc.feature import Executable
            sage: Executable(name="CSDP", spkg="csdp", executable="theta", url="http://github.org/dimpase/csdp").resolution()
            'To use this feature make sure that theta is in the PATH. To install CSDP you can try to run sage -i csdp. Further installation instructions might be available at http://github.org/dimpase/csdp.'
        """
        return "".join([
            "To use this feature make sure that %s is in the PATH."%(self.executable,),
            "  To install %s you can try to run sage -i %s."%(self.name, self.spkg) if self.spkg else "",
            "  Further installation instructions might be available at %s."%(self.url,) if self.url else ""])
