"""
Curve constructor

Curves are constructed through the curve constructor, after an ambient space is
defined either explicitly or implicitly.

EXAMPLES::

    sage: A.<x,y> = AffineSpace(QQ, 2)
    sage: Curve([y - x^2], A)
    Affine Plane Curve over Rational Field defined by -x^2 + y

::

    sage: P.<x,y,z> = ProjectiveSpace(GF(5), 2)
    sage: Curve(y^2*z^7 - x^9 - x*z^8)
    Projective Plane Curve over Finite Field of size 5 defined by -x^9 + y^2*z^7 - x*z^8

AUTHORS:

- William Stein (2005-11-13)

- David Kohel (2006-01)

- Grayson Jorgenson (2016-06)

"""
#*********************************************************************
#      Copyright (C) 2005 William Stein <wstein@gmail.com>
#
# Distributed under the terms of the GNU General Public License (GPL)
# as published by the Free Software Foundation; either version 2 of
# the License, or (at your option) any later version.
#                 http://www.gnu.org/licenses/
#*********************************************************************
from __future__ import absolute_import

from sage.rings.polynomial.multi_polynomial_element import is_MPolynomial
from sage.rings.polynomial.multi_polynomial_ring import is_MPolynomialRing
from sage.rings.finite_rings.finite_field_constructor import is_FiniteField

from sage.structure.all import Sequence

from sage.schemes.affine.affine_space import is_AffineSpace
from sage.schemes.generic.ambient_space import is_AmbientSpace
from sage.schemes.generic.algebraic_scheme import is_AlgebraicScheme
from sage.schemes.projective.projective_space import is_ProjectiveSpace

from sage.schemes.affine.all import AffineSpace

from sage.schemes.projective.all import ProjectiveSpace


from .projective_curve import (ProjectivePlaneCurve,
                               ProjectiveCurve,
                               ProjectivePlaneCurve_finite_field,
                               IntegralProjectivePlaneCurve_finite_field,
                               IntegralProjectiveCurve_finite_field)

from .affine_curve import (AffinePlaneCurve,
                           AffineCurve,
                           AffinePlaneCurve_finite_field,
                           IntegralAffinePlaneCurve_finite_field,
                           IntegralAffineCurve_finite_field)


from sage.schemes.plane_conics.constructor import Conic

def Curve(F, A=None):
    """
    Return the plane or space curve defined by ``F``, where ``F`` can be either
    a multivariate polynomial, a list or tuple of polynomials, or an algebraic
    scheme.

    If no ambient space is passed in for ``A``, and if ``F`` is not an
    algebraic scheme, a new ambient space is constructed.

    Also not specifying an ambient space will cause the curve to be defined in
    either affine or projective space based on properties of ``F``. In
    particular, if ``F`` contains a nonhomogenous polynomial, the curve is
    affine, and if ``F`` consists of homogenous polynomials, then the curve is
    projective.

    INPUT:

    - ``F`` -- a multivariate polynomial, or a list or tuple of polynomials, or an algebraic scheme.

    - ``A`` -- (default: None) an ambient space in which to create the curve.

    EXAMPLES: A projective plane curve.  ::

        sage: x,y,z = QQ['x,y,z'].gens()
        sage: C = Curve(x^3 + y^3 + z^3); C
        Projective Plane Curve over Rational Field defined by x^3 + y^3 + z^3
        sage: C.genus()
        1

    Affine plane curves.  ::

        sage: x,y = GF(7)['x,y'].gens()
        sage: C = Curve(y^2 + x^3 + x^10); C
        Affine Plane Curve over Finite Field of size 7 defined by x^10 + x^3 + y^2
        sage: C.genus()
        0
        sage: x, y = QQ['x,y'].gens()
        sage: Curve(x^3 + y^3 + 1)
        Affine Plane Curve over Rational Field defined by x^3 + y^3 + 1

    A projective space curve.  ::

        sage: x,y,z,w = QQ['x,y,z,w'].gens()
        sage: C = Curve([x^3 + y^3 - z^3 - w^3, x^5 - y*z^4]); C
        Projective Curve over Rational Field defined by x^3 + y^3 - z^3 - w^3, x^5 - y*z^4
        sage: C.genus()
        13

    An affine space curve.  ::

        sage: x,y,z = QQ['x,y,z'].gens()
        sage: C = Curve([y^2 + x^3 + x^10 + z^7,  x^2 + y^2]); C
        Affine Curve over Rational Field defined by x^10 + z^7 + x^3 + y^2, x^2 + y^2
        sage: C.genus()
        47

    We can also make non-reduced non-irreducible curves.  ::

        sage: x,y,z = QQ['x,y,z'].gens()
        sage: Curve((x-y)*(x+y))
        Projective Conic Curve over Rational Field defined by x^2 - y^2
        sage: Curve((x-y)^2*(x+y)^2)
        Projective Plane Curve over Rational Field defined by x^4 - 2*x^2*y^2 + y^4

    A union of curves is a curve.  ::

        sage: x,y,z = QQ['x,y,z'].gens()
        sage: C = Curve(x^3 + y^3 + z^3)
        sage: D = Curve(x^4 + y^4 + z^4)
        sage: C.union(D)
        Projective Plane Curve over Rational Field defined by
        x^7 + x^4*y^3 + x^3*y^4 + y^7 + x^4*z^3 + y^4*z^3 + x^3*z^4 + y^3*z^4 + z^7

    The intersection is not a curve, though it is a scheme.  ::

        sage: X = C.intersection(D); X
        Closed subscheme of Projective Space of dimension 2 over Rational Field defined by:
         x^3 + y^3 + z^3,
         x^4 + y^4 + z^4

    Note that the intersection has dimension 0.  ::

        sage: X.dimension()
        0
        sage: I = X.defining_ideal(); I
        Ideal (x^3 + y^3 + z^3, x^4 + y^4 + z^4) of Multivariate Polynomial Ring in x, y, z over Rational Field

    If only a polynomial in three variables is given, then it must be
    homogeneous such that a projective curve is constructed.  ::

        sage: x,y,z = QQ['x,y,z'].gens()
        sage: Curve(x^2+y^2)
        Projective Conic Curve over Rational Field defined by x^2 + y^2
        sage: Curve(x^2+y^2+z)
        Traceback (most recent call last):
        ...
        TypeError: x^2 + y^2 + z is not a homogeneous polynomial

    An ambient space can be specified to construct a space curve in an affine
    or a projective space.  ::

        sage: A.<x,y,z> = AffineSpace(QQ, 3)
        sage: C = Curve([y - x^2, z - x^3], A)
        sage: C
        Affine Curve over Rational Field defined by -x^2 + y, -x^3 + z
        sage: A == C.ambient_space()
        True

    The defining polynomial must be nonzero unless the ambient space itself is
    of dimension 1. ::

        sage: P1.<x,y> = ProjectiveSpace(1,GF(5))
        sage: S = P1.coordinate_ring()
        sage: Curve(S(0), P1)
        Projective Line over Finite Field of size 5
        sage: Curve(P1)
        Projective Line over Finite Field of size 5

    ::

        sage: A1.<x> = AffineSpace(1, QQ)
        sage: R = A1.coordinate_ring()
        sage: Curve(R(0), A1)
        Affine Line over Rational Field
        sage: Curve(A1)
        Affine Line over Rational Field

    """
    if A is None:
        if is_AmbientSpace(F) and F.dimension() == 1:
            return Curve(F.coordinate_ring().zero(), F)

        if is_AlgebraicScheme(F):
            return Curve(F.defining_polynomials(), F.ambient_space())

        if isinstance(F, (list, tuple)):
            P = Sequence(F).universe()
            if not is_MPolynomialRing(P):
                raise TypeError("universe of F must be a multivariate polynomial ring")
            for f in F:
                if not f.is_homogeneous():
                    A = AffineSpace(P.ngens(), P.base_ring(), names=P.variable_names())
                    A._coordinate_ring = P
                    break
            else:
                A = ProjectiveSpace(P.ngens()-1, P.base_ring(), names=P.variable_names())
                A._coordinate_ring = P
        elif is_MPolynomial(F): # define a plane curve
            P = F.parent()
            k = F.base_ring()

            if not k.is_field():
                if k.is_integral_domain():  # upgrade to a field
                    P = P.change_ring(k.fraction_field())
                    F = P(F)
                    k = F.base_ring()
                else:
                    raise TypeError("not a multivariate polynomial over a field or an integral domain")

            if F.parent().ngens() == 2:
                if F == 0:
                    raise ValueError("defining polynomial of curve must be nonzero")
                A = AffineSpace(2, P.base_ring())
                A._coordinate_ring = P
            elif F.parent().ngens() == 3:
                if F == 0:
                    raise ValueError("defining polynomial of curve must be nonzero")

                # special case: construct a conic curve
                if F.total_degree() == 2 and k.is_field():
                    return Conic(k, F)

                A = ProjectiveSpace(2, P.base_ring(), names=P.variable_names())
                A._coordinate_ring = P
            elif F.parent().ngens() == 1:
                if not F.is_zero():
                    raise ValueError("defining polynomial of curve must be zero "
                                     "if the ambient space is of dimension 1")

                A = AffineSpace(1, P.base_ring())
                A._coordinate_ring = P
            else:
                raise TypeError("number of variables of F (={}) must be 2 or 3".format(F))
            F = [F]
        else:
            raise TypeError("F (={}) must be a multivariate polynomial".format(F))
    else:
        if not is_AmbientSpace(A):
            raise TypeError("ambient space must be either an affine or projective space")
        if not isinstance(F, (list, tuple)):
            F = [F]
        if  not all(f.parent() == A.coordinate_ring() for f in F):
            raise TypeError("need a list of polynomials of the coordinate ring of {}".format(A))

    n = A.dimension_relative()
    if n < 1:
        raise TypeError("ambient space should be an affine or projective space of positive dimension")

    F = tuple(F)
    k = A.base_ring()

    if is_AffineSpace(A):
        if n != 2:
            if is_FiniteField(k):
                if A.coordinate_ring().ideal(F).is_prime():
                    return IntegralAffineCurve_finite_field(A, F)
            return AffineCurve(A, F)

        if not (len(F) == 1 and F[0] != 0 and F[0].degree() > 0):
            raise TypeError("need a single nonconstant polynomial to define a plane curve")

        F = F[0]
        if is_FiniteField(k):
            factors = F.factor()
            if len(factors) == 1 and factors[0][1] == 1: # irreducible
                return IntegralAffinePlaneCurve_finite_field(A, F)
            return AffinePlaneCurve_finite_field(A, F)
        return AffinePlaneCurve(A, F)

    elif is_ProjectiveSpace(A):
        if n != 2:
            if not all(f.is_homogeneous() for f in F):
                raise TypeError("polynomials defining a curve in a projective space must be homogeneous")
            if is_FiniteField(k):
                if A.coordinate_ring().ideal(F).is_prime():
                    return IntegralProjectiveCurve_finite_field(A, F)
            return ProjectiveCurve(A, F)

        # there is no dimension check when initializing a plane curve, so check
        # here that F consists of a single nonconstant polynomial
        if not (len(F) == 1 and F[0] != 0 and F[0].degree() > 0):
            raise TypeError("need a single nonconstant polynomial to define a plane curve")

        F = F[0]
        if not F.is_homogeneous():
            raise TypeError("{} is not a homogeneous polynomial".format(F))

        if is_FiniteField(k):
            factors = F.factor()
            if len(factors) == 1 and factors[0][1] == 1: # irreducible
                return IntegralProjectivePlaneCurve_finite_field(A, F)
            return ProjectivePlaneCurve_finite_field(A, F)
        return ProjectivePlaneCurve(A, F)

    else:
        raise TypeError('ambient space neither affine nor projective')
