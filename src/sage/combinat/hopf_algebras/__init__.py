# -*- coding: utf-8 -*-
r"""
Pattern of graded connexe Hopf algebras (with realizations)

Author:
-------

    - Jean-Baptiste Priez
"""
#*****************************************************************************
#       Copyright (C) 2014 Jean-Baptiste Priez <jbp@kerios.fr>.
#
#  Distributed under the terms of the GNU General Public License (GPL)
#
#  The full text of the GPL is available at:
#
#                  http://www.gnu.org/licenses/
#*****************************************************************************
from sage.categories.category import Category
from sage.categories.hopf_algebras import HopfAlgebras
from sage.categories.realizations import Category_realization_of_parent
from sage.categories.rings import Rings
from sage.combinat.free_module import CombinatorialFreeModule
from sage.structure.parent import Parent
from sage.structure.unique_representation import UniqueRepresentation


class PatternGradedConnectedHopfAlgebra(Parent, UniqueRepresentation):
    """
    This class is a pattern use to define easily a Hopf algebra with
    with several bases.

    """

    # Define this attribute if there a default basis index
    _default_basis_indices_ = None

    def _underlying_category_(self, R):
        """
        This method is define the category of the Hopf algebra.

        By default, we considere graded and connected Hopf algebra.

        (There is no part `WithRealizations` because it is automatically
         added in the `_init_` method.)
        """
        return HopfAlgebras(R).Graded().Connected()

    def __init__(self, R):
        """

        """
        assert(R in Rings()), '%s must be a ring' % R
        self.BasisCategory.func.ambient = lambda o: self
        Parent.__init__(self, base=R,
                    category=self._underlying_category_(R).WithRealizations())

        # define a default realization
        self._Basis.realization_of = lambda o: self

        # define a default set of indices if possible
        if self._default_basis_indices_ is not None:
            self._Basis._basis_indices_ = self._default_basis_indices_

        # register realization given by *register_basis_to_cha*
        # NOTE: it's important to register realization to use morphism!
        for real in self._list_of_realizations:
            getattr(self,real)()

        self.a_realization = lambda : self._realizations[0]

    class BasisCategory(Category_realization_of_parent):
        """
        A Hopf algebra should define the category of its basis
        """

        def super_categories(self):
            R = self.base().base_ring()
            return [self.ambient()._underlying_category_(R).\
                    WithBasis().Realizations()]

        class ParentMethods:
            pass

    class _Basis(CombinatorialFreeModule):

        _prefix_ = "** TO DEFINE **"
        _basis_indices_ = "** TO DEFINE **"

        def _morphisms_(self):
            """
            A method use to instanciate all morphisms define in the basis
            """

        def _extra_categories_(self):
            """
            Method to define extra categories of the basis

            For example, if you want use generic design for polynomial
            realizations
            """
            return []

        def __init__(self):
            CombinatorialFreeModule.__init__(
                self,
                self.realization_of().base_ring(),
                self._basis_indices_,
                prefix=self._prefix_,
                bracket=False,
                category=Category.join(
                    [self.realization_of().BasisCategory().Realizations()] +
                    self._extra_categories_()
                ))

            self._morphisms_()

        def _repr_(self):
            return repr(self.realization_of()) + " on the " + \
                self._realization_name() + " basis"

        def one_basis(self):
            """
            By default the `one` of a combinatorial Hopf algebra is the unique
            element of the homogeneous component of size `0`.
            """
            indices = self._basis_indices_
            return indices.graded_component(indices.grading_set().first()).first()

        def counit_on_basis(self, sigma):
            """
            By default the `counit` is given on basis by `1` (of the field) if
            `\sigma` is the `one` (of the module) and `0` (of the field) in
            otherwise.
            """
            indices = self._basis_indices_
            return self.base_ring().one() \
                    if indices.grading(sigma) == indices.grading_set().first() \
                    else self.base_ring().zero()

def words_like_getitem(self, c, *rest):
    """
    This method implements the abuses of notations::

        F[1,3,2]
        F[[1,3,2]]
        F[FQSym.indices()([2,1])]

    .. todo::

        This should call ``super.monomial`` if the input can't
        be made into a composition so as not to interfere with
        the standard notation ``Psi['x,y,z']``.

        This could possibly be shared with Sym, FQSym, and
        other algebras with bases indexed by list-like objects

        TODO:: généraliser la méthode...
    """
    from sage.rings.integer import Integer
    Keys = self.basis().keys()
    if c in Keys:
        assert len(rest) == 0
        c = Keys(c)
    else:
        if len(rest) > 0 or isinstance(c, (int, Integer)):
            c = Keys([c] + list(rest))
        else:
            c = Keys(list(c))
    return self.monomial(c)

def register_basis_to_cha(basis_class, name, cha_class):
    """
    Function uses to register the basis define in the class `basis_class`
    in the combinatorial Hopf algebra define in the class `cha_class`.

    The `name` is use to define a nice method to call the basis.

    For example::

        sage: from sage.combinat.hopf_algebras.exmaples.simple_fqsym import \
        ...         SimpleFQSym
        sage: F = SimpleFQSym(QQ).Fundamental()
    """
    setattr(cha_class, name, basis_class)
    setattr(cha_class, basis_class._prefix_, basis_class)
    if not hasattr(cha_class, "_list_of_realizations"):
        cha_class._list_of_realizations = []
    cha_class._list_of_realizations.append(basis_class._prefix_)
