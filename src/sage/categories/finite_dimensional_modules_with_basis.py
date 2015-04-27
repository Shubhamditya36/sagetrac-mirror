r"""
Finite dimensional modules with basis
"""
#*****************************************************************************
#  Copyright (C) 2008 Teresa Gomez-Diaz (CNRS) <Teresa.Gomez-Diaz@univ-mlv.fr>
#                2011 Nicolas M. Thiery <nthiery at users.sf.net>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#                  http://www.gnu.org/licenses/
#******************************************************************************

import operator
from sage.categories.category_with_axiom import CategoryWithAxiom_over_base_ring

class FiniteDimensionalModulesWithBasis(CategoryWithAxiom_over_base_ring):
    """
    The category of finite dimensional modules with a distinguished basis

    EXAMPLES::

      sage: C = FiniteDimensionalModulesWithBasis(ZZ); C
      Category of finite dimensional modules with basis over Integer Ring
      sage: sorted(C.super_categories(), key=str)
      [Category of finite dimensional modules over Integer Ring,
       Category of modules with basis over Integer Ring]
      sage: C is Modules(ZZ).WithBasis().FiniteDimensional()
      True

    TESTS::

        sage: TestSuite(C).run()
    """

    class ParentMethods:

        def matrix(self, vectors, base_ring=None, sparse=False, columns=False):
            r"""
            Return the matrix corresponding to a collection of vectors.

            INPUT:

            - ``vectors`` -- a list of elements of ``self``
            - ``sparse`` -- a boolean (default: False):
              whether to return a sparse matrix
            - ``column`` -- a boolean (default: False):
              whether to build a column matrix instead of a row matrix

            EXAMPLES::

                sage: F = CombinatorialFreeModule(QQ, ['a','b','c','d'])
                sage: vectors = [F.an_element(), F.zero(), F.monomial('c')]; vectors
                [2*B['a'] + 2*B['b'] + 3*B['c'], 0, B['c']]
                sage: m = F.matrix(vectors, sparse=True); m
                [2 2 3 0]
                [0 0 0 0]
                [0 0 1 0]
                sage: m.parent()
                Full MatrixSpace of 3 by 4 sparse matrices over Rational Field

            Constructing a sparse matrix with this method is currently
            really much faster than building it from sparse vectors;
            see :trac:``::

                sage: n = 10^3; F = CombinatorialFreeModule(QQ, range(n)); vectors = [F.zero()]*n
                sage: %timeit m = F.matrix(vectors, sparse=True) # not tested
                The slowest run ...
                1000 loops, best of 3: 466 µs per loop
                sage: %timeit m = matrix(QQ, [v._vector_(sparse=True) for v in vectors], sparse=True) # not tested
                1 loops, best of 3: 1.19 s per loop
            """
            from sage.matrix.matrix_space import MatrixSpace
            assert not columns
            if not isinstance(vectors, (list, tuple)):
                vectors = list(vectors)
            if base_ring is None:
                base_ring = self.base_ring()
            M = MatrixSpace(base_ring, len(vectors), self.dimension(),
                            sparse=sparse)
            if sparse:
                self.get_order()
                rank = self._rank_basis
                data = {(i, rank(j)): c
                          for i,v in enumerate(vectors)
                          for j,c in v}
            else:
                data = [v._vector_() for v in vectors]
            return M.matrix(data,
                            coerce=base_ring is not self.base_ring(), copy=False)

        def annihilator(self, S, action=operator.mul, side='right', category=None):
            r"""
            Return the annihilator of a finite set.

            INPUT:

            - ``S`` -- a finite set

            - ``action`` -- a function (default: :obj:`operator.mul`)

            - ``side`` -- 'left' or 'right' (default: 'right')

            - ``category`` -- a category

            Assumptions:

            - ``action`` takes elements of ``self`` as first argument
              and elements of ``S`` as second argument;

            - The codomain is any vector space, and ``action`` is
              linear on its first argument; typically it is bilinear;

            - If ``side`` is 'left', this is reversed.

            OUTPUT:

            The subspace of the elements `x` of ``self`` such that
            ``action(x,s) = 0`` for all `s\in S`. If ``side`` is
            'left' replace the above equation by ``action(s,x) = 0``.

            If ``self`` is a ring, ``action`` an action of ``self`` on
            a module `M` and `S` is a subset of `M`, we recover the
            :Wikipedia:`Annihilator_%28ring_theory%29`. Similarly this
            can be used to compute torsion or orthogonals.

            .. SEEALSO:: :meth:`annihilator_basis` for lots of examples.

            EXAMPLES::

                sage: F = FiniteDimensionalAlgebrasWithBasis(QQ).example(); F
                An example of a finite dimensional algebra with basis:
                the path algebra of the Kronecker quiver
                (containing the arrows a:x->y and b:x->y) over Rational Field
                sage: x,y,a,b = F.basis()
                sage: A = F.annihilator([a + 3*b + 2*y]); A
                Free module generated by {0} over Rational Field
                sage: [b.lift() for b in A.basis()]
                [-1/2*a - 3/2*b + x]

            The category can be used to specify other properties of
            this subspace, like that this is a subalgebra::

                sage: center = F.annihilator(F.basis(), F.bracket,
                ....:                        category=Algebras(QQ).Subobjects())
                sage: (e,) = center.basis()
                sage: e.lift()
                x + y
                sage: e * e == e
                True

            Taking annihilator is order reversing for inclusion::

                sage: A   = F.annihilator([]);    A  .rename("A")
                sage: Ax  = F.annihilator([x]);   Ax .rename("Ax")
                sage: Ay  = F.annihilator([y]);   Ay .rename("Ay")
                sage: Axy = F.annihilator([x,y]); Axy.rename("Axy")
                sage: P = Poset(([A, Ax, Ay, Axy], attrcall("is_submodule")))
                sage: sorted(P.cover_relations(), key=str)
                [[Ax, A], [Axy, Ax], [Axy, Ay], [Ay, A]]
            """
            return self.submodule(self.annihilator_basis(S, action, side),
                                  already_echelonized=True,
                                  category=category)

        def annihilator_basis(self, S, action=operator.mul, side='right'):
            """
            Return a basis of the annihilator of a finite set of elements.

            INPUT:

            - ``S`` -- a finite set of objects

            - ``action`` -- a function (default: :obj:`operator.mul`)

            - ``side`` -- 'left' or 'right' (default: 'right'):
              on which side of ``self`` the elements of `S` acts.

            See :meth:`annihilator` for the assumptions and definition
            of the annihilator.

            EXAMPLES:

            By default, the action is the standard `*` operation. So
            our first example is about an algebra::

                sage: F = FiniteDimensionalAlgebrasWithBasis(QQ).example(); F
                An example of a finite dimensional algebra with basis:
                the path algebra of the Kronecker quiver
                (containing the arrows a:x->y and b:x->y) over Rational Field
                sage: x,y,a,b = F.basis()

            In this algebra, multiplication on the right by `x`
            annihilates all basis elements but `x`::

                sage: x*x, y*x, a*x, b*x
                (x, 0, 0, 0)

            So the annihilator is the subspace spanned by `y`, `a`, and `b`::

                sage: F.annihilator_basis([x])
                [y, a, b]

            The same holds for `a` and `b`::

                sage: x*a, y*a, a*a, b*a
                (a, 0, 0, 0)
                sage: F.annihilator_basis([a])
                [y, a, b]

            On the other hand, `y` annihilates only `x`::

                sage: F.annihilator_basis([y])
                [x]

            Here is a non trivial annihilator::

                sage: F.annihilator_basis([a + 3*b + 2*y])
                [-1/2*a - 3/2*b + x]

            Let's check it::

                sage: (-1/2*a - 3/2*b + x) * (a + 3*b + 2*y)
                0

            Doing the same calculations on the left exchanges the
            roles of `x` and `y`::

                sage: F.annihilator_basis([y], side="left")
                [x, a, b]
                sage: F.annihilator_basis([a], side="left")
                [x, a, b]
                sage: F.annihilator_basis([b], side="left")
                [x, a, b]
                sage: F.annihilator_basis([x], side="left")
                [y]
                sage: F.annihilator_basis([a+3*b+2*x], side="left")
                [-1/2*a - 3/2*b + y]

            By specifying an inner product, this method can be used to
            compute the orthogonal of a subspace::

                sage: x,y,a,b = F.basis()
                sage: def scalar(u,v): return vector([sum(u[i]*v[i] for i in F.basis().keys())])
                sage: F.annihilator_basis([x+y, a+b], scalar)
                [x - y, a - b]

            By specifying the standard Lie bracket as action, one can
            compute the commutator of a subspace of `F`::

                sage: F.annihilator_basis([a+b], action=F.bracket)
                [x + y, a, b]

            In particular one can compute a basis of the center of the
            algebra. In our example, it is reduced to the identity::

                sage: F.annihilator_basis(F.algebra_generators(), action=F.bracket)
                [x + y]

            But see also
            :meth:`FiniteDimensionalAlgebrasWithBasis.ParentMethods.center_basis`.
            """
            # TODO: optimize this!
            from sage.matrix.constructor import matrix
            if side == 'right':
                action_left = action
                action = lambda b,s: action_left(s, b)

            mat = matrix(self.base_ring(), self.dimension(), 0)
            for s in S:
                mat = mat.augment(matrix(self.base_ring(),
                                         [action(s, b)._vector_() for b in self.basis()]))
            return map(self.from_vector, mat.left_kernel().basis())

        def quotient_module(self, submodule, check=True, already_echelonized=False, category=None):
            r"""
            Construct the quotient module ``self``/``submodule``.

            INPUT:

            - ``submodule`` -- a submodule with basis of ``self``, or
              something that can be turned into one via
              ``self.submodule(submodule)``.

            - ``check``, ``already_echelonized`` -- passed down to
              :meth:`ModulesWithBasis.ParentMethods.submodule`.

            .. WARNING::

                At this point, this only supports quotients by free
                submodules admitting a basis in unitriangular echelon
                form. In this case, the quotient is also a free
                module, with a basis consisting of the retract of a
                subset of the basis of ``self``.

            EXAMPLES::

                sage: X = CombinatorialFreeModule(QQ, range(3), prefix="x")
                sage: x = X.basis()
                sage: Y = X.quotient_module([x[0]-x[1], x[1]-x[2]], already_echelonized=True)
                sage: Y.print_options(prefix='y'); Y
                Free module generated by {2} over Rational Field
                sage: y = Y.basis()
                sage: y[2]
                y[2]
                sage: y[2].lift()
                x[2]
                sage: Y.retract(x[0]+2*x[1])
                3*y[2]

            .. SEEALSO::

                 - :meth:`Modules.WithBasis.ParentMethods.submodule`
                 - :meth:`Rings.ParentMethods.quotient`
                 - :class:`sage.modules.with_basis.subquotient.QuotientModuleWithBasis`
            """
            from sage.modules.with_basis.subquotient import SubmoduleWithBasis, QuotientModuleWithBasis
            if not isinstance(submodule, SubmoduleWithBasis):
                submodule = self.submodule(submodule, check=check,
                                           already_echelonized=already_echelonized)
            return QuotientModuleWithBasis(submodule, category=category)

    class ElementMethods:
        pass

    class MorphismMethods:
        def matrix(self, base_ring=None, side="left", sparse=False):
            r"""
            Return the matrix of this morphism in the distinguished
            bases of the domain and codomain.

            INPUT:

            - ``base_ring`` -- a ring (default: ``None``, meaning the
              base ring of the codomain)

            - ``side`` -- "left" or "right" (default: "left")

            - ``sparse`` -- a boolean (default: False)

            If ``side`` is "left", this morphism is considered as
            acting on the left; i.e. each column of the matrix
            represents the image of an element of the basis of the
            domain.

            The order of the rows and columns matches with the order
            in which the bases are enumerated.

            .. SEEALSO:: :func:`Modules.WithBasis.ParentMethods.module_morphism`

            EXAMPLES::

                sage: X = CombinatorialFreeModule(ZZ, [1,2]); x = X.basis()
                sage: Y = CombinatorialFreeModule(ZZ, [3,4]); y = Y.basis()
                sage: phi = X.module_morphism(on_basis = {1: y[3] + 3*y[4], 2: 2*y[3] + 5*y[4]}.__getitem__,
                ...                           codomain = Y)
                sage: phi.matrix()
                [1 2]
                [3 5]
                sage: phi.matrix(side="right")
                [1 3]
                [2 5]
                sage: phi.matrix(sparse=True)
                [1 2]
                [3 5]

                sage: phi.matrix().parent()
                Full MatrixSpace of 2 by 2 dense matrices over Integer Ring
                sage: phi.matrix(QQ).parent()
                Full MatrixSpace of 2 by 2 dense matrices over Rational Field
                sage: phi.matrix(sparse=True).parent()
                Full MatrixSpace of 2 by 2 sparse matrices over Integer Ring

            The resulting matrix is immutable::

                sage: phi.matrix().is_mutable()
                False

            The zero morphism has a zero matrix::

                sage: Hom(X,Y).zero().matrix()
                [0 0]
                [0 0]

            .. TODO::

                Add support for morphisms where the codomain has a
                different base ring than the domain::

                    sage: Y = CombinatorialFreeModule(QQ, [3,4]); y = Y.basis()
                    sage: phi = X.module_morphism(on_basis = {1: y[3] + 3*y[4], 2: 2*y[3] + 5/2*y[4]}.__getitem__,
                    ...                           codomain = Y)
                    sage: phi.matrix().parent()          # todo: not implemented
                    Full MatrixSpace of 2 by 2 dense matrices over Rational Field

                This currently does not work because, in this case,
                the morphism is just in the category of commutative
                additive groups (i.e. the intersection of the
                categories of modules over `\ZZ` and over `\QQ`)::

                    sage: phi.parent().homset_category()
                    Category of commutative additive semigroups
                    sage: phi.parent().homset_category() # todo: not implemented
                    Category of finite dimensional modules with basis over Integer Ring
            """
            on_basis = self.on_basis()
            basis_keys = self.domain().basis().keys()
            m = self.codomain().matrix([on_basis(x) for x in basis_keys],
                                       base_ring=base_ring,
                                       sparse=sparse)
            if side == "left":
                m = m.transpose()
            m.set_immutable()
            return m

        def __invert__(self):
            """
            Return the inverse morphism of ``self``.

            This is achieved by inverting the ``self.matrix()``.
            An error is raised if ``self`` is not invertible.

            EXAMPLES::

                sage: category = FiniteDimensionalModulesWithBasis(ZZ)
                sage: X = CombinatorialFreeModule(ZZ, [1,2], category = category); X.rename("X"); x = X.basis()
                sage: Y = CombinatorialFreeModule(ZZ, [3,4], category = category); Y.rename("Y"); y = Y.basis()
                sage: phi = X.module_morphism(on_basis = {1: y[3] + 3*y[4], 2: 2*y[3] + 5*y[4]}.__getitem__,
                ...                           codomain = Y, category = category)
                sage: psi = ~phi
                sage: psi
                Generic morphism:
                  From: Y
                  To:   X
                sage: psi.parent()
                Set of Morphisms from Y to X in Category of finite dimensional modules with basis over Integer Ring
                sage: psi(y[3])
                -5*B[1] + 3*B[2]
                sage: psi(y[4])
                2*B[1] - B[2]
                sage: psi.matrix()
                [-5  2]
                [ 3 -1]
                sage: psi(phi(x[1])), psi(phi(x[2]))
                (B[1], B[2])
                sage: phi(psi(y[3])), phi(psi(y[4]))
                (B[3], B[4])

            We check that this function complains if the morphism is not invertible::

                sage: phi = X.module_morphism(on_basis = {1: y[3] + y[4], 2: y[3] + y[4]}.__getitem__,
                ...                           codomain = Y, category = category)
                sage: ~phi
                Traceback (most recent call last):
                ...
                RuntimeError: morphism is not invertible

                sage: phi = X.module_morphism(on_basis = {1: y[3] + y[4], 2: y[3] + 5*y[4]}.__getitem__,
                ...                           codomain = Y, category = category)
                sage: ~phi
                Traceback (most recent call last):
                ...
                RuntimeError: morphism is not invertible
            """
            mat = self.matrix()
            try:
                inv_mat = mat.parent()(~mat)
            except (ZeroDivisionError, TypeError):
                raise RuntimeError, "morphism is not invertible"
            return self.codomain().module_morphism(
                matrix=inv_mat,
                codomain=self.domain(), category=self.category_for())

