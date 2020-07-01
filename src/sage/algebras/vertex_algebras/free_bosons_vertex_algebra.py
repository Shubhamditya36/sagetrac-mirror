r"""
Free Bosons Vertex Algebra

Let `R` be a commutative ring and `V` be a free `R`-module with a
non-degenerate symmetric pairing
`(\cdot,\cdot): V \otimes V \rightarrow R`. The *Free Bosons* vertex
algebra is generated by `V` with `\lambda`-brackets:

.. MATH::

    [v_\lambda w] = \lambda (v,w) |0\rangle, \qquad v,w \in V.

This is a conformal vertex algebra of central charge `\mathrm{dim} V`
where each generator has conformal weight `1`.

AUTHORS:

- Reimundo Heluani (2020-06-09): Initial implementation.
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

class FreeBosonsVertexAlgebra(UniversalEnvelopingVertexAlgebra):
    def __init__(self, R, ngens=None, gram_matrix=None, names=None,
                 index_set=None):
        r"""
        The Free Bosons vertex algebra.

        INPUT:

        - ``R`` -- a commutative ring; the base ring of this vertex
          algebra
        - ``ngens`` -- a positive Integer (default ``1``); the number of
          generators of this vertex algebra.
        - ``gram_matrix``: a symmetric square matrix with coefficients
          in ``R`` (default: ``identity_matrix(ngens)``); the Gram
          matrix of the inner product

        OUTPUT:

        The Free Bosons vertex algebra with generators
         `\alpha_i`, `i=1,...,n` and `\lambda`-brackets

         .. MATH::

            [{\alpha_i}_{\lambda} \alpha_j] = \lambda M_{ij} |0\rangle,

        where `n` is the number of generators ``ngens`` and `M` is
        the ``gram_matrix``. This vertex
        algebra is `H`-graded where every generator has conformal weight
        `1`.

        EXAMPLES:

        The normally ordered product is not associative::

            sage: V = FreeBosonsVertexAlgebra(QQ); V.inject_variables()
            Defining alpha
            sage: (alpha*alpha)*alpha - alpha*(alpha*alpha)
            2*alpha_-3|0>

        On the classical limit it is::

            sage: P = V.classical_limit()
            sage: a = P(alpha); a
            alpha_1
            sage: (a*a)*a
            alpha_1^3
            sage: (a*a)*a - a*(a*a)
            0

        With respect to the standard Virasoro vector, the generating
        vector is primary of conformal weight 1::

            sage: V.central_charge()
            1
            sage: L = alpha*alpha/2
            sage: L.bracket(alpha)
            {0: alpha_-2|0>, 1: alpha_-1|0>}

        We can use an explicit Gram Matrix::

            sage: V = FreeBosonsVertexAlgebra(QQ, gram_matrix=Matrix([[0,1],[1,0]]))
            sage: V
            The Free Bosons vertex algebra with generators (alpha0_-1|0>, alpha1_-1|0>) over Rational Field
            sage: V.inject_variables()
            Defining alpha0, alpha1
            sage: alpha0.bracket(alpha1)
            {1: |0>}
        """
        from sage.algebras.lie_conformal_algebras.\
                    free_bosons_lie_conformal_algebra import \
                     FreeBosonsLieConformalAlgebra

        ML = FreeBosonsLieConformalAlgebra(R,gram_matrix=gram_matrix,
                        ngens=ngens,names=names,index_set=index_set)

        cp = Family({ML.gen(-1):R.one()})

        super(FreeBosonsVertexAlgebra,self).__init__(R, ML,
                                                     central_parameters=cp)

        self._c = self._ngens

    def gram_matrix(self):
        """
        The Gramian of the inner product on the generators.

        EXAMPLES::

            sage: V = FreeBosonsVertexAlgebra(QQ, gram_matrix=Matrix([[0,1],[1,0]]))
            sage: V.gram_matrix()
            [0 1]
            [1 0]
        """
        return self._lca.gram_matrix()

    def _repr_(self):
        """
        The name of this vertex algebra.

        EXAMPLES::

            sage: FreeBosonsVertexAlgebra(QQbar)
            The Free Bosons vertex algebra with generators (alpha_-1|0>,) over Algebraic Field

        """
        return "The Free Bosons vertex algebra with generators {} over {}".\
                format(self.gens(),self.base_ring())





