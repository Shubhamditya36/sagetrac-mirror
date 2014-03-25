r"""
Database of reduced origamis.

Origamis are cover of the torus over one point. The group SL(2,Z) act on them
(as their mapping class group). This file contains the implementation of a
database of these SL(2,Z)-orbits. To do concrete computations with origamis see
:mod:`origami`.

EXAMPLES:

We found the Eierlegende Wollmilchsau and the Ornythorinque in the database from
their property of complete degeneracy::

    sage: q = D.query(sum_of_L_exp=1, stratum=AbelianStratum(1,1,1,1))
    sage: len(q)
    2
    sage: o0, o1 = q.list()
    sage: o0.is_isomorphic(origamis.CyclicCover([1,1,1,1])
    True
    sage: o1.is_isomorphic(origamis.CyclicCover([1,1,1,3])
    True

We check the classification of arithmetic Teichmueller curves in H(2) from
Hubert-Lelievre and McMullen::

    sage: A = AbelianStratum(2)
    sage: for n in xrange(3, 17):
    ....:     q = D.query(stratum=A, nb_squares=n)
    ....:     print "%2d %d"%(n, q.number_of())
     3 1
     4 1
     5 2
     6 1
     7 2
     8 1
     9 2
    10 1
    11 2
    12 1
    13 2
    14 1
    15 2
    16 1

And look at the conjecture of Delecroix-Lelievre in H(1,1)::

    sage: A = AbelianStratum(1,1)
    sage: for n in xrange(4,20):
    ....:     q = D.query(stratum=A, nb_squares=n)
    ....:     print "%2d %d"%(n, q.number_of())
     4 1
     5 1
     6 2
     7 2
     8 2
     9 2
    10 2
    11 2
    12 2
    13 2
    14 2
    15 2
    16 2
    17 2
    18 2
    19 2

.. NOTE::

    convention for pole_partition: if the origami is primitive, it is the
    partition of the fiber of the poles determined by half integer points. Else,
    if one of the orientation cover is hyperelliptic it is the partition with
    respect to that one. Otherwise, it is None.

AUTHOR:

- Vincent Delecroix (2011): initial version

"""
from sage.all import Integer, RealField
from sage.rings.all import ZZ,QQ,Integer
from origami import Origami, Origami_dense
from sage.dynamics.flat_surfaces.all import AbelianStratum, QuadraticStratum
from sage.interfaces.gap import gap

from sage.databases.sql_db import SQLDatabase, SQLQuery
from sage.env import SAGE_SHARE
ORIGAMI_DB_LOCATION = SAGE_SHARE + '/flat_surfaces/origamis.db'

# for primitive and primitive orientation cover
# classification of primitive group action in GAP (order < )
# (anounced to be up 4096)
#  gap.NrMovedPoints(G) : number of points on which the group act
#  gap.PrimitiveIdentification(G) : the index in the primitive group database
#  to get back the group:
#  gap.PrimitiveGroup(gap.NrMovedPoints(G),gap.PrimitiveIdentification(G))

def are_skeleton_equal(sk1, sk2):
    r"""
    Test whether the two skeleton ``sk1`` and ``sk2`` are equals.

    EXAMPLES::

        sage: from sage.dynamics.flat_surfaces.origamis.origami_database import are_skeleton_equal
        sage: sk1 = {'table1': {'col1': {'sql': 'TEXT', 'unique': True}, 'col2': {'sql': 'INTEGER'}}}
        sage: sk2 = {'table1': {'col1': {'sql': 'TEXT', 'unique': True}, 'col2': {'sql': 'INTEGER', 'unique': False}}}
        sage: are_skeleton_equal(sk1,sk2)
        True
    """
    if set(sk1.keys()) != set(sk2.keys()):
        return False

    for table in sk1:
        v1 = sk1[table]
        v2 = sk2[table]
        if set(v1.keys()) != set(v2.keys()):
            return False

        for col in v1:
            w1 = v1[col]
            w2 = v2[col]

            if w1['sql'] != w2['sql']:
                return False
            if w1.get('index',False) != w2.get('index',False):
                s1 = w1.get('index',False)
                s2 = w2.get('index',False)
                return False
            if w1.get('unique',False) != w2.get('unique',False):
                return False
            if w1.get('primary_key',False) != w2.get('primary_key',False):
                return False

    return True

ORIGAMI_DB_skeleton = {'origamis': {
    # Origami representative
    'representative'                      : {'sql': 'TEXT',    'unique': True},

    # Origami family
    'primitive'                           : {'sql': 'BOOLEAN'},
    'orientation_cover'                   : {'sql': 'BOOLEAN'},
    'hyperelliptic'                       : {'sql': 'BOOLEAN'},
    'regular'                             : {'sql': 'BOOLEAN'},
    'quasi_regular'                       : {'sql': 'BOOLEAN'},

    # Topological identification
    'stratum'                             : {'sql': 'TEXT',    'index': True},
    'component'                           : {'sql': 'TEXT',    'index': True},
    'genus'                               : {'sql': 'INTEGER', 'index': True},
    'nb_squares'                          : {'sql': 'INTEGER', 'index': True},
    'optimal_degree'                      : {'sql': 'INTEGER', 'index': True},

    # Veech group data
    'veech_group_index'                   : {'sql': 'INTEGER'},
    'veech_group_congruence'              : {'sql': 'BOOLEAN'},
    'veech_group_level'                   : {'sql': 'INTEGER'},
    'teich_curve_ncusps'                  : {'sql': 'INTEGER'},
    'teich_curve_nu2'                     : {'sql': 'INTEGER'},
    'teich_curve_nu3'                     : {'sql': 'INTEGER'},
    'teich_curve_genus'                   : {'sql': 'INTEGER'},

    # Geometry and Lyapunov exponents
    'sum_of_L_exp'                        : {'sql': 'TEXT'},
    'L_exp_approx'                        : {'sql': 'TEXT'},
    'min_nb_of_cyls'                      : {'sql': 'INTEGER'},
    'max_nb_of_cyls'                      : {'sql': 'INTEGER'},
    'min_hom_dim'                         : {'sql': 'INTEGER'},
    'max_hom_dim'                         : {'sql': 'INTEGER'},
    'minus_identity_invariant'            : {'sql': 'BOOLEAN'},

    #monodromy data
    'monodromy_name'                      : {'sql': 'TEXT',    'index': True},
    'monodromy_signature'                 : {'sql': 'BOOLEAN', 'index': True},
    'monodromy_index'                     : {'sql': 'INTEGER', 'index': True},
    'monodromy_order'                     : {'sql': 'INTEGER'},
    'monodromy_solvable'                  : {'sql': 'BOOLEAN'},
    'monodromy_nilpotent'                 : {'sql': 'BOOLEAN'},
    'monodromy_gap_primitive_id'          : {'sql': 'INTEGER'},

    # potential orientation data
    'orientation_stratum'                 : {'sql': 'TEXT'},
    'orientation_genus'                   : {'sql': 'INTEGER'},
    'pole_partition'                      : {'sql': 'TEXT'},

    # automorphism
    'automorphism_group_order'            : {'sql': 'INTEGER'},
    'automorphism_group_name'             : {'sql': 'TEXT'},
}}


ORIGAMI_DB_cols = ['representative', 'stratum', 'component', 'primitive', 'orientation_cover',
'hyperelliptic', 'regular', 'quasi_regular', 'genus', 'nb_squares', 'optimal_degree',
'veech_group_index', 'veech_group_congruence', 'veech_group_level',
'teich_curve_ncusps', 'teich_curve_nu2', 'teich_curve_nu3', 'teich_curve_genus',
'sum_of_L_exp', 'L_exp_approx', 'min_nb_of_cyls', 'max_nb_of_cyls',
'min_hom_dim', 'max_hom_dim', 'minus_identity_invariant', 'monodromy_name',
'monodromy_signature', 'monodromy_index', 'monodromy_order',
'monodromy_solvable', 'monodromy_nilpotent', 'monodromy_gap_primitive_id',
'orientation_stratum', 'orientation_genus',
'pole_partition', 'automorphism_group_order', 'automorphism_group_name']


OLDS = []
OLD_ORIGAMI_DB_skeleton = {}
OLD_ORIGAMI_DB_skeleton['origamis'] = ORIGAMI_DB_skeleton['origamis'].copy()
del OLD_ORIGAMI_DB_skeleton['origamis']['optimal_degree']

OLD_ORIGAMI_DB_cols = ORIGAMI_DB_cols[:]
OLD_ORIGAMI_DB_cols.remove('optimal_degree')

OLDS = [(OLD_ORIGAMI_DB_skeleton, OLD_ORIGAMI_DB_cols)]

#
# relabelization of columns
#

relabel_cols = {}
for col in ORIGAMI_DB_skeleton['origamis']:
    split_col = col.split('_')
    relabel_cols[col] = split_col[0].capitalize() + ' ' + ' '.join(split_col[1:])
relabel_cols['representative'] = 'Origami'
relabel_cols['component'] = 'Comp.'
relabel_cols['orientation_cover'] = 'Quad. diff.'
relabel_cols['monodromy_name'] = 'Monodromy'
relabel_cols['automorphism_group_name'] = 'Automorphism'
relabel_cols['veech_group_index'] = 'vg index'
relabel_cols['veech_group_congruence'] = 'vg congruence'
relabel_cols['veech_group_level'] = 'vg level'


#
# raw data to sqldatatype conversion
#

def real_tuple_to_data(t):
    r"""
    Convert a tuple of real numbers with same precision into a string.

    The output string is a list of numbers written in base 36 (0, 1, ..., 9, a,
    b, ..., z) separated by space ' '. The first number is the precision of the
    real field. Then each real number consists of three numbers as sign,
    mantissa, exponent.

    EXAMPLES::

        sage: import sage.dynamics.flat_surfaces.origamis.origami_database as odb
        sage: odb.real_tuple_to_data((1.23,-4))
        '1h 1 1ijk9vqiyzy -1g -1 18ce53un18g -1e'

    We may check that the first part consists of the precision::

        sage: Integer('1h', 36)
        53
        sage: RealField().precision()
        53

    And then of the two real numbers we input::

        sage: sign = Integer('1', 36)
        sage: mantissa = Integer('1ijk9vqiyzy', 36)
        sage: exponent = Integer('-1g', 36)
        sage: R(sign * mantissa * 2 ** exponent)
        1.23000000000000

        sage: sign = Integer('-1', 36)
        sage: mantissa = Integer('18ce53un18g', 36)
        sage: exponent = Integer('-1e', 36)
        -4.00000000000000

    TESTS::

        sage: import sage.dynamics.flat_surfaces.origamis.origami_database as odb
        sage: t = (RR(5.0), RR(pi))
        sage: print t
        (5.00000000000000, 3.14159265358979)
        sage: s = odb.real_tuple_to_data(t)
        sage: isinstance(s,str)
        True
        sage: t == odb.data_to_real_tuple(s)
        True
    """
    if not t:
        return ''
    prec = t[0].prec()
    for x in t:
        if x.prec() != prec:
            raise ValueError, "all reals in the tuple should have the same precision"
    s = Integer(prec).str(36)
    for x in t:
        s += ' ' + integer_tuple_to_data(x.sign_mantissa_exponent())
    return s

def data_to_real_tuple(s):
    r"""
    Convert a string into a tuple of real numbers.

    For the encoding convention, see meth:`real_tuple_to_data`.

    EXAMPLES::

        sage: import sage.dynamics.flat_surfaces.origamis.origami_database as odb
        sage: R = RealField(22)
        sage: t = (R(1), R(pi))
        sage: s = odb.real_tuple_to_data(t)
        sage: tt = odb.data_to_real_tuple(s)
        sage: s
        (1.00000, 3.14159)

        sage: s[0].parent() == R
        True
        sage: s[1].parent() == R
        True
    """
    if not s:
        return ()
    s = s.split(' ')
    prec = Integer(s[0],36)
    s = s[1:]
    R = RealField(prec)
    res = []
    for i in xrange(0,len(s),3):
        sign,mantissa,exponent = data_to_integer_tuple(s[i] + ' ' + s[i+1] + ' ' + s[i+2])
        res.append(R(sign * mantissa * 2**exponent))
    return tuple(res)

def small_positive_integer_tuple_to_data(t):
    r"""
    Convert a tuple of integers between 0 and 35 to a string.

    The encoding consists of a string of the same length as ``t`` where each
    character is the representation of the number in base `36` (0, 1, ..., 9, a,
    b, ..., z).

    EXAMPLES::

        sage: import sage.dynamics.flat_surfaces.origamis.origami_database as odb
        sage: t = (0, 35, 25, 2, 12)
        sage: s = odb.small_positive_integer_tuple_to_data(t)
        sage: s
        '0zp2c'
        sage: map(lambda x: Integer(x, 36), s)
        [0, 35, 25, 2, 12]
    """
    if not t:
        return ''
    assert(all(0 <= i and i < 36 for i in t))
    return ''.join(Integer(x).str(36) for x in t)

def data_to_small_positive_integer_tuple(s):
    r"""
    Convert a string into a tuple of Integer.

    For encoding convention, see meth:`small_positive_integer_tuple_to_data`.

    EXAMPLES::

        sage: import sage.dynamics.flat_surfaces.origamis.origami_database as odb
        sage: odb.data_to_small_positive_integer_tuple('14m')
        (1, 4, 22)
        sage: odb.data_to_small_positive_integer_tuple('')
        ()
    """
    if not s:
        return ()
    return tuple(Integer(i,36) for i in s)

def integer_tuple_to_data(t):
    r"""
    Convert a tuple of arbitrary integers into a string.

    The encoding consists in a string that are representation of the integers in
    base 36 separated by space.

    EXAMPLES::

        sage: import sage.dynamics.flat_surfaces.origamis.origami_database as odb
        sage: t = (0,-12435123,3)
        sage: s = odb.integer_tuple_to_data(t)
        sage: s
        '0 -7ej03 3'
        sage: map(lambda x: Integer(x,36), s.split(' '))
        [0, -12435123, 3]
    """
    if not t:
        return ''
    return ' '.join(Integer(x).str(36) for x in t)

def data_to_integer_tuple(s):
    r"""
    Convert a string into a tuple of integers.

    For the encoding convention, see meth:`integer_tuple_to_data`.

    EXAMPLES::

        sage: import sage.dynamics.flat_surfaces.origamis.origami_database as odb
        sage: t = (-12, 351234123, 45)
        sage: s = odb.integer_tuple_to_data(t)
        sage: odb.data_to_integer_tuple(s) == t
        True
    """
    if not s:
        return ()
    return tuple(Integer(i,36) for i in s.split(' '))

rational_to_data = str
def data_to_rational(s):
    r"""
    Convert a string into a rational.
    """
    return QQ(str(s))

# representative (ie origami)

def representative_to_data(o):
    r"""
    Convert an origami into a string.

    The maximum number of squares is 207. The encoding consists of the
    concatenation of the two permutations that define the origami.

    TESTS::

        sage: import sage.dynamics.flat_surfaces.origamis.origami_database as odb
        sage: o = Origami('(1,2,3)','(3,2,1)')
        sage: odb.representative_to_data(o)
        '120201'
        sage: o = Origami('(1,2,4,3)(5,7,6)(10,9)','(10,8,6,2,4,3,1)')
        sage: s = odb.representative_to_data(o)
        sage: isinstance(s,str)
        True
        sage: o == odb.data_to_representative(s)
        True
    """
    assert o.nb_squares() < 129
    rs = map(lambda t: chr(48+t), o.r_tuple())
    us = map(lambda t: chr(48+t), o.u_tuple())
    return ''.join(rs)+''.join(us)

def data_to_representative(s):
    r"""
    Convert data to representative.

    For encoding convention, see meth:`representative_to_data`.
    """
    from sage.dynamics.flat_surfaces.origamis.origami import Origami_dense
    n = len(s) // 2
    r = tuple(ord(i)-48 for i in s[:n])
    u = tuple(ord(i)-48 for i in s[n:])
    return Origami_dense(r,u)

def format_representative(s):
    r"""
    Convert a string that encodes an origami into a human readable string.

    The output form consists of the concatenation of the cycles without the
    paranthesis. In other words the permutation `(1,5)(2)(3,7,4)` will be
    convert into '15 374'.

    EXAMPLES::

        sage: import sage.dynamics.flat_surfaces.origamis.origami_database as odb
        sage: o = Origami('(1,2)','(1,3)')
        sage: s = odb.representative_to_data(o)
        sage: odb.format_representative(s)
        'r=12  u=13'
    """
    o = data_to_representative(s)
    r = o.r().cycle_tuples()
    u = o.u().cycle_tuples()

    format_cycles = lambda cycles: ' '.join(map(lambda c: ''.join(map(lambda x: Integer(x).str(36),c)),cycles))

    return 'r=' + format_cycles(r) + '  u=' + format_cycles(u)

# stratum and component
def stratum_to_data(h):
    r"""
    Encode the stratum entry.

    TESTS::

        sage: import sage.dynamics.flat_surfaces.origamis.origami_database as odb
        sage: h = AbelianStratum(2,0)
        sage: s = odb.stratum_to_data(h)
        sage: isinstance(s,str)
        True
        sage: h == odb.data_to_stratum(s)
        True
    """
    return integer_tuple_to_data(h.zeros())

def data_to_stratum(s):
    r"""
    Convert a string into a stratum.

    For encoding convention, see `meth:stratum_to_data`.
    """
    return AbelianStratum(data_to_integer_tuple(s))

L_exp_approx_to_data = real_tuple_to_data
data_to_L_exp_approx = data_to_real_tuple

pole_partition_to_data = small_positive_integer_tuple_to_data

def data_to_pole_partition(s):
    if s:
        return data_to_small_positive_integer_tuple(s)
    return None

def format_pole_partition(p):
    r"""
    Format into a nice readble string the pole partition.

    EXAMPLES::

        sage: import sage.dynamics.flat_surfaces.origamis.origami_database as odb
        sage: s = odb.pole_partition_to_data((0,3,5,1))
        sage: odb.pole_partition_format(s)
        '0, (3,5,1)'
    """
    p = data_to_pole_partition(p)
    if p is None:
        return ""
    assert len(p) == 4
    return "%d (%d,%d,%d)"%p

nb_cyls_spectrum_to_data = integer_tuple_to_data
data_to_nb_cyls_spectrum = data_to_integer_tuple

sum_of_L_exp_to_data = rational_to_data
data_to_sum_of_L_exp = data_to_rational

def orientation_stratum_to_data(q):
    r"""
    TESTS::

        sage: import sage.dynamics.flat_surfaces.origamis.origami_database as odb
        sage: q = QuadraticStratum(2,2,0,-1,-1,-1,-1)
        sage: s = odb.orientation_cover_stratum_to_data(q)
        sage: isinstance(s,str)
        True
        sage: q == odb.data_to_orientation_cover_stratum(s)
        True
    """
    if q is None:
        return ''
    return integer_tuple_to_data(q.zeros())

def data_to_orientation_stratum(s):
    if s:
        return QuadraticStratum(data_to_integer_tuple(s))
    return None




from sage.dynamics.flat_surfaces.abelian_strata import ASC, HypASC, NonHypASC, EvenASC, OddASC

cc_from_name = dict((cc._name, cc) for cc in [ASC,HypASC,NonHypASC,EvenASC, OddASC])

#
# db and queries
#

class EnhancedSQLQuery(SQLQuery):
    def __init__(self, query_string, database=None):
        """
        A query for a OrigamiDatabase.

        INPUT:

        - ``database`` - the OrigamiDatabase instance to query
          (if None then a new instance is created)

        - ``query_string`` - a string representing the SQL
          query
        """
        if database is None:
            database = OrigamiDatabase()
        if not isinstance(database, OrigamiDatabase):
            raise TypeError('%s is not a valid origami database'%database)
        SQLQuery.__init__(self,database,query_string)

    #TODO: moved in SQL Query
    def _show(self, max_field_size=20, field_sizes={}, format_cols={}, plot_cols={}, relabel_cols={}, id_col=None, **kwds):
        """
        Displays the result of the query in table format.

        INPUT:

        - ``max_field_size`` -- how wide each field is (default value)

        - ``field_sizes`` -- dictionnary of how wide each field is

        - ``format_cols`` -- a dictionary that allows the user to specify the format
          of a column's output by supplying a function.  The format of the
          dictionary is: {'column_name':(lambda x: format_function(x))}

        - ``plot_cols`` -- a dictionary that allows the user to specify that a plot
          should be drawn by the object generated by a data slice.  Note that
          plot kwds are permitted.  The dictionary format is:
          {'column_name':((lambda x: plot_function(x)), **kwds)}

        - ``relabel_cols`` -- a dictionary to specify a relabeling of column
          headers.  The dictionary format is:
          {'table_name':{'old_col_name':'new_col_name'}}

        - ``id_col`` -- reference to a column that can be used as an object
          identifier for each row
        """
        if not self.__query_string__:
            self.__database__.show()
            return

        try:
            cur = self.__database__.__connection__.cursor()
            cur.execute(self.__query_string__)
        except:
            raise RuntimeError('Failure to fetch query.')

        col_titles = [des[0] for des in cur.description]
        col_widths = [max_field_size] * len(col_titles)
        fcol_index = []   # format
        fcol_titles = []
        pcol_index = []   # plot
        pcol_titles = []

        if id_col:
            id_col_index = col_titles.index(id_col)
        else:
            id_col_index = None

        for i,title in enumerate(col_titles):
            if title in field_sizes:
                col_widths[i] = field_sizes[title]

            if title in format_cols:
                fcol_index.append(i)
                fcol_titles.append(title)

            if title in plot_cols:
                pcol_index.append(i)
                pcol_titles.append(title)

            if title in relabel_cols:
                col_titles[i] = relabel_cols[title]

        width = sum(col_widths)

        from sage.server.support import EMBEDDED_MODE
        if EMBEDDED_MODE:
            # Notebook Version
            print '<html><!--notruncate--><table bgcolor=lightgrey cellpadding=0><tr>'
            for col in col_titles:
                print '<td bgcolor=white align=center> ' + col + ' </td>'
            print '</tr>'
            p = 0
            for row in cur:
                f = 0
                print '<tr>'
                for index in range(len(col_titles)):
                    if index in fcol_index:
                        if id_col_index is not None:
                            print _apply_format(format_cols[fcol_titles[f]], row[index], True, row[id_col_index])
                        else:
                            print _apply_format(format_cols[fcol_titles[f]], row[index], True)
                        f += 1
                    elif index in pcol_index:
                        print _apply_plot(plot_cols[pcol_titles[p%len(pcol_titles)]], row[index], p)
                        p += 1
                    else:
                        print '<td bgcolor=white align=center> ' + str(row[index]) + ' </td>'
                print '</tr>'
            print '</table></html>'

        else: # Command Prompt Version
            # print the title
            for i,col in enumerate(col_titles):
                print col.ljust(col_widths[i]),
            print # new line
            print '-' * width  # separator

            # print each row
            for row in cur:
                f = 0
                for index in xrange(len(col_titles)):
                    if index in fcol_index:
                        if id_col_index is not None:
                            field_val = _apply_format(format_cols[fcol_titles[f]], \
                                                    row[index], False, row[id_col_index])
                        else:
                            field_val = _apply_format(format_cols[fcol_titles[f]], \
                                                    row[index], False)
                        f += 1
                    elif index in pcol_index:
                        raise NotImplementedError, 'Cannot display plot on command line.'
                    else:
                        field_val = str(row[index])
                    print field_val.ljust(col_widths[index]),
                print # new line

class OrigamiQuery:
    r"""
    Origami database query.
    """
    def __init__(self, db, query_string, cols, **kwds):
        """
        A query for an instance of OrigamiDatabase. This class nicely wraps
        the SQLQuery class located in sage.databases.database.py to make
        the query constraints intuitive and with as many pre-definitions as
        possible. (i.e.: since it has to be a OrigamiDatabase, we already know
        the table structure and types; and since it is immutable, we can
        treat these as a guarantee).

        INPUT:

        - ``origami_db`` - The OrigamiDatabase instance to apply
          the query to. (If None, then a new instance is created).

        - ``cols`` - A list of column names (strings)
          to display in the result when running or showing a query.

        - ``query_string`` - A string associated to a query (allow =, <=, <,
          AND OR NOT). It consists only of the SQL statement which appear after
          the 'WHERE' directive.
        """
        self._cols = cols
        self._query_string = query_string
        self._display_options = kwds
        self._order = [("nb_squares",1)]

        if db is None:
            self._db = OrigamiDatabase()
        elif not isinstance(db, OrigamiDatabase):
            raise TypeError("%s is not a valid origami database"%database)
        else:
            self._db = db

    def __repr__(self):
        r"""
        String representation.

        EXAMPLES::

            sage: O = OrigamiDatabase()
            sage: O.query(("nb_squares","=",5))
            Origami query: SELECT representative FROM origamis WHERE nb_squares=5 ORDER BY nb_squares ASC
        """
        return 'Origami query: %s'%self.get_query_string()

    def database(self):
        r"""
        Returns the database of that query.
        """
        return self._db

    def cols(self, *cols):
        r"""
        Get or modify columns.

        In sql query, it corresponds to the clause 'SELECT'.

        EXAMPLES::

            sage: O = OrigamiDatabase()
            sage: q = O.query()
            sage: q.cols()
            ["representative"]
            sage: q.cols("nb_squares")
            sage: q.cols()
            ["nb_squares"]
            sage: q.cols("veech_group_index","primitive")
            sage: q.cols()
            ["veech_group_index", "primitive"]
        """
        if not cols:
            return self._cols[:]

        if len(cols) == 1 and isinstance(cols[0], (list,tuple)):
            cols = cols[0]

        if len(cols) == 1 and cols[0] == '*':
            self._cols = ORIGAMI_DB_cols

        else:
            assert all(c in ORIGAMI_DB_cols for c in cols)
            self._cols = list(cols)

    def order(self, *args):
        r"""
        Get or modify order.

        Order should be a list (col_name, +1) or (col_name, -1). First one means
        ascending and the second one decending. In a sql query, it corresponds
        to the clause 'ORDER BY'.

        EXAMPLES::

            sage: O = OrigamiDatabase()
            sage: q = O.query()
            sage: q.order(("nb_squares",1),("pole_partition",1))
            sage: q.get_query_string()
            'SELECT representative FROM origamis ORDER BY nb_squares ASC,pole_partition ASC'
            sage: q.order(("nb_squares",-1))
            sage: q.get_query_string()
            'SELECT representative FROM origamis ORDER BY nb_squares DESC'
        """
        if not args:
            return self._order

        if len(args) == 0 and isinstance(args, list):
            args = args[0]

        tt = []
        for t in args:
            assert isinstance(t,tuple)
            assert len(t) == 2
            assert t[0] in ORIGAMI_DB_cols
            assert t[1] == 1 or t[1] == -1
            tt.append((t[0],int(t[1])))
        if not len(set(x[0] for x in tt)) == len(tt):
            raise ValueError, "duplicate in your list"
        self._order = tt

    def get_query_string(self):
        r"""
        Output the query string in sql format.
        """
        query = 'SELECT ' + ','.join(self._cols) + ' FROM origamis'
        if self._query_string:
            query += ' WHERE ' + self._query_string
        if self._order:
            d = {1: ' ASC', -1: ' DESC'}
            query += " ORDER BY " + ','.join(col_name + d[i] for col_name,i in self._order)
        return query

    def sql_query(self):
        r"""
        Returns the SQLQuery.
        """
        return SQLQuery(self._db, self.get_query_string())

    def __iter__(self):
        r"""
        Iterate through the results of self.

        The function essentially wraps the iteration of SQLQuery in order to
        perform some data conversion.
        """
        from itertools import izip
        db = self._db
        for result in self.sql_query():
            r = []
            for i,j in izip(self._cols,result):
                if i in db._data_to_entry:
                    r.append(db._data_to_entry[i](j))
                elif ORIGAMI_DB_skeleton['origamis'][i]['sql'] == 'BOOLEAN':
                    r.append(eval(j))
                else:
                    r.append(j)
            if len(r) == 1:
                yield r[0]
            else:
                yield r

    def list(self):
        """
        Returns the list of entries of the query.

        The output is either a list of objects if there is only one column for
        that query. Otherwise, it is a list of lists where each item is the
        entries of columns.

        See also `meth:dict` to get a dictionnary output.

        EXAMPLES::

            sage: S = OrigamiDatabase(read_only=False)
            sage: q = S.query(('stratum','=',AbelianStratum(1,1)),('nb_squares','=',6))
            sage: q.list()
            [(1)(2)(3,4,5,6)
            (1,2,3)(4,5,6), (1)(2)(3)(4,5,6)
            (1,2,3,4)(5,6), (1)(2)(3,4)(5)(6)
            (1,2,3)(4,5,6), (1)(2)(3)(4,5)(6)
            (1,2,3,4)(5,6), (1)(2,3)(4,5)(6)
            (1,2,4)(3,5,6)]
        """
        return list(self)

    def dict(self):
        r"""
        Returns a list of dictionnaries: col -> value.

        EXAMPLES::

            sage: D = OrigamiDatabase(old_version=0)
            sage: q = D.query(stratum=AbelianStratum(1,1), nb_squares=8)
            sage: q.cols('teich_curve_genus')
            sage: q.dict()
            [{'teich_curve_genus': 1},
             {'teich_curve_genus': 1},
             {'teich_curve_genus': 0},
             {'teich_curve_genus': 0}]

            sage: q.cols('pole_partition', 'primitive')
            sage: q.dict()
            [{'pole_partition': (0, 2, 2, 2), 'primitive': True},
             {'pole_partition': (2, 0, 2, 2), 'primitive': True},
             {'pole_partition': (0, 0, 2, 4), 'primitive': False},
             {'pole_partition': (0, 0, 2, 4), 'primitive': False}]
        """
        if len(self._cols) == 1:
            return [{self._cols[0]:x} for x in self]
        else:
            return [dict(zip(self._cols,x)) for x in self]

    def number_of(self):
        """
        Returns the number of entries in the database that satisfy the
        query.
        """
        return sum(1 for _ in self)

    __len__ = number_of

    def latex(self):
        r"""
        Returns a nice latex array for that query.
        """
        from sage.misc.latex import Latex
        latex = Latex()

        l.append("\\begin{array}{|" + "c|"*len(self._cols) + "}")
        l.append("\\hline")
        l.append("&".join(map(str,self._cols)) + "\\\\")
        l.append("\\hline")
        for l in self:
            print '&'.join(latex(x) for x in l) + '\\\\'
        l.append("\\end{array}")
        return "\n".join(l)

    _latex_ = latex

    def show(self, **opts):
        r"""
        Output a text array with the results of that query.

        EXAMPLES:

        There is a problem with show method the SQLQuery::

            sage: O = OrigamiDatabase()
            sage: q = O.query(("nb_squares","=",6))
            sage: q.cols(("stratum","sum_of_L_exp","L_exp_approx"))
            sage: q.show()
            Traceback (most recent call last):
            ...
            TypeError: XXX
        """
        opts['format_cols'] = self._db._get_format(self._cols)
        opts['relabel_cols'] = relabel_cols
        return self.sql_query().show(**opts)


def build_local_data(o):
    r"""
    Build local data for the origami ``o``.

    The ouptut is a dictionnary that is intended to be used to feed the database
    of origamis. The local data are geometrical aspects (stratum, genus, ...) the
    monodromy group (primitivity, orientation cover, ...) and the automorphisms
    of ``o``.

    See also :func:`build_lyapunov_exponents` to construct Lyapunov exponents
    and :func:`build_global_data`.

    EXAMPLES::

        sage: o = Origami('(1,2)','(1,3)')
        sage: import sage.dynamics.flat_surfaces.origamis.origami_database as odb
        sage: data = odb.build_local_data(o) # optional -- database_gap
        sage: data['stratum']
        H_2(2)
        sage: data['nb_squares']
        3
    """
    from sage.functions.other import factorial

    data = {}

    data['representative'] = o

    data['stratum']    = o.stratum()
    data['component']  = o.stratum_component()._name
    data['genus']      = o.genus()
    data['nb_squares'] = o.nb_squares()

    G = o.monodromy()
    data['monodromy_order'] = G.order()
    data['monodromy_index'] = factorial(o.nb_squares()) / G.order()
    data['monodromy_signature'] = o.r().sign() == -1 or o.u().sign() == -1
    data['monodromy_solvable'] = G.is_solvable()
    data['monodromy_nilpotent'] = G.is_nilpotent()

    if o.is_primitive():
        data['primitive'] = True
        data['automorphism_group_order'] = 1
        data['automorphism_group_name'] = '1'
        data['regular'] = data['quasi_regular'] = False
        data['monodromy_name'] = gap.StructureDescription(G)
        data['optimal_degree'] = a*u

        d = o.orientation_data()
        if d:
            data['orientation_cover'] = True
            data['minus_identity_invariant'] = True
            assert len(d) == 1
            d = d[0]
            data['orientation_stratum'] = d[0]
            data['orientation_genus'] = d[0].genus()
            data['hyperelliptic'] = (d[0].genus() == 0)
            p0 = d[1].count(0)
            p1 = sorted(d[2])
            data['pole_partition'] = (p0,p1[0],p1[1],p1[2])

        else:
            data['orientation_cover'] = data['hyperelliptic'] = False
            data['pole_partition'] = data['orientation_stratum'] = data['orientation_genus'] = None

        if G.order() < 2500:
            data['monodromy_gap_primitive_id'] = gap.PrimitiveIdentification(G)
        else:
            data['monodromy_gap_primitive_id'] = None


    else: # non primitive
        data['primitive'] = False
        data['monodromy_name'] = data['monodromy_gap_primitive_id'] = None

        a,t,u = o.lattice_of_absolute_periods()
        data['optimal_degree'] = a*u

        A = o.automorphism_group()
        d = o.orientation_data()

        if not d:
            data['orientation_cover'] = False
            data['orientation_stratum'] = data['orientation_genus'] = data['pole_partition'] = None
            data['orientation_genus'] = None
            data['hyperelliptic'] = False

        elif A.order() == 1:
            data['orientation_cover'] = True
            data['orientation_stratum'] = d[0][0]
            data['orientation_genus'] = d[0][0].genus()
            data['hyperelliptic'] = (d[0][0].genus() == 0)
            data['minus_identity_invariant'] = True
            p0 = d[0][1].count(0)
            p1 = sorted(d[0][2])
            data['pole_partition'] = (p0,p1[0],p1[1],p1[2])

        else:
            data['orientation_cover'] = True
            data['orientation_stratum'] = data['orientation_genus'] = data['pole_partition'] = None
            data['hyperelliptic'] = any(x[0].genus() == 0 for x in d)
            if data['hyperelliptic']:
                dd = filter(lambda x: x[0].genus() == 0, d)
                assert len(dd) == 1
                dd = dd[0]
                p0 = dd[1].count(0)
                p1 = sorted(dd[2])
                data['pole_partition'] = (p0,p1[0],p1[1],p1[2])

        if o.is_regular():
            data['regular'] = data['quasi_regular'] = True
        elif o.is_quasi_regular():
            data['regular'] = False
            data['quasi_regular'] = True
        else:
            data['regular'] = data['quasi_regular'] = False

        data['automorphism_group_order'] = A.order()
        data['automorphism_group_name'] = gap.StructureDescription(A)

    return data

def build_lyapunov_exponents(o, nb_iterations=0X10000, nb_experiments=10):
    r"""
    Compute the lyapunov exponents for the origami ``o`` and update the
    database.

    TODO: when possible, separate exponents with respect to invariant subbundle
    of the Hodge bundle.
    """
    data = {}

    data['L_exp_approx'] = o.lyapunov_exponents_approx(
            nb_iterations=nb_iterations,
            nb_experiments=nb_experiments)

    return data

def build_global_data(o, c=None):
    r"""
    Compute the global data that are obtained from the Teichmueller curve of the
    origami ``o``. If the Teichmueller curve ``c`` is not provided, then it is
    recomputed from scratch (and may be long).
    """
    data = {}

    if c is None:
        c = o.teichmueller_curve()

    data['minus_identity_invariant'] = o.inverse().relabel() in c

    V = c.veech_group()
    data['veech_group_index'] = V.index()
    data['veech_group_congruence'] = V.is_congruence()
    data['veech_group_level'] = V.generalised_level()
    data['teich_curve_ncusps'] = V.ncusps()
    data['teich_curve_nu2'] = V.nu2()
    data['teich_curve_nu3'] = V.nu3()
    data['teich_curve_genus'] = V.genus()

    s = 0                   # sum of L. exp (Kontsevich formula)
    m_ncyls = 4*o.genus()+4 # min. nb cyls
    M_ncyls = 0             # max. nb cyls
    m_hd = 4*o.genus()+4    # min. Hom. dim
    M_hd = 0                # max. Hom. dim
    for (oo,l) in c.cusp_representative_iterator():
        cc,w,h,_ = oo.cylinder_diagram(data=True)
        nc = cc.ncyls()
        if nc < m_ncyls:
            m_ncyls = nc
        if nc > M_ncyls:
            M_ncyls = nc
        hd = cc.homological_dimension_of_cylinders()
        if hd < m_hd:
            m_hd = hd
        if hd > M_hd:
            M_hd = hd
        for j,bot in enumerate(cc.bot_cycle_tuples()):
            ww = sum(w[i] for i in bot)
            s += l * Integer(h[j]) / Integer(ww)

    s /= V.index()
    s += Integer(1)/Integer(12) * sum(m*(m+2)/(m+1) for m in o.stratum().zeros())

    data['sum_of_L_exp'] = s
    data['min_nb_of_cyls'] = m_ncyls
    data['max_nb_of_cyls'] = M_ncyls
    data['min_hom_dim'] = m_hd
    data['max_hom_dim'] = M_hd

    return data


class OrigamiDatabase(SQLDatabase):
    r"""
    Database of arithmetic Teichmueller curves.

    EXAMPLES:

    To query the database the main method is meth:`query`::

        sage: D = OrigamiDatabase()
        sage: q = D.query(genus=3, nb_squares=12)
        sage: q.number_of()
        146
        sage: l = q.list()
        sage: o = l[0]
        (1)(2)(3)(4)(5)(6)(7)(8)(9,10)(11,12)
        (1,2,3,4,5,6,7,8,9)(10,11)(12)
        sage: o.genus()
        3
        sage: o.nb_squares()
        12

    For the precise usage of the method query, see the documentation of that
    function. Here is an example to show how to found the Eierlegende
    Wollmilchsau in the database from its property of complete degenerate
    spectrum::

        sage: q = D.query(sum_of_L_exp=1, stratum=AbelianStratum(1,1,1,1))
        sage: len(q)
        1
        sage: o = q.list()[0]
        sage: o.is_isomorphic(origamis.EierlegendeWollmilchsau())
        True

    We check the classification of arithmetic Teichmueller curves in H(2) from
    Hubert-Lelievre and McMullen::

        sage: A = AbelianStratum(2)
        sage: for n in xrange(3, 15):
        ...     q = D.query(stratum=A, nb_squares=n)
        ...     print "%2d %d"%(n, q.number_of())
         3 1
         4 1
         5 2
         6 1
         7 2
         8 1
         9 2
        10 1
        11 2
        12 1
        13 2
        14 1

    To know all entries of the database look at `meth:cols`, `meth:info` or
    `meth:help`. The latter also provides a summary description of the columns.
    """
    def __init__(self, dblocation=None, read_only=True, force_creation=False,
            old_version=False):
        """
        INPUT:

        - ``dblocation`` - string - name of the database to use (optional).

        - ``read_only`` - bool (default: True) - if True, then the database is
          read_only and changes cannot be commited to disk.

        - ``force_creation`` - bool (default: False) - whether or not create the database.
        """
        import os.path
        import sage.dynamics.flat_surfaces.origamis.origami_database as odb

        if dblocation is None:
            dblocation = ORIGAMI_DB_LOCATION

        self._old_version = old_version
        if old_version is not False:
            skeleton = OLDS[old_version][0]
        else:
            skeleton = ORIGAMI_DB_skeleton

        if force_creation or not os.path.isfile(dblocation):
            assert read_only is False
            if os.path.isfile(dblocation):
                os.remove(dblocation)
            SQLDatabase.__init__(self,
                    dblocation,
                    read_only=read_only,
                    skeleton = skeleton)

        else:
            SQLDatabase.__init__(self, dblocation, read_only=read_only)
            if not are_skeleton_equal(self.get_skeleton(), skeleton):
                k0 = set(self.get_skeleton()['origamis'].keys())
                k1 = set(skeleton['origamis'].keys())

                k01 = k0.difference(k1)
                k10 = k1.difference(k0)

                msg = ""

                if k10:
                    msg += "\ncolumn(s) {} appear(s) in the skeleton but not in the database".format(sorted(k10))
                if k01:
                    msg += "\ncolumn(s) {} appear(s) in the database but not in the skeleton".format(sorted(k01))

                raise RuntimeError('Database at %s does not appear to be a valid origami databse'%dblocation + msg)

        self._data_to_entry = {}
        self._entry_to_data = {}
        self._format = {}
        for kwd in skeleton['origamis']:
            if hasattr(odb, 'data_to_' + kwd):
                self._format[kwd] = self._data_to_entry[kwd] = getattr(odb,'data_to_' + kwd)
            if hasattr(odb, kwd + '_to_data'):
                self._entry_to_data[kwd] = getattr(odb,kwd + '_to_data')
            if hasattr(odb, 'format_' + kwd):
                self._format[kwd] = getattr(odb, 'format_' + kwd)

        self._default_display = ['representative', 'stratum', 'component', 'veech_group_index']

    def __repr__(self):
        r"""
        String representation.

        TESTS::

            sage: OrigamiDatabase().__repr__()
            'Database of origamis'
        """
        return "Database of origamis"

    def __iter__(self):
        r"""
        Returns an iterator over all origami contained in that database.
        """
        return iter(self.query())

    def __len__(self):
        r"""
        Number of entry in that database.
        """
        return self.query().number_of()

    def cols(self):
        r"""
        Returns the skeleton of self (which is the list of possible entries).

        EXAMPLES::

            sage: O = OrigamiDatbase()
            sage: cols = O.cols()
            sage: "representative" in cols
            True
            sage: len(cols)
        """
        if self._old_version is not False:
            return OLDS[self._old_version][1][:]
        else:
            return ORIGAMI_DB_cols[:]

    def build(self, comp, N, force_computation=False, verbose=False):
        r"""
        Update the database for the given component ``comp`` up to ``N`` squares.

        Note that in order to work the database should not be in read only mode.

        INPUT:

        - ``comp`` - stratum or component of stratum

        - ``N`` - integer

        - ``force_computation`` - force computation of data which may be yet in
          the database.

        - ``verbose`` - boolean - if True, print useful interactive informations
          during the process.
        """
        assert not self.__read_only__, "The database should be not in read only"
        import sys
        from time import time

        if self._old_version is not False:
            columns = OLDS[self._old_version][1]
        else:
            columns = ORIGAMI_DB_cols

        k = 0 # counter for the number of modifications
        m = comp.stratum().dimension()-1
        if not force_computation:
            m = max(m,self.max_nb_squares(comp)+1)

        if verbose:
            T0 = time()

        for n in xrange(m, N):
            if verbose:
                print "nb_squares: %2d"%n
                print "=============="
                sys.stdout.flush()
                T1 = time()
            for c in comp.arithmetic_teichmueller_curves(n):
                data = {}
                o = c.origami()
                k += 1

                if verbose:
                    print "new entry r=%s u=%s"%(o.r(),o.u())
                    print " build local data...",
                    sys.stdout.flush()
                    t0 = time()
                data.update(build_local_data(o))
                if verbose:
                    print "done in %s s"%(time()-t0)
                    print " build lyapunov exponents...",
                    sys.stdout.flush()
                    t1 = time()
                data.update(build_lyapunov_exponents(o))
                if verbose:
                    print "done in %s s"%(time()-t1)
                    print " build global data...",
                    sys.stdout.flush()
                    t1 = time()
                data.update(build_global_data(o,c))
                if verbose:
                    t2 = time()
                    print "done in %s s"%(t2-t1)
                    print " total time: %s s"%(t2-t0)

                q = self.query(('representative','=',data['representative']))
                if len(q) == 1:
                    if verbose:
                        print "... the entry is yet in the database: update it."
                    self.delete_rows(q.sql_query())

                # check if there are missing columns
                s1 = set(ORIGAMI_DB_skeleton['origamis'].keys())
                s2 = set(data.keys())

                if verbose:
                    for x in s1.difference(s2):
                        print "WARNING: col %s does not appear in the request"%x
                    for x in s2.difference(s1):
                        print "WARNING: col %s appear in the request and should not"%x

                # convert data to fit the database format
                for key in data:
                    if key in self._data_to_entry:
                        data[key] = self._entry_to_data[key](data[key])

                value = [data.get(e,None) for e in columns]
                self.add_row('origamis', value, columns)

                if verbose:
                    print
                    sys.stdout.flush()

            if verbose:
                print "TOTAL TIME: %s\n"%(time()-T1)

        if verbose:
            print "%d Teichmueller curves added in %ss\n"%(k,time()-T0)

        self.commit()

    def _update_from_old_versions(self, other, verbose=False):
        r"""
        Update the database from an old one.

        As from time to time we might update the list of columns, this method is
        here to help the transition.

        INPUT:

        - ``other`` -- an OrigamiDatabase in an older version than ``self``

        - ``verbose`` -- if ``True`` print information about the missing columns
          in ``other`` and each column added
        """
        assert not self.__read_only__, "the database should not be in read only mode"

        if isinstance(other, OrigamiQuery):
            old_db = other.database()
            q = other
        elif isinstance(other, OrigamiDatabase):
            old_db = other
            q = other.query()
        else:
            raise ValueError("other must be a query or a database")

        old_cols = old_db.cols()
        q.cols(old_cols)
        new_cols = sorted(set(self.cols()).difference(old_cols))
        entry_order = old_cols + new_cols

        if verbose:
            print "new columns are: {}".format(new_cols)

        for x in q.dict():
            if verbose:
                print "consider new entry %s"%x['representative']

            if 'optimal_degree' in new_cols:
                x['optimal_degree'] = x['representative'].optimal_degree()

            for key in x:
                if key in self._data_to_entry:
                    x[key] = self._entry_to_data[key](x[key])

            entry_order = list(x)
            value = [x[e] for e in entry_order]
            self.add_row('origamis', value, entry_order)

        self.commit()


    def update(self, other, replace=False, verbose=False):
        r"""
        Update the content of this database with the content of another one.

        INPUT:

        - ``other`` - a query, an origami database or a path to an origami
          database

        - ``replace`` - boolean - whether or not replace entries which are yet
          in the database.

        - ``verbose`` - boolean - if True, displays information during the
          transfer.
        """
        assert not self.__read_only__, "the database should not be in read only mode"

        if isinstance(other, OrigamiQuery):
            q = other
            q.cols(ORIGAMI_DB_cols)
            q = q.sql_query()
        else:
            if isinstance(other, str):
                other = OrigamiDatabase(other)
            assert isinstance(other, OrigamiDatabase)
            q = SQLQuery(other, 'SELECT ' + ','.join(ORIGAMI_DB_cols) + ' FROM origamis')

        for x in q.query_results():
            if verbose:
                print "consider new entry %s"%x[0]
            qq = SQLQuery(self, "SELECT * FROM origamis WHERE representative='%s'"%str(x[0]))
            if len(qq.query_results()) == 1:
                if verbose:
                    print "yet in database"
                if not replace:
                    continue
                else:
                    self.delete_rows(qq)

            self.add_row('origamis', x, ORIGAMI_DB_cols)

        self.commit()

    def rebuild(self, q=None, local_data=False, lyapunov_exponents=False,
            global_data=False, nb_iterations=0X1000, nb_experiments=5,
            verbose=False):
        r"""
        Rebuild some of the data for the origami in the query ``q``.

        INPUT:

        - ``q`` - a query

        - ``local_data`` - boolean - whether or not we rebuild local data.

        - ``lyapunov_exponents`` - boolean - whether or not rebuild lyapunov
          exponents approximation (time consuming).

        - ``global_data`` - boolean - whether or not rebuild global data (time
          and memory consuming).

        - ``nb_experiments``, ``nb_iterations`` - integers - option for the
          computation of Lyapunov exponents.

        - ``verbose`` - boolean - if True displays nice informations in real
          time.
        """
        assert not self.__read_only__, "the database should not be in read only mode"
        if q is None:
            q = self.query()
        else:
            assert isinstance(q, OrigamiQuery) and q.database() == self
        q.cols('*')
        for x in q.dict():
            o = x['representative']
            qq = self.query(('representative','=',o))
            assert len(qq) == 1, "there is a problem!"
            self.delete_rows(qq.sql_query())

            if verbose:
                print "modifiy r=%s u=%s"%(o.r(),o.u())

            if local_data:
                x.update(build_local_data(o))
            if lyapunov_exponents:
                x.update(build_lyapunov_exponents(o,
                    nb_iterations=nb_iterations,
                    nb_experiments=nb_experiments))
            if global_data:
                x.update(build_global_data(o))

            for key in x:
                if key in self._data_to_entry:
                    x[key] = self._entry_to_data[key](x[key])

            entry_order = list(x)
            value = [x[e] for e in entry_order]
            self.add_row('origamis', value, entry_order)

        self.commit()

#    def strata(self, **kwds):
#        r"""
#        Return the list of strata for which some orbit are computed.
#
#        For precisions, see `meth:components` and `meth:info`.
#
#        INPUT:
#
#        - ``genus`` (optional)
#
#        - ``dimension`` (optional)
#
#        EXAMPLES::
#
#            sage: O = OrigamiDatabase()
#            sage: O.strata(genus=3)
#            [H_3(4), H_3(2^2), H_3(3, 1), H_3(2, 1^2), H_3(1^4)]
#        """
#        q = tuple((x,"=",kwds[x]) for x in kwds)
#        return sorted(set(self.query(*q,cols='stratum')))
#
#    def components(self):
#        r"""
#        Return the list of components for which some orbit are computed.
#
#        For more precisions, see `meth:info`.
#
#        EXAMPLES::
#
#            sage: O = OrigamiDatabase()
#            sage: O.components()
#            []
#        """
#        q = self.query()
#        q.cols(("stratum","component"))
#        return sorted(cc_from_name[x[1]](x[0]) for x in set(map(tuple,q)))

    def info(self, genus=None, dimension=None, print_all=False):
        r"""
        Print the list of connected components and the number of squares up to
        which the database is filled.

        INPUT:

        - ``genus`` - integer (default: None) - if not None, print only info for
          that genus.

        - ``dimension`` - Integer (default: None) - if not None, print only info
          for that dimension.

        - ``print_all`` - boolean (default: False) - print also the components
          for which nothing has been computed yet.

        EXAMPLES::

            sage: O = OrigamiDatabase()
            sage: O.info()
            genus 2
            =======
            ...
        """
        from sage.dynamics.flat_surfaces.abelian_strata import AbelianStrata

        if genus is None:
            q = self.query(cols='genus')
            if not q.number_of():
                print "Empty database"
                return
            genera = range(2,max(q)+1)
        elif isinstance(genus,(int,Integer)):
            genera = [genus]
        else:
            raise ValueError

        m = max(len(str(cc)) for a in AbelianStrata(genus=genera[-1]) for cc in a.components())
        s = ' {0!s:%s}: {1!s:>3} T. curves (up to {2!s:>2} squares)'%m

        n_total = 0
        for g in genera:
            AA = AbelianStrata(genus=g,dimension=dimension)
            if AA.cardinality():
                print "genus %d"%g
                print "======="
                for A in AA:
                    for CC in A.components():
                        n = self.query(("stratum","=",A),("component","=",CC._name)).number_of()
                        if n or print_all:
                            print s.format(CC,n,self.max_nb_squares(CC))
                            n_total += n
                print
        print
        print "Total: %d Teichmueller curves"%n_total

    def help(self, cols=None):
        r"""
        Print some help relative to the columns of the database.

        If ``cols`` is provided then gives help only for these columns.
        """
        raise NotImplementedError

    def max_nb_squares(self, comp=None):
        r"""
        Returns the maximum number of squares for which Teichmueller curves have
        been computed.

        If ``comp`` is None (default), then returns the biggest integer for
        which the database contains all data up to that integer. If ``comp`` is
        a stratum or a component of stratum, then returns the maximum number of
        squares computed for that stratum.

        EXAMPLES::

            sage: O = OrigamiDatabase()
            sage: O.max_nb_squares(AbelianStratum(2))
            25
            sage: O.max_nb_squares()
            4
        """
        from sage.dynamics.flat_surfaces.abelian_strata import \
        AbelianStratum,  AbelianStratumComponent, AbelianStrata

        if comp is None:
            m = self.max_nb_squares(AbelianStratum(2))
            d = 5
            while True:
                # at each step we test strata of dimension d and we have m >= d-1
                # if we do have equality at the end of the loop, we can not go
                # further
                for a in AbelianStrata(dimension=d):
                    k = self.max_nb_squares(a)
                    if k == 0: # we miss an origami with d-1 squares
                        return d-2
                    else:      # we can update m
                        m = min(k,m)
                if m == d-1:
                    return m
                d += 1

        elif isinstance(comp, AbelianStratum):
            return min(self.max_nb_squares(comp) for comp in comp.components())

        elif isinstance(comp, AbelianStratumComponent):
            stratum = comp.stratum()
            comp = comp._name
            query = self.query(('stratum','=',stratum),('component','=',comp))
            query.cols('nb_squares')
            if query.number_of() == 0:
                return 0
            return max(query.list())

        else:
            raise ValueError, "\"comp\" shoud be None, a stratum of Abelian differential or a component of stratum"

    def _get_format(self, cols):
        r"""
        Returns the dictionnary of functions for formatting the given the list
        ``cols`` of columns to display.

        EXAMPLES::

            sage: OrigamiDatabase().show() #indirect doctest
        """
        format_cols = {}
        for key in cols:
            if key in self._format:
                format_cols[key] = self._format[key]
        return format_cols

    def query(self, *query_list, **kwds):
        """
        From a list of restriction, returns a list of possible entry in the
        database. By default, returns only the found origamis.

        Where to find the possible entries self.cols() then a sign among '='
        (equality), '<>' (difference), '<', '>', '<=', >=' (comparisons).

        EXAMPLES::

            sage: D = OrigamiDatabase()
            sage: for o in D.query(stratum=AbelianStratum(1,1), nb_squares=6):
            ...    print o,"\n"
            (1)(2)(3,4,5,6)
            (1,2,3)(4,5,6)

            (1)(2)(3)(4,5,6)
            (1,2,3,4)(5,6)

            (1)(2)(3,4)(5)(6)
            (1,2,3)(4,5,6)

            (1)(2)(3)(4,5)(6)
            (1,2,3,4)(5,6)

            (1)(2,3)(4,5)(6)
            (1,2,4)(3,5,6)
        """
        if self._old_version:
            skeleton,columns = OLDS[self._old_version]
        else:
            skeleton = ORIGAMI_DB_skeleton
            columns = ORIGAMI_DB_cols

        if 'cols' in kwds:
            cols = kwds['cols']
            del kwds['cols']
        else:
            cols = ['representative']

        if isinstance(cols,str):
            cols = [cols]

        query_list = list(query_list)
        query_list.extend((entry,'=',value) for entry,value in kwds.iteritems())

        qq = []
        for entry,sign,value in query_list:
            if entry not in columns:
                raise ValueError("{} is not a valid column name".format(entry))
            if entry in self._entry_to_data:
                value = self._entry_to_data[entry](value)
            typ = skeleton['origamis'][entry]['sql']
            if typ == 'TEXT':
                qq.append("%s%s'%s'" %(entry,sign,str(value)))
            elif typ == 'BOOLEAN':
                if value:
                    qq.append("%s%s'True'"%(entry,sign))
                else:
                    qq.append("%s%s'False'"%(entry,sign))
            else:
                qq.append("%s%s%s"%(entry,sign,str(value)))

        if qq:
            query_string = ' AND '.join(qq)
        else:
            query_string = ''

        return OrigamiQuery(
                self,
                query_string = query_string,
                cols = cols,
                format_cols = self._get_format(cols))

