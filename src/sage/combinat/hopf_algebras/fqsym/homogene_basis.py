# -*- coding: utf-8 -*-
r"""
The homogeneous basis of FQSym Hopf algebra.

H-basis of FQSym
"""
#*****************************************************************************
#       Copyright (C) 2013 Jean-Baptiste Priez <jbp@kerios.fr>.
#
#  Distributed under the terms of the GNU General Public License (GPL)
#
#                  http://www.gnu.org/licenses/
#*****************************************************************************
from sage.combinat.hopf_algebras.fqsym import FreeQuasiSymmetricFunctions
from sage.combinat.hopf_algebras import register_as_realization


class Homogene(FreeQuasiSymmetricFunctions.Bases.Base):
    '''
    This multiplicative basis is called the homogene basis of
    FQSym, denoted: `(\mathcal{H}_\sigma)`.

    EXAMPLES::

        sage: H = FQSym(QQ).H(); H
        The combinatorial Hopf algebra of Free Quasi-Symmetric Functions over the Rational Field on the Homogene basis

    An element `\mathcal H_\sigma` is defined as the sum of all
    element in the fundamental basis generated by the permutations
    `\mu` such that `\mu` is greater than `\sigma`
    for weak order. (greater in the right permutohedron)

    .. MATH::

        \mathcal H_\sigma = \sum_{\mu \preceq \sigma} \mathbb F_\mu

    EXAMPLES::

        sage: F = FQSym(QQ).F()
        sage: F(H[2,1,4,3])
        F[1, 2, 3, 4] + F[1, 2, 4, 3] + F[2, 1, 3, 4] + F[2, 1, 4, 3]

    (See [NCSF-VII]_.)

     TESTS::

        sage: H = FQSym(QQ).H(); H
        The combinatorial Hopf algebra of Free Quasi-Symmetric Functions over the Rational Field on the Homogene basis
        sage: TestSuite(H).run()
    '''
    _prefix = "H"

    def dual_basis(self):
        return self.realization_of().m()

    def product_on_basis(self, e1, e2):
        '''
        TESTS::

            sage: H = FQSym(QQ).H()
            sage: H[2,1,3,4] * H[1,2]
            H[5, 6, 2, 1, 3, 4]
            sage: H[1,2] * H[2,1]
            H[4, 3, 1, 2]
        '''
        if len(e1) == 0:
            return self.monomial(e2)
        return self.monomial(
            self.basis().keys()([i + max(e1) for i in e2] + list(e1)))

    def build_morphisms(self):
        '''
        TESTS::

            sage: FQS = FQSym(ZZ); F = FQS.F(); H = FQS.H()
            sage: F(H[3,2,1])
            F[1, 2, 3] + F[1, 3, 2] + F[2, 1, 3] + F[2, 3, 1] + F[3, 1, 2] + F[3, 2, 1]
            sage: F(H[1,2,3])
            F[1, 2, 3]
        '''
        morph = lambda F, T, func, tri = None, comp = None: (
            F._module_morphism(func, codomain=T, triangular=tri, cmp=comp)
            if comp is not None else
            F._module_morphism(func, codomain=T, triangular=tri))

        F = self.realization_of().F()
        H = self

        # H <-> F
        H_to_F = morph(H, F,
            lambda sigma: F.sum_of_monomials(sigma.permutohedron_smaller()),
            tri="upper")
        H_to_F.register_as_coercion()
        (~H_to_F).register_as_coercion()

register_as_realization(FreeQuasiSymmetricFunctions, Homogene, "H")