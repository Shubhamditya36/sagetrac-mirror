r"""
Center of the Symmetric Group Algebra

This contains the following rings:

- :class:`FarahatHigmanAlgebra`:

  The Farahat-Higman algebra, a kind of inverse limit of all centers of
  symmetric group algebras. Isomorphic to the ring of symmetric functions over
  a polynomial ring in one variable, and to the partial class algebra.

- :class:`PartialClassAlgebra`:

  The partial class algebra, which can be seen as a different basis for the
  Farahat-Higman algebra.

AUTHORS:

- Mathieu Guay-Paquet, Travis Scrimshaw (2010-08-25): initial version
"""

#*****************************************************************************
#       Copyright (C) 2010 Mathieu Guay-Paquet <mathieu.guaypaquet@gmail.com>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#                  http://www.gnu.org/licenses/
#*****************************************************************************

from sage.misc.abstract_method import abstract_method
from sage.misc.cachefunc import cached_method
from sage.misc.bindable_class import BindableClass
from sage.misc.misc_c import prod
from sage.misc.all import srange
from sage.structure.all import UniqueRepresentation, Parent

from sage.categories.all import Rings, Fields, Hom, GradedAlgebrasWithBasis
from sage.categories.morphism import SetMorphism
from sage.categories.realizations import Realizations, Category_realization_of_parent
from sage.combinat.free_module import CombinatorialFreeModule
from sage.combinat.partition import Partition, Partitions
from sage.combinat.permutation import Permutations
from sage.combinat.sf.all import SymmetricFunctions
from sage.combinat.symmetric_group_algebra import SymmetricGroupAlgebra
from sage.combinat.symmetric_group_algebra_center import SymmetricGroupAlgebraCenter
from sage.rings.all import ZZ, QQ, Integer, PolynomialRing

class FarahatHigmanAlgebra(CombinatorialFreeModule):
    """
    Create the Farahat-Higman algebra over a given base ring.
    
    Given a permutation, its reduced cycle type is obtained from its cycle type
    by subtracting one from each cycle length (and discarding and resulting
    zeros).
    
    Given a symmetric group `S_n`, its conjugacy classes can be indexed by
    partitions corresponding to reduced cycle type instead of cycle type. Then,
    the same partition corresponds to conjugacy classes in all `S_n` for large
    enough `n`. When multiplying the corresponding elements of the centers of
    symmetric group algebras, the results depend polynomially on `n`, and this
    can be used to define a ring structure.
    
    The Farahat-Higman algebra with parameter `t` is the resulting ring. It
    specializes to the center of the group algebra of `S_n` if `t` is set to
    `n` and basis elements corresponding

    The Farahat-Higman algebra over a ring `R` with parameter `t` is isomorphic
    to the ring of symmetric functions over `R[t]` via the Jucys-Murphy
    isomorphism, and to the partial class algebra over `R` (see
    ``PartialClassAlgebra``) via their projections to the center of `R[S_n]`
    for `n \geq 0`.

    .. NOTE::

        Calling ``FarahatHigmanAlgebra(R, 't').base_ring()`` returns
        ``R['t']``, whereas :meth:`ground_field()` returns ``R``.
    
    INPUT:
    
    - ``ground_field`` -- the ground field for this algebra
    - ``name`` -- the name of the parameter to use

    EXAMPLES::

        sage: K = FarahatHigmanAlgebra(QQ, 't')
        sage: elt = K[1]
        sage: elt^1
        K[1]
        sage: elt^2
        (1/2*t^2-1/2*t)*K[] + 2*K[1, 1] + 3*K[2]
        sage: elt^3
        (3/2*t^2+1/2*t-6)*K[1] + 6*K[1, 1, 1] + 9*K[2, 1] + 16*K[3]
        sage: elt^4
        (3/4*t^4-1/2*t^3-13/4*t^2+3*t)*K[] + (6*t^2+10*t-32)*K[1, 1] + 24*K[1, 1, 1, 1]
         + (9*t^2+18*t-108)*K[2] + 36*K[2, 1, 1] + 54*K[2, 2] + 64*K[3, 1] + 125*K[4]
        sage: K[3] * K[1]
        4*K[1, 1] + (3*t-9)*K[2] + K[3, 1] + 5*K[4]

    We can go between the Farahat-Higman algebra an the partial
    class algebra::

        sage: A = PartialClassAlgebra(QQ)
        sage: k = K[2] * K[3]; k
        (2*t^2-10*t+12)*K[1] + 12*K[2, 1] + (4*t-12)*K[3] + K[3, 2] + 6*K[5]
        sage: a = A[3] * A[4]; a
        4*A[2, 1, 1] + 12*A[3, 2] + 4*A[4] + 4*A[4, 1] + A[4, 3] + 6*A[6]
        sage: K(a)
        (2*t^2-10*t+12)*K[1] + 12*K[2, 1] + (4*t-12)*K[3] + K[3, 2] + 6*K[5]
        sage: A(k)
        4*A[2, 1, 1] + 12*A[3, 2] + 4*A[4] + 4*A[4, 1] + A[4, 3] + 6*A[6]

    We can also convert between symmetric functions::

        sage: Sym = SymmetricFunctions(QQ['t'])
        sage: e = Sym.e()
        sage: m = Sym.m()
        sage: h = Sym.h()
        sage: K(e[4])
        K[1, 1, 1, 1] + K[2, 1, 1] + K[2, 2] + K[3, 1] + K[4]
        sage: K(m[4])
        (2/3*t^3-3/2*t^2+5/6*t)*K[] + 4*K[1, 1] + (3*t-4)*K[2] + K[4]
        sage: K(h[4])
        (1/8*t^4+7/12*t^3-17/8*t^2+17/12*t)*K[] + (1/2*t^2+7/2*t-2)*K[1, 1] + K[1, 1, 1, 1]
         + (t^2+8*t-23)*K[2] + 2*K[2, 1, 1] + 4*K[2, 2] + 5*K[3, 1] + 14*K[4]
        sage: e(K[4])
        (5/6*t^3-4*t^2+19/6*t)*e[] + (-3*t+8)*e[1, 1] + e[1, 1, 1, 1]
         + (6*t-20)*e[2] - 4*e[2, 1, 1] + 2*e[2, 2] + 4*e[3, 1] - 4*e[4]
        sage: m(K[4])
        (5/6*t^3-4*t^2+19/6*t)*m[] - 4*m[1, 1] + (-3*t+8)*m[2] + m[4]
        sage: h(K[4])
        (5/6*t^3-4*t^2+19/6*t)*h[] + (3*t-12)*h[1, 1] - h[1, 1, 1, 1] + (-6*t+20)*h[2]
         + 4*h[2, 1, 1] - 2*h[2, 2] - 4*h[3, 1] + 4*h[4]
        sage: h(K(A[5]))
        (5/6*t^3-4*t^2+19/6*t)*h[] + (3*t-12)*h[1, 1] - h[1, 1, 1, 1] + (-6*t+20)*h[2]
         + 4*h[2, 1, 1] - 2*h[2, 2] - 4*h[3, 1] + 4*h[4]
    """
    def __init__(self, ground_field, name):
        """
        Initialize ``self``.

        TESTS::

            sage: K = FarahatHigmanAlgebra(QQ, 't')
            sage: TestSuite(K).run()
        """
        if ground_field not in Fields():
            raise TypeError('ground_field must be a field')
        base = PolynomialRing(ground_field, [name])
        self._sym = SymmetricFunctions(base)
        CombinatorialFreeModule.__init__(self, base, Partitions(),
            prefix='K', bracket=False,
            # Graded algebras over R[t] are not considered to also be
            # graded algebras over R automatically, but this is needed
            # for the coercions to and from PartialClassAlgebra, so we
            # take the join of the two categories.
            category=(GradedAlgebrasWithBasis(base),
                GradedAlgebrasWithBasis(ground_field)))
    
    def __init_extra__(self):
        """
        Set up various coercions.

        Coercions are set up to and from ``SymmetricFunctions`` over
        ``self.base_ring()`` via the Jucys-Murphy isomorphism (evaluation of
        symmetric functions at Jucys-Murphy elements).

        Coercions are set up to and from ``PartialClassAlgebra`` over
        ``self.ground_field()``.

        TESTS::

            sage: K = FarahatHigmanAlgebra(QQ, 't')
            sage: elt = K[1]
            sage: A = PartialClassAlgebra(QQ)
            sage: A(elt)
            A[2]
            sage: e = SymmetricFunctions(QQ['t']).e()
            sage: K(e[1])
            K[1]
        """
        sym = self._sym
        e = sym.elementary()
        m = sym.monomial()
        
        # The coercion from symmetric functions in the elementary basis is the
        # easiest to define.
        e.module_morphism(codomain=self, on_basis=self._from_elementary
                          ).register_as_coercion()
        
        # The coercion from symmetric functions in the monomial basis is
        # currently defined by going through elementary functions. Unlike the
        # coercion from the elementary basis, it is upper unitriangular
        # so it is easy to invert. The inverse is used as a coercion to
        # symmetric functions.
        from_monomial = m.module_morphism(codomain=self,
            on_basis=self._from_monomial, triangular='upper',
            unitriangular=True, cmp=partition_lex_cmp)
        (~from_monomial).register_as_coercion()
        
        # The partial class algebra isomorphic to this ring is not over
        # self.base_ring(), which is a polynomial ring, but over
        # self.ground_field(), which is its ground field.
        ground = self.ground_field()
        category = GradedAlgebrasWithBasis(ground)
        A = PartialClassAlgebra(ground)

        SetMorphism(Hom(A, self, category), self._from_partial_class
                    ).register_as_coercion()
        
        SetMorphism(Hom(self, A, category), self._to_partial_class
                    ).register_as_coercion()

    @cached_method
    def _from_elementary(self, partition):
        """
        Coerce an elementary symmetric function to ``self``.

        For an integer `k`, the elementary symmetric function `e_k` evaluated
        at the Jucys-Murphy elements is the sum of all permutations of rank `k`.

        INPUT:

        - ``partition`` -- the index of an elementary symmetric function

        TESTS::

            sage: K = FarahatHigmanAlgebra(QQ, 't')
            sage: K._from_elementary(Partition([1]))
            K[1]
            sage: K._from_elementary(Partition([2,1,1]))
            (1/4*t^4-1/2*t^3-1/4*t^2+1/2*t)*K[] + (5/2*t^2+3/2*t-12)*K[1, 1] + 12*K[1, 1, 1, 1]
             + (7/2*t^2+5/2*t-33)*K[2] + 17*K[2, 1, 1] + 24*K[2, 2] + 28*K[3, 1] + 50*K[4]
            sage: K._from_elementary(Partition([]))
            K[]
        """
        return self.prod(self.sum_of_monomials(Partitions(k)) for k in reversed(partition))

    @cached_method
    def _from_monomial(self, partition):
        """
        Coerce a monomial symmetric function to ``self``.

        This is done by using whatever other coercion is currently registered
        from symmetric functions to ``self``. It is intended to help define
        the inverse coercion.

        .. NOTE::

            This should not be used to define a coercion from
            symmetric functions to ``self``.
        
        INPUT:

        - ``partition`` -- the index of a monomial symmetric function

        TESTS::

            sage: K = FarahatHigmanAlgebra(QQ, 't')
            sage: K._from_monomial(Partition([1]))
            K[1]
            sage: K._from_monomial(Partition([2,1,1]))
            (1/2*t^2-1/2*t-2)*K[1, 1] + (1/2*t^2-1/2*t-3)*K[2] + K[2, 1, 1] + 2*K[2, 2] + 3*K[3, 1] + 6*K[4]
            sage: K._from_monomial(Partition([]))
            K[]
        """
        return self.coerce(self._sym.m().monomial(partition))

    @cached_method
    def _from_partial_class(self, element):
        """
        Coerce a partial class algebra element to ``self``.
        
        The partial permutation conjugacy class for a given cycle type maps to
        the basis element of ``self`` for the corresponding reduced cycle type,
        scaled by a binomial coefficient involving the parameter of
        ``self.base_ring()``. The degree of the scaling factor, as a polynomial
        in the parameter, is the number of ones in the original cycle type.
        
        Note that this is linear over the ground field, but not the base ring.
        
        INPUT:

        - ``element`` -- an element of
          ``PartialClassAlgebra(self.ground_field())``

        TESTS::

            sage: K = FarahatHigmanAlgebra(QQ, 't')
            sage: A = PartialClassAlgebra(QQ)
            sage: K._from_partial_class(A[1])
            t*K[]
            sage: K._from_partial_class(A[2,1,1])
            (1/2*t^2-5/2*t+3)*K[1]
            sage: K._from_partial_class(A[2] + 3*A[3,1])
            K[1] + (3*t-9)*K[2]
            sage: K._from_partial_class(A.one())
            K[]
        """
        base_ring = self.base_ring()
        parameter = base_ring.gen()
        result = self.zero()
        for (partition, coeff) in element:
            exp = partition.to_exp(1)
            ones = Integer(exp[0])
            deflated = Partition(exp=exp[1:])
            support = deflated.size() + deflated.length()
            result += self.term(
                deflated,
                coeff * prod([(parameter - support - i) / (ones - i) for i in srange(ones)], base_ring.one()))
                # The prod here is a workaround for a bug elsewhere.
                # It's just a binomial coefficient, but the usual binomial
                # coefficient function returns a polynomial in the wrong ring,
                # and there is an error in the coercion to the right ring.
        return result

    @cached_method
    def _to_partial_class(self, element):
        """
        Coerce an element of ``self`` to the partial class algebra.
        
        This implements the inverse of :meth:`_from_partial_class` by
        evaluating iterated forward differences of polynomials in the
        parameter of ``self.base_ring()``.
        
        Note that this is linear over the ground field, but not the base ring.
        
        INPUT:
        
        - ``element`` -- an element of ``self``
        
        OUTPUT:
        
        The corresponding element of
        ``PartialClassAlgebra(self.base_ring().base_ring())``.
        
        TESTS::

            sage: R.<t> = QQ[]
            sage: K = FarahatHigmanAlgebra(QQ, 't')
            sage: A = PartialClassAlgebra(QQ)
            sage: K._to_partial_class(K[1])
            A[2]
            sage: K._to_partial_class(K[2,1,1])
            A[3, 2, 2]
            sage: K._to_partial_class(K[2] + 3*t*K[3,1])
            A[3] + 18*A[4, 2] + 3*A[4, 2, 1]
            sage: K._to_partial_class(K.one())
            A[]
        """
        base_ring = self.base_ring()
        parameter = base_ring.gen()
        ground = base_ring.base_ring()
        A = PartialClassAlgebra(ground)
        result = A.zero()
        for (partition, coeff) in element:
            inflated = inflate_partition(partition)
            support = inflated.size()
            while coeff:
                result += A.term(inflated, coeff(support))
                inflated = Partition(inflated + [1])
                coeff = coeff(parameter + 1) - coeff
        return result
    
    def _repr_(self):
        """
        Return a string representation of ``self``.
        
        TESTS::

            sage: FarahatHigmanAlgebra(QQ, 't')
            Farahat-Higman algebra with parameter t over Rational Field
        """
        base = self.base_ring()
        return "Farahat-Higman algebra with parameter %s over %s" % (base.gen(), base.base_ring())

    def __getitem__(self, i):
        """
        Return the basis element indexed by ``i``.

        INPUT:

        - ``i`` -- a partition

        EXAMPLES::

            sage: K = FarahatHigmanAlgebra(QQ, 't')
            sage: K[5]
            K[5]
            sage: K[4,2,1]
            K[4, 2, 1]
            sage: K[[]]
            K[]
        """
        if i in ZZ:
            i = [i]
        return self.monomial(Partition(i))

    def ground_field(self):
        """
        Return the ground field of ``self``.

        EXAMPLES::

            sage: K = FarahatHigmanAlgebra(QQ, 't')
            sage: K.ground_field()
            Rational Field
        """
        return self.base_ring().base_ring()

    def one_basis(self):
        """
        Return the monomial index of the identity element.
        
        TESTS::

            sage: K = FarahatHigmanAlgebra(QQ, 't')
            sage: K.one_basis()
            []
            sage: K.one_basis().parent()
            Partitions
        """
        return Partition([])
    
    @cached_method
    def product_on_basis(self, left, right):
        """
        Compute the product of two basis elements of the ring.
        
        This is done by computing the product of the corresponding conjugacy
        classes in enough centers of symmetric group algebras that the
        polynomial coefficients for the product in ``self`` can be obtained
        by polynomial interpolation.
        
        Note that the computation is done in the symmetric group algebras over
        ``QQ`` regardless of ``self.base_ring()``, since it relies on the
        characteristic of the ground field being zero. It's possible to remove
        this dependence by including all coefficients of all possible conjugacy
        classes in the polynomial interpolations, even when they are zero, in
        which case the result would be correct in positive characteristic.
        (Zero coefficients are currently (correctly) discarded.)
        
        INPUT:
        
        - ``left`` -- a partition indexing a basis element of the ring
        - ``right`` -- a partition indexing a basis element of the ring
        
        OUTPUT:
        
        The product, which is a ring element.
        
        EXAMPLES::

            sage: K = FarahatHigmanAlgebra(QQ, 't')
            sage: K.product_on_basis(Partition([3]), Partition([1]))
            4*K[1, 1] + (3*t-9)*K[2] + K[3, 1] + 5*K[4]
        """
        # Figure which symmetric group algebras to compute in.
        sizes = [p.size() + p.length() for p in [left, right]]
        low = max(sizes)
        high = sum(sizes)
        
        # Define representatives for the two factors in the
        # relevant symmetric group algebras.
        C = SymmetricGroupAlgebraCenter(QQ).C()
        left_low = inflate_partition(left, low)
        left_rep = C.sum_of_monomials(Partition(left_low + [1] * i)
                                      for i in range(high - low + 1))
        right_low = inflate_partition(right, low)
        right_rep = C.sum_of_monomials(Partition(right_low + [1] * i)
                                       for i in range(high - low + 1))
        
        # Collect coefficients from the products.
        points = {}
        for (p, c) in left_rep * right_rep:
            points.setdefault(deflate_partition(p), []).append([p.size(), c])
        
        # Do the polynomial interpolation and return the result.
        R = self.base_ring()
        return self.sum_of_terms((partition, R.lagrange_polynomial(point_list))
                                 for (partition, point_list) in points.iteritems())


class PartialClassAlgebra(CombinatorialFreeModule):
    """
    Create the partial class algebra over a given base ring.
    
    A partial permutation is a permutation of the positive integers, together
    with a finite support set, outside of which it acts as the identity. Its
    support set may include fixed points. Partial permutations are multiplied
    by composing their underlying permutations, and taking the union of their
    support sets as the support set of the product.
    
    The cycle type of a partial permutation is the cycle type of the
    underlying permutation restricted to the support set.
    
    The partial class algebra has a basis indexed by all partitions, where the
    basis element indexed by a partition corresponds to the formal sum of all
    partial permutations with this cycle type.
    
    This algebra is isomorphic to the Farahat-Higman algebra.
    See ``FarahatHigmanAlgebra``.
    
    INPUT:
    
    - ``base_ring`` -- the base ring for this algebra; currently, this must
      be a field

    EXAMPLES::

        sage: A = PartialClassAlgebra(QQ)
        sage: elt = A([2])
        sage: elt^1
        A[2]
        sage: elt^2
        A[1, 1] + 2*A[2, 2] + 3*A[3]
        sage: elt^3
        A[2] + 8*A[2, 1] + 3*A[2, 1, 1] + 6*A[2, 2, 2] + 9*A[3, 2] + 16*A[4]
        sage: elt^4
        A[1, 1] + 24*A[1, 1, 1] + 18*A[1, 1, 1, 1] + 104*A[2, 2] + 64*A[2, 2, 1]
         + 12*A[2, 2, 1, 1] + 24*A[2, 2, 2, 2] + 27*A[3] + 81*A[3, 1] + 18*A[3, 1, 1]
         + 36*A[3, 2, 2] + 54*A[3, 3] + 64*A[4, 2] + 125*A[5]
        sage: A[4] * A[2]
        4*A[2, 2] + 3*A[3, 1] + A[4, 2] + 5*A[5]

    We can also convert between symmetric functions::

        sage: Sym = SymmetricFunctions(QQ['t'])
        sage: e = Sym.e()
        sage: m = Sym.m()
        sage: h = Sym.h()
        sage: A(e[4])
        A[2, 2, 2, 2] + A[3, 2, 2] + A[3, 3] + A[4, 2] + A[5]
        sage: A(m[4])
        A[1, 1] + 4*A[1, 1, 1] + 4*A[2, 2] + 5*A[3] + 3*A[3, 1] + A[5]
        sage: A(h[4])
        A[1, 1] + 8*A[1, 1, 1] + 3*A[1, 1, 1, 1] + 20*A[2, 2] + 8*A[2, 2, 1]
         + A[2, 2, 1, 1] + A[2, 2, 2, 2] + 10*A[3] + 15*A[3, 1] + 2*A[3, 1, 1]
         + 2*A[3, 2, 2] + 4*A[3, 3] + 5*A[4, 2] + 14*A[5]
        sage: e(A[5])
        (5/6*t^3-4*t^2+19/6*t)*e[] + (-3*t+8)*e[1, 1] + e[1, 1, 1, 1] + (6*t-20)*e[2] - 4*e[2, 1, 1] + 2*e[2, 2] + 4*e[3, 1] - 4*e[4]
        sage: m(A[5])
        (5/6*t^3-4*t^2+19/6*t)*m[] - 4*m[1, 1] + (-3*t+8)*m[2] + m[4]
        sage: h(A[5]) # Coercion problem? needs to be checked !
        (5/6*t^3-4*t^2+19/6*t)*h[] + (3*t-12)*h[1, 1] - h[1, 1, 1, 1] + (-6*t+20)*h[2] + 4*h[2, 1, 1] - 2*h[2, 2] - 4*h[3, 1] + 4*h[4]
    """
    def __init__(self, base_ring):
        """
        Initialize ``self``.
        
        TESTS::

            sage: A = PartialClassAlgebra(QQ)
            sage: TestSuite(A).run()
        """
        if base_ring not in Fields():
            raise TypeError('base_ring must be a field.')
        CombinatorialFreeModule.__init__(self, base_ring, Partitions(),
            prefix='A', bracket=False, category=GradedAlgebrasWithBasis(base_ring))

    def _repr_(self):
        """
        Return a print representation of ``self``.

        TESTS::

            sage: PartialClassAlgebra(QQ)
            Partial class algebra over Rational Field
        """
        return "Partial class algebra over %s" % self.base_ring()

    def __getitem__(self, i):
        """
        Return the basis element indexed by ``i``.

        INPUT:

        - ``i`` -- a partition

        EXAMPLES::

            sage: A = PartialClassAlgebra(QQ)
            sage: A[5]
            A[5]
            sage: A[4,2,1]
            A[4, 2, 1]
            sage: A[[]]
            A[]
        """
        if i in ZZ:
            i = [i]
        return self.monomial(Partition(i))
    
    @cached_method
    def one_basis(self):
        """
        Return the monomial index of the identity element.

        TESTS::

            sage: A = PartialClassAlgebra(QQ)
            sage: A.one_basis()
            []
            sage: A.one_basis().parent()
            Partitions
        """
        return Partition([])
    
    def product(self, left, right):
        """
        Compute the product of two elements of the ring.
        
        This is done by coercing the elements to the Farahat-Higman algebra,
        computing the product there, and coercing the result back.
        
        INPUT:
        
        - ``left`` -- an element of the ring
        - ``right`` -- an element of the ring
        
        OUTPUT:
        
        The product of the two elements.
        
        EXAMPLES::

            sage: A = PartialClassAlgebra(QQ)
            sage: A.product(A[3], A[1,1])
            3*A[3] + 3*A[3, 1] + A[3, 1, 1]
        """
        K = FarahatHigmanAlgebra(self.base_ring(), 't')
        return self(K(left) * K(right))


###########################################################
## Helper functions

def deflate_partition(partition):
    """
    Reduce each part of ``partition`` by one.

    INPUT:

    - ``partition`` -- a partition

    OUTPUT:

    A new partition obtained by reducing each part of ``partition`` by one.
    Any resulting zero parts are discarded.

    EXAMPLES::

        sage: from sage.combinat.farahat_higman import deflate_partition
        sage: deflate_partition(Partition([5, 3, 3, 2, 1, 1, 1]))
        [4, 2, 2, 1]
    """
    return Partition(exp=partition.to_exp()[1:])


def inflate_partition(partition, size=None):
    """
    Increase each part of ``partition`` by one.
    
    INPUT:
    
    - ``partition`` -- a partition
    - ``size`` -- (default: ``None``) the size of the resulting partition;
      if ``size`` is ``None``, use the minimum possible size
    
    OUTPUT:
    
    A new partition obtained by increasing each part of ``partition`` by one.
    If ``size`` is not ``None``, the result is padded out with parts of size
    one so that the resulting partition has the specified size. Raises
    ``ValueError`` if ``size`` is too small.
    
    EXAMPLES::
        
        sage: from sage.combinat.farahat_higman import inflate_partition
        sage: inflate_partition(Partition([4, 2, 2, 1]))
        [5, 3, 3, 2]
        sage: inflate_partition(Partition([4, 2, 2, 1]), 16)
        [5, 3, 3, 2, 1, 1, 1]
        sage: inflate_partition(Partition([4, 2, 2, 1]), 10)
        Traceback (most recent call last):
        ...
        ValueError: size is too small.
    """
    if size is None:
        extra_ones = 0
    else:
        extra_ones = size - partition.size() - partition.length()
        if extra_ones < 0:
            raise ValueError('size is too small.')
    return Partition(exp=[extra_ones] + partition.to_exp())


def partition_lex_cmp(left, right):
    """
    Compare two partitions by size, then lexicographically.
    
    INPUT:
    
    - ``left`` -- a partition
    - ``right`` -- a partition
    
    OUTPUT:
    
    Return `-1, 0, 1` according to whether ``left`` is less than, equal to, or
    greater than (respectively) to ``right``.
    
    EXAMPLES::
        
        sage: from sage.combinat.farahat_higman import partition_lex_cmp
        sage: a = Partition([3, 2])
        sage: b = Partition([6])
        sage: c = Partition([4, 1, 1])
        sage: d = Partition([1, 1, 1, 1, 1, 1])
        sage: partition_lex_cmp(a, b)
        -1
        sage: partition_lex_cmp(c, b)
        1
        sage: partition_lex_cmp(c, d)
        -1
        sage: partition_lex_cmp(c, c)
        0
        sage: all(partition_lex_cmp(b, p) <= 0 for p in Partitions(6))
        True
        sage: all(partition_lex_cmp(d, p) >= 0 for p in Partitions(6))
        True
    """
    return cmp(left.size(), right.size()) or cmp(right, left)

