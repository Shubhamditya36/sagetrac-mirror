r"""
Universal Enveloping Vertex Algebra

Let `L` be a finitely generated
:mod:`Lie Conformal Algebra<sage.categories.lie_conformal_algebras>`
over `R`. Suppose that as `R[T]` module, we have

.. MATH::

    L = \bigoplus_{i = 1}^N R[T]\cdot a^i \oplus \bigoplus_{j \in J}
    R[T] \cdot C^j/R[T],

that is, `L` is freely generated by some finite vectors `a^i` and some
central vectors `C^j` satisfying `TC^j = 0`.

Then for any collection `c = \{c^j\}_{j \in J} \subset R`, the free
`R`-module generated by vectors of the form

.. MATH::
    :label: pbw_basis

    a^1_{(-n_{1,1} -1)} \cdots a^1_{(-n_{1,k_{1}} - 1)} a^2_{(-n_{2,1}
    -1)} \cdots a^N_{(-n_{N,k_N}-1)} |0\rangle,

with `n_{i,1} \geq n_{i,2} ... \geq n_{i,k_i} \geq 0` for all `i`,
carries a natural
:mod:`Vertex Algebra<sage.categories.vertex_algebras>` structure.
This is the quotient `V^c` of `U(L)`, the *universal enveloping* vertex
algebra of `L` by the central ideal generated by
`\{ C^j - c^j|0\rangle\}_{j \in J}`.

The basis :eq:`pbw_basis` is called a *PBW basis* for `V^c`. It is
naturally parametrized by
:mod:`Partition Tuples<sage.combinat.partition_tuple>` of level `N`.

In the case when `L` is a super Lie conformal algebra, a similar
construction exists where the PBW basis is parametrized by *regular*
partition tuples.

If `L` is an `H`-graded Lie conformal algebra, so is `V^c`, in this case
instead of the usual `(n)`-th products used in the PBW basis
:eq:`pbw_basis`, it is natural to use the *shifted* products defined
by `a_{n} = a_{(n+w-1)}` where `w` is the conformal weight of `a`. The
basis is then parametrized by :mod:`Energy Partition Tuples\
<sage.algebras.vertex_algebras.energy_partition_tuples>`.

.. NOTE::

    We consider only rational gradings where each generator has
    positive rational conformal weight. Thus, `V^c` is
    `\mathbb{Q}_+`-graded with finite dimensional graded pieces.

AUTHORS:

- Reimundo Heluani (2019-08-09): Initial implementation.
"""

#******************************************************************************
#       Copyright (C) 2019 Reimundo Heluani <heluani@potuz.net>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#                  http://www.gnu.org/licenses/
#*****************************************************************************


from .vertex_algebra import VertexAlgebra
from sage.categories.lie_conformal_algebras import LieConformalAlgebras
from sage.categories.vertex_algebras import VertexAlgebras
from sage.sets.family import Family
from sage.combinat.free_module import CombinatorialFreeModule
from sage.misc.cachefunc import cached_method
from .vertex_algebra_element import UniversalEnvelopingVertexAlgebraElement
from .energy_partition_tuples import EnergyPartitionTuples

class UniversalEnvelopingVertexAlgebra(VertexAlgebra,CombinatorialFreeModule):

    def __init__(self, R, L, category=None,
                 central_parameters=None,
                 names=None, latex_names=None):
        r"""
        The (central quotient of the) universal enveloping vertex
        algebra of the Lie conformal algebra `L`.


        INPUT:

        - ``R`` -- a commutative ring; the base ring of this vertex
          algebra

        - ``L`` -- a :mod:`LieConformalAlgebra`

        - ``category`` -- a ``Category``; the category this vertex
          algebra belongs to

        - ``central_parameters`` -- a finite
          :mod:`Family<sage.sets.family>`
          parametrized by central generators of ``L`` (default: ``0``
          for each central generator of ``L``);
          a family describing the central character

        - ``names`` -- a list of ``str``; alternative names for the
          generators

        - ``latex_names`` -- a list of ``str``; alternative names for
          the `\LaTeX` representation of the generators

        .. WARNING::

            We allow ``R`` to be an arbitrary commutative ring to
            perform basic computations of OPE. However, behaviour is
            undefined if ``R`` is not a field of characteristic ``0``.

        .. NOTE::

            This class should not be called directly by the user.
            Instead the user should call the method
            :meth:`~sage.categories.lie_conformal_algebras.LieConformalAlgebras.ParentMethods.universal_enveloping_algebra`
            of ``L``.

        EXAMPLES::

            sage: Vir = VirasoroLieConformalAlgebra(QQ)
            sage: Vir.inject_variables()
            Defining L, C
            sage: cp = Family({C:1})
            sage: from sage.algebras.vertex_algebras.universal_enveloping_vertex_algebra import UniversalEnvelopingVertexAlgebra
            sage: V = UniversalEnvelopingVertexAlgebra(QQ, Vir, central_parameters=cp); V
            The universal enveloping vertex algebra of the Virasoro Lie conformal algebra over Rational Field
            sage: L*L
            L_-2L_-2|0>
            sage: _.parent() is V
            True
            sage: W = Vir.universal_enveloping_algebra({C:1})
            sage: W is V
            True

        TESTS:

        Test that regular partition tuples of level 1 are being used::

            sage: bd = {('a','a'): {1: {('K',0): 1}}}
            sage: R = LieConformalAlgebra(QQ, bd, central_elements=('K',), names = ('a',))
            sage: R.inject_variables()
            Defining a, K
            sage: V = R.universal_enveloping_algebra({K:1}); V
            The universal enveloping vertex algebra of Lie conformal algebra with generators (a, K) over Rational Field
            sage: V._indices
            0-Regular partition tuples of level 1

        Test that the beta-gamma system is not graded::

            sage: R = BosonicGhostsLieConformalAlgebra(QQ)
            sage: V = R.universal_enveloping_algebra()
            sage: V.category()
            Category of finitely generated vertex algebras with basis over Rational Field
            sage: V._indices
            0-Regular partition tuples of level 2
        """
        if L not in LieConformalAlgebras(R).WithBasis().FinitelyGenerated():
            raise ValueError ( "L needs to be a finitely generated " \
                "Lie conformal algebra with basis, got {}".format(L) )

        category = VertexAlgebras(R).FinitelyGenerated().WithBasis().\
           or_subcategory(category)

        if L in LieConformalAlgebras(R).Graded():
            from sage.rings.all import QQ
            if all(g.degree() in QQ and g.degree() > 0 for g in L.gens() if \
                   g not in L.central_elements()):
                category = category.Graded()

        if L in LieConformalAlgebras(R).Super():
            category = category.Super()

        if names is None:
            try:
                gnames = L.variable_names()
            except ValueError:
                gnames = None
            if gnames is not None:
                if not len(L.central_elements()):
                    names = gnames
                else:
                    names = gnames[:-len(L.central_elements())]

        if latex_names is None:
            latex_names = L._latex_names

        VertexAlgebra.__init__(self, R, category=category, names=names,
                                latex_names=latex_names)

        self._lca = L
        if not central_parameters:
            central_parameters = Family({i:0  for i in L.central_elements()})
        if set(central_parameters.keys()) != set(L.central_elements()):
            raise ValueError ("central_parameters must be parametrized by "\
                              "central elements")

        self._central_parameters = central_parameters
        self._ngens = L.ngens() - central_parameters.cardinality()

        #need to call directly this because of 1 generator.
        #Also:self._module is needed for self.ngens()
        regular = tuple([2*g.is_even_odd() for g in L.gens()\
                    if g not in L.central_elements()])
        if self.is_graded():
            weights = tuple([g.degree() for g in L.gens() if g not in\
                             L.central_elements()])
            basis = EnergyPartitionTuples(weights,self._ngens,regular=regular)
        else:
            from sage.combinat.partition_tuple import \
                                                   RegularPartitionTuples_level
            basis = RegularPartitionTuples_level(level=self._ngens,
                                                                regular=regular)
        CombinatorialFreeModule.__init__(self, R, basis_keys=basis,
                        category=category,
                        element_class=UniversalEnvelopingVertexAlgebraElement)
        self.register_lift()


    def _repr_(self):
        """
        The name of this vertex algebra.

        EXAMPLES::

            sage: L = NeveuSchwarzLieConformalAlgebra(QQ)
            sage: L.universal_enveloping_algebra()
            The universal enveloping vertex algebra of the Neveu-Schwarz super Lie conformal algebra over Rational Field
        """
        lcafirst,lcaleft = format(self._lca).split(' ',1)
        if lcafirst == "The":
            return "The universal enveloping vertex algebra of the " + lcaleft
        return "The universal enveloping vertex algebra of " + lcafirst +\
                " " + lcaleft

    def register_lift(self):
        """
        Register a new coercion from its Lie conformal algebra.

        If this vertex algebra is the universal enveloping vertex
        algebra of the Lie conformal algebra `L`, register a new
        coercion from `L`.

        .. SEEALSO::

            :meth:`sage.algebras.lie_conformal_algebras.lie_conformal_algebra_element.lift`

        EXAMPLES::

            sage: L = VirasoroLieConformalAlgebra(QQ);
            sage: V = L.universal_enveloping_algebra()
            sage: L.lift
            Generic morphism:
              From: The Virasoro Lie conformal algebra over Rational Field
              To:   The universal enveloping vertex algebra of the Virasoro Lie conformal algebra over Rational Field
            sage: W = VirasoroVertexAlgebra(QQ,1/2)
            sage: L.lift
            Generic morphism:
              From: The Virasoro Lie conformal algebra over Rational Field
              To:   The Virasoro vertex algebra of central charge 1/2 over Rational Field
            sage: V.register_lift()
            sage: L.lift
            Generic morphism:
              From: The Virasoro Lie conformal algebra over Rational Field
              To:   The universal enveloping vertex algebra of the Virasoro Lie conformal algebra over Rational Field
        """
        f = None
        try:
            f = self._lca.lift
        except AttributeError:
            pass

        if f is not None and f.codomain() is self:
            return

        from sage.categories.homset import Hom
        from sage.algebras.lie_conformal_algebras.\
            lie_conformal_algebra_with_structure_coefs import _LiftMorphism
        newlift = _LiftMorphism(Hom(self._lca, self,
                        category = LieConformalAlgebras(self._lca.base_ring())))
        self._lca.set_lift(newlift)

    @cached_method
    def gens(self):
        """
        The generators of this vertex algebra.

        EXAMPLES::

            sage: V = NeveuSchwarzVertexAlgebra(QQ,1); V.gens()
            (L_-2|0>, G_-3/2|0>)
            sage: V = AffineVertexAlgebra(QQ,'A1', 1, names =('e','h', 'f')); V.gens()
            (e_-1|0>, h_-1|0>, f_-1|0>)
            sage: V = AffineVertexAlgebra(QQ,'A1', 1); V.gens()
            (E(alpha[1])_-1|0>, E(alphacheck[1])_-1|0>, E(-alpha[1])_-1|0>)
        """
        gens = []
        for i in range(self._ngens):
            l = [[]]*self._ngens
            l[i] = [1]
            gens.append(self(l))
        return tuple(gens)

    def ngens(self):
        """
        The number of generators of this vertex algebra.

        EXAMPLES::

            sage: V = AffineVertexAlgebra(QQ, 'B3', 1); V.ngens()
            21
            sage: V = N2VertexAlgebra(QQ,1); V.ngens()
            4
        """
        return self._ngens

    @cached_method
    def central_parameters(self):
        """
        The central character used to construct this universal
        enveloping vertex algebra.

        EXAMPLES::

            sage: V = FreeFermionsVertexAlgebra(QQ); V.central_parameters()
            Finite family {K: 1}
        """
        return self._central_parameters

    @cached_method
    def vacuum(self):
        """
        The vacuum vector of this vertex algebra.

        EXAMPLES::

            sage: VirasoroVertexAlgebra(QQ,1).vacuum()
            |0>
        """
        vac = [[],]*self.ngens()
        return self(vac)

    def ideal(self, *gens, check=True):
        """
        The ideal of this vertex algebra generated by ``gens``.

        INPUT:

        - ``gens`` -- a ``list`` or ``tuple`` of elements of this
          vertex algebra.

        - ``check`` -- a boolean (default: ``True``); whether to
          check that the generators are singular vectors.

        EXAMPLES:

        We construct the ideal defining the *Virasoro Ising* module::

            sage: V = VirasoroVertexAlgebra(QQ,1/2); V.register_lift()
            sage: L = V.0
            sage: v = L*(L*L) + 93/64*L.T()*L.T() - 33/16*L.T(2)*L - 9/128*L.T(4)
            sage: I = V.ideal(v)
            sage: I
            ideal of The Virasoro vertex algebra of central charge 1/2 over Rational Field generated by (L_-2L_-2L_-2|0> + 93/64*L_-3L_-3|0> - 33/8*L_-4L_-2|0> - 27/16*L_-6|0>,)

        If we instead use a non-singular vector::

            sage: V.ideal(L*L)
            Traceback (most recent call last):
            ...
            ValueError: Generators must be singular vectors of The Virasoro vertex algebra of central charge 1/2 over Rational Field

        NOTE::

            We only implement ideals of universal enveloping vertex
            algebras and their quotients, generated by singular
            vectors.
        """
        from .vertex_algebra_ideal import VertexAlgebraIdeal
        return VertexAlgebraIdeal(self, *gens, check=check)

    def quotient(self, I, names=None):
        """
        The quotient of this vertex algebra by the ideal ``I``.

        INPUT:

        - ``I`` -- a
          :class:`~sage.algebras.vertex_algebras.vertex_algebra_ideal.VertexAlgebraIdeal`
        - ``names`` a list of ``str`` or ``None`` (default: ``None``);
          alternative names for the generators


        EXAMPLES::

            sage: V = VirasoroVertexAlgebra(QQ,1/2)
            sage: L = V.0
            sage: v = L*(L*L) + 93/64*L.T()*L.T() - 33/16*L.T(2)*L - 9/128*L.T(4)
            sage: I = V.ideal(v)
            sage: Q = V.quotient(I); Q
            Quotient of The Virasoro vertex algebra of central charge 1/2 over Rational Field by the ideal generated by (L_-2L_-2L_-2|0> + 93/64*L_-3L_-3|0> - 33/8*L_-4L_-2|0> - 27/16*L_-6|0>,)
            sage: Q(L*(L*L))
            -93/64*L_-3L_-3|0> + 33/8*L_-4L_-2|0> + 27/16*L_-6|0>
        """
        from .vertex_algebra_quotient import VertexAlgebraQuotient
        return VertexAlgebraQuotient(I, category=self.category().Quotients(),
                                     names=names)

    def arc_algebra(self):
        r"""
        The arc algebra of this vertex algebra.

        The graded :mod:`PoissonVertexAlgebra\
        <sage.algebras.poisson_vertex_algebras.poisson_vertex_algebra>`
        freely generated as a differential algebra by the `C_2`
        quotient of this vertex algebra.

        .. TODO::

            We only support arc algebras of universal enveloping
            vertex algebras and their quotients.

        EXAMPLES::

            sage: V = VirasoroVertexAlgebra(QQ, 1/2); P = V.arc_algebra()
            sage: P.category()
            Category of finitely generated H-graded Poisson vertex algebras with basis over Rational Field
            sage: P is V.classical_limit()
            True
            sage: Q = V.quotient(V.ideal(V.find_singular(6)))
            sage: R = Q.arc_algebra(); R
            Quotient of The classical limit of The Virasoro vertex algebra of central charge 1/2 over Rational Field by the ideal generated by (L_2^3,)
            sage: R.cover_algebra() is P
            True
        """
        return self.classical_limit()
