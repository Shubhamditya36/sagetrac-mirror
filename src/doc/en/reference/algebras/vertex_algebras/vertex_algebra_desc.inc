
Let `R` be a ring. A *Vertex algebra* [Kac1997]_ over `R` is the datum of:

- an `R` module `V` called *the space of states*
- a vector `|0\rangle \in V` called the *vacuum* vector.
- an endomorphism `T \in End(V)` called the *translation operator*
- a bilinear multiplication map 

.. MATH:: 
    V \otimes V \rightarrow V( (z)), \qquad a \otimes b \mapsto Y(a,z)b =:
    \sum_{n \in \ZZ} a_{(n)}b z^{-1-n}.
    :label: statefield

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

    (z-w)^n Y(a,z)Y(b,w) = (z-w)^n Y(b,w)Y(a,z), \qquad a,b \in V, \: n \gg 0

The `\ZZ`-many products `a_{(n)}b` defined in :eq:`statefield` are called the
*nth*-products. A vertex algebra toghether with its non-negative nth-products
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
    only non-negative integer gradings. 

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
with a finite `I`.

EXAMPLES:

Typical examples of finitely and strongly generated H-Graded vertex algebra
arise as twisted universal enveloping vertex algebras of a finitely generated
H-Graded :mod:`Lie conformal algebra<sage.categories.lie_conformal_algebras>`.
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

Every vertex algebra carries a decreasing filtration 
called the *Li standard filtration*
[Li2005]_. It is defined as follows, we define `F^pV` to be the subspace spanned
by vectors of the form

.. MATH::
    a^1_{(-n_1-1)} \cdots a^r_{(-n_r -1)} b, \qquad a^i,b \in V, n_i \in
    \ZZ_{\geq 0}, \: n_1 + \cdots n_r \geq p.

The associated graded `\mathrm{gr}_FV` is a
:mod:`Poisson vertex algebra<sage.categories.poisson_vertex_algebras>` is 
known as the *quasi-classical limit of* `V`. 


.. SEEALSO::
    :mod:`sage.algebras.vertex_algebras.vertex_algebra`
