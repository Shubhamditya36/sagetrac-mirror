r"""
Vertex algebras
AUTHORS

- Reimundo Heluani (10-09-2019): Initial implementation

.. include:: ../../../algebras/vertex_algebras/vertex_algebra_desc.rst
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

from sage.categories.category_types import Category_over_base_ring
from sage.categories.category_with_axiom import CategoryWithAxiom_over_base_ring
from sage.misc.abstract_method import abstract_method
from sage.categories.category_with_axiom import all_axioms as all_axioms
from sage.categories.quotients import QuotientsCategory
from lie_conformal_algebras import LieConformalAlgebras
from sage.algebras.vertex_algebras.vertex_algebra_quotient import VertexAlgebraQuotient
from sage.functions.other import factorial

all_axioms += ("FinitelyGeneratedAsVertexAlgebra","HGraded")
class VertexAlgebras(Category_over_base_ring):
    """
    The category of vertex algebras.
    
    EXAMPLES::

        sage: VertexAlgebras(QQ)
        Category of Vertex algebras over Rational Field
        sage: VertexAlgebras(QQ).is_subcategory(LieConformalAlgebras(QQ))
        True

    """

    def super_categories(self):
        """
        The super categories of this category

        EXAMPLES::

            sage: C = VertexAlgebras(QQ)
            sage: C.super_categories()
            [Category of Lie conformal algebras over Rational Field]

        """
        return [LieConformalAlgebras(self.base_ring()),]

    def _repr_object_names(self):
        """
        The name of the objects of this category
        """
        return "Vertex algebras over {}".format(self.base_ring())

    class Quotients(QuotientsCategory):
        """
        The category of quotients of vertex algebras
        """
        pass

    class ParentMethods:
        def ideal(self, *gens):
            """
            The ideal of this vertex algebra generated by ``gens``

            INPUT: 

            - ``gens`` -- a list or tuple of elements of this vertex algebra.
              They must be singular vectors. 

            EXAMPLES:

            We construct the ideal defining the *Virasoro Ising* module::

                sage: V = VirasoroVertexAlgebra(QQ,1/2) 
                sage: L = V.0
                sage: v = L*(L*L) + 93/64*L.T()*L.T() - 33/16*L.T(2)*L - 9/128*L.T(4)
                sage: I = V.ideal(v)
                sage: I
                ideal of The Virasoro vertex algebra at central charge 1/2 generated by (L_-2L_-2L_-2|0>-27/16*L_-6|0>+93/64*L_-3L_-3|0>-33/8*L_-4L_-2|0>,)

            If we instead use a non-singular vector::

                sage: V.ideal(L*L)
                Traceback (most recent call last):
                ...
                ValueError: Generators must be singular vectors of The Virasoro vertex algebra at central charge 1/2

            """
            from sage.algebras.vertex_algebras.vertex_algebra_ideal import VertexAlgebraIdeal
            return VertexAlgebraIdeal(self,gens)

        def quotient(self, I):
            """ 
            The quotient of this vertex algebra by the ideal ``I``

            EXAMPLES::

                sage: V = VirasoroVertexAlgebra(QQ,1/2)
                sage: L = V.0
                sage: v = L*(L*L) + 93/64*L.T()*L.T() - 33/16*L.T(2)*L - 9/128*L.T(4)
                sage: I = V.ideal(v)
                sage: Q = V.quotient(I); Q
                Quotient of The Virasoro vertex algebra at central charge 1/2 by the ideal generated by (L_-2L_-2L_-2|0>-27/16*L_-6|0>+93/64*L_-3L_-3|0>-33/8*L_-4L_-2|0>,)
                sage: Q(L*(L*L))
                33/8*L_-4L_-2|0>+27/16*L_-6|0>-93/64*L_-3L_-3|0>
            
            """
            return VertexAlgebraQuotient(I)

        def classical_limit(self):
            """
            The Poisson vertex algebra classical limit of this vertex algebra

            EXAMPLES:

            We construct the classical limit of the universal Virasoro vertex
            algebra at central charge `1/2`::

                sage: V = VirasoroVertexAlgebra(QQ, 1/2)
                sage: P = V.classical_limit()
                sage: V.inject_variables()
                Defining L
                sage: (L*L)*L == L*(L*L)
                False
                sage: (P(L)*P(L))*P(L) == P(L)*(P(L)*P(L))
                True
                sage: V(L).bracket(V(L))
                {0: L_-3|0>, 1: 2*L_-2|0>, 3: 1/4*|0>}
                sage: P(L).bracket(P(L))
                {}

            We construct the classical limit of the *Ising* model::

                sage: V = VirasoroVertexAlgebra(QQ,1/2); L = V.0
                sage: v = L*(L*L) + 93/64*L.T()*L.T() - 33/16*L.T(2)*L - 9/128*L.T(4)
                sage: Q = V.quotient(V.ideal(v)); P = Q.classical_limit()
                sage: L*(L*L)
                L_-2L_-2L_-2|0>
                sage: Q(L)*(Q(L)*Q(L))
                33/8*L_-4L_-2|0>+27/16*L_-6|0>-93/64*L_-3L_-3|0>
                sage: P(L)*(P(L)*P(L)) == P.zero()
                True

            """
            raise NotImplementedError("General classical limit is only"+
                " implemented for H-graded vertex agebras")

        def _element_constructor_(self,x):
            """ 
            Constructs elements of this vertex algebra

            EXAMPLES::

                sage: V = VirasoroVertexAlgebra(QQ, 3)
                sage: V([[3]])
                L_-4|0>
                sage: V.0
                L_-2|0>
                sage: V.zero()
                0
                sage: V.zero().__class__
                <class 'sage.algebras.vertex_algebras.vertex_algebra.VirasoroVertexAlgebra_with_category.element_class'>
                sage: W = AffineVertexAlgebra(QQ, 'A1', 1)
                sage: W([[2,1],[],[3]])
                E(alpha[1])_-2E(alpha[1])_-1E(-alpha[1])_-3|0>
                sage: 3*W.0
                3*E(alpha[1])_-1|0>

            TESTS::

                sage: V = VirasoroVertexAlgebra(QQ,1/2)
                sage: V([[1],[2]])
                Traceback (most recent call last):
                ...
                TypeError: do not know how to convert [[1], [2]] into an element of The Virasoro vertex algebra at central charge 1/2

            """
            if x in self.base_ring():
                if x != 0 :
                    raise ValueError("can only convert the scalar 0 "\
                                     "into a vertex algebra element")
                return self.zero()
            return self.element_class(self,x)

        def is_strongly_generated(self):
            """
            If this vertex algebra is strongly generated

            EXAMPLES::

                sage: V = VirasoroVertexAlgebra(QQ, 3)
                sage: V.is_strongly_generated()
                True
                sage: W = AffineVertexAlgebra(QQ, 'A1', 1)
                sage: W.is_strongly_generated()
                True
            """
            return self in VertexAlgebras(self.base_ring()).FinitelyGenerated()

        def is_graded(self):
            """
            If this vertex algebra is H-Graded

            EXAMPLES::

                sage: V = VirasoroVertexAlgebra(QQ, 3)
                sage: V.is_graded()
                True
                sage: W = AffineVertexAlgebra(QQ, 'A1', 1)
                sage: W.is_graded()
                True

            """
            return self in VertexAlgebras(self.base_ring()).HGraded()

        @abstract_method
        def vacuum(self):
            """
            The vacuum vector of this vertex algebra

            EXAMPLES::

                sage: V = VirasoroVertexAlgebra(QQ, 3)
                sage: V.vacuum()
                |0>

            """
            raise NotImplementedError("Not implemented")

        @abstract_method
        def module(self):
            """
            The underlying module of this vertex algebra

            EXAMPLES:

            For universal enveloping vertex algebras we get a
            :class:`CombinatorialFreeModule<sage.combinat.free_module.CombinatorialFreeModule>`::

                sage: W = AffineVertexAlgebra(QQ, 'A1', 2)
                sage: W.module()
                Free module generated by Partition tuples of level 3 over Rational Field

            For quotient algebras we get the algebra itself::

                sage: V = VirasoroVertexAlgebra(QQ, 1/2)
                sage: V.register_lift()
                sage: L = V.0
                sage: v = L*(L*L) + 93/64*L.T()*L.T() - 33/16*L.T(2)*L - 9/128*L.T(4)
                sage: Q = V.quotient(V.ideal(v))
                sage: Q.module()
                Quotient of The Virasoro vertex algebra at central charge 1/2 by the ideal generated by (L_-2L_-2L_-2|0>-27/16*L_-6|0>+93/64*L_-3L_-3|0>-33/8*L_-4L_-2|0>,)
                sage: Q.module() is Q
                True

            """
            raise NotImplementedError("Not implemented")

        @abstract_method
        def zero(self):
            """
            The zero vector in this vertex algebra

            EXAMPLES::

                sage: V = VirasoroVertexAlgebra(QQ, 1/2); L = V.0
                sage: v = L*(L*L) + 93/64*L.T()*L.T() - 33/16*L.T(2)*L - 9/128*L.T(4)
                sage: Q = V.quotient(V.ideal(v))
                sage: Q(0)
                0
                sage: V(0)
                0
                sage: V(0) == V.zero()
                True
                sage: Q(0) == Q.zero()
                True

            """
            raise NotImplementedError("Not Implemented")

    class ElementMethods:
        def _nproduct_(self,rhs,n):
            """
            The `n`-th product of these two elements. 

            EXAMPLES::

                sage: V = VirasoroVertexAlgebra(QQ,1/2); L = V.0
                sage: L.nproduct(L,3)
                1/4*|0>
                sage: L.nproduct(L,-3)
                L_-4L_-2|0>

            """
            if n >= 0 :
                return self.bracket(rhs).get(n,self.parent().zero())
            else:
                return factorial(-1-n)**(-1)*self.T(-n-1)._mul_(rhs)


    class SubcategoryMethods:
        def Graded(self):
            """
            The subcategory of H-Graded vertex algebras
            """
            return self.HGraded()

        def HGraded(self):
            """
            The subcategory of H-Graded vertex algebras
            """
            return self._with_axiom('HGraded')

        def FinitelyGeneratedAsVertexAlgebra(self):
            """
            The subcategory of finitely and strongly generated vertex algebras
            """
            return self._with_axiom("FinitelyGeneratedAsVertexAlgebra")

        def FinitelyGenerated(self):
            """
            The subcategory of finitely and strongly generated vertex algebras
            """
            return self.FinitelyGeneratedAsVertexAlgebra()

        def WithBasis(self):
            """
            The subcategory of vertex algebras with a preferred basis
            """
            return self._with_axiom("WithBasis")

    class WithBasis(CategoryWithAxiom_over_base_ring):
        def _repr_object_names(self):
            """
            The names of objects in this category
            """
            return "vertex algebras with basis over {}".format(self.base_ring())

        class ElementMethods:
            def monomials(self):
                """
                The tuple of monomials in this element

                EXAMPLES::

                    sage: V = VirasoroVertexAlgebra(QQ,1/2); L = V.0; w = (L*L)*L; 
                    sage: w.monomials()
                    (4*L_-4L_-2|0>, 2*L_-3L_-3|0>, 1/2*L_-6|0>, L_-2L_-2L_-2|0>)

                """
                return tuple(v[1]*v[0] for v in 
                            self.monomial_coefficients().items())
 

    class HGraded(CategoryWithAxiom_over_base_ring):

        def _repr_object_names(self):
            """
            The names of objects in this category
            """
            return "H-graded vertex algebras over {}".format(self.base_ring())

        class SubcategoryMethods:
            def FinitelyGenerated(self):
                """
                The subcategory of finitely and strongly generated H-Graded
                vertex algebras
                """
                return self._with_axiom("FinitelyGeneratedAsVertexAlgebra")

        class WithBasis(CategoryWithAxiom_over_base_ring):
            """
            The subcategory of H-Graded vertex algebras with a preferred
            basis
            """
            def _repr_object_names(self):
                """
                The names of objects in this category
                """
                return "H-graded vertex algebras with basis "\
                            "over {}".format(self.base_ring())


        class ParentMethods:
            def classical_limit(self):
                """
                The Poisson vertex algebra classical limit of this vertex algebra

                EXAMPLES:

                We construct the classical limit of the universal Virasoro vertex
                algebra at central charge `1/2`::

                    sage: V = VirasoroVertexAlgebra(QQ, 1/2)
                    sage: P = V.classical_limit()
                    sage: V.inject_variables()
                    Defining L
                    sage: (L*L)*L == L*(L*L)
                    False
                    sage: (P(L)*P(L))*P(L) == P(L)*(P(L)*P(L))
                    True
                    sage: L.bracket(L)
                    {0: L_-3|0>, 1: 2*L_-2|0>, 3: 1/4*|0>}
                    sage: P(L).bracket(P(L))
                    {}

                We construct the classical limit of the *Ising* model::

                    sage: V = VirasoroVertexAlgebra(QQ,1/2); L = V.0
                    sage: v = L*(L*L) + 93/64*L.T()*L.T() - 33/16*L.T(2)*L - 9/128*L.T(4)
                    sage: Q = V.quotient(V.ideal(v)); P = Q.classical_limit()
                    sage: L*(L*L)
                    L_-2L_-2L_-2|0>
                    sage: Q(L)*(Q(L)*Q(L))
                    33/8*L_-4L_-2|0>+27/16*L_-6|0>-93/64*L_-3L_-3|0>
                    sage: P(L)*(P(L)*P(L)) == P.zero()
                    True

                """
                from sage.algebras.vertex_algebras.poisson_vertex_algebra import PoissonVertexAlgebra
                return PoissonVertexAlgebra(self.base_ring(), self)

        class ElementMethods:
            #for compatibility with LCA as `self` is in LCA
            def degree(self):
                """
                The conformal weight of this element

                EXAMPLES::

                    sage: V = VirasoroVertexAlgebra(QQ,1/2); L = V.0
                    sage: L.degree()
                    2
                    sage: W = AffineVertexAlgebra(QQ, 'A1', 2); E = W.0
                    sage: E.degree()
                    1
                    sage: L.T().degree()
                    3
                    sage: (L + L.T()).degree()
                    Traceback (most recent call last):
                    ...
                    ValueError: L_-2|0>+L_-3|0> is not homogeneous!

                """
                return self.weight()

            def filtered_degree(self):
                """
                The smallest space `F^p` in the Li filtration of this vertex
                algebra containing this element

                EXAMPLES::

                    sage: V = VirasoroVertexAlgebra(QQ,1/2); L = V.0
                    sage: L.li_filtration_degree()
                    0
                    sage: (L.T(2)*L.T()).li_filtration_degree()
                    3

                """
                return max(m.weight() for m in self.monomial_coefficients())

            @abstract_method
            def weight(self):
                """
                The conformal weight of this element

                This method is an alias of :meth:`degree`
                """

            def is_homogeneous(self):
                """
                Whether this element is homogeneous with respect to conformal
                weight

                EXAMPLES::

                    sage: V = VirasoroVertexAlgebra(QQ,1/2); L = V.0
                    sage: L.is_homogeneous()
                    True
                    sage: (L + L.T()).is_homogeneous()
                    False

                """
                try:
                    self.weight()
                except ValueError:
                    return False
                return True

            def nmodeproduct(self, other, n):
                r"""
                The shifted product of these two elements

                The element needs to be homogeneous. 
                If `a \in V_p`, then `a_n b` is defined as 
                `a_{(n+p-1)}b`. 

                EXAMPLES::
                    
                    sage: V = VirasoroVertexAlgebra(QQ, 1/2)
                    sage: V.inject_variables()
                    Defining L
                    sage: L.nmodeproduct(L.T(),0)
                    3*L_-3|0>

                    sage: (L + V.vacuum()).nmodeproduct(L,0)
                    Traceback (most recent call last):
                    ...
                    ValueError: Couldn't compute weight of L_-2|0>+|0>, it's not homogeneous?

                """
                try:
                    weight = self.weight()
                except ValueError:
                    raise ValueError("Couldn't compute weight of {}, "\
                                    "it's not homogeneous?".format(self))
                return self.nproduct(other, n+weight-1)

    class FinitelyGeneratedAsVertexAlgebra(CategoryWithAxiom_over_base_ring):

        def _repr_object_names(self):
            """
            The names of objects of this category
            """
            return "finitely and strongly generated" \
                        " vertex algebras over {}".format(self.base_ring())
        
        class ParentMethods:
            @abstract_method
            def gens(self):
                """
                The list of generators of this vertex algebra

                EXAMPLES::

                    sage: V = VirasoroVertexAlgebra(QQ,1/2)
                    sage: V.gens()
                    (L_-2|0>,)
                    sage: L = V.0; L in V
                    True
                    sage: v =  L*(L*L) + 93/64*L.T()*L.T() - 33/16*L.T(2)*L - 9/128*L.T(4)
                    sage: Q = V.quotient(V.ideal(v))
                    sage: Q.gens()
                    (L_-2|0>,)
                    sage: Q.gens()[0] in Q
                    True
                    sage: V = AffineVertexAlgebra(QQ, 'A1', 1); V
                    The universal affine vertex algebra of CartanType ['A', 1] at level 1
                    sage: V.gens()
                    (E(alpha[1])_-1|0>, E(alphacheck[1])_-1|0>, E(-alpha[1])_-1|0>)          

                """

            @abstract_method
            def ngens(self):
                """
                The number of generators of this vertex algebra
                
                EXAMPLES::

                    sage: VirasoroVertexAlgebra(QQ,1/2).ngens()
                    1
                    sage: AffineVertexAlgebra(QQ,'A2',1).ngens()
                    8

                """

            def hilbert_series(self,ord):
                """
                The graded dimension of this algebra

                INPUT:

                - ``ord`` -- integer; the precision order of the result

                OUTPUT: The sum

                .. MATH::
                    \sum_{n = 0}^{ord} q^n \mathrm{dim} V_n

                EXAMPLES::

                    sage: V = VirasoroVertexAlgebra(QQ,1/2)
                    sage: V.hilbert_series(8)
                    1 + q^2 + q^3 + 2*q^4 + 2*q^5 + 4*q^6 + 4*q^7 + 7*q^8
                    sage: L = V.0; v =  L*(L*L) + 93/64*L.T()*L.T() - 33/16*L.T(2)*L - 9/128*L.T(4)
                    sage: Q = V.quotient(V.ideal(v))
                    sage: Q.hilbert_series(9)
                    1 + q^2 + q^3 + 2*q^4 + 2*q^5 + 3*q^6 + 3*q^7 + 5*q^8 + 5*q^9

                """
                from sage.rings.power_series_ring import PowerSeriesRing
                q = PowerSeriesRing(self.base_ring(),'q', 
                                    default_prec = ord+1).gen()
                return sum(self.dimension(n)*q**n for n in range(ord+1 ))     

       
        class SubcategoryMethods:
            def HGraded(self):
                """
                The subcategory of finitely generated H-Graded vertex algebras
                """
                return self._with_axiom('HGraded')

        class HGraded(CategoryWithAxiom_over_base_ring):
            def _repr_object_names(self):
                return "H-graded finitely and strongly generated vertex"\
                    " algebras over {}".format(self.base_ring())

            class SubcategoryMethods:
                def WithBasis(self):
                    """
                    The subcategory of finitely generated
                    H-Graded Vertex algebras with a preferred
                    basis
                    """
                    return self._with_axiom("WithBasis")

            class WithBasis(CategoryWithAxiom_over_base_ring):
                def _repr_object_names(self):
                    return "H-graded finitely and strongly generated vertex"\
                        " algebras with basis over {}".format(self.base_ring())

            class ParentMethods:

                def find_singular(self,n):
                    """
                    Return the vector space of singular vectors of weight `n`
                    """
                    M = self.get_graded_part(n)
                    B = M.basis()
                    from sage.matrix.constructor import Matrix
                    ret = Matrix(self.base_ring(),B.cardinality(),0,0)
                    for g in self.gens():
                        for j in range(1,n+1):
                            Mj = self.get_graded_part(n-j)
                            ret = ret.augment(Matrix([Mj._from_dict(
                                g.nmodeproduct(self._from_dict(
                                v.monomial_coefficients()),j).value\
                                .monomial_coefficients()).to_vector() 
                                for v in B ]))
                    myker = ret.kernel().basis()
                    return [self._from_dict(M.from_vector(v)\
                        .monomial_coefficients()) for v in myker]
                            

            class ElementMethods:
                def is_singular(self):
                    """
                    Return whether this vector is a singular vector 

                    If `a \in V` is a vector in a finitely generated H-Graded
                    vertex algebra, then `a` is singular if for each homogeneous
                    vector `v in V` we have `v_n a = 0` whenever `n > 0`.

                    EXAMPLES::

                        sage: V = VirasoroVertexAlgebra(QQ,1/2); L = V.0
                        sage: v =  L*(L*L) + 93/64*L.T()*L.T() - 33/16*L.T(2)*L - 9/128*L.T(4)
                        sage: v.is_singular()
                        True
                        sage: V = AffineVertexAlgebra(QQ, 'A1', 2); E = V.0
                        sage: (E*E*E).is_singular()
                        True

                    """
                    p = self.parent()
                    try:
                        weight = self.weight()
                    except ValueError:
                        raise ValueError("Couldn't compute weight of {}, "\
                                         "it's not homogeneous?".format(self))
                    return all (g.nmodeproduct(self,n).is_zero() for 
                                n in range(1,weight+2) for g in p.gens())

                def _action_from_partition_tuple(self,p,negative=True):
                    """
                    helper function to apply elements of a vertex algebra
                    constructed from partitions

                    INPUT:

                    - ``p`` -- `PartitionTuple`. The level of ``p`` needs to
                      equal the number of generators of the vertex algebra
                    - ``negative`` -- boolean (default: `True`); 

                    OUTPUT: the result of repeatedly applying 
                    modes determined by ``p`` of the generators of
                    this vertex algebra to the vector ``self``. By default
                    negative modes are applied. Thus if `p = [[1]]` and `L` is
                    the unique generator of `V`, the mode `L_{-1}` will be
                    applied. If ``negative`` is `False`, non-negative modes are
                    applied instead. Thus in the example above `L_0` will be
                    applied. 

                    EXAMPLES:

                        sage: V = AffineVertexAlgebra(QQ, 'A1', 1); F = V.2
                        sage: F._action_from_partition_tuple(PartitionTuple([[2,1],[3],[]]))
                        E(alpha[1])_-2E(alpha[1])_-1E(alphacheck[1])_-3E(-alpha[1])_-1|0>      

                    """
                    ngens = self.parent().ngens()
                    if len(p) != ngens:
                        raise ValueError("p has to be a partition tuple of "
                                         "level {0}, got {1}".format(ngens,p))
                    ret = self
                    p = p.to_list()
                    p.reverse()
                    for j in range(ngens):
                        p[j].reverse()
                        g = self.parent()(self.parent().gen(ngens-j-1))
                        for n in p[j]:
                            if negative:
                                ret = g.nmodeproduct(ret,-n)
                            else:
                                ret = g.nmodeproduct(ret, n-1 )
                    return ret


