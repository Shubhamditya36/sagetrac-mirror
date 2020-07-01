r"""
Affine Vertex Algebra

Given a simple finite dimensional Lie algebra `\mathfrak{g}` over a
commutative ring `R` and an element `k \in R`, the *universal affine
vertex algebra of level* `k` is the vertex algebra generated by
`\mathfrak{g}` with `\lambda`-brackets:

.. MATH::

    [a_\lambda b] = [a,b] + \lambda (a,b) k |0\rangle, \qquad a,b \in
    \mathfrak{g},

where `(\cdot,\cdot) : \mathfrak{g} \otimes_R \mathfrak{g} \rightarrow
R` is the invariant, non-degenerate, bilinear form on `\mathfrak{g}`
normalized so that the highest root has square-norm `2`.

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

from .universal_enveloping_vertex_algebra import \
                                                UniversalEnvelopingVertexAlgebra
from sage.sets.family import Family

class AffineVertexAlgebra(UniversalEnvelopingVertexAlgebra):
    r"""
    The universal affine vertex algebra.

    INPUT:

    - ``R`` -- a commutative ring; the base ring of this vertex
      algebra.
    - ``ct`` -- a ``str`` or a
      :mod:`CartanType<sage.combinat.root_system.cartan_type>`;
      the cartan type of the corresponding finite dimensional Lie
      algebra `\mathfrak{g}`
    - ``k`` -- an element of ``R``; the level
    - ``names`` -- a list of ``str`` or ``None`` (default:
      ``None``); alternative names for the generators of this
      vertex algebra

    EXAMPLES:

    We construct the universal affine vertex algebra of
    `\mathfrak{sl}_2` at level `1`::

        sage: V = vertex_algebras.Affine(QQ, 'A1', 1, names=('e','h','f')); V
        The universal affine vertex algebra of CartanType ['A', 1] at level 1 over Rational Field
        sage: V.central_charge()
        1
        sage: V.inject_variables()
        Defining e, h, f

    We check that the Sugawara construction gives a Virasoro
    vector of central charge `1`::

        sage: L = (e*f + h*h/2 + f*e)/6
        sage: L.bracket(L) == {0: L.T(), 1: 2*L, 3: 1/2*V.vacuum()}
        True

    We find all singular vectors of conformal weight `2` and
    construct the irreducible quotient::

        sage: sing = V.find_singular(2); sing
        (e_-1e_-1|0>,
         e_-1h_-1|0> + e_-2|0>,
         h_-1h_-1|0> - 2*e_-1f_-1|0> + h_-2|0>,
         h_-1f_-1|0> + f_-2|0>,
         f_-1f_-1|0>)
        sage: I = V.ideal(sing); I
        ideal of The universal affine vertex algebra of CartanType ['A', 1] at level 1 over Rational Field generated by (e_-1e_-1|0>, e_-1h_-1|0> + e_-2|0>, h_-1h_-1|0> - 2*e_-1f_-1|0> + h_-2|0>, h_-1f_-1|0> + f_-2|0>, f_-1f_-1|0>)
        sage: Q = V.quotient(I)
        sage: Q.hilbert_series(4)           # long time (2 seconds)
        1 + 3*q + 4*q^2 + 7*q^3 + O(q^4)
        sage: Q.find_singular(2)            # long time (1 second)
        ()

    TESTS::

        sage: V = vertex_algebras.Affine(QQ, CartanType('A1'),1); V
        The universal affine vertex algebra of CartanType ['A', 1] at level 1 over Rational Field
    """
    def __init__(self, R, ct, k, names=None):
        """
        Initialize self.

        TESTS::

            sage: V = vertex_algebras.Affine(QQ,'A1',1)
            sage: TestSuite(V).run()
        """
        from sage.algebras.lie_conformal_algebras.affine_lie_conformal_algebra\
                    import AffineLieConformalAlgebra
        if names is not None:
            prefix = ''
            bracket = ''
        else:
            prefix = 'E'
            bracket = '('
        ML = AffineLieConformalAlgebra(R, ct, names=names, prefix=prefix,
                                       bracket=bracket)
        cp = Family({ML.central_elements()[0]: k})
        super(AffineVertexAlgebra,self).__init__(R, ML, central_parameters=cp)

        self._level = k
        self._ct = self._lca.cartan_type()
        if not self.is_critical():
           self._c = k*self._ngens/(k+self._ct.dual_coxeter_number())

    def level(self):
        r"""
        The level of this affine vertex algebra.

        EXAMPLES::

            sage: V = vertex_algebras.Affine(QQ, 'B3', 1); V
            The universal affine vertex algebra of CartanType ['B', 3] at level 1 over Rational Field
            sage: V.level()
            1
        """
        return self._level

    def cartan_type(self):
        """
        The Cartan Type of this affine vertex algebra.

        EXAMPLES::

            sage: V = vertex_algebras.Affine(QQ, 'B3', 1); V
            The universal affine vertex algebra of CartanType ['B', 3] at level 1 over Rational Field
            sage: V.cartan_type()
            ['B', 3]
        """
        return self._ct

    def is_critical(self):
        """
        Whether the level is critical.

        The level is critical if it equals the negative of the dual
        Coxeter number of its Cartan Type.

        EXAMPLES::

            sage: V = vertex_algebras.Affine(QQ, 'A1', -2); V
            The universal affine vertex algebra of CartanType ['A', 1] at critical level over Rational Field
            sage: V.is_critical()
            True
        """
        return self.level() == -self.cartan_type().dual_coxeter_number()

    def _repr_(self):
        """
        The name of this vertex algebra.

        EXAMPLES::
            sage: V = vertex_algebras.Affine(QQ, 'A1', -2); V
            The universal affine vertex algebra of CartanType ['A', 1] at critical level over Rational Field
            sage: V = vertex_algebras.Affine(QQbar, 'A1', 1, names=('e','h','f')); V
            The universal affine vertex algebra of CartanType ['A', 1] at level 1 over Algebraic Field
        """
        if self.is_critical():
            return "The universal affine vertex algebra of CartanType {} at"\
                   " critical level over {}".format(self.cartan_type(),
                   self.base_ring())
        else:
            return "The universal affine vertex algebra of CartanType {} at "\
                   "level {} over {}".format(self.cartan_type(),
                                             self.level(), self.base_ring())