from sage.misc.cachefunc import cached_method
from sage.categories.all import OperadsWithBasis
from sage.combinat.free_module import CombinatorialFreeModule
from sage.combinat.words.words import Words
class AssociativeOperad(CombinatorialFreeModule):
    r"""
    The Associative operad
    """

    def __init__(self, R):
        """
        EXAMPLES::

            sage: A = AssociativeOperad(QQ); A
            The Associative operad over Rational Field
            sage: TestSuite(A).run()

        """
        CombinatorialFreeModule.__init__(self, R, Words(), category = OperadsWithBasis(R))

    def _repr_(self):
        """
        EXAMPLES::

            sage: AssociativeOperad(QQ)       # indirect doctest
            The Associative operad over Rational Field
        """
        return "The Associative operad over %s"%(self.base_ring())

    def species(self):
        """
        The species of non-empty lists

        EXAMPLES::

            sage: f=AssociativeOperad(QQ).species()
            sage: f.generating_series().coefficients(5)
            [0, 1, 1, 1, 1]
        """
        from sage.combinat.species.linear_order_species import LinearOrderSpecies
        return LinearOrderSpecies().restricted(min=1)

    @cached_method
    def one_basis(self,letter):
        """
        Returns the word of length one, which index the one of this operad,
        as per :meth:`OperadsWithBasis.ParentMethods.one_basis`.

        EXAMPLES::

            sage: A = AssociativeOperad(QQ)
            sage: A.one_basis("a")
            word: a
        """
        return self.basis().keys()([letter])

    def degree_on_basis(self,t):
        """
        Returns the degree of a word `t` in the Associative operad.

        EXAMPLES::

            sage: A = AssociativeOperad(QQ)
            sage: Words = A.basis().keys()
            sage: m = Words([4,3,2,1])
            sage: A.degree_on_basis(m)
            4
        """
        return t.length()

    def map_labels(self,t,f):
        """
        Maps the function `f` on the word `t`.

        EXAMPLES::

            sage: A = AssociativeOperad(QQ)
            sage: Words = A.basis().keys()
            sage: m = Words([4,3,2,1])
            sage: A.map_labels(m,lambda u:u)
            word: 4321
        """
        return self.basis().keys()([f(u) for u in t])

    def labelling_on_basis(self,t):
        """
        Put canonical labels on a word in the Associative operad.

        EXAMPLES::

            sage: A = AssociativeOperad(QQ)
            sage: Words = A.basis().keys()
            sage: m = Words([4,3,2,1])
            sage: A.labelling_on_basis(m)
            B[word: 1234]
        """
        return self.basis()[self.basis().keys()([1+i for i in range(t.length())])]

    def unlabelling_on_basis(self,t):
        """
        Removes the labels of a tree in the Associative operad.

        EXAMPLES::

            sage: A = AssociativeOperad(QQ)
            sage: Words = A.basis().keys()
            sage: m = Words([4,3,2,1])
            sage: A.unlabelling_on_basis(m)
            B[word: 1111]
        """
        return self.basis()[self.basis().keys()([1 for i in range(t.length())])]

    def grafts(self,x,y,i):
        """
        Auxiliary procedure: inserts a word y at position i in a word x
        and returns a word

        EXAMPLES::

            sage: A = AssociativeOperad(QQ)
            sage: Words = A.basis().keys()
            sage: A.grafts(Words("acb"), Words("de"),"c")
            word: adeb

        """
        if x[0]==i:
            return y+x[1:]
        else:
            return x[:1]+self.grafts(x[1:],y,i)

    def composition_on_basis(self,x,y,i):
        """
        Composition of basis elements, as per :meth:`OperadsWithBasis.ParentMethods.composition_on_basis`.

        EXAMPLES::

            sage: A = AssociativeOperad(QQ)
            sage: Words = A.basis().keys()
            sage: A.composition_on_basis(Words("acb"), Words("de"),"c")
            B[word: adeb]
        """
        if not(i in x):
            return "The composition index is not present."
        else:
            return self.basis()[self.grafts(x,y,i)]

    def associative_product(self, x, y):
        """
        This computes the associative product.

        EXAMPLES::

            sage: A = AssociativeOperad(QQ)
            sage: W = A.basis().keys()
            sage: x = A(W('ab'))
            sage: y = A(W('dc'))
            sage: A.associative_product(x, y)
            B[word: abdc]
        """
        gen=self.basis()[self.basis().keys()([0,1])]
        return gen.compose(x,0).compose(y,1)

    def operad_generators(self):
        """
        EXAMPLES::

        sage: AssociativeOperad(QQ).operad_generators()
        Finite family {'associative_product': B[word: 12]}
        """
        from sage.sets.family import Family
        return Family(dict([("associative_product",
                             self.basis()[self.basis().keys()([1,2])])]))

    def operad_morphism_on_basis(self,t,codomain):
        """
        defines a morphism from the Associative operad to the target operad

        the target operad has to possess a method called associative_product

        the argument should not have repeated labels

        EXAMPLES::

            sage: A = AssociativeOperad(QQ)
            sage: D = DendriformOperad(QQ)
            sage: A.operad_morphism_on_basis(A.one_basis('a'),D)
            B[a[., .]]
        """
        targetProduct=codomain.associative_product
        n = len(t)
        if n==1 :
            return codomain.one(t[0])
        else:
            return targetProduct(self.operad_morphism_on_basis(t[0],codomain),self.operad_morphism_on_basis(t[1:],codomain))
