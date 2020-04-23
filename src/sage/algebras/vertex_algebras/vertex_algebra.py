r"""
Vertex algebras
AUTHORS

- Reimundo Heluani (08-09-2019): Initial implementation

.. include:: ../../../vertex_algebras/vertex_algebra_desc.inc

EXAMPLES:

The base class for all vertex algebras is :class:`VertexAlgebra`. 
All subclasses are called through its method ``__classcall_private__``. 
We provide some convenience functions to define named vertex algebras
like :meth:`VirasoroVertexAlgebra` and :meth:`AffineVertexAlgebra`

- We create the Universal Virasoro Vertex algebra at central charge c=1/2 and
  perform some basic computations::

    sage: V = VirasoroVertexAlgebra(QQ,1/2); V.inject_variables()
    Defining L
    sage: L*L
    L_-2L_-2|0>
    sage: (L*L).T()
    2*L_-3L_-2|0>+L_-5|0>
    sage: L.bracket(L*L)
    {0: 2*L_-3L_-2|0>+L_-5|0>,
     2: 3*L_-3|0>,
     3: 17/2*L_-2|0>,
     5: 3/2*|0>,
     1: 4*L_-2L_-2|0>}

- We compute it's irreducible quotient::

    sage: V.find_singular(6)
    [L_-2L_-2L_-2|0>-33/8*L_-4L_-2|0>+93/64*L_-3L_-3|0>-27/16*L_-6|0>]
    sage: v = _[0]; I = V.ideal(v)
    sage: I
    ideal of The Virasoro vertex algebra at central charge 1/2 generated by (L_-2L_-2L_-2|0>-33/8*L_-4L_-2|0>+93/64*L_-3L_-3|0>-27/16*L_-6|0>,)
    sage: Q = V.quotient(I)
    sage: Q
    Quotient of The Virasoro vertex algebra at central charge 1/2 by the ideal generated by (L_-2L_-2L_-2|0>-33/8*L_-4L_-2|0>+93/64*L_-3L_-3|0>-27/16*L_-6|0>,)
    sage: Q.retract(L*L*L)
    65/8*L_-4L_-2|0>+35/64*L_-3L_-3|0>+35/16*L_-6|0>

- We construct the universal Affine vertex algebra for `\mathfrak{sl}_3` at level
  2 and perform some basic computations::

    sage: V = AffineVertexAlgebra(QQ,'A2',2)
    sage: V.gens()
    (E(alpha[2])_-1|0>,
     E(alpha[1])_-1|0>,
     E(alpha[1] + alpha[2])_-1|0>,
     E(alphacheck[1])_-1|0>,
     E(alphacheck[2])_-1|0>,
     E(-alpha[2])_-1|0>,
     E(-alpha[1])_-1|0>,
     E(-alpha[1] - alpha[2])_-1|0>)
    sage: e = V.gen(0); f = V.gen(7)
    sage: e.bracket(f)
    {0: -E(-alpha[1])_-1|0>}
    sage: e*f
    E(alpha[2])_-1E(-alpha[1] - alpha[2])_-1|0>

- We construct the universal affine vertex algebra for `\mathfrak{sl}_2` at level
  3 and check that a vector is singular::

    sage: V = AffineVertexAlgebra(QQ,'A1',3)
    sage: V.gens()
    (E(alpha[1])_-1|0>, E(alphacheck[1])_-1|0>, E(-alpha[1])_-1|0>)
    sage: e = V.gen(0)
    sage: e*(e*(e*e))
    E(alpha[1])_-1E(alpha[1])_-1E(alpha[1])_-1E(alpha[1])_-1|0>
    sage: (e*(e*(e*e))).is_singular()
    True

- We construct the classical limit of `V` and check that the multiplication is
  associative in this limit while not in `V`::

    sage: P = V.classical_limit()
    sage: P
    The Poisson vertex algebra quasi-classical limit of The universal affine vertex algebra of CartanType ['A', 1] at level 3
    sage: f = V.gen(2)
    sage: e*(e*f) == (e*e)*f
    False
    sage: e=P(e); e.parent()
    The Poisson vertex algebra quasi-classical limit of The universal affine vertex algebra of CartanType ['A', 1] at level 3
    sage: f=P(f)
    sage: e*(e*f) == (e*e)*f
    True

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

from sage.structure.unique_representation import UniqueRepresentation
from sage.structure.parent import Parent
from sage.combinat.partition_tuple import PartitionTuples_level
from sage.categories.vertex_algebras import VertexAlgebras
from sage.categories.lie_conformal_algebras import LieConformalAlgebras, LiftMorphism
from sage.combinat.free_module import CombinatorialFreeModule
from sage.combinat.partition import Partition
from sage.combinat.partition_tuple import PartitionTuples
from sage.functions.other import binomial, factorial
from sage.misc.misc_c import prod
from sage.rings.infinity import Infinity
from sage.sets.family import Family
from sage.structure.element import parent
from sage.rings.integer import Integer
from sage.misc.cachefunc import cached_method

class VertexAlgebra(Parent, UniqueRepresentation):
    @staticmethod
    def __classcall_private__(cls, R=None, arg0 = None, category=None,
                              central_parameters=None, names=None):
        if R is None: 
            raise ValueError("First argument must be a ring!")
       
        try: 
            if R.has_coerce_map_from(arg0.base_ring()) and \
                arg0 in LieConformalAlgebras(arg0.base_ring()):
                return UniversalEnvelopingVertexAlgebra(R, arg0, 
                        category=category, central_parameters=central_parameters,
                        names=names)
        except AttributeError: 
            pass

        print ("Nothing to construct")

    def __init__(self, R, category=None,names=None):
        r"""Vertex algebras base class and factory

        INPUT:

        - ``R`` -- a ring (Default: None); The base ring of this vertex algebra.
          Behaviour is undefined if it is not a field of characteristic zero. 

        - ``arg0`` -- There are several methods of constructing vertex algebras.
          Currently we only support the construction as the universal enveloping
          vertex algebra of a Lie conformal algebra, which is best achieved by
          calling
          :meth:`~sage.categories.lie_conformal_algebras.ParentMethods.universal_enveloping_algebra`,
          or as derived constructions like quotients by calling
          :func:`~sage.categories.vertex_algebras.VertexAlgebras.ParentMethods.quotient`.
          Currently we only support ``arg0`` being a Lie conformal algebra. in
          which case this returns the quotient of its universal enveloping
          vertex algebra by the central ideal described by the argument
          ``central_parameters``. 

        - ``central_parameters`` -- A family defining a central ideal in the
          universal enveloping vertex algebra of the Lie conformal algebra
          ``arg0``. 

        EXAMPLES::

            sage: Vir = VirasoroLieConformalAlgebra(QQ)
            sage: Vir.inject_variables()
            Defining L, C
            sage: cp = Family({C:1/2})
            sage: V = VertexAlgebra(QQ,Vir,central_parameters=cp)
            sage: V
            The universal enveloping vertex algebra of Lie conformal algebra on 2 generators
            (L, C) over Rational Field.

        """
        category = VertexAlgebras(R).or_subcategory(category)
        super(VertexAlgebra, self).__init__(base=R, names=names,
                                            category = category)

    def base_ring(self):
        r"""The base ring of this vertex algebra
        EXAMPLES::

            sage: V = VirasoroVertexAlgebra(QQ,1/2); V
            The Virasoro vertex algebra at central charge 1/2
            sage: V.base_ring()
            Rational Field   

        """
        return self.category().base_ring()


class UniversalEnvelopingVertexAlgebra(VertexAlgebra):

    def __init__(self, R, L, category=None, central_parameters=None, names=None):
        r"""The (central quotient of the) universal enveloping vertex algebra of
        the Lie conformal algebra `L` over the ring `R`.

        INPUT:

        - ``R`` a ring, this is the base ring of this vertex algebra. Undefined
          behaviour if this ring is not a field of characteristic zero.

        - ``L`` a Lie conformal algebra. 

        - ``central_parameters`` A Family describing the action of the central
          elements in this vertex algebra. (Default: 0 for each central element
          of ``L``)
        """

        if L not in LieConformalAlgebras(R).WithBasis().FinitelyGenerated():
            raise ValueError ( "L needs to be a finitely generated " \
                "Lie conformal algebra with basis, got {}".format(L) )

        category = VertexAlgebras(R).FinitelyGenerated().WithBasis().\
           or_subcategory(category)

        if L in LieConformalAlgebras(R).Graded():
            category = category.Graded()

        super(UniversalEnvelopingVertexAlgebra, self).__init__(R, 
            category=category, names=names)

        self._lca = L
        if central_parameters:
            cp = central_parameters
        else: 
            cp = { i:0  for i in L.central_elements() }
        if set(cp.keys()) != set(L.central_elements()):
            raise ValueError ("central_parameters must be parametrized by "\
                              "central elements")

        self._central_parameters = Family(cp)
        #need to call directly this because of 1 generator. 
        #Also:self._module is needed for self.ngens()
        _basis = PartitionTuples_level(L.ngens()-len(L.central_elements()))
        self._module = CombinatorialFreeModule(self.base_ring(), _basis)
        self.register_lift()
    
    def _repr_(self):
        return "The universal enveloping vertex algebra of {}".format(
            self._lca)

    def register_lift(self):
        from sage.categories.homset import Hom
        self._lca.lift = LiftMorphism(Hom(self._lca, self, category = 
                        LieConformalAlgebras(self._lca.base_ring())))
        try: 
            self._lca.lift.register_as_coercion()
        except AssertionError:
            #we already constructed this morphisms and its fine
            pass



    def basis(self,n=None):
        r"""A lazy family describing a basis of this family

        EXAMPLES::
            sage: V = VirasoroVertexAlgebra(QQ,1/2); V
            The Virasoro vertex algebra at central charge 1/2
            sage: V.basis()
            Lazy family (<lambda>(i))_{i in Partition tuples of level 1}
            sage: V = AffineVertexAlgebra(QQ, 'A1', 1); V.basis()
            Lazy family (<lambda>(i))_{i in Partition tuples of level 3}

        """
        if n == None:
            return Family( PartitionTuples_level(level = self.ngens()), 
                    lambda i : self(i), lazy = True)
        else:
            return Family ( (self(self.module()._from_dict(
                b.monomial_coefficients())) for b in 
                self.get_graded_part(n).basis() ) )

    def gens(self):
        """The generators of this vertex algebra"""
        return tuple(self.gen(i) for i in range(self.ngens()))

    def ngens(self):
        """
        The number of generators of this vertex algebra
        """
        return self._lca.ngens() - len(self._lca.central_elements())

    def gen(self,i):
        r"""The `i`-th generator of this vertex algebra"""
        l = [[]]*self.ngens()
        l[i] = [1]
        return self(l)

    def central_elements(self):
        r"""If this vertex algebra is the universal enveloping vertex algebra of
        the Lie conformal algebra `L`. This method returns the family of central
        elements of the `L`.""" 
        return tuple ( self(i) for i in self._lca.central_elements())

    def central_parameters(self):
        """Return the central character used to construct this universal
        enveloping vertex algebra""" 
        return self._central_parameters

    def get_degree(self,n):
        r"""
        return the degree n filtered part of `self`. This is a 
        `CombinatorialFreeModule` with the same dictionary keys as 
        `self.module()`. 
        """
        #TODO: deal with the vacuum in a better way
        basis = [PartitionTuples_level(self.ngens())([[],]*self.ngens()),]
        basis += [PartitionTuples_level(self.ngens())(p) for m in range(1 ,n+1) 
            for p in PartitionTuples(self.ngens(),m) if 
            self(PartitionTuples_level(self.ngens())(p)).weight() <= n ]
        return CombinatorialFreeModule(self.base_ring(), basis)

    def get_graded_part(self,n):
        r"""
        return the degree n filtered part of `self`. This is a 
        `CombinatorialFreeModule` with the same dictionary keys as 
        `self.module()`. 
        """
        #TODO: deal with the vacuum in a better way
        if n == 0:
            return CombinatorialFreeModule( self.base_ring(),
                [PartitionTuples_level(self.ngens())([[]]*self.ngens()),] )
        else:
            basis = [PartitionTuples_level(self.ngens())(p) for m in range(1 ,n+1) 
            for p in PartitionTuples(self.ngens(),m) if 
            self(PartitionTuples_level(self.ngens())(p)).weight() == n ]
        return CombinatorialFreeModule(self.base_ring(), basis)

    def dimension(self,n):
        r"""The dimension of the degree `n` part of this vertex algebra

        EXAMPLES::

            sage: V = VirasoroVertexAlgebra(QQ,1/2); V.dimension(4)
            2
            sage: V.dimension(6)
            4
            sage: V.dimension(0)
            1
            sage: V.dimension(1)
            0
            sage: V = AffineVertexAlgebra(QQ, 'A1', 1); V.dimension(1)
            3
            sage: V.dimension(2)
            9

        """

        return self.get_graded_part(n).dimension()


    def module(self):
        r"""Return the `CombinatorialFreeModule` underlying this vertex
        algebra"""
        return self._module

    @cached_method
    def vacuum(self):
        """The vacuum vector of this vertex algebra"""
        vac = [Partition([]),]*self.ngens()
        return self.element_class(self, self.module()(vac))

    @cached_method
    def zero(self):
        """The zero element of this vertex algebra"""
        return self.element_class(self, self.module().zero())

    def _element_constructor_(self,x):
        if x == self.base_ring().zero():
            return self.zero()
        try:
            v = self._module(x)
        except TypeError:
            raise TypeError("do not know how to convert {0} into an element "\
                            "of {1}".format(x,self))
        return self.element_class(self, v)

    def li_filtration(self,n,k=None):
        r"""Let `V` be this vertex algebra and `V_n` its conformal weight `n`
        part. This method returns the filtered vector space `F_\bullet V_n` with respect
        to the Li filtration. If ``k`` is specified it returns `F_k V_n`.

        EXAMPLES::

            sage: V = AffineVertexAlgebra(QQ, 'A1', 1); 
            sage: V.li_filtration(2)
            {0: Free module generated by {0, 1, 2, 3, 4, 5, 6, 7, 8} over Rational Field,
             1: Free module generated by {0, 1, 2} over Rational Field,
             2: Free module generated by {} over Rational Field,
             3: Free module generated by {} over Rational Field}
            sage: V.li_filtration(2,1)
            Free module generated by {0, 1, 2} over Rational Field
            sage: V = VirasoroVertexAlgebra(QQ,1/2); V.dimension(12)
            21
            sage: V.li_filtration(12,7)
            Free module generated by {0, 1, 2, 3, 4, 5} over Rational Field

        """
        A = self.get_graded_part(n)
        ret = {}
        for m in range(n+2) if k==None else range(k,k+1):
            basis = [b for b in A.basis() if self._from_dict(
                b.monomial_coefficients()).li_filtration_degree()>=m]
            ret[m] = A.submodule(basis)
        return ret if k==None else ret[k]
         
    from sage.structure.element_wrapper import ElementWrapper
    class Element(ElementWrapper):
        def _repr_(self):
            p = self.parent()
            if self == p.zero():
                return "0";
            coeff = list(self.value.monomial_coefficients().items())
            ret = ""
            for i in range(len(coeff)):
                if i > 0  and coeff[i][1] > 0:
                    ret += "+"
                if coeff[i][1] < 0:
                    ret += "-"

                if abs(coeff[i][1]) != 1:
                    ret += "{}*".format(abs(coeff[i][1]))
                for idx,j in enumerate(coeff[i][0]):
                    for k in j.to_list():
                        ret += "{}_".format(p._lca._repr_generator(p._lca.gen(idx)))
                        if p.is_graded():
                            ret+= "{}".format(1 -k-p._lca.gen(idx).degree())
                        else:
                            ret+= "({})".format(-k)
                ret+="|0>"
            return ret

        def _add_(self,right):
            return type(self)(self.parent(), self.value + right.value)

        def __nonzero__(self):
            return bool(self.value)

        def _sub_(self, right):
            return type(self)(self.parent(), self.value - right.value)

        def _neg_(self):
            return type(self)(self.parent(), -self.value)

        def _bracket_(self, other):
            # sum over monomials for other. Use non-commutative Wick formula to 
            # Reduce to other being a generator or a derivative. 
            # Use Skew-Symmetry to reduce to self being a generator or a
            # derivative.
            p = self.parent()
            ret = {}
            svmc = other.value.monomial_coefficients()
            for k in svmc.keys():
                c = svmc[k]
                i = next((j for j,x in enumerate(k) if x), None)
                if i is None:
                    continue
                l = [Partition([]),]*p.ngens()
                l[i] = Partition([k[i].get_part(0)])
                if k == l:
                    svmc2 = self.value.monomial_coefficients()
                    for k2 in svmc2.keys():
                        c2 = svmc2[k2]
                        i2 = next((j for j,x in enumerate(k2) if x), None)
                        if i2 is None:
                            continue
                        l2 = [Partition([]),]*p.ngens()
                        l2[i2] = Partition([k2[i2].get_part(0)])
                        if k2 == l2:
                            #Here we only use T from LieConformalAlgebras
                            br = p._lca.gen(i2).T(l2[i2].size()-1) \
                                ._bracket_(p._lca.gen(i).T(l[i].size()-1))
                            for j in br.keys():
                                rec = ret.get(j,p.zero())
                                ret[j] = rec + factorial(l[i].size()-1)**(-1)*\
                                factorial(l2[i2].size()-1)**(-1)*c*c2*p(br[j])
                        else:
                            #skew-symmetry
                            #Here is the only place we use T from VertexAlgebra
                            #We need T^j (other_(n) self)
                            #Note however that these terms are lower in the PBW
                            #filtration. 
                            br = p(k)._bracket_(p(k2))
                            for cl in range(max(br.keys())+1):
                                rec = ret.get(cl, p.zero())
                                ret[cl] = rec+sum(c*c2*(-1)**(j+1)\
                                          *p.base_ring()(factorial(j-cl))\
                                          .inverse_of_unit()\
                                          *br[j].T(j-cl) 
                                          for j in br.keys() if j >= cl)
                else:
                    #non-commutative Wick Formula
                    sf = k.to_list()
                    sf[i] = Partition(Partition(sf[i]).to_list()[1:])
                    br = self._bracket_(p(l))
                    for j in br.keys():
                        rec = ret.get(j, p.zero())
                        ret[j] = rec + c*br[j]._mul_(p(sf))
                        #integral term
                        br2 = br[j]._bracket_(p(sf))
                        for m in br2.keys():
                            rec = ret.get(j+m+1 ,p.zero())
                            ret[j+m+1] = rec + c*binomial(j+m+1,j)*br2[m]
                    br = self._bracket_(p(sf))
                    for j in br.keys():
                        rec = ret.get(j, p.zero())
                        ret[j] = rec + c*p(l)._mul_(br[j])
            return {k:ret[k] for k in ret.keys() if ret[k]} 

        def _mul_(self,right):
            r"""
            returns the normally ordered product :`self``right`:
            This is where the magic happens
            """
            #Use quasi-associativity to reduce to self being a generator. This
            #uses T and bracket from Vertex Algebra, but for terms lower in the
            #PBW filtration
            p = self.parent()
            ret = p.zero()
            svmc = self.value.monomial_coefficients()
            for k in svmc.keys():
                c = svmc[k]
                i = next((j for j,x in enumerate(k) if x), None)
                if i is None:
                    ret += c*right
                else:
                    l = [Partition([]),]*p.ngens()
                    l[i] = Partition([k[i].get_part(0)])
                    if k == l:
                        ni = k[i].get_part(0)
                        rvmc = right.value.monomial_coefficients()
                        for k2 in rvmc.keys():
                            c2 = rvmc[k2]
                            i2 = next((j for j,x in enumerate(k2) if x), None)
                            if i2 is None:
                                ret += c*c2*p(l)
                            elif  i2 < i or (i2==i and k2[i2].get_part(0)>ni):
                                ni2 = k2[i2].get_part(0)
                                l2 = [Partition([]),]*p.ngens()
                                l2[i2] = Partition([ni2])
                                sf = k2.to_list()
                                sf[i2] = Partition(Partition(sf[i2]).to_list()[1:])
                                rec = p(l)._mul_(p(sf))
                                ret += c*c2*p(l2)._mul_(rec)
                                #Here's the only place where we need the
                                #structure constants. We are using that
                                #T^(n)a_{(-1)} = a_{(-1-n)} and the commutator 
                                #formula. Given the implementation it's faster
                                #to compute the bracket in the other direction
                                #We only use T from LieConformalAlgebra and we 
                                #only use the bracket in LieConformalAlgebra
                                br = p._lca.gen(i2).bracket(p._lca.gen(i))
                                if br:
                                    ret -= c*c2*sum( binomial(-ni2,j)*\
                                    factorial(ni+ni2+j-1)**(-1)*p(br[j].\
                                    T(ni+ni2+j-1))._mul_(p(sf)) for j in br.keys() )
                            else:
                                sf = k2.to_list()
                                l2 = Partition(k2[i]).to_list()
                                l2.insert(0,ni)
                                sf[i] = Partition(l2)
                                ret += c*c2*p(sf)
                    else:
                        #quasi-associativity
                        #This uses bracket in VerteAlgebra and T in Vertex
                        #algebra but it computes T in terms lower in the PBW
                        #filtration. 

                        l = p(l)
                        sf = k.to_list()
                        sf[i] = Partition(Partition(sf[i]).to_list()[1:])
                        sf = p(sf)
                        rec = sf._mul_(right)
                        ret+= c*l._mul_(rec)
                        sfbr = sf.bracket(right)
                        lbr = l.bracket(right)
                        if sfbr:
                            ret+=c*sum(prod(Integer(1)/i for i in range(1 ,j+2 ))*
                                l.T(j+1)._mul_(sfbr[j]) for j in sfbr.keys())
                        if lbr:
                            ret+=c*sum(prod(Integer(1)/i for i in range(1 ,j+2 ))*
                                sf.T(j+1)._mul_(lbr[j]) for j in lbr.keys())
            return ret

        def T(self,n=1):
            r"""The `n`-th derivative of this element. If ``n`` is not provided
            it defaults to `1`. 

            EXAMPLES::

                sage: V = VirasoroVertexAlgebra(QQ,1/2); V.inject_variables()
                Defining L
                sage: L.T()
                L_-3|0>
                sage: v = V.vacuum(); v.T()
                0
                sage: L.T(3)
                6*L_-5|0>
                sage: (L*L).T()
                2*L_-3L_-2|0>+L_-5|0>

            """
            if n==0:
                return self
            if n > 1:
                return self.T().T(n-1)

            p = self.parent()
            if self.is_zero() or self == p.vacuum():
                return p.zero()

            selfmon = self.monomials()
            if len(selfmon) > 1:
                return sum( m.T() for m in selfmon)

            #Now we just have a monomial to compute. 
            k,c = list(self.value.monomial_coefficients().items())[0]
            kl = k.to_list()
            i = next((i for i,x in enumerate(k) if x))
            g = kl[i].pop(0)
            PT = PartitionTuples_level(k.level())
            return factorial(g-1)**(-1)*c*p(p._lca.gen(i).T(g))._mul_(
                        p(PT(kl)))+ factorial(g-1)**(-1)*c*\
                        p(p._lca.gen(i).T(g-1))._mul_(p(PT(kl)).T())


        def __getitem__(self, i):
            return self.value.__getitem__(i)

        def _acted_upon_(self, scalar, self_on_left=False):
            scalar_parent = parent(scalar)
            if scalar_parent != self.parent().base_ring():
                if self.parent().base_ring() \
                        .has_coerce_map_from(scalar_parent):
                    scalar = self.parent().base_ring()( scalar )
                else:
                    return None
            if self_on_left:
                return type(self)(self.parent(), self.value * scalar)
            return type(self)(self.parent(), scalar * self.value)

        def monomial_coefficients(self):
            r"""
            Return the monomial coefficients of ``self`` as a dictionary.
            """
            c = self.value.monomial_coefficients()
            p = self.parent()
            return { p(k) : c[k] for k in c.keys() } 

        def is_monomial(self):
            """Return whether this element is a monomial"""
            return (len(self.monomial_coefficients()) == 1 or self.is_zero())

        def index(self):
            r"""If this element is a monomial it returns the index parametrizing
            this element in the basis of this vertex algebra. If it is not a
            monomial it raises an error. 

            EXAMPLES::

                sage: V = AffineVertexAlgebra(QQ, 'A1', 1); e = V.gen(0); f = V.gen(2);
                sage: e.index()
                ([1], [], [])
                sage: f.index()
                ([], [], [1])
                sage: e.T()*e*f
                E(alpha[1])_-3E(alphacheck[1])_-1|0>+E(alpha[1])_-4|0>+E(alpha[1])_-2E(alpha[1])_-1E(-alpha[1])_-1|0>
                sage: _.index()
                Traceback (most recent call last):
                ...
                ValueError: index can only be computed for monomials
                sage: e.T()*(e*f)
                E(alpha[1])_-2E(alpha[1])_-1E(-alpha[1])_-1|0>
                sage: _.index()
                ([2, 1], [], [1])

            """
            if self.is_zero():
                return None
            if not self.is_monomial():
                raise ValueError ("index can only be computed for"
                         " monomials")
            return list(self.value.monomial_coefficients().keys())[0]

        def weight(self):
            r"""The conformal weight o this element. It raises an error if the
            element is not homogeneous
            
            EXAMPLES::

                sage: V = AffineVertexAlgebra(QQ, 'A1', 1); e = V.gen(0); f = V.gen(2);
                sage: (e*f).weight()
                2
                sage: V.vacuum().weight()
                0
                sage: V.zero().weight()
                +Infinity
                sage: f*e
                E(alpha[1])_-1E(-alpha[1])_-1|0>-E(alphacheck[1])_-2|0>
                sage: (f*e).weight()
                2
                sage: (e*f + e).weight()
                Traceback (most recent call last)
                ...
                ValueError: E(alpha[1])_-1E(-alpha[1])_-1|0>+E(alpha[1])_-1|0> is not homogeneous!

            """
            p = self.parent()
            if not p.is_graded():
                raise ValueError("Weight is only defined in H-graded"
                    " vertex algebras")
            if self.is_zero():
                return Infinity
            ls = []
            for idx in self.value.monomial_coefficients().keys():
                ret = sum(len(idx[i])*(p._lca.gen(i).degree()-1) + idx[i].size() 
                    for i in range(p.ngens()))
                ls.append(ret)
            if ls[1:] == ls[:-1]:
                return ls[0]
            raise ValueError("{} is not homogeneous!".format(self))

        def _li_filtration_monomial_degree(self):
            r"""The Li filtration degree of this non-zero monomial"""
            p = list(self.value.monomial_coefficients().keys())[0]
            return p.size() - sum(j.length() for j in p.components())

        def li_filtration_leading_terms(self):
            r"""Returns the leading terms of this element with respect to the Li
            filtration

            EXAMPLES::

                sage: V = VirasoroVertexAlgebra(QQ,1/2); 
                sage: V.find_singular(6)
                [L_-2L_-2L_-2|0>-33/8*L_-4L_-2|0>+93/64*L_-3L_-3|0>-27/16*L_-6|0>]
                sage: v = _[0]
                sage: v
                L_-2L_-2L_-2|0>-33/8*L_-4L_-2|0>+93/64*L_-3L_-3|0>-27/16*L_-6|0>
                sage: v.li_filtration_leading_terms()
                L_-2L_-2L_-2|0>
                
            """
            if self.is_zero():
                return self
            lt = [(m._li_filtration_monomial_degree(),m) for m in
                  self.monomials()]
            lideg = min(k[0] for k in lt)
            return sum(k[1] for k in lt if k[0]==lideg)

        def li_filtration_degree(self):
            r"""Let `F_pV` denote the Li filtration of this vertex algebra. This
            method returns the maximum `p` such that this element belongs in
            `F_pV`. 

            EXAMPLES::

                sage: V = VirasoroVertexAlgebra(QQ,1/2); V.inject_variables
                sage: Defining L
                sage: V.find_singular(6)
                [L_-2L_-2L_-2|0>-33/8*L_-4L_-2|0>+93/64*L_-3L_-3|0>-27/16*L_-6|0>]
                sage: v = _[0]
                sage: v
                L_-2L_-2L_-2|0>-33/8*L_-4L_-2|0>+93/64*L_-3L_-3|0>-27/16*L_-6|0>
                sage: v.li_filtration_leading_terms()
                L_-2L_-2L_-2|0>
                sage: v.li_filtration_degree()
                0
                sage: w = (L*L).T(); w
                2*L_-3L_-2|0>+L_-5|0>
                sage: w.li_filtration_degree()
                1
                sage: (w*v).li_filtration_degree()
                1

            """
            if self.is_zero():
                return Infinity
            return min(m._li_filtration_monomial_degree() for m in 
                       self.monomials())
        
        def degrevlex_lm(self):
            r"""
            Returns the leading monomials with respect to the degrevlex
            monomial order. Let this vertex algebra `V` be generated by fields
            `a^1,\dots,a^n` of conformal weights `\Delta_1,\dots,\Delta_n`. A
            typical monomial element of `V` is written as a product of elements 
            `a^i_{-j - \Delta_i}` for `i=1,\dots,n` and `j \geq 0`. We define a
            lexycografical order on 
            these generators in by degree first, and then by the order in the
            list of generators, namely 
            `a^i_{-j-\Delta_i} < a^{i'}_{-j' - \Delta_{i'}}` if
            `j+\Delta_i < j' + \Delta_{i'}` or if 
            `j+\Delta_i = j' + \Delta_{i'}` and `i < i'`. 

            This method then returns the leading monomial with respect to the
            weighted degree reverse lexycographical order. 

            EXAMPLES::

                sage: V = VirasoroVertexAlgebra(QQ,1/2); 
                sage: v = L*L*L + L.T()*L.T() + L.T(4)
                sage: v
                3*L_-3L_-3|0>+4*L_-4L_-2|0>+49/2*L_-6|0>+L_-2L_-2L_-2|0>
                sage: v.degrevlex_lm()
                49/2*L_-6|0>
                sage: V = AffineVertexAlgebra(QQ, 'A1', 1); e = V.gen(0); h = V.gen(1); f = V.gen(2);
                sage: v = e.T() + f*f; v
                E(alpha[1])_-2|0>+E(-alpha[1])_-1E(-alpha[1])_-1|0>
                sage: v.degrevlex_lm()
                E(-alpha[1])_-1E(-alpha[1])_-1|0>
                sage: v = f.T() + e*e; v.degrevlex_lm() == e*e
                False
                sage: v.degrevlex_lm()
                E(-alpha[1])_-2|0>

            """
            def dgrlcmp(a):
                pa = list(a.value.monomial_coefficients().keys())[0]
                bigest = max(p.get_part(0) for p in pa)
                pa = pa.to_exp(bigest)
                ret = [a.weight(),]
                for j in range(bigest):
                    for l in range(len(pa)):
                        ret.append(pa[l][bigest-j-1])
                return ret
            if self.is_zero():
                return self
            return sorted(self.monomials(),key=dgrlcmp)[0]

        def PBW_filtration_degree(self):
            r"""If `G_pV` is the increasing PBW filtration in this universal
            enveloping vertex algebra, this method returns the minimal `p` such
            that this element belongs to `G_pV`

            EXAMPLES::

                sage: V = AffineVertexAlgebra(QQ, 'A1', 1); e = V.gen(0); h = V.gen(1); f = V.gen(2);
                sage: e.PBW_filtration_degree()
                1
                sage: (e*f.T()).PBW_filtration_degree()
                2
                sage: (e*f - f*e).PBW_filtration_degree()
                1
                sage: V.vacuum().PBW_filtration_degree()
                0

            """
            p = self.parent()
            if self.is_zero():
                return -1 
            ls = []
            for p in self.value.monomial_coefficients().keys():
                ret = sum(j.length() for j in p.components())
                ls.append(ret)
            return max(ls)

        def _pbw_one_less(self):
            if self.is_zero():
                return (None, None, None)
            svmc = self.value.monomial_coefficients()
            if len(svmc) != 1:
                raise ValueError("{} is not a monomial.".format(self))
            k = list(svmc.keys())[0]
            c = svmc[k] 
            p = self.parent()
            i = next((j for j,x in enumerate(k) if x), None)
            if i is None:
                return (p.vacuum(), p.vacuum(), c)
            l = [Partition([]), ]*p.ngens()
            l[i] = Partition([k[i].get_part(0)])
            sf = k.to_list()
            sf[i] = Partition(Partition(sf[i]).to_list()[1:])
            return (p(l),p(sf),c) 

        
class VirasoroVertexAlgebra(UniversalEnvelopingVertexAlgebra):
    def __init__(self, R, c, arg0 = None, names="L"):
        r"""
        The universal Virasoro vertex algebra 

        INPUT:

        - ``R`` a ring, the base ring of this vertex algebra. Undefined behaviour if
          this is not a Field of characteristic zero. 

        - ``c`` The central charge of this vertex algebra if ``arg0`` is not
          specified. 

        - ``arg0`` a positive integer or ``None`` (Default: ``None``). If specified
          a positive integer `q` then the parameter `c` has to be a positive integer
          `p` coprime with `q` and this vertex algebra returns the irreducible
          quotient of the Virasoro vertex algebra at central charge 

        ..MATH::
            c = 1 - 6 \\frac{(p-q)^2}{pq}


        EXAMPLES::

            sage: V = VirasoroVertexAlgebra(QQ,1/2); V
            The Virasoro vertex algebra at central charge 1/2

        """
        from .lie_conformal_algebra import VirasoroLieConformalAlgebra
        ML = VirasoroLieConformalAlgebra(R)
        if arg0 is not None:
            c = 1  - 6*(c-arg0)**2/(c*arg0)
        cp = Family({ML.gen(1):c})
        super(VirasoroVertexAlgebra,self).__init__(R, ML,
                 central_parameters=cp, names = names)
        self._c = c

    def _repr_(self):
        return "The Virasoro vertex algebra at central charge {}".format(self.central_charge())

    def central_charge(self):
        return self._c

class AffineVertexAlgebra(UniversalEnvelopingVertexAlgebra):
    def __init__(self, R, ct, k, names=None):
        r"""The universal affine vertex algebra over the ring `R` of the Lie
        algebra of finite Cartan Type `ct` at level `k`

        EXAMPLES::

            sage: V = AffineVertexAlgebra(QQ, 'A1', 1); V
            The universal affine vertex algebra of CartanType ['A', 1] at level 1
            sage: V = AffineVertexAlgebra(QQ, 'B3', 1); V
            The universal affine vertex algebra of CartanType ['B', 3] at level 1

        """
        from .lie_conformal_algebra import AffineLieConformalAlgebra
        if names is not None:
            prefix = ''
            bracket = ''
        else:
            prefix = 'E'
            bracket = '('
        ML = AffineLieConformalAlgebra(R, ct, names=names, prefix=prefix,
                                       bracket=bracket)
        cp = Family({ML.central_elements()[0]: k})
        super(AffineVertexAlgebra,self).__init__(R, ML, 
            central_parameters = cp, names=names)

        self._level = k
        if type(ct) is str:
            from sage.combinat.root_system.cartan_type import CartanType
            ct = CartanType(ct)
        self._ct = ct
    
    def level(self):
        r"""The level of this Affine vertex algebra

        EXAMPLES:

        sage: V = AffineVertexAlgebra(QQ, 'B3', 1); V
        The universal affine vertex algebra of CartanType ['B', 3] at level 1
        sage: V.level()
        1

        """
        return self._level

    def cartan_type(self):
        r"""The Cartan Type of this Affine vertex algebra

        EXAMPLES::

            sage: V = AffineVertexAlgebra(QQ, 'B3', 1); V
            The universal affine vertex algebra of CartanType ['B', 3] at level 1
            sage: V.cartan_type()
            ['B', 3]

        """
        return self._ct

    def is_critical(self):
        r"""True if the level equals minus the dual Coxeter number of its Cartan
        Type

        EXAMPLES::

            sage: V = AffineVertexAlgebra(QQ, 'A1', -2); V
            The universal affine vertex algebra of CartanType ['A', 1] at critical level
            sage: V.is_critical()
            True

        """
        return self.level() == -self.cartan_type().dual_coxeter_number()

    def _repr_(self):
        if self.is_critical():
            return "The universal affine vertex algebra of CartanType {} at critical level".format(self.cartan_type())
        else:
            return "The universal affine vertex algebra of CartanType {0} at level {1}".format(self.cartan_type(), self.level())

