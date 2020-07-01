r"""
Vertex Algebra

Let `R` be a commutative ring. A *super vertex algebra* [Kac1997]_ over `R` is
the datum of:

- an `R` super-module `V` called *the space of states*
- an even vector `|0\rangle \in V` called the *vacuum* vector.
- an even endomorphism `T \in End(V)` called the *translation operator*
- a graded bilinear multiplication map

.. MATH::

    V \otimes V \rightarrow V( (z)), \qquad a \otimes b \mapsto Y(a,z)b =:
    \sum_{n \in \ZZ} a_{(n)}b z^{-1-n}.

Subject to the following set of axioms:

- The vacuum axioms:

.. MATH::

    Y(a,z)|0\rangle = a + Ta \cdot z + O(z^2), \qquad Y(|0\rangle,z)a = a,
    \qquad a \in V.

- Translation invariance:

.. MATH::

    [T,Y(a,z)] = \frac{d}{dz} Y(a,z)

- Locality:

.. MATH::

    (z-w)^n Y(a,z)Y(b,w) = (-1)^{p(a)p(b)} (z-w)^n Y(b,w)Y(a,z),
    \qquad a,b \in V, \: n \gg 0,

where `p(a)` is `0` if `a` is even and `1` if `a` is odd. The `\ZZ`-many
products `a_{(n)}b` defined above are called the
*nth*-products. A vertex algebra together with its non-negative nth-products
and its translation operator `T` is a
:mod:`Lie Conformal Algebra<sage.categories.lie_conformal_algebras>`.
The generating function for these non-negative products

.. MATH::

    [a_\lambda b] = \sum_{n \geq 0} \frac{\lambda^n}{n!} a_{(n)} b

is called the *OPE* or the `\lambda`-bracket of `a` and `b`. This forgetful
functor admits a
left adjoint: to each Lie conformal algebra `L` we attach a universal enveloping
vertex algebra `U(L)`. This vertex algebra admits an embedding (when `R` is a
field of characteristic zero) `L \hookrightarrow U(L)` of Lie conformal
algebras.

A vertex algebra is called H-Graded [DSK2006]_ if there exists a diagonalizable
operator `H \in End(V)` such that

.. MATH::

    [H,Y(a,z)] = Y(Ha,z) + z \frac{d}{dz} Y(a,z).

Equivalently, there exists a decomposition `V = \oplus_{\Delta \in \CC}
V_\Delta` such that the nth product becomes graded of degree `-1-n`, that is

.. MATH::

    a_{(n)}b \in V_{p + q - 1 - n} \qquad a \in V_p, b \in V_q, n \in \ZZ.

.. NOTE::

    Although arbitrary gradings are allowed in the literature, we implement here
    only non-negative rational gradings.

In this situation, for `a \in V_p` we define the *shifted nth-product* `a_n b =
a_{(n+p-1)}b`. With this convention, the *shifted nth-product* map `a \otimes b
\mapsto a_n b`  is graded of degree `-n`.

A vertex algebra is called *strongly generated* by a collection of vectors `a^i
\in V` indexed by an ordered set `I`,
if every vector of `V` can be written as a linear combination of vectors
of the form

.. MATH::

    a^{i_1}_{(-j_{1,1})} \cdots a^{i_1}_{(-j_{1,n_1})} a^{i_2}_{(-j_{2,1})}
    \cdots a^{i_k}_{(-j_{k,n_j})} |0\rangle, \qquad i_1 < \ldots < i_k,
    \: j_{i,l} > 0.

A vertex algebra is called *finitely strongly generated* if there is such a set
with a finite `I`, we will call these vertex algebras simply *finitely
generated*

Typical examples of finitely and strongly generated H-Graded vertex algebra
arise as twisted universal enveloping vertex algebras of a finitely generated
H-Graded :mod:`Lie conformal algebras<sage.categories.lie_conformal_algebras>`.
They are described explicitly in terms of the OPE (`\lambda`-brackets) of
their generators:

- The **Virasoro** vertex algebra of central charge `c` is generated by one
  vector `L` with `\lambda`-bracket

  .. MATH::

        [L_\lambda L] = TL + 2 \lambda L + \frac{\lambda^3}{12} c |0\rangle

- The **universal affine** vertex algebra `V^\kappa(\mathfrak{g})` with level
  `\kappa` associated to a finite dimensional
  Lie algebra `\mathfrak{g}` with non-degenerate,
  invariant `R`-bilinear form `\kappa(,)` is generated by `\mathfrak{g}` with
  `\lambda`-bracket of generators given by

  .. MATH::

        [a_\lambda b] = [a,b] + \lambda \kappa(a,b) |0\rangle,
        \qquad a,b \in \mathfrak{g}


- The **Weyl** vertex algebra, or `\beta-\gamma` system has two generators
  `\beta` and
  `\gamma` The only non-trivial brackets among
  generators are

    .. MATH::

        [\beta_\lambda \gamma] = - [\gamma_\lambda \beta] = |0\rangle

- The **Neveu-Schwarz** super vertex algebra of central charge `c` is a super
  vertex algebra which is an extension of the Virasoro vertex
  algebra. It consists of a Virasoro generator `L` as above
  and an *odd* generator `G`. The remaining brackets are given by:

  .. MATH::

        [L_\lambda G] = \left( T + \frac{3}{2} \lambda \right) G \qquad
        [G_\lambda G] = 2 L + \frac{\lambda^2}{3} c |0\rangle

.. SEEALSO::

    :mod:`sage.algebras.vertex_algebras.examples`

Every vertex algebra carries a decreasing filtration
called the *Li standard filtration*
[Li2005]_. It is defined as follows, we define `F^pV` to be the subspace spanned
by vectors of the form

.. MATH::

    a^1_{(-n_1-1)} \cdots a^r_{(-n_r -1)} b, \qquad a^i,b \in V, n_i \in
    \ZZ_{\geq 0}, \: n_1 + \cdots n_r \geq p.

The associated graded `\mathrm{gr}_FV` is a
:mod:`Poisson vertex algebra<sage.categories.poisson_vertex_algebras>`
known as the *quasi-classical limit* or *singular support* of `V`.

EXAMPLES:

The base class for all vertex algebras is :class:`VertexAlgebra`.
All subclasses are called through its method ``__classcall_private__``.
We provide some convenience classes to define named vertex algebras
like :class:`VirasoroVertexAlgebra` and :class:`AffineVertexAlgebra` and
super vertex algebras like :class:`NeveuSchwarzVertexAlgebra` and
:class:`FreeFermionsVertexAlgebra`.

- We create the Universal Virasoro Vertex algebra of central charge
  c=1/2 and perform some basic computations::

    sage: V = vertex_algebras.Virasoro(QQ,1/2); V.inject_variables()
    Defining L
    sage: L*L
    L_-2L_-2|0>
    sage: (L*L).T()
    2*L_-3L_-2|0> + L_-5|0>
    sage: L.bracket(L*L)
    {0: 2*L_-3L_-2|0> + L_-5|0>,
     1: 4*L_-2L_-2|0>,
     2: 3*L_-3|0>,
     3: 17/2*L_-2|0>,
     5: 3/2*|0>}

- We compute its irreducible quotient::

    sage: V.find_singular(6)
    (L_-2L_-2L_-2|0> + 93/64*L_-3L_-3|0> - 33/8*L_-4L_-2|0> - 27/16*L_-6|0>,)
    sage: I = V.ideal(_); I
    ideal of The Virasoro vertex algebra of central charge 1/2 over Rational Field generated by (L_-2L_-2L_-2|0> + 93/64*L_-3L_-3|0> - 33/8*L_-4L_-2|0> - 27/16*L_-6|0>,)
    sage: Q = V.quotient(I); Q
    Quotient of The Virasoro vertex algebra of central charge 1/2 over Rational Field by the ideal generated by (L_-2L_-2L_-2|0> + 93/64*L_-3L_-3|0> - 33/8*L_-4L_-2|0> - 27/16*L_-6|0>,)
    sage: Q.retract(L*(L*L))
    -93/64*L_-3L_-3|0> + 33/8*L_-4L_-2|0> + 27/16*L_-6|0>

- We compute the arc algebra and the classical limit of ``Q``::

    sage: P = Q.arc_algebra(); P
    Quotient of The classical limit of The Virasoro vertex algebra of central charge 1/2 over Rational Field by the ideal generated by (L_2^3,)
    sage: R = Q.classical_limit(); R
    The classical limit of Quotient of The Virasoro vertex algebra of central charge 1/2 over Rational Field by the ideal generated by (L_-2L_-2L_-2|0> + 93/64*L_-3L_-3|0> - 33/8*L_-4L_-2|0> - 27/16*L_-6|0>,)
    sage: P.hilbert_series(10)
    1 + q^2 + q^3 + 2*q^4 + 2*q^5 + 3*q^6 + 3*q^7 + 5*q^8 + 6*q^9 + O(q^10)
    sage: R.hilbert_series(10)
    1 + q^2 + q^3 + 2*q^4 + 2*q^5 + 3*q^6 + 3*q^7 + 5*q^8 + 5*q^9 + O(q^10)

- The result above indicates that ``Q`` is not *classically free*::

    sage: f = R.arc_algebra_cover; f
    Ring morphism:
      From: Quotient of The classical limit of The Virasoro vertex algebra of central charge 1/2 over Rational Field by the ideal generated by (L_2^3,)
      To:   The classical limit of Quotient of The Virasoro vertex algebra of central charge 1/2 over Rational Field by the ideal generated by (L_-2L_-2L_-2|0> + 93/64*L_-3L_-3|0> - 33/8*L_-4L_-2|0> - 27/16*L_-6|0>,)
      Defn: L_2 |--> L_2
    sage: f.kernel(9)
    Free module generated by {0} over Rational Field
    sage: _.an_element().lift()
    2*L_4*L_3*L_2 + 1/3*L_5*L_2^2

- We construct the universal Affine vertex algebra for
  `\mathfrak{sl}_3` at level 2 and perform some basic computations::

    sage: V = vertex_algebras.Affine(QQ,'A2',2)
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

- We construct the universal affine vertex algebra for
  `\mathfrak{sl}_2` at level 3 and check that a vector is singular::

    sage: V = vertex_algebras.Affine(QQ,'A1',3)
    sage: V.gens()
    (E(alpha[1])_-1|0>, E(alphacheck[1])_-1|0>, E(-alpha[1])_-1|0>)
    sage: e = V.gen(0)
    sage: e*(e*(e*e))
    E(alpha[1])_-1E(alpha[1])_-1E(alpha[1])_-1E(alpha[1])_-1|0>
    sage: (e*(e*(e*e))).is_singular()
    True

- We construct the classical limit of `V` and check that the
  multiplication is associative in this limit while not in `V`::

    sage: P = V.classical_limit()
    sage: P
    The classical limit of The universal affine vertex algebra of CartanType ['A', 1] at level 3 over Rational Field
    sage: f = V.gen(2)
    sage: e*(e*f) == (e*e)*f
    False
    sage: e=P(e); e.parent()
    The classical limit of The universal affine vertex algebra of CartanType ['A', 1] at level 3 over Rational Field
    sage: f=P(f)
    sage: e*(e*f) == (e*e)*f
    True

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

from sage.structure.unique_representation import UniqueRepresentation
from sage.categories.commutative_rings import CommutativeRings
from sage.categories.lie_conformal_algebras import LieConformalAlgebras
from sage.categories.vertex_algebras import VertexAlgebras
from sage.structure.parent import Parent

class VertexAlgebra(UniqueRepresentation, Parent):
    r"""
    Vertex algebras base class and factory.

    INPUT:

    - ``base_ring`` -- a commutative ring (default: ``None``); the
      base ring of this vertex algebra

    - ``lie_conformal_algebra`` a :class:`LieConformalAlgebra`
      (default: ``None``); if specified, this class
      returns the quotient of its universal enveloping vertex
      algebra by the central ideal defined by the parameter
      ``central_parameters``

    - ``central_parameters`` -- A finite family (default: ``None``);
      a family defining a central ideal in the
      universal enveloping vertex algebra of the Lie conformal
      algebra ``lie_conformal_algebra``

    - ``names`` -- a list or tuple of ``str``; alternative names
      for the generators

    - ``latex_names`` -- a list or tuple of ``str``; alternative
      names for the `\LaTeX` representation of generators

    .. WARNING::

        We allow ``R`` to be an arbitrary commutative ring to
        perform basic computations of OPE. However, behaviour is
        undefined if ``R`` is not a field of characteristic ``0``.

    .. NOTE::

      There are several methods of constructing vertex
      algebras. Currently we only support the construction as the
      universal enveloping
      vertex algebra of a Lie conformal algebra, which is best
      achieved by calling
      :meth:`~sage.categories.lie_conformal_algebras.LieConformalAlgebras.ParentMethods.universal_enveloping_algebra`,
      or as derived constructions like quotients by calling
      :meth:`~sage.categories.vertex_algebras.VertexAlgebras.ParentMethods.quotient`.

    EXAMPLES::

        sage: Vir = lie_conformal_algebras.Virasoro(CC)
        sage: Vir.inject_variables()
        Defining L, C
        sage: cp = Family({C:1/3})
        sage: V = VertexAlgebra(CC,Vir,central_parameters=cp)
        sage: V
        The universal enveloping vertex algebra of the Virasoro Lie conformal algebra over Complex Field with 53 bits of precision
    """
    @staticmethod
    def __classcall_private__(cls, base_ring=None,
                              lie_conformal_algebra = None,
                              category=None,
                              central_parameters=None,
                              names=None,
                              latex_names=None):

        if base_ring not in CommutativeRings():
            raise ValueError("base_ring must must be a commutative ring, "+
                             "got {}".format(base_ring))

        try:
            if base_ring.has_coerce_map_from(lie_conformal_algebra.base_ring())\
                and lie_conformal_algebra in LieConformalAlgebras(
                    lie_conformal_algebra.base_ring()):
                from .universal_enveloping_vertex_algebra import \
                                                UniversalEnvelopingVertexAlgebra
                return UniversalEnvelopingVertexAlgebra(base_ring,
                        lie_conformal_algebra,
                        category=category,
                        central_parameters=central_parameters,
                        names=names,latex_names=latex_names)
        except AttributeError:
            pass

        raise NotImplementedError("Not Implemented")

    def __init__(self, R, category=None, names=None, latex_names=None):
        """
        Initialize self.

        EXAMPLES::

            sage: Vir = lie_conformal_algebras.Virasoro(CC)
            sage: Vir.inject_variables()
            Defining L, C
            sage: cp = Family({C:1/3})
            sage: V = VertexAlgebra(CC,Vir,central_parameters=cp)
            sage: TestSuite(V).run()
        """

        category = VertexAlgebras(R).or_subcategory(category)
        super(VertexAlgebra, self).__init__(R, names=names,
                                            category = category)
        self._latex_names = latex_names


    def base_ring(self):
        """
        The base ring of this vertex algebra.

        EXAMPLES::

            sage: V = vertex_algebras.Virasoro(QQ,1/2); V
            The Virasoro vertex algebra of central charge 1/2 over Rational Field
            sage: V.base_ring()
            Rational Field
        """
        return self.category().base_ring()