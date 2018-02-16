r"""
Integral lattices

An integral lattice is a finitely generated free abelian group
`L \cong \ZZ^r` equipped with a non-degenerate, symmetric bilinear
form `L \times L \colon \rightarrow \ZZ`.

Here, lattices have an ambient quadratic space `\QQ^n` and
a distinguished basis.

EXAMPLES::

    sage: M = Matrix(ZZ, [[0,1], [1,0]])
    sage: IntegralLattice(M)
    Lattice of degree 2 and rank 2 over Integer Ring
    Basis matrix:
    [1 0]
    [0 1]
    Inner product matrix:
    [0 1]
    [1 0]

A lattice can be defined by an inner product matrix of the
ambient space and a basis::

    sage: G = matrix.identity(3)
    sage: basis = [[1,-1,0], [0,1,-1]]
    sage: L = IntegralLattice(G, basis)
    sage: L
    Lattice of degree 3 and rank 2 over Integer Ring
    Basis matrix:
    [ 1 -1  0]
    [ 0  1 -1]
    Inner product matrix:
    [1 0 0]
    [0 1 0]
    [0 0 1]

    sage: L.gram_matrix()
    [ 2 -1]
    [-1  2]

AUTHORS:

- Simon Brandhorst (2017-09): First created
"""

#*****************************************************************************
#       Copyright (C) 2017 Simon Brandhorst <sbrandhorst@web.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#                  http://www.gnu.org/licenses/
#*****************************************************************************

from sage.rings.integer_ring import ZZ
from sage.rings.integer import Integer
from sage.rings.rational_field import QQ
from sage.modules.free_quadratic_module import FreeQuadraticModule_submodule_with_basis_pid, FreeQuadraticModule
from sage.matrix.constructor import matrix
from sage.structure.element import is_Matrix
from sage.arith.misc import gcd
from sage.combinat.root_system.cartan_matrix import CartanMatrix
from sage.categories.homset import Hom

###############################################################################
#
# Constructor functions
#
###############################################################################

def IntegralLattice(data, basis=None):
    r"""
    Return the integral lattice spanned by ``basis`` in the ambient space.

    A lattice is a finitely generated free abelian group `L \cong \ZZ^r`
    equipped with a non-degenerate, symmetric bilinear form
    `L \times L \colon \rightarrow \ZZ`. Here, lattices have an
    ambient quadratic space `\QQ^n` and a distinguished basis.

    INPUT:

    The input is a descriptor of the lattice and a (optional) basis.
    - ``data`` -- can be one of the following:

      * a symmetric matrix over the rationals -- the inner product matrix
      * an integer -- the dimension for a euclidian lattice
      * a symmetric Cartan type or anything recognized by
        :class:`CartanMatrix` (see also
        :mod:`Cartan types <sage.combinat.root_system.cartan_type>`)
        -- for a root lattice
      * the string ``"U"`` or ``"H"`` -- for hyperbolic lattices

    - ``basis`` -- (optional) a matrix whose rows form a basis of the
      lattice,  or a list of module elements forming a basis

    OUTPUT:

    A lattice in the ambient space defined by the inner_product_matrix.
    Unless specified, the basis of the lattice is the standard basis.

    EXAMPLES::

        sage: H5 = Matrix(ZZ, 2, [2,1,1,-2])
        sage: IntegralLattice(H5)
        Lattice of degree 2 and rank 2 over Integer Ring
        Basis matrix:
        [1 0]
        [0 1]
        Inner product matrix:
        [ 2  1]
        [ 1 -2]

    A basis can be specified too::

        sage: IntegralLattice(H5, Matrix([1,1]))
        Lattice of degree 2 and rank 1 over Integer Ring
        Basis matrix:
        [1 1]
        Inner product matrix:
        [ 2  1]
        [ 1 -2]

    We can define a Euclidian lattice just by its dimension::

        sage: IntegralLattice(3)
        Lattice of degree 3 and rank 3 over Integer Ring
        Basis matrix:
        [1 0 0]
        [0 1 0]
        [0 0 1]
        Inner product matrix:
        [1 0 0]
        [0 1 0]
        [0 0 1]

    Here is an example of the `A_2` root lattice in Euclidian space::

        sage: basis = Matrix([[1,-1,0], [0,1,-1]])
        sage: A2 = IntegralLattice(3, basis)
        sage: A2
        Lattice of degree 3 and rank 2 over Integer Ring
        Basis matrix:
        [ 1 -1  0]
        [ 0  1 -1]
        Inner product matrix:
        [1 0 0]
        [0 1 0]
        [0 0 1]
        sage: A2.gram_matrix()
        [ 2 -1]
        [-1  2]

    We use ``"U"`` or ``"H"`` for defining a hyperbolic lattice::

        sage: L1 = IntegralLattice("U")
        sage: L1
        Lattice of degree 2 and rank 2 over Integer Ring
        Basis matrix:
        [1 0]
        [0 1]
        Inner product matrix:
        [0 1]
        [1 0]
        sage: L1 == IntegralLattice("H")
        True

    We can construct root lattices by specifying their type
    (see :mod:`Cartan types <sage.combinat.root_system.cartan_type>`
    and :class:`CartanMatrix`)::

        sage: IntegralLattice(["E", 7])
        Lattice of degree 7 and rank 7 over Integer Ring
        Basis matrix:
        [1 0 0 0 0 0 0]
        [0 1 0 0 0 0 0]
        [0 0 1 0 0 0 0]
        [0 0 0 1 0 0 0]
        [0 0 0 0 1 0 0]
        [0 0 0 0 0 1 0]
        [0 0 0 0 0 0 1]
        Inner product matrix:
        [ 2  0 -1  0  0  0  0]
        [ 0  2  0 -1  0  0  0]
        [-1  0  2 -1  0  0  0]
        [ 0 -1 -1  2 -1  0  0]
        [ 0  0  0 -1  2 -1  0]
        [ 0  0  0  0 -1  2 -1]
        [ 0  0  0  0  0 -1  2]
        sage: IntegralLattice(["A", 2])
        Lattice of degree 2 and rank 2 over Integer Ring
        Basis matrix:
        [1 0]
        [0 1]
        Inner product matrix:
        [ 2 -1]
        [-1  2]
        sage: IntegralLattice("D3")
        Lattice of degree 3 and rank 3 over Integer Ring
        Basis matrix:
        [1 0 0]
        [0 1 0]
        [0 0 1]
        Inner product matrix:
        [ 2 -1 -1]
        [-1  2  0]
        [-1  0  2]
        sage: IntegralLattice(["D", 4])
        Lattice of degree 4 and rank 4 over Integer Ring
        Basis matrix:
        [1 0 0 0]
        [0 1 0 0]
        [0 0 1 0]
        [0 0 0 1]
        Inner product matrix:
        [ 2 -1  0  0]
        [-1  2 -1 -1]
        [ 0 -1  2  0]
        [ 0 -1  0  2]

    We can specify a basis as well::

        sage: G = Matrix(ZZ, 2, [0,1,1,0])
        sage: B = [vector([1,1])]
        sage: IntegralLattice(G, basis=B)
        Lattice of degree 2 and rank 1 over Integer Ring
        Basis matrix:
        [1 1]
        Inner product matrix:
        [0 1]
        [1 0]
        sage: IntegralLattice(["A", 3], [[1,1,1]])
        Lattice of degree 3 and rank 1 over Integer Ring
        Basis matrix:
        [1 1 1]
        Inner product matrix:
        [ 2 -1  0]
        [-1  2 -1]
        [ 0 -1  2]
        sage: IntegralLattice(4, [[1,1,1,1]])
        Lattice of degree 4 and rank 1 over Integer Ring
        Basis matrix:
        [1 1 1 1]
        Inner product matrix:
        [1 0 0 0]
        [0 1 0 0]
        [0 0 1 0]
        [0 0 0 1]
        sage: IntegralLattice("A2", [[1,1]])
        Lattice of degree 2 and rank 1 over Integer Ring
        Basis matrix:
        [1 1]
        Inner product matrix:
        [ 2 -1]
        [-1  2]

    TESTS::

        sage: IntegralLattice(["A", 1, 1])
        Traceback (most recent call last):
        ...
        ValueError: lattices must be nondegenerate; use FreeQuadraticModule instead
        sage: IntegralLattice(["D", 3, 1])
        Traceback (most recent call last):
        ...
        ValueError: lattices must be nondegenerate; use FreeQuadraticModule instead
    """
    if is_Matrix(data):
        inner_product_matrix = data
    elif isinstance(data, Integer):
        inner_product_matrix = matrix.identity(ZZ, data)
    elif data == "U" or data == "H":
        inner_product_matrix = matrix([[0,1],[1,0]])
    else:
        inner_product_matrix = CartanMatrix(data)
    if basis is None:
        basis = matrix.identity(ZZ, inner_product_matrix.ncols())
    if inner_product_matrix != inner_product_matrix.transpose():
        raise ValueError("the inner product matrix must be symmetric\n%s"
                         % inner_product_matrix)

    A = FreeQuadraticModule(ZZ,
                            inner_product_matrix.ncols(),
                            inner_product_matrix=inner_product_matrix)
    return FreeQuadraticModule_integer_symmetric(ambient=A,
                                                 basis=basis,
                                                 inner_product_matrix=inner_product_matrix,
                                                 already_echelonized=False)

###############################################################################
#
# Base class for Lattices
#
###############################################################################

class FreeQuadraticModule_integer_symmetric(FreeQuadraticModule_submodule_with_basis_pid):
    r"""
    This class represents non-degenerate, integral,
    symmetric free quadratic `\ZZ`-modules.

    INPUT:

    - ``ambient`` -- an ambient free quadratic module
    - ``basis`` -- a list of elements of ambient or a matrix
    - ``inner_product_matrix`` -- a symmetric matrix over the rationals

    EXAMPLES::

        sage: IntegralLattice("U",basis=[vector([1,1])])
        Lattice of degree 2 and rank 1 over Integer Ring
        Basis matrix:
        [1 1]
        Inner product matrix:
        [0 1]
        [1 0]
    """
    def __init__(self, ambient, basis, inner_product_matrix,
                 check=True, already_echelonized=False):
        r"""
        Create the integral lattice spanned by ``basis`` in the ambient space.

        TESTS::

            sage: L = IntegralLattice("U")
            sage: TestSuite(L).run()
        """
        FreeQuadraticModule_submodule_with_basis_pid.__init__(
                                        self,
                                        ambient,
                                        basis,
                                        inner_product_matrix,
                                        check=check,
                                        already_echelonized=already_echelonized)
        if self.determinant() == 0:
            raise ValueError("lattices must be nondegenerate; "
                            "use FreeQuadraticModule instead")
        if self.gram_matrix().base_ring() is not ZZ:
            if self.gram_matrix().denominator() != 1:
                raise ValueError("lattices must be integral; "
                            "use FreeQuadraticModule instead")

    def _repr_(self):
        r"""
        The print representation of this lattice.

        EXAMPLES::

            sage: A2 = IntegralLattice("A2")
            sage: A2
            Lattice of degree 2 and rank 2 over Integer Ring
            Basis matrix:
            [1 0]
            [0 1]
            Inner product matrix:
            [ 2 -1]
            [-1  2]
        """
        if self.is_sparse():
            s = "Sparse lattice of degree %s and rank %s over %s\n"%(
                self.degree(), self.rank(), self.base_ring()) + \
                "Basis matrix:\n%s\n" % self.basis_matrix() + \
                "Inner product matrix:\n%s" % self.inner_product_matrix()
        else:
            s = "Lattice of degree %s and rank %s over %s\n"%(
                self.degree(), self.rank(), self.base_ring()) + \
                "Basis matrix:\n%s\n" % self.basis_matrix() + \
                "Inner product matrix:\n%s" % self.inner_product_matrix()
        return s

    def is_even(self):
        r"""
        Return whether the diagonal entries of the Gram matrix are even.

        EXAMPLES::

            sage: G = Matrix(ZZ,2,2,[-1,1,1,2])
            sage: L = IntegralLattice(G)
            sage: L.is_even()
            False
            sage: L = IntegralLattice("A2")
            sage: L.is_even()
            True
        """
        return all(d % 2 == 0 for d in self.gram_matrix().diagonal())

    def dual_lattice(self):
        r"""
        Return the dual lattice as a :class:`FreeQuadraticModule`

        Let `L` be a lattice. Its dual lattice is

        .. MATH::

            L^\vee = \{x \in L \otimes \QQ :  (x, l) \in \ZZ \; \forall l \in L \}.

        EXAMPLES::

            sage: L = IntegralLattice("A2")
            sage: Ldual=L.dual_lattice()
            sage: Ldual
            Free module of degree 2 and rank 2 over Integer Ring
            Echelon basis matrix:
            [1/3 2/3]
            [  0   1]

        Since our lattices are always integral, a lattice is contained in its dual::

            sage: L.is_submodule(Ldual)
            True
        """
        return self.span(self.gram_matrix().inverse()*self.basis_matrix())

    def discriminant_group(self, s=0):
        r"""
        Return the discriminant group `L^\vee / L` of this lattice.

        INPUT:

        - ``s`` -- an integer (default: 0)

        OUTPUT:

        The `s` primary part of the discriminant group.
        If `s=0`, returns the whole discriminant group.

        EXAMPLES::

            sage: L = IntegralLattice(Matrix(ZZ,2,2,[2,1,1,-2])*2)
            sage: L.discriminant_group()
            Finite quadratic module over Integer Ring with invariants (2, 10)
            Gram matrix of the quadratic form with values in Q/2Z:
            [  1 1/2]
            [1/2 9/5]
            sage: L.discriminant_group(2)
            Finite quadratic module over Integer Ring with invariants (2, 2)
            Gram matrix of the quadratic form with values in Q/2Z:
            [  1 1/2]
            [1/2   1]
            sage: L.discriminant_group(5)
            Finite quadratic module over Integer Ring with invariants (5,)
            Gram matrix of the quadratic form with values in Q/2Z:
            [6/5]

        TESTS::

            sage: L = IntegralLattice("H")
            sage: L.discriminant_group()
            Finite quadratic module over Integer Ring with invariants ()
            Gram matrix of the quadratic form with values in Q/2Z:
            []
        """
        from sage.modules.torsion_quadratic_module import TorsionQuadraticModule
        D = TorsionQuadraticModule(self.dual_lattice(), self)
        d = D.annihilator().gen()
        a = d.prime_to_m_part(s)
        Dp_gens = [a*g for g in D.gens()]
        return D.submodule(Dp_gens)

    def signature(self):
        r"""
        Return the signature of this lattice, which is defined as
        the difference between the number of positive eigenvalues and
        the number of negative eigenvalues in the Gram matrix.

        EXAMPLES::

            sage: U = IntegralLattice("U")
            sage: U.signature()
            0
        """
        from sage.quadratic_forms.quadratic_form import QuadraticForm
        return QuadraticForm(QQ, self.gram_matrix()).signature()

    def signature_pair(self):
        r"""
        Return the signature tuple `(n_+,n_-)` of this lattice.

        Here `n_+` (resp. `n_-`) is the number of positive (resp. negative)
        eigenvalues of the Gram matrix.

        EXAMPLES::


            sage: A2 = IntegralLattice("A2")
            sage: A2.signature_pair()
            (2, 0)
        """
        from sage.quadratic_forms.quadratic_form import QuadraticForm
        return QuadraticForm(QQ, self.gram_matrix()).signature_vector()[:2]

    def direct_sum(self, M):
        r"""
        Return the direct sum of this lattice with ``M``.

        INPUT:

        - ``M`` -- a module over `\ZZ`

        EXAMPLES::

            sage: A = IntegralLattice(1)
            sage: A.direct_sum(A)
            Lattice of degree 2 and rank 2 over Integer Ring
            Basis matrix:
            [1 0]
            [0 1]
            Inner product matrix:
            [1|0]
            [-+-]
            [0|1]
        """
        IM = matrix.block_diagonal([self.inner_product_matrix(),
                                    M.inner_product_matrix()])
        ambient = FreeQuadraticModule(ZZ,
                                      self.degree() + M.degree(),
                                    inner_product_matrix=IM)
        smzero = matrix.zero(self.rank(), M.degree())
        mszero = matrix.zero(M.rank(), self.degree())
        basis = self.basis_matrix().augment(smzero).stack(
                            mszero.augment(M.basis_matrix()))
        ipm = ambient.inner_product_matrix()
        return FreeQuadraticModule_integer_symmetric(ambient=ambient,
                                                     basis=basis,
                                                     inner_product_matrix=ipm,
                                                     already_echelonized=False)

    def is_primitive(self, M):
        r"""
        Return whether ``M`` is a primitive submodule of this lattice.

        A `\ZZ`-submodule ``M`` of a `\ZZ`-module ``L`` is called primitive if
        the quotient ``L/M`` is torsion free.

        INPUT:

        - ``M`` -- a submodule of this lattice

        EXAMPLES::

            sage: U = IntegralLattice("U")
            sage: L1 = U.span([vector([1,1])])
            sage: L2 = U.span([vector([1,-1])])
            sage: U.is_primitive(L1)
            True
            sage: U.is_primitive(L2)
            True
            sage: U.is_primitive(L1+L2)
            False

        We can also compute the index::

            sage: (L1+L2).index_in(U)
            2
        """
        return (gcd((self/M).invariants()) == 0)

    def orthogonal_complement(self, M):
        r"""
        Return the orthogonal complement of ``M`` in this lattice.

        INPUT:

        - ``M`` -- a module in the same ambient space or
          a list of elements of the ambient space

        EXAMPLES::

            sage: H5 = Matrix(ZZ,2,[2,1,1,-2])
            sage: L = IntegralLattice(H5)
            sage: S = L.span([vector([1,1])])
            sage: L.orthogonal_complement(S)
            Lattice of degree 2 and rank 1 over Integer Ring
            Basis matrix:
            [1 3]
            Inner product matrix:
            [ 2  1]
            [ 1 -2]

            sage: L = IntegralLattice(2)
            sage: L.orthogonal_complement([vector(ZZ,[1,0])])
            Lattice of degree 2 and rank 1 over Integer Ring
            Basis matrix:
            [0 1]
            Inner product matrix:
            [1 0]
            [0 1]
        """
        from sage.modules.free_module import FreeModule_generic
        if not isinstance(M,FreeModule_generic):
            M = self.span(M)
        elif M.ambient_vector_space() != self.ambient_vector_space():
            raise ValueError("M must have the same "
                             "ambient vector space as this lattice")

        K = (self.inner_product_matrix() * M.basis_matrix().transpose()).kernel()
        K = self.span(K.basis())
        K = K.base_extend(QQ)
        return self.sublattice(self.intersection(K).basis())

    def sublattice(self, basis):
        r"""
        Return the sublattice spanned by ``basis``.

        INPUT:

        - ``basis`` -- A list of elements of this lattice.

        EXAMPLES::

            sage: U = IntegralLattice("U")
            sage: S = U.sublattice([vector([1,1])])
            sage: S
            Lattice of degree 2 and rank 1 over Integer Ring
            Basis matrix:
            [1 1]
            Inner product matrix:
            [0 1]
            [1 0]
            sage: U.sublattice([vector([1,-1])/2])
            Traceback (most recent call last):
            ...
            ValueError: lattices must be integral; use FreeQuadraticModule instead
            sage: S.sublattice([vector([1,-1])])
            Traceback (most recent call last):
            ...
            ValueError: the basis (= [(1, -1)]) does not span a submodule
        """
        M = FreeQuadraticModule_integer_symmetric(
            ambient=self.ambient_module(), basis=basis,
            inner_product_matrix=self.inner_product_matrix(),
            already_echelonized=False)
        if not M.is_submodule(self):
            raise ValueError("the basis (= %s) does not span "
                             "a submodule" % basis)
        return M

    def overlattice(self, gens):
        r"""
        Return the lattice spanned by this lattice and ``gens``.

        INPUT:

        - ``gens`` -- a list of elements or a rational matrix

        EXAMPLES::

            sage: L = IntegralLattice(Matrix(ZZ,2,2,[2,0,0,2]))
            sage: M = L.overlattice([vector([1,1])/2])
            sage: M.gram_matrix()
            [1 1]
            [1 2]
        """
        basis = (self + self.span(gens)).basis()
        return FreeQuadraticModule_integer_symmetric(
            ambient=self.ambient_module(), basis=basis,
            inner_product_matrix=self.inner_product_matrix(),
            already_echelonized=False)

    def genus(self):
        r"""
        Return the genus of this lattice.

        EXAMPLES::

            sage: L = IntegralLattice("U")
            sage: L.genus()
            Genus of
            [0 1]
            [1 0]
            Genus symbol at 2:    1^2
        """
        from sage.quadratic_forms.genera.genus import Genus
        return Genus(self.gram_matrix())
        
    def mul(self, d):
        r"""
        Return the lattice defined by the inner product matrix of ``self`` 
        multiplied by ``d``.
        
        INPUT::

        - ``d`` -- an integer

        EXAMPLES::

            sage: L = IntegralLattice("A4")
            sage: L.mul(3)
            Lattice of degree 4 and rank 4 over Integer Ring
            Basis matrix:
            [1 0 0 0]
            [0 1 0 0]
            [0 0 1 0]
            [0 0 0 1]
            Inner product matrix:
            [ 6 -3  0  0]
            [-3  6 -3  0]
            [ 0 -3  6 -3]
            [ 0  0 -3  6]

            sage: L = IntegralLattice(3,[[2,1,0],[0,1,1]])
            sage: L
            Lattice of degree 3 and rank 2 over Integer Ring
            Basis matrix:
            [2 1 0]
            [0 1 1]
            Inner product matrix:
            [1 0 0]
            [0 1 0]
            [0 0 1]
            sage: L.mul(1)
            Lattice of degree 2 and rank 2 over Integer Ring
            Basis matrix:
            [1 0]
            [0 1]
            Inner product matrix:
            [5 1]
            [1 2]

        """
        return IntegralLattice(d*self.gram_matrix())

def PrimitiveExtension(Lattices, glue):
    r"""
    Return the overlattice of L1+L2 spanned by the elements of the discriminant group
    given by ``glue``
    
    INPUT::
    
    - ``Lattices`` - a list of lattices ``[L_1,...,L_n]`` 
    - ``glue`` - a list where the elements are lists in the form ``[g_1,...,g_n]`` where ``g_i`` is an
      element of the discriminant group of ``L_i``
      
    EXAMPLES::
    
        
        sage: from sage.modules.free_quadratic_module_integer_symmetric import PrimitiveExtension
        sage: L1 = IntegralLattice(matrix([[4]]))
        sage: g1 = L1.discriminant_group().gens()[0]
        sage: glue = [[2*g1]]
        sage: PrimitiveExtension([L1],glue)
        (Lattice of degree 1 and rank 1 over Integer Ring
         Basis matrix:
         [1]
         Inner product matrix:
         [1], [Free module morphism defined by the matrix
          [2]
          Domain: Lattice of degree 1 and rank 1 over Integer Ring
          Basis matrix:
          [1]
          Inner product matrix:
          [4]
          Codomain: Lattice of degree 1 and rank 1 over Integer Ring
          Basis matrix:
          [1]
          Inner product matrix:
          [1]])
        
        sage: from sage.modules.free_quadratic_module_integer_symmetric import PrimitiveExtension
        sage: L1 = IntegralLattice([[2]])
        sage: L2 = IntegralLattice([[2]])
        sage: AL1 = L1.discriminant_group()
        sage: AL2 = L2.discriminant_group()         
        sage: AL1            
        Finite quadratic module over Integer Ring with invariants (2,)
        Gram matrix of the quadratic form with values in Q/2Z:
        [1/2]                                   
        sage: g1 = L1.discriminant_group().gens()[0] 
        sage: g2 = L2.discriminant_group().gens()[0]      
        sage: glue = [[g1,g2]]                       
        sage: PrimitiveExtension([L1,L2],glue)
        (Lattice of degree 2 and rank 2 over Integer Ring
         Basis matrix:
         [1 0]
         [0 1]
         Inner product matrix:
         [1 1]
         [1 2], [Free module morphism defined by the matrix
          [ 2 -1]
          Domain: Lattice of degree 1 and rank 1 over Integer Ring
          Basis matrix:
          [1]
          Inner product matrix:
          [2]
          Codomain: Lattice of degree 2 and rank 2 over Integer Ring
          Basis matrix:
          [1 0]
          [0 1]
          Inner product matrix:
          [1 1]
          [1 2], Free module morphism defined by the matrix
          [0 1]
          Domain: Lattice of degree 1 and rank 1 over Integer Ring
          Basis matrix:
          [1]
          Inner product matrix:
          [2]
          Codomain: Lattice of degree 2 and rank 2 over Integer Ring
          Basis matrix:
          [1 0]
          [0 1]
          Inner product matrix:
          [1 1]
          [1 2]])

        sage: from sage.modules.free_quadratic_module_integer_symmetric import PrimitiveExtension
        sage: L1 = IntegralLattice("A4")
        sage: L2 = IntegralLattice("A4")
        sage: g1 = L1.discriminant_group().gens()[0]
        sage: g2 = L2.discriminant_group().gens()[0]
        sage: glue = [[g1,2*g2]]
        sage: [V,phi] = PrimitiveExtension([L1,L2],glue)
        sage: V
        Lattice of degree 8 and rank 8 over Integer Ring
        Basis matrix:
        [1 0 0 0 0 0 0 0]
        [0 1 0 0 0 0 0 0]
        [0 0 1 0 0 0 0 0]
        [0 0 0 1 0 0 0 0]
        [0 0 0 0 1 0 0 0]
        [0 0 0 0 0 1 0 0]
        [0 0 0 0 0 0 1 0]
        [0 0 0 0 0 0 0 1]
        Inner product matrix:
        [ 2  0  0  1  0  1 -1  1]
        [ 0  2 -1  0  0  0  0  0]
        [ 0 -1  2 -1  0  0  0  0]
        [ 1  0 -1  2  0  0  0  0]
        [ 0  0  0  0  2 -1  0  0]
        [ 1  0  0  0 -1  2 -1  0]
        [-1  0  0  0  0 -1  2 -1]
        [ 1  0  0  0  0  0 -1  2]
        sage: V.sublattice(phi[0].image().basis_matrix())
        Lattice of degree 8 and rank 4 over Integer Ring
        Basis matrix:
        [ 5  0  0  0 -2 -4 -1 -3]
        [ 0  1  0  0  0  0  0  0]
        [ 0  0  1  0  0  0  0  0]
        [ 0  0  0  1  0  0  0  0]
        Inner product matrix:
        [ 2  0  0  1  0  1 -1  1]
        [ 0  2 -1  0  0  0  0  0]
        [ 0 -1  2 -1  0  0  0  0]
        [ 1  0 -1  2  0  0  0  0]
        [ 0  0  0  0  2 -1  0  0]
        [ 1  0  0  0 -1  2 -1  0]
        [-1  0  0  0  0 -1  2 -1]
        [ 1  0  0  0  0  0 -1  2]
        
        sage: from sage.modules.free_quadratic_module_integer_symmetric import PrimitiveExtension
        sage: D4 = IntegralLattice("D4")
        sage: D4.discriminant_group()
        Finite quadratic module over Integer Ring with invariants (2, 2)
        Gram matrix of the quadratic form with values in Q/2Z:
        [  1 1/2]
        [1/2   1] 
        sage: L2 = IntegralLattice(2).mul(2)
        sage: L2.discriminant_group()
        Finite quadratic module over Integer Ring with invariants (2, 2)
        Gram matrix of the quadratic form with values in Q/2Z:
        [1/2   0]
        [  0 1/2]
        sage: g1 = D4.discriminant_group().gens()[0]
        sage: g2 = L2.discriminant_group().gens()[0]+L2.discriminant_group().gens()[1]
        sage: [D6,phi] = PrimitiveExtension([D4,L2],[[g1,g2]])
        sage: AD6 = D6.discriminant_group()
        sage: AD6.normal_form()
        Finite quadratic module over Integer Ring with invariants (2, 2)
        Gram matrix of the quadratic form with values in Q/2Z:
        [3/2   0]
        [  0 3/2]
        sage: [f1,g1] = AD6.normal_form().gens()
        sage: [f2,g2] = L2.discriminant_group().gens()
        sage: [E8,psi] = PrimitiveExtension([D6,L2],[[f1,f2],[g1,g2]])
        sage: D4embed = E8.sublattice(psi[0](phi[0].image()).basis_matrix())
        sage: D4embed
        Lattice of degree 8 and rank 4 over Integer Ring
        Basis matrix:
        [ 2  0  0  0  0 -1  0 -1]
        [ 0  1  0  0  0  0  0  0]
        [ 0  0  2  0 -2  0  1  1]
        [ 0  0  0  1  0  0  0  0]
        Inner product matrix:
        [ 2 -1  1  1  1  1  0  1]
        [-1  2 -1 -1  0  0  0  0]
        [ 1 -1  2  1  1  1  0  0]
        [ 1 -1  1  2  0  0  0  0]
        [ 1  0  1  0  2  1  1  1]
        [ 1  0  1  0  1  2  0  0]
        [ 0  0  0  0  1  0  2  0]
        [ 1  0  0  0  1  0  0  2]

        sage: from sage.modules.free_quadratic_module_integer_symmetric import PrimitiveExtension
        sage: A7 = IntegralLattice("A7")
        sage: D5 = IntegralLattice("D5")
        sage: gA7 = A7.discriminant_group().gens()[0]
        sage: gD5 = D5.discriminant_group().gens()[0]
        sage: [L,phi] = PrimitiveExtension([A7,A7,D5,D5],[[gA7,gA7,gD5,2*gD5],[gA7,7*gA7,2*gD5,gD5]])
        sage: L.determinant()
        1       
    """   
    N = len(Lattices)
    GramList = [L_i.gram_matrix() for L_i in Lattices]
    M = matrix.block_diagonal(GramList)
    L = IntegralLattice(M)
    Dims = [L_i.dimension() for L_i in Lattices]
    SumDims = [sum(Dims[:i]) for i in range(len(Dims)+1)]
    EmbeddingList = [L.submodule(L.basis()[SumDims[i]:SumDims[i+1]]) for i in range(N)]
    #It calculates the direct sum of L_i
    AL = L.discriminant_group()
    Discriminants = [L_i.discriminant_group() for L_i in Lattices]
    Bases = [matrix.zero(SumDims[i],Dims[i]).stack(matrix.identity(Dims[i])).stack(
            matrix.zero(SumDims[-1]-SumDims[i+1],Dims[i])) for i in range(N)]
    vect_phi = [[AL(Bases[i]*(Discriminants[i].gen(x).lift())) for x in 
               range(Discriminants[i].ngens())] for i in range(N)]
    phi_bar = [Discriminants[i].hom(vect_phi[i]) for i in range(N)]
    #It defines the injection from the discriminant groupa AL1,AL2 to AL
    generators = [sum(phi_bar[i](g[i]) for i in range(N)) for g in glue]
    HL = AL.submodule(generators)
    #It takes the submodule spanned by ``glue``
    if (HL.gram_matrix_bilinear()!=0):
        raise ValueError("the generators (= %s) does not span "
                         "a totally isotropic submodule" % generators)
    V = L.overlattice(HL.V().gens())
    Vnew = V.mul(1)
    G = V.basis_matrix().inverse()
    HomSpaces = [Hom(Lattices[i],Vnew) for i in range(N)]
    phi = [HomSpaces[i](Bases[i].transpose()*G) for i in range(N)]
    return (Vnew,phi)
