r"""
Irreducible factors of associate polynomials needed for OM computations

AUTHORS:

- Brian Sinclair and Sebastian Pauli (2012-02-22): initial version

"""
#*****************************************************************************
#       Copyright (C) 2012-2017 Brian Sinclair <bsinclai@gmail.com>
#                               Sebastian Pauli <s_pauli@uncg.edu>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#                  http://www.gnu.org/licenses/
#*****************************************************************************
from sage.rings.polynomial.polynomial_ring_constructor import PolynomialRing
from sage.rings.finite_rings.finite_field_constructor import GF
from sage.matrix.constructor import Matrix
from sage.rings.polynomial.padics.omtree.frameelt import FrameElt
from sage.rings.infinity import infinity

class AssociatedFactor:
    r"""
    An irreducible factor of the associated polynomials of higher order
    newton polygon segments needed for OM computation.

    For each distinct irreducible factor of the associated polynomial,
    the tree of OM representations branches, thus producing distinct factors
    of the original polynomial.

    If ``rho`` is not linear, then we have found inertia. Future associated
    polynomials will need to be produced over an extension over our ground
    field by ``rho``.  This can produce a tower of finite field extensions
    to be worked in.

    INPUT:

    - ``segment`` -- the segment whose associated polynomial this is a factor
      of

    - ``rho`` -- the irreducible finite field polynomial factor of the
      associated polynomial

    - ``rhoexp`` -- the multiplicity of the factor

    EXAMPLES:

    This class is used internally by the OM computation::

        sage: from sage.rings.polynomial.padics.omtree.omtree import OMTree
        sage: k = ZpFM(2, 20, 'terse')
        sage: kx.<x> = k[]
        sage: t = OMTree(x^4 + 20*x^3 + 44*x^2 + 80*x + 1040)
        sage: factor = t.leaves()[0].prev

    TESTS::

        sage: from sage.rings.polynomial.padics.omtree.associatedfactor import AssociatedFactor
        sage: isinstance(factor, AssociatedFactor)
        True

    """
    def __init__(self, segment, rho, rhoexp):
        """
        Initialization.

        TESTS::

            sage: from sage.rings.polynomial.padics.omtree.omtree import OMTree
            sage: k = ZpFM(2, 20, 'terse')
            sage: kx.<x> = k[]
            sage: t = OMTree(x^4 + 20*x^3 + 44*x^2 + 80*x + 1040)
            sage: factor = t.leaves()[0].prev
            sage: TestSuite(factor).run()

        """
        self.segment = segment
        self.rho = rho
        self.rhoexp = rhoexp
        self.Fplus = self.rho.degree()
        fr = self.segment.frame

        if self.segment.frame.is_first():
            # In the first frame, so FFbase is the residue class field of O
            self.FFbase = fr.R
        else:
            # Not the first frame
            self.FFbase = fr.prev.FF

        if self.Fplus == 1:
            self.FF = self.FFbase
            self.FFz = PolynomialRing(self.FF,'z'+str(fr.depth))
            # rho is linear delta is the root of rho
            self.delta = self.rho.roots()[0][0]
        else:
            self.FF = GF(self.FFbase.order()**self.Fplus,'a'+str(fr.depth))
            self.FFz = PolynomialRing(self.FF,'z'+str(fr.depth))
            self.FFbase_gamma = (self.FFz(self.FFbase.modulus())).roots()[0][0]
            FFrho = self.FFz([self.FFbase_elt_to_FF(a) for a in list(rho)])
            self.gamma = FFrho.roots()[0][0]
            basis = [(self.gamma**j*self.FFbase_gamma**i).polynomial() for j in range(0,self.Fplus) for i in range(0,self.FFbase.degree())]
            self.basis_trans_mat = Matrix([self.FF(b)._vector_() for b in basis])

    def __cmp__(self, other):
        """
        Comparison.

        EXAMPLES::

            sage: from sage.rings.polynomial.padics.omtree.omtree import OMTree
            sage: k = ZpFM(2,20,'terse'); kx.<x> = k[]
            sage: t = OMTree(x^4+20*x^3+44*x^2+80*x+1040)
            sage: t.leaves()[0].prev == t.leaves()[0].polygon[0].factors[0]
            False
        """
        c = cmp(type(self), type(other))
        if c: return c
        return cmp((self.segment, self.rho, self.rhoexp), (other.segment, other.rho, other.rhoexp))

    def FF_elt_to_FFbase_vector(self,a):
        """
        Represents an element in our current extended residue field as a
        vector over its ground residue field.

        INPUT:

        - ``a`` -- Element of our extended residue field

        OUTPUT:

        - A list representing a vector of ``a`` over the ground field of
          the latest extension.

        EXAMPLES::

        First we set up AssociatedFactors building a tower of extensions::

            sage: from sage.rings.polynomial.padics.omtree.omtree import OMTree
            sage: k = ZpFM(2,20,'terse'); kx.<x> = k[]
            sage: t = OMTree(x^4+20*x^3+44*x^2+80*x+1040).leaves()[0].prev_frame()
            sage: t.prev
            AssociatedFactor of rho z^2 + z + 1
            sage: t.polygon[0].factors[0]
            AssociatedFactor of rho z0^2 + a0*z0 + 1

        Then we take elements in the different finite fields and represent
        them as vectors over their base residue field::

            sage: K.<a0> = t.prev.FF;K
            Finite Field in a0 of size 2^2
            sage: t.prev.FF_elt_to_FFbase_vector(a0+1)
            [1, 1]
            sage: L.<a1> = t.polygon[0].factors[0].FF;L
            Finite Field in a1 of size 2^4
            sage: t.polygon[0].factors[0].FF_elt_to_FFbase_vector(a1)
            [1, a0 + 1]

        """
        if self.segment.frame.is_first() and self.Fplus == 1:
            return a
        elif self.Fplus == 1:
            return self.segment.frame.prev.FF_elt_to_FFbase_vector(a)
        else:
            basedeg = self.FFbase.degree()
            avec = self.FF(a)._vector_()
            svector = self.basis_trans_mat.solve_left(Matrix(self.FF.prime_subfield(),avec))
            s_list = svector.list()
            s_split = [ s_list[i*basedeg:(i+1)*basedeg] for i in range(0,self.Fplus)]
            s = [sum([ss[i]*self.FFbase.gen()**i for i in range(0,len(ss))]) for ss in s_split]
            return s

    def FFbase_elt_to_FF(self,b):
        """
        Lifts an element up from the previous residue field to the current
        extended residue field.

        INPUT:

        - ``b`` -- Element in the previous residue field.

        OUTPUT:

        - An element in the current extended residue field.

        EXAMPLES::

        First we set up AssociatedFactors building a tower of extensions::

            sage: from sage.rings.polynomial.padics.omtree.omtree import OMTree
            sage: k = ZpFM(2,20,'terse'); kx.<x> = k[]
            sage: t = OMTree(x^4+20*x^3+44*x^2+80*x+1040).leaves()[0].prev_frame()

        Then we take elements in the different finite fields and lift them
        to the next residue field upward in the extension tower::

            sage: K.<a0> = t.prev.FF;K
            Finite Field in a0 of size 2^2
            sage: L.<a1> = t.polygon[0].factors[0].FF;L
            Finite Field in a1 of size 2^4
            sage: t.prev.FFbase_elt_to_FF(1)
            1
            sage: t.polygon[0].factors[0].FFbase_elt_to_FF(a0+1)
            a1^2 + a1 + 1

        """
        fr = self.segment.frame
        if fr.is_first() and self.Fplus == 1:
            return b
        elif self.Fplus == 1:
            return fr.prev.FFbase_elt_to_FF(b)
        elif fr.F == 1 and self.FFbase.is_prime_field():
            return b * self.FFbase_gamma
        else:
            bvec = b._vector_()
            return sum([ bvec[i]*self.FFbase_gamma**i for i in range(len(bvec))])

    def __repr__(self):
        """
        Representation of self.

        EXAMPLES::

            sage: from sage.rings.polynomial.padics.omtree.omtree import OMTree
            sage: k = ZpFM(2,20,'terse'); kx.<x> = k[]
            sage: t = OMTree(x^4+20*x^3+44*x^2+80*x+1040).leaves()[0].prev_frame()
            sage: t.prev.__repr__()
            'AssociatedFactor of rho z^2 + z + 1'
            sage: t.polygon[0].factors[0].__repr__()
            'AssociatedFactor of rho z0^2 + a0*z0 + 1'

        """
        return "AssociatedFactor of rho "+repr(self.rho)

    def lift(self,delta):
        """
        FrameElt representation of a lift of residue field element ``delta``.

        EXAMPLES::

            sage: from sage.rings.polynomial.padics.omtree.omtree import OMTree
            sage: k = ZpFM(2,20,'terse'); kx.<x> = k[]
            sage: t = OMTree(x^4+20*x^3+44*x^2+80*x+1040).leaves()[0].prev_frame()
            sage: K.<a0> = t.prev.FF;K
            Finite Field in a0 of size 2^2
            sage: t.polygon[0].factors[0].lift(a0+1)
            [[1*2^0]phi1^0, [1*2^-1]phi1^1]

        """
        fr = self.segment.frame
        if fr.F == 1:
            return FrameElt(fr,fr.Ox(delta))
        elif fr.prev.Fplus == 1:
            return FrameElt(fr,fr.prev.lift(delta),this_exp=0)
        else:
            dvec = fr.prev.FF_elt_to_FFbase_vector(delta)
            return sum([fr.prev.gamma_frameelt**i*FrameElt(fr,fr.prev.lift(dvec[i]),this_exp=0) for i in range(len(dvec)) if dvec[i] != 0])

    def next_frame(self,length=infinity):
        """
        Produce the child Frame in the tree of OM representations with the
        partitioning from self.

        This method generates a new Frame with the ``self`` as previous and
        seeds it with a new approximation with strictly greater valuation
        than the current one.

        INPUT:

        - ``length`` -- Integer or infinity, default infinity; The length of
          the segment generating this factor.  This is used to reduce the
          total number of quotient with remainder operations needed in the
          resulting Frame.

        EXAMPLES::

            sage: from sage.rings.polynomial.padics.omtree.frame import Frame
            sage: Phi = ZpFM(2,20,'terse')['x'](x^32+16)
            sage: f = Frame(Phi)
            sage: f.seed(Phi.parent().gen());f
            Frame with phi (1 + O(2^20))*x + (0 + O(2^20))
            sage: f = f.polygon[0].factors[0].next_frame();f
            Frame with phi (1 + O(2^20))*x^8 + (0 + O(2^20))*x^7 + (0 + O(2^20))*x^6 + (0 + O(2^20))*x^5 + (0 + O(2^20))*x^4 + (0 + O(2^20))*x^3 + (0 + O(2^20))*x^2 + (0 + O(2^20))*x + (1048574 + O(2^20))
            sage: f = f.polygon[0].factors[0].next_frame();f
            Frame with phi (1 + O(2^20))*x^8 + (0 + O(2^20))*x^7 + (0 + O(2^20))*x^6 + (0 + O(2^20))*x^5 + (0 + O(2^20))*x^4 + (0 + O(2^20))*x^3 + (1048574 + O(2^20))*x^2 + (0 + O(2^20))*x + (1048574 + O(2^20))
            sage: f = f.polygon[0].factors[0].next_frame();f
            Frame with phi (1 + O(2^20))*x^16 + (0 + O(2^20))*x^15 + (0 + O(2^20))*x^14 + (0 + O(2^20))*x^13 + (0 + O(2^20))*x^12 + (0 + O(2^20))*x^11 + (1048572 + O(2^20))*x^10 + (0 + O(2^20))*x^9 + (1048572 + O(2^20))*x^8 + (0 + O(2^20))*x^7 + (0 + O(2^20))*x^6 + (1048572 + O(2^20))*x^5 + (4 + O(2^20))*x^4 + (0 + O(2^20))*x^3 + (8 + O(2^20))*x^2 + (0 + O(2^20))*x + (4 + O(2^20))

        """
        from frame import Frame
        fr = self.segment.frame
        if self.segment.slope is infinity:
            next = Frame(fr.Phi, self, fr.iteration)
            self.next = next
            next.seed(fr.phi, length=length)
            return next
        if self.Fplus == 1 and self.segment.Eplus == 1:
            next = Frame(fr.Phi, fr.prev, fr.iteration)
        else:
            next = Frame(fr.Phi, self, fr.iteration)
        self.next = next
        self.gamma_frameelt = FrameElt(next, self.segment.psi**-1, self.segment.Eplus)
        if self.Fplus == 1 and fr.F == 1:
            next_phi = fr.phi**self.segment.Eplus - (self.segment.psi.polynomial() * fr.Ox(self.delta))
            self.reduce_elt = FrameElt(next, self.segment.psi * self.lift(self.delta), 0)
            next.seed(next_phi, length=length)
        elif self.Fplus == 1 and self.segment.Eplus == 1:
            delta_elt = self.lift(self.delta)
            next_phi_tail = self.segment.psi * delta_elt.reduce()
            next_phi = fr.phi - next_phi_tail.polynomial()
            self.reduce_elt = FrameElt(next, next_phi_tail, 0)
            next.seed(next_phi, length=length)
        else:
            lifted_rho_coeffs = [self.lift(r) for r in list(self.rho)]
            lifted_rho_coeffs_with_psi = [FrameElt(next, (self.segment.psi**(self.Fplus - i) * lifted_rho_coeffs[i]).reduce(), 0) for i in range(len(lifted_rho_coeffs))]
            phi_elt = FrameElt(next, fr.Ox(1), 1)
            next_phi_tail = sum([phi_elt**(self.segment.Eplus * i) * lifted_rho_coeffs_with_psi[i] for i in range(len(lifted_rho_coeffs_with_psi) - 1)])
            next_phi = (phi_elt**(self.segment.Eplus * self.Fplus) + next_phi_tail).polynomial()
            self.reduce_elt = FrameElt(next) - next_phi_tail
            next.seed(next_phi, length=length)
        return next
