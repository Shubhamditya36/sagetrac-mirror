r"""
Value groups of discrete valuations

This file defines additive subgroups of `\QQ` generated by a rational number.

AUTHORS:

- Julian Rueth (2013-09-06): initial version

"""
#*****************************************************************************
#       Copyright (C) 2013 Julian Rueth <julian.rueth@fsfe.org>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#  as published by the Free Software Foundation; either version 2 of
#  the License, or (at your option) any later version.
#                  http://www.gnu.org/licenses/
#*****************************************************************************
from sage.rings.all import ZZ, QQ, Rational, infinity
from sage.categories.modules import Modules
from sage.structure.parent import Parent
from sage.structure.unique_representation import UniqueRepresentation

category = Modules(ZZ)


class DiscreteValueGroup(UniqueRepresentation, Parent):
    r"""
    The value group of a discrete valuation, an additive subgroup of `\QQ`
    generated by ``generator``.

    INPUT:

    - ``generator`` -- a rational number

    EXAMPLES::

        sage: D1 = DiscreteValueGroup(0); D1
        DiscreteValueGroup(0)
        sage: D2 = DiscreteValueGroup(4/3); D2
        DiscreteValueGroup(4/3)
        sage: D3 = DiscreteValueGroup(-1/3); D3
        DiscreteValueGroup(1/3)

    TESTS::

        sage: TestSuite(D1).run()
        sage: TestSuite(D2).run()
        sage: TestSuite(D3).run()

    """
    @staticmethod
    def __classcall__(cls, generator, category=category):
        r"""
        Normalizes ``generator`` to a positive rational so that this is a
        unique parent.

        TESTS::

            sage: DiscreteValueGroup(1) is DiscreteValueGroup(-1)
            True

        """
        from sage.misc.functional import coerce
        generator = coerce(QQ, generator)
        generator = generator.abs()
        return super(DiscreteValueGroup, cls).__classcall__(cls, generator, category)

    def __init__(self, generator, category):
        r"""
        Initialization.

        TESTS::

            sage: type(DiscreteValueGroup(0))
            <class 'sage.rings.padics.discrete_value_group.DiscreteValueGroup_with_category'>

        """
        self._generator = generator

        Parent.__init__(self, facade=QQ, category=category)

    def _element_constructor_(self, x):
        r"""
        Create an element in this group from ``x``.

        INPUT:

        - ``x`` -- a rational number

        TESTS::

            sage: DiscreteValueGroup(0)(0)
            0
            sage: DiscreteValueGroup(0)(1)
            Traceback (most recent call last):
            ...
            ValueError: `1` is not in DiscreteValueGroup(0).
            sage: DiscreteValueGroup(1)(1)
            1
            sage: DiscreteValueGroup(1)(1/2)
            Traceback (most recent call last):
            ...
            ValueError: `1/2` is not in DiscreteValueGroup(1).

        """
        from sage.misc.functional import coerce
        x = coerce(QQ, x)
        if x == 0 or (self._generator != 0 and x/self._generator in ZZ):
            return x

        raise ValueError("`{0}` is not in {1}.".format(x,self))

    def _repr_(self):
        r"""
        Return a printable representation for this group.

        EXAMPLES::

            sage: DiscreteValueGroup(0) # indirect doctest
            DiscreteValueGroup(0)

        """
        return "DiscreteValueGroup({0})".format(self._generator)

    def __add__(self, other):
        r"""
        Return the subgroup of `\QQ` generated by this group and ``other``.

        INPUT:

        - ``other`` -- a discrete value group or a rational number

        EXAMPLES::

            sage: D = DiscreteValueGroup(1/2)
            sage: D + 1/3
            DiscreteValueGroup(1/6)
            sage: D + D
            DiscreteValueGroup(1/2)
            sage: D + 1
            DiscreteValueGroup(1/2)
            sage: DiscreteValueGroup(2/7) + DiscreteValueGroup(4/9)
            DiscreteValueGroup(2/63)

        """
        if not isinstance(other, DiscreteValueGroup):
            from sage.structure.element import is_Element
            if is_Element(other) and QQ.has_coerce_map_from(other.parent()):
                return self + DiscreteValueGroup(other, category=self.category())
            raise ValueError("`other` must be a DiscreteValueGroup or a rational number")
        if self.category() is not other.category():
            raise ValueError("`other` must be in the same category")
        return DiscreteValueGroup(self._generator.gcd(other._generator), category=self.category())

    def _mul_(self, other, switch_sides=False):
        r"""
        Return the group generated by ``other`` times the generator of this
        group.

        INPUT:

        - ``other`` -- a rational number

        EXAMPLES::

            sage: D = DiscreteValueGroup(1/2)
            sage: 1/2 * D
            DiscreteValueGroup(1/4)
            sage: D * (1/2)
            DiscreteValueGroup(1/4)
            sage: D * 0
            DiscreteValueGroup(0)

        """
        from sage.misc.functional import coerce
        other = coerce(QQ, other)
        return DiscreteValueGroup(self._generator*other, category=self.category())

    def index(self, other):
        r"""
        Return the index of ``other`` in this group.

        INPUT:

        - ``other`` -- a subgroup of this group

        EXAMPLES::

            sage: DiscreteValueGroup(3/8).index(DiscreteValueGroup(3))
            8
            sage: DiscreteValueGroup(3).index(DiscreteValueGroup(3/8))
            Traceback (most recent call last):
            ...
            ValueError: `other` must be a subgroup of this group
            sage: DiscreteValueGroup(3).index(DiscreteValueGroup(0))
            +Infinity
            sage: DiscreteValueGroup(0).index(DiscreteValueGroup(0))
            1
            sage: DiscreteValueGroup(0).index(DiscreteValueGroup(3))
            Traceback (most recent call last):
            ...
            ValueError: `other` must be a subgroup of this group

        """
        if not isinstance(other, DiscreteValueGroup):
            raise ValueError("`other` must be a DiscreteValueGroup")
        if other._generator not in self:
            raise ValueError("`other` must be a subgroup of this group")
        if other._generator == 0:
            if self._generator == 0:
                return ZZ(1)
            else:
                return infinity
        return ZZ(other._generator / self._generator)
