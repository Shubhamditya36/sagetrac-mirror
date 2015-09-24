r"""
Set Operads
"""
#*****************************************************************************
#  Copyright (C) 2008 Teresa Gomez-Diaz (CNRS) <Teresa.Gomez-Diaz@univ-mlv.fr>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#                  http://www.gnu.org/licenses/
#******************************************************************************

from category_types import Category
from sage.categories.sets_cat import Sets
from sage.misc.cachefunc import cached_method
from sage.categories.cartesian_product import cartesian_product
from sage.misc.abstract_method import abstract_method
from sage.categories.category_singleton import Category_singleton


class SetOperads(Category_singleton):
    """
    The category of set operads.

    EXAMPLES::

        sage: SetOperads()
        Category of set operads
        sage: SetOperads().super_categories()
        [Category of sets]

    TESTS::

        sage: C = SetOperads()
        sage: TestSuite(C).run()
    """

    @cached_method
    def super_categories(self):
        """
        Return the super-categories of ``self``.

        EXAMPLES::

            sage: SetOperads().super_categories()
            [Category of sets]
        """
        return [Sets()]

    def example(self):
        """
        Return an example of set operad.

        Here, the associative operad.

        EXAMPLES::

            sage: SetOperads().example()
            An example of a set operad: the Associative operad
        """
        from sage.categories.examples.set_operads import Example
        return Example()

    class ParentMethods:

        @abstract_method(optional=True)
        def composition(self, left, right, index):
            """
            Return the composition of ``left`` with ``right`` at position
            ``index``.

            EXAMPLES::

                sage: P = SetOperads().example()
                sage: x = P.one('i')
                sage: y = P.one('j')
                sage: P.composition(x, y, 'i')
                'j'
            """

        @abstract_method(optional=True)
        def composition_with_numbers(self):
            """
            This is a variant of composition, where one assumes that
            the objects are labelled by integers from `1` to `n`. The
            result is labelled in the same way.
            """

        def global_composition(self, left, list_right):
            r"""
            Return the global composition of ``left`` with a list of elements.
            """
            if self.composition is not NotImplemented:
                if left.degree() != len(list_right):
                    raise ValueError("the degree of x is not equal to the length of list_right")
                res = left
                for i in xrange(left.degree(), 0, -1):
                    res = res.compose(list_right[i - 1], i)
                    return res
            else:
                return NotImplemented

        def global_composition_with_numbers(self, left, list_right):
            r"""
            Return the global composition of ``left`` with a list of elements.

            The elements are supposed to be labelled by consecutive integers.
            """
            if self.composition_with_numbers is not NotImplemented:
                if left.degree() != len(list_right):
                    raise ValueError("the degree of x is not equal to the length of list_right")
                res = left
                for i in xrange(left.degree(), 0, -1):
                    res = res.compose_with_numbers(list_right[i - 1], i)
                    return res
            else:
                return NotImplemented

        @abstract_method(optional=True)
        def operad_morphism(self, arg, codomain):
            """
            Return the image of ``arg`` by a morphism from ``self`` to
            ``codomain``.
            """

        @abstract_method(optional=True)
        def one(self, letter):
            """
            Return the one of the operad.

            INPUT:

            ``letter`` -- the chosen labelling.

            EXAMPLES::

                sage: A = SetOperads().example()
                sage: A.one('x')
                'x'
            """

        @abstract_method(optional=True)
        def is_symmetric(self):
            r"""
            Return ``True`` if the operad is symmetric.
            """
            pass

        @abstract_method(optional=True)
        def elements(self, n):
            """
            Return the set of elements in degree `n`.
            """
            pass

        def cardinality(self):
            """
            Return the cardinality.

            This is usually infinity.

            EXAMPLES::

                sage: A = SetOperads().example()
                sage: A.cardinality()
                +Infinity
            """
            from sage.rings.infinity import Infinity
            return Infinity

    class ElementMethods:

        def compose(self, other, index):
            """
            Return the composition of ``self`` with ``other`` at position
            ``index``.

            EXAMPLES::

                sage: A = SetOperads().example()
                sage: x = A('fou')
                sage: y = A('pi')
                sage: x.compose(y,'u')
                'fopi'
            """
            return self.parent().composition(self, other, index)

        def compose_with_numbers(self, other, index):
            """
            Return the composition of ``self`` with ``other`` at position
            ``index``.

            The elements are supposed to be labelled by consecutive integers.

            EXAMPLES::

                sage: A = SetOperads().example()
                sage: x = A('123')
                sage: y = A('12')
                sage: x.compose_with_numbers(y,3)
                '1234'
            """
            return self.parent().composition_with_numbers(self, other, index)

        @abstract_method(optional=True)
        def degree(self):
            """
            Return the degree of an element.

            EXAMPLES::

                sage: A = SetOperads().example()
                sage: y = A('12')
                sage: y.degree()
                2
            """
            pass

        @abstract_method(optional=True)
        def map_labels(self, f):
            """
            Apply the function `f` to the labels of an element.

            EXAMPLES::

                sage: A = SetOperads().example()
                sage: y = A('R2D2')
                sage: y.map_labels(lambda u: u.lower())
                'r2d2'
            """
            pass
