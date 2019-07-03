"""
AG Codes

Algebraic geometry codes are codes defined using functions or differentials on
algebraic curves over finite fields.

Sage provides Goppa's original evaluation AG codes and differential AG codes on
algebraic curves.

EXAMPLES::

    sage: F.<a> = GF(4)
    sage: P.<x,y> = AffineSpace(F, 2);
    sage: C = Curve(y^2 + y - x^3)
    sage: F = C.function_field()
    sage: pls = F.places()
    sage: p = C([0,0])
    sage: Q, = p.places()
    sage: D = [pl for pl in pls if pl != Q]
    sage: G = 5*Q
    sage: codes.EvaluationAGCode(D, G)
    [8, 5] evaluation AG code over GF(4)
    sage: codes.DifferentialAGCode(D, G)
    [8, 3] differential AG code over GF(4)

A natural generalization of classical Goppa codes is Cartier codes. Cartier codes are
subfield subcodes of differential AG codes.

EXAMPLES::

    sage: F.<a> = GF(9)
    sage: P.<x,y,z> = ProjectiveSpace(F, 2);
    sage: C = Curve(x^3*y + y^3*z + x*z^3)
    sage: F = C.function_field()
    sage: pls = F.places()
    sage: Z, = C([0,0,1]).places()
    sage: D = [p for p in pls if p != Z]
    sage: G = 3*Z
    sage: codes.CartierCode(D, G)
    [9, 4] Cartier code over GF(3)

Decoders and their connected encoders for both evaluation and differential AG
codes are available.

.. toctree::

  ag_code_decoders

AUTHORS:

- Kwankyu Lee (2019-03): initial version

"""
#*****************************************************************************
#       Copyright (C) 2019 Kwankyu Lee <kwankyu@gmail.com>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#  as published by the Free Software Foundation; either version 2 of
#  the License, or (at your option) any later version.
#                  http://www.gnu.org/licenses/
#*****************************************************************************
from sage.misc.lazy_attribute import lazy_attribute

from sage.modules.all import vector
from sage.matrix.all import matrix

from .linear_code import AbstractLinearCode

from .ag_code_decoders import (EvaluationAGCodeEncoder,
                               EvaluationAGCodeUniqueDecoder,
                               DifferentialAGCodeEncoder,
                               DifferentialAGCodeUniqueDecoder)


class AGCode(AbstractLinearCode):
    """
    Base class of algebraic geometry codes.

    Algebraic geometry codes are codes defined using functions or differentials
    on algebraic curves over finite fields.

    A subclass of this class is required to define ``_function_field`` attribute
    that refers an abstract functiom field or the function field of the
    underlying curve used to construct codes of the class.
    """
    def base_function_field(self):
        """
        Return the function field used to construct the code.

        EXAMPLES::

            sage: F.<a> = GF(4)
            sage: P.<x,y> = AffineSpace(F, 2);
            sage: C = Curve(y^2 + y - x^3)
            sage: F = C.function_field()
            sage: pls = F.places()
            sage: p = C([0,0])
            sage: Q, = p.places()
            sage: D = [pl for pl in pls if pl != Q]
            sage: G = 5*Q
            sage: code = codes.EvaluationAGCode(D, G)
            sage: code.base_function_field()
            Function field in y defined by y^2 + y + x^3
        """
        return self._function_field


class EvaluationAGCode(AGCode):
    """
    Evaluation AG code defined by rational places ``pls`` and a divisor ``G``.

    INPUT:

    - ``pls`` -- a list of rational places of a function field

    - ``G`` -- a divisor of the function field whose support is disjoint from
      ``pls``

    EXAMPLES::

        sage: F.<a> = GF(4)
        sage: P.<x,y> = AffineSpace(F, 2);
        sage: C = Curve(y^2 + y - x^3)
        sage: F = C.function_field()
        sage: pls = F.places()
        sage: Q, = C.places_at_infinity()
        sage: D = [pl for pl in pls if pl != Q]
        sage: G = 5*Q
        sage: codes.EvaluationAGCode(D, G)
        [8, 5] evaluation AG code over GF(4)
    """
    def __init__(self, pls, G):
        """
        Initialize.

        TESTS::

            sage: F.<a> = GF(4)
            sage: P.<x,y> = AffineSpace(F, 2);
            sage: C = Curve(y^2 + y - x^3)
            sage: F = C.function_field()
            sage: pls = F.places()
            sage: Q, = C.places_at_infinity()
            sage: D = [pl for pl in pls if pl != Q]
            sage: G = 5*Q
            sage: code = codes.EvaluationAGCode(D, G)
            sage: TestSuite(code).run()
        """
        F = G.parent().function_field()
        K = F.constant_base_field()
        n = len(pls)

        if any(p.degree() > 1 for p in pls):
            raise ValueError("There is a nonrational place among the places")

        if any(p in pls for p in G.support()):
            raise ValueError("The support of the divisor is not disjoint from the places")

        AbstractLinearCode.__init__(self, K, n,
                                    default_encoder_name='Systematic',
                                    default_decoder_name='Syndrome')

        self._registered_encoders['evaluation'] = EvaluationAGCodeEncoder
        self._registered_decoders['uniqueK'] = EvaluationAGCodeUniqueDecoder

        m = []
        for b in G.basis_function_space():
            m.append(vector(K, [b.evaluate(p) for p in pls]))

        self._generator_matrix = matrix(m).row_space().basis_matrix()

        self._pls = tuple(pls)
        self._G = G
        self._function_field = F

    def __eq__(self, other):
        """
        Test equality of ``self`` with ``other``.

        EXAMPLES::

            sage: F.<a> = GF(4)
            sage: P.<x,y> = AffineSpace(F, 2);
            sage: C = Curve(y^2 + y - x^3)
            sage: F = C.function_field()
            sage: pls = F.places()
            sage: Q, = C.places_at_infinity()
            sage: D = [pl for pl in pls if pl != Q]
            sage: codes.EvaluationAGCode(D, 5*Q) == codes.EvaluationAGCode(D, 6*Q)
            False
        """
        if not isinstance(other, EvaluationAGCode):
            return False

        return self._pls == other._pls and self._G == other._G

    def __hash__(self):
        """
        Return the hash value of ``self``.

        EXAMPLES::

            sage: F.<a> = GF(4)
            sage: P.<x,y> = AffineSpace(F, 2);
            sage: C = Curve(y^2 + y - x^3)
            sage: F = C.function_field()
            sage: pls = F.places()
            sage: Q, = C.places_at_infinity()
            sage: D = [pl for pl in pls if pl != Q]
            sage: code = codes.EvaluationAGCode(D, 5*Q)
            sage: {code: 1}
            {[8, 5] evaluation AG code over GF(4): 1}
        """
        return hash((self._pls, self._G))

    def _repr_(self):
        """
        Return the string representation of ``self``.

        EXAMPLES::

            sage: F.<a> = GF(4)
            sage: P.<x,y> = AffineSpace(F, 2);
            sage: C = Curve(y^2 + y - x^3)
            sage: F = C.function_field()
            sage: pls = F.places()
            sage: Q, = C.places_at_infinity()
            sage: D = [pl for pl in pls if pl != Q]
            sage: codes.EvaluationAGCode(D, 7*Q)
            [8, 7] evaluation AG code over GF(4)
        """
        return "[{}, {}] evaluation AG code over GF({})".format(
                self.length(), self.dimension(), self.base_field().cardinality())

    def _latex_(self):
        r"""
        Return the latex representation of ``self``.

        EXAMPLES::

            sage: F.<a> = GF(4)
            sage: P.<x,y> = AffineSpace(F, 2);
            sage: C = Curve(y^2 + y - x^3)
            sage: F = C.function_field()
            sage: pls = F.places()
            sage: Q, = C.places_at_infinity()
            sage: D = [pl for pl in pls if pl != Q]
            sage: code = codes.EvaluationAGCode(D, 3*Q)
            sage: latex(code)
            [8, 3]\text{ evaluation AG code over }\Bold{F}_{2^{2}}
        """
        return r"[{}, {}]\text{{ evaluation AG code over }}{}".format(
                self.length(), self.dimension(), self.base_field()._latex_())

    def generator_matrix(self):
        r"""
        Return a generator matrix of the code.

        EXAMPLES::

            sage: F.<a> = GF(4)
            sage: P.<x,y> = AffineSpace(F, 2);
            sage: C = Curve(y^2 + y - x^3)
            sage: F = C.function_field()
            sage: pls = F.places()
            sage: Q, = C.places_at_infinity()
            sage: D = [pl for pl in pls if pl != Q]
            sage: code = codes.EvaluationAGCode(D, 3*Q)
            sage: code.generator_matrix()
            [    1     0     0     1     a a + 1     1     0]
            [    0     1     0     1     1     0 a + 1     a]
            [    0     0     1     1     a     a a + 1 a + 1]
        """
        return self._generator_matrix

    def designed_distance(self):
        """
        Return the designed distance of the AG code.

        If the code is of dimension zero, then a ``ValueError`` is raised.

        EXAMPLES::

            sage: F.<a> = GF(4)
            sage: P.<x,y> = AffineSpace(F, 2);
            sage: C = Curve(y^2 + y - x^3)
            sage: F = C.function_field()
            sage: pls = F.places()
            sage: Q, = C.places_at_infinity()
            sage: D = [pl for pl in pls if pl != Q]
            sage: code = codes.EvaluationAGCode(D, 3*Q)
            sage: code.designed_distance()
            5
        """
        if self.dimension() == 0:
            raise ValueError("not defined for zero code")

        d = self.length() - self._G.degree()
        return d if d > 0 else 1


class DifferentialAGCode(AGCode):
    """
    Differential AG code defined by rational places ``pls`` and a divisor ``D``

    INPUT:

    - ``pls`` -- a list of rational places of a functio field

    - ``G`` -- a divisor whose support is disjoint from ``pls``

    EXAMPLES::

        sage: F.<a> = GF(4)
        sage: A2.<x,y> = AffineSpace(F, 2)
        sage: C = A2.curve(y^3 + y - x^4)
        sage: Q = C.places_at_infinity()[0]
        sage: O = C([0,0]).place()
        sage: pls = [p for p in C.places() if p not in [O, Q]]
        sage: G = -O + 3*Q
        sage: codes.DifferentialAGCode(pls, -O + Q)
        [3, 2] differential AG code over GF(4)
    """
    def __init__(self, pls, G):
        """
        Initialize.

        TESTS::

            sage: F.<a> = GF(4)
            sage: P.<x,y> = AffineSpace(F, 2);
            sage: C = Curve(y^2 + y - x^3)
            sage: F = C.function_field()
            sage: pls = F.places()
            sage: Q, = C.places_at_infinity()
            sage: D = [pl for pl in pls if pl != Q]
            sage: code = codes.DifferentialAGCode(D, 3*Q)
            sage: TestSuite(code).run()
        """
        F = G.parent().function_field()
        K = F.constant_base_field()
        n = len(pls)

        if any(p.degree() > 1 for p in pls):
            raise ValueError("There is a nonrational place among the places")

        if any(p in pls for p in G.support()):
            raise ValueError("The support of the divisor is not disjoint from the places")

        AbstractLinearCode.__init__(self, K, n,
                                    default_encoder_name='Systematic',
                                    default_decoder_name='Syndrome')

        self._registered_encoders['residue'] = DifferentialAGCodeEncoder
        self._registered_decoders['uniqueK'] = DifferentialAGCodeUniqueDecoder

        D = sum(pls)
        m = []
        for b in (-D+G).basis_differential_space():
            m.append(vector(K, [b.residue(p) for p in pls]))

        self._generator_matrix =  matrix(m).row_space().basis_matrix()

        self._pls = tuple(pls)
        self._G = G
        self._function_field = F

    def __eq__(self, other):
        """
        Test equality of ``self`` with ``other``.

        EXAMPLES::

            sage: F.<a> = GF(4)
            sage: P.<x,y> = AffineSpace(F, 2);
            sage: C = Curve(y^2 + y - x^3)
            sage: F = C.function_field()
            sage: pls = F.places()
            sage: Q, = C.places_at_infinity()
            sage: D = [pl for pl in pls if pl != Q]
            sage: c1 = codes.DifferentialAGCode(D, 3*Q)
            sage: c2 = codes.DifferentialAGCode(D, 3*Q)
            sage: c1 is c2
            False
            sage: c1 == c2
            True
        """
        if not isinstance(other, DifferentialAGCode):
            return False

        return self._pls == other._pls and self._G == other._G

    def __hash__(self):
        """
        Return the hash of ``self``.

        EXAMPLES::

            sage: F.<a> = GF(4)
            sage: P.<x,y> = AffineSpace(F, 2);
            sage: C = Curve(y^2 + y - x^3)
            sage: F = C.function_field()
            sage: pls = F.places()
            sage: Q, = C.places_at_infinity()
            sage: D = [pl for pl in pls if pl != Q]
            sage: code = codes.DifferentialAGCode(D, 3*Q)
            sage: {code: 1}
            {[8, 5] differential AG code over GF(4): 1}
        """
        return hash((self._pls, self._G))

    def _repr_(self):
        """
        Return the string representation of ``self``.

        EXAMPLES::

            sage: F.<a> = GF(4)
            sage: P.<x,y> = AffineSpace(F, 2);
            sage: C = Curve(y^2 + y - x^3)
            sage: F = C.function_field()
            sage: pls = F.places()
            sage: Q, = C.places_at_infinity()
            sage: D = [pl for pl in pls if pl != Q]
            sage: codes.DifferentialAGCode(D, 3*Q)
            [8, 5] differential AG code over GF(4)
        """
        return "[{}, {}] differential AG code over GF({})".format(
                self.length(), self.dimension(), self.base_field().cardinality())

    def _latex_(self):
        r"""
        Return a latex representation of ``self``.

        EXAMPLES::

            sage: F.<a> = GF(4)
            sage: P.<x,y> = AffineSpace(F, 2);
            sage: C = Curve(y^2 + y - x^3)
            sage: F = C.function_field()
            sage: pls = F.places()
            sage: Q, = C.places_at_infinity()
            sage: D = [pl for pl in pls if pl != Q]
            sage: code = codes.DifferentialAGCode(D, 3*Q)
            sage: latex(code)
            [8, 5]\text{ differential AG code over }\Bold{F}_{2^{2}}
        """
        return r"[{}, {}]\text{{ differential AG code over }}{}".format(
                self.length(), self.dimension(), self.base_field()._latex_())

    def generator_matrix(self):
        """
        Return a generator matrix of the code.

        EXAMPLES::

            sage: F.<a> = GF(4)
            sage: P.<x,y> = AffineSpace(F, 2);
            sage: C = Curve(y^2 + y - x^3)
            sage: F = C.function_field()
            sage: pls = F.places()
            sage: Q, = C.places_at_infinity()
            sage: D = [pl for pl in pls if pl != Q]
            sage: code = codes.DifferentialAGCode(D, 3*Q)
            sage: code.generator_matrix()
            [    1     0     0     0     0 a + 1 a + 1     1]
            [    0     1     0     0     0 a + 1     a     0]
            [    0     0     1     0     0     a     1     a]
            [    0     0     0     1     0     a     0 a + 1]
            [    0     0     0     0     1     1     1     1]
        """
        return self._generator_matrix

    def designed_distance(self):
        """
        Return the designed distance of the differential AG code.

        If the code is of dimension zero, then a ``ValueError`` is raised.

        EXAMPLES::

            sage: F.<a> = GF(4)
            sage: P.<x,y> = AffineSpace(F, 2);
            sage: C = Curve(y^2 + y - x^3)
            sage: F = C.function_field()
            sage: pls = F.places()
            sage: Q, = C.places_at_infinity()
            sage: D = [pl for pl in pls if pl != Q]
            sage: code = codes.DifferentialAGCode(D, 3*Q)
            sage: code.designed_distance()
            3
        """
        if self.dimension() == 0:
            raise ValueError("not defined for zero code")

        d = self._G.degree() - 2*self._function_field.genus() + 2
        return d if d > 0 else 1


class CartierCode(AGCode):
    r"""
    Cartier code defined by rational places ``pls`` and a divisor ``G`` of a function field.

    INPUT:

    - ``pls`` -- a list of rational places

    - ``G`` -- a divisor whose support disjoint from ``pls``

    - ``r`` -- integer (default: 1)

    - ``name`` -- string; name of the generator of the subfield `\GF{p^r}`

    OUTPUT: Cartier code over `\GF{p^r}` where `p` is the characteristic of the
    base constant field of the function field

    Note that if ``r`` is 1 the default, then ``name`` can be omitted.

    EXAMPLES::

        sage: F.<a> = GF(9)
        sage: P.<x,y,z> = ProjectiveSpace(F, 2);
        sage: C = Curve(x^3*y + y^3*z + x*z^3)
        sage: F = C.function_field()
        sage: pls = F.places()
        sage: Z, = C([0,0,1]).places()
        sage: D = [p for p in pls if p != Z]
        sage: G = 3*Z
        sage: code = codes.CartierCode(D, G)
        sage: code.minimum_distance()
        2
    """
    def __init__(self, pls, G, r=1, name=None):
        """
        Initialize.

        TESTS::

            sage: F.<a> = GF(9)
            sage: P.<x,y,z> = ProjectiveSpace(F, 2);
            sage: C = Curve(x^3*y + y^3*z + x*z^3)
            sage: F = C.function_field()
            sage: pls = F.places()
            sage: Z, = C([0,0,1]).places()
            sage: D = [p for p in pls if p != Z]
            sage: G = 3*Z
            sage: code = codes.CartierCode(D, G)
            sage: TestSuite(code).run()
        """
        F = G.parent().function_field()
        K = F.constant_base_field()

        if any(p.degree() > 1 for p in pls):
            raise ValueError("There is a nonrational place among the places")

        if any(p in pls for p in G.support()):
            raise ValueError("The support of the divisor is not disjoint from the places")

        if K.degree() % r != 0:
            raise ValueError("{} does not divide the degree of the constant base field".format(r))

        n = len(pls)
        D = sum(pls)
        p = K.characteristic()

        subfield = K.subfield(r, name=name)

        def cartier_fixed(E):
            """
            Compute a basis of the space of differentials in `Omega(E)` fixed
            by the Cartier operator.
            """
            Grp = E.parent()  # group of divisors

            V, fr_V, to_V = E.differential_space()

            EE = Grp(0)
            dic = E.dict()
            for place in dic:
                mul = dic[place]
                if mul > 0:
                    mul = mul // p**r
                EE += mul * place

            W, fr_W, to_W = EE.differential_space()

            a = K.gen()
            field_basis = [a**i for i in range(K.degree())] # over prime subfield
            basis = E.basis_differential_space()

            m = []
            for w in basis:
                for c in field_basis:
                    cw = F(c) * w # c does not coerce...
                    carcw = cw
                    for i in range(r): # apply cartier r times
                        carcw = carcw.cartier()
                    m.append([f for e in to_W(carcw - cw) for f in vector(e)])

            ker = matrix(m).kernel()

            R = []
            s = len(field_basis)
            ncols = s * len(basis)
            for row in ker.basis():
                v = vector([K(row[d:d+s]) for d in range(0,ncols,s)])
                R.append(fr_V(v))

            return R

        R = cartier_fixed(G - D)

        # construct a generator matrix
        m = []
        col_index = D.support()
        for w in R:
            row = []
            for p in col_index:
                res = w.residue(p).trace() # lies in constant base field
                c = subfield(res) # as w is Cartier fixed
                row.append(c)
            m.append(row)

        self._generator_matrix = matrix(m).row_space().basis_matrix()

        self._pls = tuple(pls)
        self._G = G
        self._r = r
        self._function_field = F

        AbstractLinearCode.__init__(self, subfield, n,
                                    default_encoder_name='Systematic',
                                    default_decoder_name='Syndrome')

        self._registered_encoders['residue'] = DifferentialAGCodeEncoder
        self._registered_decoders['uniqueK'] = DifferentialAGCodeUniqueDecoder

    def __eq__(self, other):
        """
        Test equality of ``self`` with ``other``.

        EXAMPLES::

            sage: F.<a> = GF(9)
            sage: P.<x,y,z> = ProjectiveSpace(F, 2);
            sage: C = Curve(x^3*y + y^3*z + x*z^3)
            sage: F = C.function_field()
            sage: Z, = C([0,0,1]).places()
            sage: pls = [p for p in F.places() if p != Z]
            sage: c1 = codes.CartierCode(pls, 3*Z)
            sage: c2 = codes.CartierCode(pls, 1*Z)
            sage: c1 == c2
            False
        """
        if not isinstance(other, CartierCode):
            return False

        return self._pls == other._pls and self._G == other._G and self._r == other._r

    def __hash__(self):
        """
        Return the hash of ``self``.

        EXAMPLES::

            sage: F.<a> = GF(9)
            sage: P.<x,y,z> = ProjectiveSpace(F, 2);
            sage: C = Curve(x^3*y + y^3*z + x*z^3)
            sage: F = C.function_field()
            sage: pls = F.places()
            sage: Z, = C([0,0,1]).places()
            sage: D = [p for p in pls if p != Z]
            sage: G = 3*Z
            sage: code = codes.CartierCode(D, G)
            sage: {code: 1}
            {[9, 4] Cartier code over GF(3): 1}
        """
        return hash((self._pls, self._G, self._r))

    def _repr_(self):
        """
        Return the string representation of ``self``.

        EXAMPLES::

            sage: F.<a> = GF(9)
            sage: P.<x,y,z> = ProjectiveSpace(F, 2);
            sage: C = Curve(x^3*y + y^3*z + x*z^3)
            sage: F = C.function_field()
            sage: pls = F.places()
            sage: Z, = C([0,0,1]).places()
            sage: D = [p for p in pls if p != Z]
            sage: G = 3*Z
            sage: codes.CartierCode(D, G)
            [9, 4] Cartier code over GF(3)
        """
        return "[{}, {}] Cartier code over GF({})".format(
                self.length(), self.dimension(), self.base_field().cardinality())

    def _latex_(self):
        r"""
        Return the latex representation of ``self``.

        EXAMPLES::

            sage: F.<a> = GF(9)
            sage: P.<x,y,z> = ProjectiveSpace(F, 2);
            sage: C = Curve(x^3*y + y^3*z + x*z^3)
            sage: F = C.function_field()
            sage: pls = F.places()
            sage: Z, = C([0,0,1]).places()
            sage: D = [p for p in pls if p != Z]
            sage: G = 3*Z
            sage: code = codes.CartierCode(D, G)
            sage: latex(code)
            [9, 4]\text{ Cartier code over }\Bold{F}_{3}
        """
        return r"[{}, {}]\text{{ Cartier code over }}{}".format(
                self.length(), self.dimension(), self.base_field()._latex_())

    def generator_matrix(self):
        r"""
        Return the latex representation of ``self``.

        EXAMPLES::

            sage: F.<a> = GF(9)
            sage: P.<x,y,z> = ProjectiveSpace(F, 2);
            sage: C = Curve(x^3*y + y^3*z + x*z^3)
            sage: F = C.function_field()
            sage: pls = F.places()
            sage: Z, = C([0,0,1]).places()
            sage: D = [p for p in pls if p != Z]
            sage: G = 3*Z
            sage: code = codes.CartierCode(D, G)
            sage: code.generator_matrix()
            [1 0 0 2 2 0 2 2 0]
            [0 1 0 2 2 0 2 2 0]
            [0 0 1 0 0 0 0 0 2]
            [0 0 0 0 0 1 0 0 2]
        """
        return self._generator_matrix

    def designed_distance(self):
        """
        Return the designed distance of the Cartier code.

        The designed distance is that of the differential code of which the
        Cartier code is a subcode.

        EXAMPLES::

            sage: F.<a> = GF(9)
            sage: P.<x,y,z> = ProjectiveSpace(F, 2);
            sage: C = Curve(x^3*y + y^3*z + x*z^3)
            sage: F = C.function_field()
            sage: pls = F.places()
            sage: Z, = C([0,0,1]).places()
            sage: D = [p for p in pls if p != Z]
            sage: G = 3*Z
            sage: code = codes.CartierCode(D, G)
            sage: code.designed_distance()
            1
        """
        if self.dimension() == 0:
            raise ValueError("not defined for zero code")

        d = self._G.degree() - 2*self._function_field.genus() + 2
        return d if d > 0 else 1
