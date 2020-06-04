"""
Free Bosons Lie Conformal Algebra.

AUTHORS:

- Reimundo Heluani (08-09-2019): Initial implementation.
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

from sage.matrix.special import identity_matrix
from .graded_lie_conformal_algebra import GradedLieConformalAlgebra
from sage.structure.indexed_generators import standardize_names_index_set

class FreeBosonsLieConformalAlgebra(GradedLieConformalAlgebra):
    def __init__(self,R,gram_matrix=None,ngens=None,names=None,
                 index_set=None):
        r"""
        The Free Bosons Lie conformal algebra.

        INPUT:

        - ``R``: a commutative ring.
        - ``gram_matrix``: a matrix (default: ``[1]``); a symmetric
          square matrix with coefficients in ``R``.
        - ``ngens``: a positive Integer (default ``1``); the number of
          non-central generators of this Lie conformal algebra.

        OUTPUT:

        The Free Bosons Lie conformal algebra with generators
         `\alpha_i`, `i=1,...,n` and `\lambda`-brackets

         .. MATH::

            [{\alpha_i}_{\lambda} \alpha_j] = \lambda M_{ij} K,

        where `n` is the number of generators ``ngens`` and `M` is
        the ``gram_matrix``. This Lie conformal
        algebra is `H`-graded where every generator has conformal weight
        `1`.

        EXAMPLES::

            sage: R = FreeBosonsLieConformalAlgebra(AA); R
            The free Bosons Lie conformal algebra with generators (alpha, K) over Algebraic Real Field.
            sage: R.inject_variables()
            Defining alpha, K
            sage: alpha.bracket(alpha)
            {1: K}
            sage: M = identity_matrix(QQ,2); R = FreeBosonsLieConformalAlgebra(QQ,gram_matrix=M, names='alpha,beta'); R
            The free Bosons Lie conformal algebra with generators (alpha, beta, K) over Rational Field.
            sage: R.inject_variables(); alpha.bracket(beta)
            Defining alpha, beta, K
            {}
            sage: alpha.bracket(alpha)
            {1: K}
            sage: R = FreeBosonsLieConformalAlgebra(QQbar, ngens=3); R
            The free Bosons Lie conformal algebra with generators (alpha0, alpha1, alpha2, K) over Algebraic Field.

        TESTS::
            sage: R = FreeBosonsLieConformalAlgebra(QQ); R.0.degree()
            1
            sage: R = FreeBosonsLieConformalAlgebra(QQbar, ngens=2, gram_matrix=identity_matrix(QQ,1,1))
            Traceback (most recent call last):
            ...
            ValueError: The gram_matrix should be a symmetric 2 x 2 matrix, got [1]
            sage: R = FreeBosonsLieConformalAlgebra(QQbar, ngens=2, gram_matrix=Matrix(QQ,[[0,1],[-1,0]]))
            Traceback (most recent call last):
            ...
            ValueError: The gram_matrix should be a symmetric 2 x 2 matrix, got [ 0  1]
            [-1  0]
        """
        from sage.matrix.matrix_space import MatrixSpace
        if (gram_matrix is not None):
            if ngens is None:
                ngens = gram_matrix.dimensions()[0]
            try:
                assert (gram_matrix in MatrixSpace(R,ngens,ngens))
            except AssertionError:
                raise ValueError("The gram_matrix should be a symmetric " +
                    "{0} x {0} matrix, got {1}".format(ngens,gram_matrix))
            if not gram_matrix.is_symmetric():
                raise ValueError("The gram_matrix should be a symmetric " +
                    "{0} x {0} matrix, got {1}".format(ngens,gram_matrix))
        else:
            if ngens is None:
                ngens = 1;
            gram_matrix = identity_matrix(R,ngens,ngens)

        if (names is None) and (index_set is None):
            names = 'alpha'
            self._latex_names = tuple(r'\alpha_{%d}' % i \
                                      for i in range (ngens)) + ('K',)
        names,index_set = standardize_names_index_set(names=names,
                                                      index_set=index_set,
                                                      ngens=ngens)
        bosondict = { (i,j): {1: {('K',0): gram_matrix[index_set.rank(i),
                    index_set.rank(j)]}} for i in index_set for j in index_set}

        GradedLieConformalAlgebra.__init__(self,R,bosondict,names=names,
                                           index_set=index_set,
                                           central_elements=('K',))

        self._gram_matrix = gram_matrix

    def _repr_(self):
        return "The free Bosons Lie conformal algebra with generators {}"\
                " over {}.".format(self.gens(),self.base_ring())

    def gram_matrix(self):
        r"""
        The Gram matrix that specifies the `\lambda`-brackets of the
        generators.

        EXAMPLES::

            sage: R = FreeBosonsLieConformalAlgebra(QQ,ngens=2);
            sage: R.gram_matrix()
            [1 0]
            [0 1]
        """
        return self._gram_matrix
