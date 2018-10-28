# -*- coding: utf-8 -*-
r"""
Directed graphs

This module implements functions and operations involving directed
graphs. Here is what they can do

**Graph basic operations:**

.. csv-table::
    :class: contentstable
    :widths: 30, 70
    :delim: |

    :meth:`~DiGraph.layout_acyclic_dummy` | Compute a (dummy) ranked layout so that all edges point upward.
    :meth:`~DiGraph.layout_acyclic` | Compute a ranked layout so that all edges point upward.
    :meth:`~DiGraph.reverse` | Return a copy of digraph with edges reversed in direction.
    :meth:`~DiGraph.reverse_edge` | Reverse an edge.
    :meth:`~DiGraph.reverse_edges` | Reverse a list of edges.
    :meth:`~DiGraph.out_degree_sequence` | Return the outdegree sequence.
    :meth:`~DiGraph.out_degree_iterator` | Same as degree_iterator, but for out degree.
    :meth:`~DiGraph.out_degree` | Same as degree, but for out degree.
    :meth:`~DiGraph.in_degree_sequence` | Return the indegree sequence of this digraph.
    :meth:`~DiGraph.in_degree_iterator` | Same as degree_iterator, but for in degree.
    :meth:`~DiGraph.in_degree` | Same as degree, but for in-degree.
    :meth:`~DiGraph.neighbors_out` | Return the list of the out-neighbors of a given vertex.
    :meth:`~DiGraph.neighbor_out_iterator` | Return an iterator over the out-neighbors of a given vertex.
    :meth:`~DiGraph.neighbors_in` | Return the list of the in-neighbors of a given vertex.
    :meth:`~DiGraph.neighbor_in_iterator` | Return an iterator over the in-neighbors of vertex.
    :meth:`~DiGraph.outgoing_edges` | Return a list of edges departing from vertices.
    :meth:`~DiGraph.outgoing_edge_iterator` | Return an iterator over all departing edges from vertices
    :meth:`~DiGraph.incoming_edges` | Return a list of edges arriving at vertices.
    :meth:`~DiGraph.incoming_edge_iterator` | Return an iterator over all arriving edges from vertices
    :meth:`~DiGraph.sources` | Return the list of all sources (vertices without incoming edges) of this digraph.
    :meth:`~DiGraph.sinks` | Return the list of all sinks (vertices without outgoing edges) of this digraph.
    :meth:`~DiGraph.to_undirected` | Return an undirected version of the graph.
    :meth:`~DiGraph.to_directed` | Since the graph is already directed, simply returns a copy of itself.
    :meth:`~DiGraph.is_directed` | Since digraph is directed, returns True.
    :meth:`~DiGraph.dig6_string` | Return the ``dig6`` representation of the digraph as an ASCII string.

**Paths and cycles:**

.. csv-table::
    :class: contentstable
    :widths: 30, 70
    :delim: |

    :meth:`~DiGraph.all_paths_iterator` | Return an iterator over the paths of ``self``.
    :meth:`~DiGraph.all_simple_paths` | Return a list of all the simple paths of ``self`` starting with one of the given vertices.
    :meth:`~DiGraph.all_cycles_iterator` | Return an iterator over all the cycles of ``self`` starting with one of the given vertices.
    :meth:`~DiGraph.all_simple_cycles` | Return a list of all simple cycles of ``self``.

**Representation theory:**

.. csv-table::
    :class: contentstable
    :widths: 30, 70
    :delim: |

    :meth:`~DiGraph.path_semigroup` | Return the (partial) semigroup formed by the paths of the digraph.

**Connectivity:**

.. csv-table::
    :class: contentstable
    :widths: 30, 70
    :delim: |

    :meth:`~DiGraph.is_strongly_connected` | Check whether the current ``DiGraph`` is strongly connected.
    :meth:`~DiGraph.strongly_connected_components_digraph` | Return the digraph of the strongly connected components
    :meth:`~DiGraph.strongly_connected_components_subgraphs` | Return the strongly connected components as a list of subgraphs.
    :meth:`~DiGraph.strongly_connected_component_containing_vertex` | Return the strongly connected component containing a given vertex
    :meth:`~DiGraph.strongly_connected_components` | Return the list of strongly connected components.
    :meth:`~DiGraph.immediate_dominators` | Return the immediate dominators of all vertices reachable from `root`.
    :meth:`~DiGraph.strong_articulation_points` | Return the strong articulation points of this digraph.


**Acyclicity:**

.. csv-table::
    :class: contentstable
    :widths: 30, 70
    :delim: |

    :meth:`~DiGraph.is_directed_acyclic` | Check whether the digraph is acyclic or not.
    :meth:`~DiGraph.is_transitive` | Check whether the digraph is transitive or not.
    :meth:`~DiGraph.is_aperiodic` | Check whether the digraph is aperiodic or not.
    :meth:`~DiGraph.is_tournament` | Check whether the digraph is a tournament.
    :meth:`~DiGraph.period` | Return the period of the digraph.
    :meth:`~DiGraph.level_sets` | Return the level set decomposition of the digraph.
    :meth:`~DiGraph.topological_sort_generator` | Return a list of all topological sorts of the digraph if it is acyclic
    :meth:`~DiGraph.topological_sort` | Return a topological sort of the digraph if it is acyclic

**Hard stuff:**

.. csv-table::
    :class: contentstable
    :widths: 30, 70
    :delim: |

    :meth:`~DiGraph.feedback_edge_set` | Compute the minimum feedback edge (arc) set of a digraph

**Miscellanous:**

.. csv-table::
    :class: contentstable
    :widths: 30, 70
    :delim: |

    :meth:`~DiGraph.flow_polytope` | Compute the flow polytope of a digraph
    :meth:`~DiGraph.degree_polynomial` | Return the generating polynomial of degrees of vertices in ``self``.

Methods
-------
"""

# ****************************************************************************
#       Copyright (C) 2010      Alexandre Blondin Masse <alexandre.blondin.masse at gmail.com>
#                               Carl Witty <cwitty@newtonlabs.com>
#                               Gregory McWhirter <gmcwhirt@uci.edu>
#                               Minh Van Nguyen <nguyenminh2@gmail.com>
#                     2010-2011 Robert L. Miller <rlm@rlmiller.org>
#                     2010-2015 Nathann Cohen <nathann.cohen@gmail.com>
#                               Nicolas M. Thiery <nthiery@users.sf.net>
#                     2011      Johannes Klaus Fichte <fichte@kr.tuwien.ac.at>
#                     2012      Javier López Peña <vengoroso@gmail.com>
#                     2012      Jim Stark <jstarx@gmail.com>
#                     2012      Karl-Dieter Crisman <kcrisman@gmail.com>
#                     2012      Keshav Kini <keshav.kini@gmail.com>
#                     2012      Lukas Lansky <lansky@kam.mff.cuni.cz>
#                     2012-2015 Volker Braun <vbraun.name@gmail.com>
#                     2012-2017 Jeroen Demeyer <jdemeyer@cage.ugent.be>
#                     2012-2018 David Coudert <david.coudert@inria.fr>
#                     2013      Emily Gunawan <egunawan@umn.edu>
#                     2013      Gregg Musiker <musiker@math.mit.edu>
#                     2013      Mathieu Guay-Paquet <mathieu.guaypaquet@gmail.com>
#                     2013-2014 Simon King <simon.king@uni-jena.de>
#                     2014      Clemens Heuberger <clemens.heuberger@aau.at>
#                               Erik Massop <e.massop@hccnet.nl>
#                               R. Andrew Ohana <andrew.ohana@gmail.com>
#                               Wilfried Luebbe <wluebbe@gmail.com>
#                     2014-2015 André Apitzsch <andre.apitzsch@etit.tu-chemnitz.de>
#                               Darij Grinberg <darijgrinberg@gmail.com>
#                               Travis Scrimshaw <tscrim at ucdavis.edu>
#                               Vincent Delecroix <20100.delecroix@gmail.com>
#                     2014-2017 Frédéric Chapoton <chapoton@math.univ-lyon1.fr>
#                     2015      Michele Borassi <michele.borassi@imtlucca.it>
#                     2015-2017 John H. Palmieri <palmieri@math.washington.edu>
#                               Jori Mäntysalo <jori.mantysalo@uta.fi>
#                     2016      Dima Pasechnik <dimpase@gmail.com>
#                     2018      Meghana M Reddy <mreddymeghana@gmail.com>
#                               Julian Rüth <julian.rueth@fsfe.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#                  https://www.gnu.org/licenses/
# ****************************************************************************
from __future__ import print_function, absolute_import

from copy import copy
from sage.rings.integer import Integer
from sage.rings.integer_ring import ZZ
from sage.misc.superseded import deprecation
import sage.graphs.generic_graph_pyx as generic_graph_pyx
from sage.graphs.generic_graph import GenericGraph
from sage.graphs.dot2tex_utils import have_dot2tex


class DiGraph(GenericGraph):
    r"""
    Directed graph.

    A digraph or directed graph is a set of vertices connected by oriented
    edges. See also the :wikipedia:`Directed_graph`. For a collection of
    pre-defined digraphs, see the :mod:`~sage.graphs.digraph_generators` module.

    A :class:`DiGraph` object has many methods whose list can be obtained by
    typing ``g.<tab>`` (i.e. hit the 'tab' key) or by reading the documentation
    of :mod:`~sage.graphs.digraph`, :mod:`~sage.graphs.generic_graph`, and
    :mod:`~sage.graphs.graph`.

    INPUT:

    By default, a :class:`DiGraph` object is simple (i.e. no *loops* nor
    *multiple edges*) and unweighted. This can be easily tuned with the
    appropriate flags (see below).

    - ``data`` -- can be any of the following (see the ``format`` argument):

      #. ``DiGraph()`` -- build a digraph on 0 vertices

      #. ``DiGraph(5)`` -- return an edgeless digraph on the 5 vertices 0,...,4

      #. ``DiGraph([list_of_vertices, list_of_edges])`` -- return a digraph with
         given vertices/edges

         To bypass auto-detection, prefer the more explicit
         ``DiGraph([V, E], format='vertices_and_edges')``.

      #. ``DiGraph(list_of_edges)`` -- return a digraph with a given list of
         edges (see documentation of
         :meth:`~sage.graphs.generic_graph.GenericGraph.add_edges`).

         To bypass auto-detection, prefer the more explicit
         ``DiGraph(L, format='list_of_edges')``.

      #. ``DiGraph({1: [2,3,4], 3: [4]})`` -- return a digraph by associating to
         each vertex the list of its out-neighbors.

         To bypass auto-detection, prefer the more explicit
         ``DiGraph(D, format='dict_of_lists')``.

      #. ``DiGraph({1: {2: 'a', 3: 'b'}, 3: {2: 'c'}})`` -- return a digraph by
         associating a list of out-neighbors to each vertex and providing its
         edge label.

         To bypass auto-detection, prefer the more explicit
         ``DiGraph(D, format='dict_of_dicts')``.

         For digraphs with multiple edges, you can provide a list of labels
         instead, e.g.: ``DiGraph({1: {2: ['a1', 'a2'], 3:['b']},
         3:{2:['c']}})``.

      #. ``DiGraph(a_matrix)`` -- return a digraph with given (weighted)
         adjacency matrix (see documentation of
         :meth:`~sage.graphs.generic_graph.GenericGraph.adjacency_matrix`).

         To bypass auto-detection, prefer the more explicit ``DiGraph(M,
         format='adjacency_matrix')``. To take weights into account, use
         ``format='weighted_adjacency_matrix'`` instead.

      #. ``DiGraph(a_nonsquare_matrix)`` -- return a digraph with given
         incidence matrix (see documentation of
         :meth:`~sage.graphs.generic_graph.GenericGraph.incidence_matrix`).

         To bypass auto-detection, prefer the more explicit ``DiGraph(M,
         format='incidence_matrix')``.

      #. ``DiGraph([V, f])`` -- return a digraph with a vertex set ``V`` and an
         edge `u,v` whenever `f(u, v)` is ``True``. Example: ``DiGraph([
         [1..10], lambda x,y: abs(x - y).is_square()])``

      #. ``DiGraph('FOC@?OC@_?')`` -- return a digraph from a ``dig6`` string
         (see documentation of :meth:`~dig6_string`).

      #. ``DiGraph(another_digraph)`` -- return a digraph from a Sage (di)graph,
         `pygraphviz <https://pygraphviz.github.io/>`__ digraph, `NetworkX
         <https://networkx.github.io/>`__ digraph, or `igraph
         <http://igraph.org/python/>`__ digraph.

    - ``pos`` -- dict (default: ``None``); a positioning dictionary. For
      example, the spring layout from NetworkX for the 5-cycle is::

         {0: [-0.91679746, 0.88169588],
          1: [ 0.47294849, 1.125     ],
          2: [ 1.125     ,-0.12867615],
          3: [ 0.12743933,-1.125     ],
          4: [-1.125     ,-0.50118505]}

    - ``name`` -- string (default: ``None``); gives the graph a name (e.g.,
      name="complete")

    - ``loops`` -- boolean (default: ``None``); whether to allow loops (ignored
      if data is an instance of the DiGraph class)

    - ``multiedges`` -- boolean (default: ``None``); whether to allow multiple
      edges (ignored if data is an instance of the DiGraph class)

    - ``weighted`` -- boolean (default: ``None``); whether digraph thinks of
      itself as weighted or not. See ``self.weighted()``

    - ``format`` -- string (default: ``None``); if set to ``None``,
      :class:`DiGraph` tries to guess input's format. To avoid this possibly
      time-consuming step, one of the following values can be specified (see
      description above): ``"int"``, ``"dig6"``, ``"rule"``,
      ``"list_of_edges"``, ``"dict_of_lists"``, ``"dict_of_dicts"``,
      ``"adjacency_matrix"``, ``"weighted_adjacency_matrix"``,
      ``"incidence_matrix"``, ``"NX"``, ``"igraph"``.

    - ``sparse`` -- boolean (default: ``True``); ``sparse=True`` is an alias for
      ``data_structure="sparse"``, and ``sparse=False`` is an alias for
      ``data_structure="dense"``

    - ``data_structure`` -- string (default: ``"sparse"``); one of the following
      (for more information, see :mod:`~sage.graphs.base.overview`):

      * ``"dense"`` -- selects the :mod:`~sage.graphs.base.dense_graph` backend

      * ``"sparse"`` -- selects the :mod:`~sage.graphs.base.sparse_graph`
        backend

      * ``"static_sparse"`` -- selects the
        :mod:`~sage.graphs.base.static_sparse_backend` (this backend is faster
        than the sparse backend and smaller in memory, and it is immutable, so
        that the resulting graphs can be used as dictionary keys).

    - ``immutable`` -- boolean (default: ``False``); whether to create a
      immutable digraph. Note that ``immutable=True`` is actually a shortcut for
      ``data_structure='static_sparse'``.

    - ``vertex_labels`` -- boolean (default: ``True``); whether to allow any
      object as a vertex (slower), or only the integers `0,...,n-1`, where `n`
      is the number of vertices.

    - ``convert_empty_dict_labels_to_None`` -- boolean (default: ``None``); this
      arguments sets the default edge labels used by NetworkX (empty
      dictionaries) to be replaced by ``None``, the default Sage edge label. It
      is set to ``True`` iff a NetworkX graph is on the input.

    EXAMPLES:

    #. A dictionary of dictionaries::

            sage: g = DiGraph({0: {1: 'x', 2: 'z', 3: 'a'}, 2: {5: 'out'}}); g
            Digraph on 5 vertices

       The labels ('x', 'z', 'a', 'out') are labels for edges. For example,
       'out' is the label for the edge from 2 to 5. Labels can be used as
       weights, if all the labels share some common parent.

    #. A dictionary of lists (or iterables)::

            sage: g = DiGraph({0: [1, 2, 3], 2: [4]}); g
            Digraph on 5 vertices
            sage: g = DiGraph({0: (1, 2, 3), 2: (4,)}); g
            Digraph on 5 vertices

    #. A list of vertices and a function describing adjacencies. Note that the
       list of vertices and the function must be enclosed in a list (i.e.,
       ``[list of vertices, function]``).

       We construct a graph on the integers 1 through 12 such that there is a
       directed edge from `i` to `j` if and only if `i` divides `j`.::

            sage: g = DiGraph([[1..12], lambda i,j: i != j and i.divides(j)])
            sage: g.vertices()
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
            sage: g.adjacency_matrix()
            [0 1 1 1 1 1 1 1 1 1 1 1]
            [0 0 0 1 0 1 0 1 0 1 0 1]
            [0 0 0 0 0 1 0 0 1 0 0 1]
            [0 0 0 0 0 0 0 1 0 0 0 1]
            [0 0 0 0 0 0 0 0 0 1 0 0]
            [0 0 0 0 0 0 0 0 0 0 0 1]
            [0 0 0 0 0 0 0 0 0 0 0 0]
            [0 0 0 0 0 0 0 0 0 0 0 0]
            [0 0 0 0 0 0 0 0 0 0 0 0]
            [0 0 0 0 0 0 0 0 0 0 0 0]
            [0 0 0 0 0 0 0 0 0 0 0 0]
            [0 0 0 0 0 0 0 0 0 0 0 0]

    #. A Sage matrix: Note: If format is not specified, then Sage assumes a
       square matrix is an adjacency matrix, and a nonsquare matrix is an
       incidence matrix.

       - an adjacency matrix::

            sage: M = Matrix([[0, 1, 1, 1, 0],[0, 0, 0, 0, 0],[0, 0, 0, 0, 1],[0, 0, 0, 0, 0],[0, 0, 0, 0, 0]]); M
            [0 1 1 1 0]
            [0 0 0 0 0]
            [0 0 0 0 1]
            [0 0 0 0 0]
            [0 0 0 0 0]
            sage: DiGraph(M)
            Digraph on 5 vertices

            sage: M = Matrix([[0,1,-1],[-1,0,-1/2],[1,1/2,0]]); M
            [   0    1   -1]
            [  -1    0 -1/2]
            [   1  1/2    0]
            sage: G = DiGraph(M,sparse=True,weighted=True); G
            Digraph on 3 vertices
            sage: G.weighted()
            True

       - an incidence matrix::

            sage: M = Matrix(6, [-1,0,0,0,1, 1,-1,0,0,0, 0,1,-1,0,0, 0,0,1,-1,0, 0,0,0,1,-1, 0,0,0,0,0]); M
            [-1  0  0  0  1]
            [ 1 -1  0  0  0]
            [ 0  1 -1  0  0]
            [ 0  0  1 -1  0]
            [ 0  0  0  1 -1]
            [ 0  0  0  0  0]
            sage: DiGraph(M)
            Digraph on 6 vertices

    #. A ``dig6`` string: Sage automatically recognizes whether a string is in
       ``dig6`` format, which is a directed version of ``graph6``::

            sage: D = DiGraph('IRAaDCIIOWEOKcPWAo')
            sage: D
            Digraph on 10 vertices

            sage: D = DiGraph('IRAaDCIIOEOKcPWAo')
            Traceback (most recent call last):
            ...
            RuntimeError: the string (IRAaDCIIOEOKcPWAo) seems corrupt: for n = 10, the string is too short

            sage: D = DiGraph("IRAaDCI'OWEOKcPWAo")
            Traceback (most recent call last):
            ...
            RuntimeError: the string seems corrupt: valid characters are
            ?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~

    #. A NetworkX XDiGraph::

            sage: import networkx
            sage: g = networkx.MultiDiGraph({0: [1, 2, 3], 2: [4]})
            sage: DiGraph(g)
            Digraph on 5 vertices


    #. A NetworkX digraph::

            sage: import networkx
            sage: g = networkx.DiGraph({0: [1, 2, 3], 2: [4]})
            sage: DiGraph(g)
            Digraph on 5 vertices

    #. An igraph directed Graph (see also
       :meth:`~sage.graphs.generic_graph.GenericGraph.igraph_graph`)::

           sage: import igraph                                  # optional - python_igraph
           sage: g = igraph.Graph([(0,1),(0,2)], directed=True) # optional - python_igraph
           sage: DiGraph(g)                                     # optional - python_igraph
           Digraph on 3 vertices

       If ``vertex_labels`` is ``True``, the names of the vertices are given by
       the vertex attribute ``'name'``, if available::

           sage: g = igraph.Graph([(0,1),(0,2)], directed=True, vertex_attrs={'name':['a','b','c']})  # optional - python_igraph
           sage: DiGraph(g).vertices()                                                                # optional - python_igraph
           ['a', 'b', 'c']
           sage: g = igraph.Graph([(0,1),(0,2)], directed=True, vertex_attrs={'label':['a','b','c']}) # optional - python_igraph
           sage: DiGraph(g).vertices()                                                                # optional - python_igraph
           [0, 1, 2]

       If the igraph Graph has edge attributes, they are used as edge labels::

           sage: g = igraph.Graph([(0,1),(0,2)], directed=True, edge_attrs={'name':['a','b'], 'weight':[1,3]}) # optional - python_igraph
           sage: DiGraph(g).edges()                                                                            # optional - python_igraph
           [(0, 1, {'name': 'a', 'weight': 1}), (0, 2, {'name': 'b', 'weight': 3})]


    TESTS::

        sage: DiGraph({0:[1,2,3], 2:[4]}).edges()
        [(0, 1, None), (0, 2, None), (0, 3, None), (2, 4, None)]
        sage: DiGraph({0:(1,2,3), 2:(4,)}).edges()
        [(0, 1, None), (0, 2, None), (0, 3, None), (2, 4, None)]
        sage: DiGraph({0:Set([1,2,3]), 2:Set([4])}).edges()
        [(0, 1, None), (0, 2, None), (0, 3, None), (2, 4, None)]

    Demonstrate that digraphs using the static backend are equal to mutable
    graphs but can be used as dictionary keys::

        sage: import networkx
        sage: g = networkx.DiGraph({0:[1,2,3], 2:[4]})
        sage: G = DiGraph(g)
        sage: G_imm = DiGraph(G, data_structure="static_sparse")
        sage: H_imm = DiGraph(G, data_structure="static_sparse")
        sage: H_imm is G_imm
        False
        sage: H_imm == G_imm == G
        True
        sage: {G_imm:1}[H_imm]
        1
        sage: {G_imm:1}[G]
        Traceback (most recent call last):
        ...
        TypeError: This graph is mutable, and thus not hashable. Create an
        immutable copy by `g.copy(immutable=True)`

    The error message states that one can also create immutable graphs by
    specifying the ``immutable`` optional argument (not only by
    ``data_structure='static_sparse'`` as above)::

        sage: J_imm = DiGraph(G, immutable=True)
        sage: J_imm == G_imm
        True
        sage: type(J_imm._backend) == type(G_imm._backend)
        True

    From a a list of vertices and a list of edges::

        sage: G = DiGraph([[1,2,3],[(1,2)]]); G
        Digraph on 3 vertices
        sage: G.edges()
        [(1, 2, None)]
    """
    _directed = True

    def __init__(self, data=None, pos=None, loops=None, format=None,
                 weighted=None, implementation='c_graph',
                 data_structure="sparse", vertex_labels=True, name=None,
                 multiedges=None, convert_empty_dict_labels_to_None=None,
                 sparse=True, immutable=False):
        """
        TESTS::

            sage: D = DiGraph()
            sage: loads(dumps(D)) == D
            True

            sage: a = matrix(2,2,[1,2,0,1])
            sage: DiGraph(a,sparse=True).adjacency_matrix() == a
            True

            sage: a = matrix(2,2,[3,2,0,1])
            sage: DiGraph(a,sparse=True).adjacency_matrix() == a
            True

        The positions are copied when the DiGraph is built from another DiGraph
        or from a Graph ::

            sage: g = DiGraph(graphs.PetersenGraph())
            sage: h = DiGraph(g)
            sage: g.get_pos() == h.get_pos()
            True
            sage: g.get_pos() == graphs.PetersenGraph().get_pos()
            True

        The position dictionary is not the input one (:trac:`22424`)::

            sage: my_pos = {0:(0,0), 1:(1,1)}
            sage: D = DiGraph([[0,1], [(0,1)]], pos=my_pos)
            sage: my_pos == D._pos
            True
            sage: my_pos is D._pos
            False

        Detection of multiple edges::

            sage: DiGraph({1:{2:[0,1]}})
            Multi-digraph on 2 vertices
            sage: DiGraph({1:{2:0}})
            Digraph on 2 vertices

        An empty list or dictionary defines a simple graph (:trac:`10441` and
        :trac:`12910`)::

            sage: DiGraph([])
            Digraph on 0 vertices
            sage: DiGraph({})
            Digraph on 0 vertices
            sage: # not "Multi-digraph on 0 vertices"

        Problem with weighted adjacency matrix (:trac:`13919`)::

            sage: B = {0:{1:2,2:5,3:4},1:{2:2,4:7},2:{3:1,4:4,5:3},3:{5:4},4:{5:1,6:5},5:{4:1,6:7,5:1}}
            sage: grafo3 = DiGraph(B, weighted=True)
            sage: matad = grafo3.weighted_adjacency_matrix()
            sage: grafo4 = DiGraph(matad, format="adjacency_matrix", weighted=True)
            sage: grafo4.shortest_path(0, 6, by_weight=True)
            [0, 1, 2, 5, 4, 6]

        Building a DiGraph with ``immutable=False`` returns a mutable graph::

            sage: g = graphs.PetersenGraph()
            sage: g = DiGraph(g.edges(), immutable=False)
            sage: g.add_edge("Hey", "Heyyyyyyy")
            sage: {g:1}[g]
            Traceback (most recent call last):
            ...
            TypeError: This graph is mutable, and thus not hashable. Create an immutable copy by `g.copy(immutable=True)`
            sage: copy(g) is g
            False
            sage: {g.copy(immutable=True):1}[g.copy(immutable=True)]
            1

        But building it with ``immutable=True`` returns an immutable graph::

            sage: g = DiGraph(graphs.PetersenGraph(), immutable=True)
            sage: g.add_edge("Hey", "Heyyyyyyy")
            Traceback (most recent call last):
            ...
            NotImplementedError
            sage: {g:1}[g]
            1
            sage: copy(g) is g    # copy is mutable again
            False

        Unknown input format::

            sage: DiGraph(4, format="HeyHeyHey")
            Traceback (most recent call last):
            ...
            ValueError: unknown input format 'HeyHeyHey'

        Sage DiGraph from igraph undirected graph::

            sage: import igraph           # optional - python_igraph
            sage: DiGraph(igraph.Graph()) # optional - python_igraph
            Traceback (most recent call last):
            ...
            ValueError: a *directed* igraph graph was expected. To build an undirected graph, call the Graph constructor
        """
        msg = ''
        GenericGraph.__init__(self)
        from sage.structure.element import is_Matrix

        if sparse is False:
            if data_structure != "sparse":
                raise ValueError("the 'sparse' argument is an alias for "
                                 "'data_structure', please do not define both")
            data_structure = "dense"

        # Choice of the backend

        if implementation != 'c_graph':
            from sage.misc.superseded import deprecation
            deprecation(18375,"The 'implementation' keyword is deprecated, "
                        "and the graphs has been stored as a 'c_graph'")

        if multiedges or weighted:
            if data_structure == "dense":
                raise RuntimeError("multiedge and weighted c_graphs must be sparse")

        if immutable:
            data_structure = 'static_sparse'

        # If the data structure is static_sparse, we first build a graph
        # using the sparse data structure, then reencode the resulting graph
        # as a static sparse graph.
        from sage.graphs.base.sparse_graph import SparseGraphBackend
        from sage.graphs.base.dense_graph import DenseGraphBackend
        if data_structure in ["sparse", "static_sparse"]:
            CGB = SparseGraphBackend
        elif data_structure == "dense":
             CGB = DenseGraphBackend
        else:
            raise ValueError("data_structure must be equal to 'sparse', "
                             "'static_sparse' or 'dense'")
        self._backend = CGB(0, directed=True)

        if format is None and isinstance(data, str):
            format = 'dig6'
            if data[:8] == ">>dig6<<":
                data = data[8:]
        if format is None and is_Matrix(data):
            if data.is_square():
                format = 'adjacency_matrix'
            else:
                format = 'incidence_matrix'
                msg += "Non-symmetric or non-square matrix assumed to be an incidence matrix: "
        if format is None and isinstance(data, DiGraph):
            format = 'DiGraph'
        from sage.graphs.all import Graph
        if format is None and isinstance(data, Graph):
            data = data.to_directed()
            format = 'DiGraph'
        if format is None and isinstance(data,list) and \
           len(data) >= 2 and callable(data[1]):
            format = 'rule'

        if (format is None            and
            isinstance(data, list)    and
            len(data) == 2            and
            isinstance(data[0], list) and # a list of two lists, the second of
            isinstance(data[1], list) and # which contains iterables (the edges)
            (not data[1] or callable(getattr(data[1][0], "__iter__", None)))):
            format = "vertices_and_edges"

        if format is None and isinstance(data, dict):
            if not data:
                format = 'dict_of_dicts'
            else:
                val = next(iter(data.values()))
                if isinstance(val, dict):
                    format = 'dict_of_dicts'
                else:
                    format = 'dict_of_lists'
        if format is None and hasattr(data, 'adj'):
            import networkx
            if isinstance(data, (networkx.Graph, networkx.MultiGraph)):
                data = data.to_directed()
                format = 'NX'
            elif isinstance(data, (networkx.DiGraph, networkx.MultiDiGraph)):
                format = 'NX'
        if (format is None          and
            hasattr(data, 'vcount') and
            hasattr(data, 'get_edgelist')):
            try:
                import igraph
            except ImportError:
                raise ImportError("the data seems to be a igraph object, but "
                                  "igraph is not installed in Sage. To install "
                                  "it, run 'sage -i python_igraph'")
            if format is None and isinstance(data, igraph.Graph):
                format = 'igraph'
        if format is None and isinstance(data, (int, Integer)):
            format = 'int'
        if format is None and data is None:
            format = 'int'
            data = 0

        # Input is a list of edges
        if format is None and isinstance(data,list):
            format = "list_of_edges"
            if weighted is None: weighted = False

        if format == 'weighted_adjacency_matrix':
            if weighted is False:
                raise ValueError("format was weighted_adjacency_matrix but weighted was False")
            if weighted   is None: weighted   = True
            if multiedges is None: multiedges = False
            format = 'adjacency_matrix'

        if format is None:
            raise ValueError("This input cannot be turned into a graph")

        # At this point, format has been set. We build the graph

        if format == 'dig6':
            if weighted is None: self._weighted = False
            self.allow_loops(True if loops else False, check=False)
            self.allow_multiple_edges(True if multiedges else False, check=False)
            from .graph_input import from_dig6
            from_dig6(self, data)

        elif format == 'adjacency_matrix':
            from .graph_input import from_adjacency_matrix
            from_adjacency_matrix(self, data, loops=loops, multiedges=multiedges, weighted=weighted)

        elif format == 'incidence_matrix':
            from .graph_input import from_oriented_incidence_matrix
            from_oriented_incidence_matrix(self, data, loops=loops, multiedges=multiedges, weighted=weighted)

        elif format == 'DiGraph':
            if loops is None: loops = data.allows_loops()
            elif not loops and data.has_loops():
                raise ValueError("the digraph was built with loops=False but input data has a loop")
            if multiedges is None: multiedges = data.allows_multiple_edges()
            elif not multiedges:
                e = data.edges(labels=False)
                if len(e) != len(set(e)):
                    raise ValueError("no multiple edges but input digraph"
                                     " has multiple edges")
            self.allow_multiple_edges(multiedges, check=False)
            self.allow_loops(loops, check=False)
            if weighted is None: weighted = data.weighted()
            if data.get_pos() is not None:
                pos = data.get_pos()
            self.add_vertices(data.vertex_iterator())
            self.add_edges(data.edge_iterator())
            self.name(data.name())
        elif format == 'rule':
            f = data[1]
            if loops is None: loops = any(f(v,v) for v in data[0])
            if weighted is None: weighted = False
            self.allow_multiple_edges(True if multiedges else False, check=False)
            self.allow_loops(loops,check=False)
            self.add_vertices(data[0])
            self.add_edges((u, v) for u in data[0] for v in data[0] if f(u, v))

        elif format == "vertices_and_edges":
            self.allow_multiple_edges(bool(multiedges), check=False)
            self.allow_loops(bool(loops), check=False)
            self.add_vertices(data[0])
            self.add_edges(data[1])

        elif format == 'dict_of_dicts':
            from .graph_input import from_dict_of_dicts
            from_dict_of_dicts(self, data, loops=loops, multiedges=multiedges, weighted=weighted,
                               convert_empty_dict_labels_to_None=False if convert_empty_dict_labels_to_None is None else convert_empty_dict_labels_to_None)

        elif format == 'dict_of_lists':
            from .graph_input import from_dict_of_lists
            from_dict_of_lists(self, data, loops=loops, multiedges=multiedges, weighted=weighted)

        elif format == 'NX':
            # adjust for empty dicts instead of None in NetworkX default edge labels
            if convert_empty_dict_labels_to_None is None:
                convert_empty_dict_labels_to_None = (format == 'NX')

            if weighted is None:
                if isinstance(data, networkx.DiGraph):
                    weighted = False
                    if multiedges is None:
                        multiedges = False
                    if loops is None:
                        loops = False
                else:
                    weighted = True
                    if multiedges is None:
                        multiedges = data.multiedges
                    if loops is None:
                        loops = data.selfloops
            if convert_empty_dict_labels_to_None:
                r = lambda x: None if x == {} else x
            else:
                r = lambda x: x

            self.allow_multiple_edges(multiedges, check=False)
            self.allow_loops(loops ,check=False)
            self.add_vertices(data.nodes())
            self.add_edges((u, v, r(l)) for u, v, l in data.edges(data=True))
        elif format == 'igraph':
            if not data.is_directed():
                raise ValueError("a *directed* igraph graph was expected. To "
                                 "build an undirected graph, call the Graph "
                                 "constructor")

            self.add_vertices(range(data.vcount()))
            self.add_edges((e.source, e.target, e.attributes()) for e in data.es())

            if vertex_labels and 'name' in data.vertex_attributes():
                vs = data.vs()
                self.relabel({v: vs[v]['name'] for v in self})

        elif format == 'int':
            if weighted   is None: weighted   = False
            self.allow_loops(True if loops else False, check=False)
            self.allow_multiple_edges(True if multiedges else False, check=False)
            if data < 0:
                raise ValueError("the number of vertices cannot be strictly negative")
            elif data:
                self.add_vertices(range(data))
        elif format == 'list_of_edges':
            self.allow_multiple_edges(False if multiedges is False else True)
            self.allow_loops(False if loops is False else True)
            self.add_edges(data)
            if multiedges is not True and self.has_multiple_edges():
                from sage.misc.superseded import deprecation
                deprecation(15706, "You created a graph with multiple edges "
                            "from a list. Please set 'multiedges' to 'True' "
                            "when you do so, as in the future the default "
                            "behaviour will be to ignore those edges")
            elif multiedges is None:
                self.allow_multiple_edges(False)

            if loops is not True and self.has_loops():
                from sage.misc.superseded import deprecation
                deprecation(15706, "You created a graph with loops from a list. "+
                            "Please set 'loops' to 'True' when you do so, as in "+
                            "the future the default behaviour will be to ignore "+
                            "those edges")
            elif loops is None:
                self.allow_loops(False)
        else:
            raise ValueError("unknown input format '{}'".format(format))

        # weighted, multiedges, loops, verts and num_verts should now be set
        self._weighted = weighted

        self._pos = copy(pos)

        if format != 'DiGraph' or name is not None:
            self.name(name)

        if data_structure == "static_sparse":
            from sage.graphs.base.static_sparse_backend import StaticSparseBackend
            ib = StaticSparseBackend(self,
                                     loops = self.allows_loops(),
                                     multiedges = self.allows_multiple_edges())
            self._backend = ib
            self._immutable = True

    ### Formats
    def dig6_string(self):
        r"""
        Return the ``dig6`` representation of the digraph as an ASCII string.

        This is only valid for single (no multiple edges) digraphs on at most
        `2^{18} - 1 = 262143` vertices.

        .. NOTE::

            As the ``dig6`` format only handles graphs with vertex set `\{0,
            \ldots, n-1\}`, a :meth:`relabelled copy
            <sage.graphs.generic_graph.GenericGraph.relabel>` will be encoded,
            if necessary.

        .. SEEALSO::

            * :meth:`~sage.graphs.graph.Graph.graph6_string` -- a similar string
              format for undirected graphs

        EXAMPLES::

            sage: D = DiGraph({0: [1, 2], 1: [2], 2: [3], 3: [0]})
            sage: D.dig6_string()
            'CW`_'

        TESTS::

            sage: DiGraph().dig6_string()
            '?'
        """
        n = self.order()
        if n > 262143:
            raise ValueError('dig6 format supports graphs on 0 to 262143 vertices only')
        elif self.has_multiple_edges():
            raise ValueError('dig6 format does not support multiple edges')
        else:
            return generic_graph_pyx.small_integer_to_graph6(n) + generic_graph_pyx.binary_string_to_graph6(self._bit_vector())

    ### Attributes

    def is_directed(self):
        """
        Since digraph is directed, return ``True``.

        EXAMPLES::

            sage: DiGraph().is_directed()
            True
        """
        return True

    ### Properties

    def is_directed_acyclic(self, certificate=False):
        """
        Return whether the digraph is acyclic or not.

        A directed graph is acyclic if for any vertex `v`, there is no directed
        path that starts and ends at `v`. Every directed acyclic graph (DAG)
        corresponds to a partial ordering of its vertices, however multiple dags
        may lead to the same partial ordering.

        INPUT:

        - ``certificate`` -- boolean (default: ``False``); whether to return a
          certificate

        OUTPUT:

        * When ``certificate=False``, returns a boolean value.

        * When ``certificate=True``:

          * If the graph is acyclic, returns a pair ``(True, ordering)`` where
            ``ordering`` is a list of the vertices such that ``u`` appears
            before ``v`` in ``ordering`` if ``u, v`` is an edge.

          * Else, returns a pair ``(False, cycle)`` where ``cycle`` is a list of
            vertices representing a circuit in the graph.

        EXAMPLES:

        At first, the following graph is acyclic::

            sage: D = DiGraph({0:[1, 2, 3], 4:[2, 5], 1:[8], 2:[7], 3:[7], 5:[6,7], 7:[8], 6:[9], 8:[10], 9:[10]})
            sage: D.plot(layout='circular').show()
            sage: D.is_directed_acyclic()
            True

        Adding an edge from `9` to `7` does not change it::

            sage: D.add_edge(9, 7)
            sage: D.is_directed_acyclic()
            True

        We can obtain as a proof an ordering of the vertices such that `u`
        appears before `v` if `uv` is an edge of the graph::

            sage: D.is_directed_acyclic(certificate=True)
            (True, [4, 5, 6, 9, 0, 1, 2, 3, 7, 8, 10])

        Adding an edge from 7 to 4, though, makes a difference::

            sage: D.add_edge(7, 4)
            sage: D.is_directed_acyclic()
            False

        Indeed, it creates a circuit `7, 4, 5`::

            sage: D.is_directed_acyclic(certificate=True)
            (False, [7, 4, 5])

        Checking acyclic graphs are indeed acyclic ::

            sage: def random_acyclic(n, p):
            ....:  g = graphs.RandomGNP(n, p)
            ....:  h = DiGraph()
            ....:  h.add_edges(((u, v) if u < v else (v, u)) for u, v in g.edge_iterator(labels=False))
            ....:  return h
            ...
            sage: all(random_acyclic(100, .2).is_directed_acyclic()    # long time
            ....:      for i in range(50))                             # long time
            True

        TESTS:

        What about loops? ::

            sage: g = digraphs.ButterflyGraph(3)
            sage: g.allow_loops(True)
            sage: g.is_directed_acyclic()
            True
            sage: g.add_edge(0, 0)
            sage: g.is_directed_acyclic()
            False
        """
        return self._backend.is_directed_acyclic(certificate=certificate)

    def to_directed(self):
        """
        Since the graph is already directed, simply returns a copy of itself.

        EXAMPLES::

            sage: DiGraph({0: [1, 2, 3], 4: [5, 1]}).to_directed()
            Digraph on 6 vertices
        """
        return self.copy()

    def to_undirected(self, implementation='c_graph', data_structure=None,
                      sparse=None):
        """
        Return an undirected version of the graph.

        Every directed edge becomes an edge.

        INPUT:

         - ``data_structure`` -- string (default: ``None``); one of
           ``"sparse"``, ``"static_sparse"``, or ``"dense"``. See the
           documentation of :class:`Graph` or :class:`DiGraph`.

         - ``sparse`` -- boolean (default: ``None``); ``sparse=True`` is an
           alias for ``data_structure="sparse"``, and ``sparse=False`` is an
           alias for ``data_structure="dense"``.

        EXAMPLES::

            sage: D = DiGraph({0: [1, 2], 1: [0]})
            sage: G = D.to_undirected()
            sage: D.edges(labels=False)
            [(0, 1), (0, 2), (1, 0)]
            sage: G.edges(labels=False)
            [(0, 1), (0, 2)]

        TESTS:

        Immutable graphs yield immutable graphs (:trac:`17005`)::

            sage: DiGraph([[1, 2]], immutable=True).to_undirected()._backend
            <sage.graphs.base.static_sparse_backend.StaticSparseBackend object at ...>
        """
        if sparse is not None:
            if data_structure is not None:
                raise ValueError("the 'sparse' argument is an alias for "
                                 "'data_structure'. Please do not define both")
            data_structure = "sparse" if sparse else "dense"

        if data_structure is None:
            from sage.graphs.base.dense_graph import DenseGraphBackend
            from sage.graphs.base.sparse_graph import SparseGraphBackend
            if isinstance(self._backend, DenseGraphBackend):
                data_structure = "dense"
            elif isinstance(self._backend, SparseGraphBackend):
                data_structure = "sparse"
            else:
                data_structure = "static_sparse"
        from sage.graphs.all import Graph
        G = Graph(name           = self.name(),
                  pos            = self._pos,
                  multiedges     = self.allows_multiple_edges(),
                  loops          = self.allows_loops(),
                  implementation = implementation,
                  data_structure = (data_structure if data_structure!="static_sparse"
                                    else "sparse")) # we need a mutable copy first

        G.add_vertices(self.vertex_iterator())
        G.add_edges(self.edge_iterator())
        if hasattr(self, '_embedding'):
            G._embedding = copy(self._embedding)
        G._weighted = self._weighted

        if data_structure == "static_sparse":
            G = G.copy(data_structure=data_structure)

        return G

    ### Edge Handlers

    def incoming_edge_iterator(self, vertices, labels=True):
        """
        Return an iterator over all arriving edges from vertices.

        INPUT:

        - ``vertices`` -- a vertex or a list of vertices

        - ``labels`` -- boolean (default: ``True``); whether to return edges as
          pairs of vertices, or as triples containing the labels

        EXAMPLES::

            sage: D = DiGraph({0: [1,2,3], 1: [0,2], 2: [3], 3: [4], 4: [0,5], 5: [1]})
            sage: for a in D.incoming_edge_iterator([0]):
            ....:     print(a)
            (1, 0, None)
            (4, 0, None)
        """
        if vertices is None:
            vertices = self
        elif vertices in self:
            vertices = [vertices]
        else:
            vertices = [v for v in vertices if v in self]
        return self._backend.iterator_in_edges(vertices, labels)

    def incoming_edges(self, vertices, labels=True):
        """
        Return a list of edges arriving at vertices.

        INPUT:

        - ``vertices`` -- a vertex or a list of vertices

        - ``labels`` -- boolean (default: ``True``); whether to return edges as
          pairs of vertices, or as triples containing the labels.

        EXAMPLES::

            sage: D = DiGraph({0: [1,2,3], 1: [0,2], 2: [3], 3: [4], 4: [0,5], 5: [1]})
            sage: D.incoming_edges([0])
            [(1, 0, None), (4, 0, None)]
        """
        return list(self.incoming_edge_iterator(vertices, labels=labels))

    def outgoing_edge_iterator(self, vertices, labels=True):
        """
        Return an iterator over all departing edges from vertices.

        INPUT:

        - ``vertices`` -- a vertex or a list of vertices

        - ``labels`` -- boolean (default: ``True``); whether to return edges as
          pairs of vertices, or as triples containing the labels.

        EXAMPLES::

            sage: D = DiGraph({0: [1,2,3], 1: [0,2], 2: [3], 3: [4], 4: [0,5], 5: [1]})
            sage: for a in D.outgoing_edge_iterator([0]):
            ....:     print(a)
            (0, 1, None)
            (0, 2, None)
            (0, 3, None)
        """
        if vertices is None:
            vertices = self
        elif vertices in self:
            vertices = [vertices]
        else:
            vertices = [v for v in vertices if v in self]
        return self._backend.iterator_out_edges(vertices, labels)

    def outgoing_edges(self, vertices, labels=True):
        """
        Return a list of edges departing from vertices.

        INPUT:

        - ``vertices`` -- a vertex or a list of vertices

        - ``labels`` -- boolean (default: ``True``); whether to return edges as
          pairs of vertices, or as triples containing the labels.

        EXAMPLES::

            sage: D = DiGraph({0: [1,2,3], 1: [0,2], 2: [3], 3: [4], 4: [0,5], 5: [1]})
            sage: D.outgoing_edges([0])
            [(0, 1, None), (0, 2, None), (0, 3, None)]
        """
        return list(self.outgoing_edge_iterator(vertices, labels=labels))

    def neighbor_in_iterator(self, vertex):
        """
        Return an iterator over the in-neighbors of ``vertex``.

        An vertex `u` is an in-neighbor of a vertex `v` if `uv` in an edge.

        EXAMPLES::

            sage: D = DiGraph({0: [1,2,3], 1: [0,2], 2: [3], 3: [4], 4: [0,5], 5: [1]})
            sage: for a in D.neighbor_in_iterator(0):
            ....:     print(a)
            1
            4
        """
        return iter(set(self._backend.iterator_in_nbrs(vertex)))

    def neighbors_in(self, vertex):
        """
        Return the list of the in-neighbors of a given vertex.

        A vertex `u` is an in-neighbor of a vertex `v` if `uv` in an edge.

        EXAMPLES::

            sage: D = DiGraph({0: [1,2,3], 1: [0,2], 2: [3], 3: [4], 4: [0,5], 5: [1]})
            sage: D.neighbors_in(0)
            [1, 4]
        """
        return list(self.neighbor_in_iterator(vertex))

    def neighbor_out_iterator(self, vertex):
        """
        Return an iterator over the out-neighbors of a given vertex.

        A vertex `u` is an out-neighbor of a vertex `v` if `vu` in an edge.

        EXAMPLES::

            sage: D = DiGraph({0: [1,2,3], 1: [0,2], 2: [3], 3: [4], 4: [0,5], 5: [1]})
            sage: for a in D.neighbor_out_iterator(0):
            ....:     print(a)
            1
            2
            3
        """
        return iter(set(self._backend.iterator_out_nbrs(vertex)))

    def neighbors_out(self, vertex):
        """
        Return the list of the out-neighbors of a given vertex.

        A vertex `u` is an out-neighbor of a vertex `v` if `vu` in an edge.

        EXAMPLES::

            sage: D = DiGraph({0: [1,2,3], 1: [0,2], 2: [3], 3: [4], 4: [0,5], 5: [1]})
            sage: D.neighbors_out(0)
            [1, 2, 3]
        """
        return list(self.neighbor_out_iterator(vertex))

    ### Degree functions

    def in_degree(self, vertices=None, labels=False):
        """
        Same as degree, but for in degree.

        EXAMPLES::

            sage: D = DiGraph({0: [1,2,3], 1: [0,2], 2: [3], 3: [4], 4: [0,5], 5: [1]})
            sage: D.in_degree(vertices=[0, 1, 2], labels=True)
            {0: 2, 1: 2, 2: 2}
            sage: D.in_degree()
            [2, 2, 2, 2, 1, 1]
            sage: G = graphs.PetersenGraph().to_directed()
            sage: G.in_degree(0)
            3
        """
        if vertices in self:
            return self._backend.in_degree(vertices)
        elif labels:
            return {v: d for v, d in self.in_degree_iterator(vertices, labels=labels)}
        else:
            return list(self.in_degree_iterator(vertices, labels=labels))

    def in_degree_iterator(self, vertices=None, labels=False):
        """
        Same as degree_iterator, but for in degree.

        EXAMPLES::

            sage: D = graphs.Grid2dGraph(2,4).to_directed()
            sage: for i in D.in_degree_iterator():
            ....:     print(i)
            3
            3
            2
            2
            3
            2
            2
            3
            sage: for i in D.in_degree_iterator(labels=True):
            ....:    print(i)
            ((0, 1), 3)
            ((1, 2), 3)
            ((0, 0), 2)
            ((0, 3), 2)
            ((1, 1), 3)
            ((1, 3), 2)
            ((1, 0), 2)
            ((0, 2), 3)
        """
        if vertices is None:
            vertices = self.vertex_iterator()
        if labels:
            for v in vertices:
                yield (v, self.in_degree(v))
        else:
            for v in vertices:
                yield self.in_degree(v)

    def in_degree_sequence(self):
        r"""
        Return the in-degree sequence.

        EXAMPLES:

        The in-degree sequences of two digraphs::

            sage: g = DiGraph({1: [2, 5, 6], 2: [3, 6], 3: [4, 6], 4: [6], 5: [4, 6]})
            sage: g.in_degree_sequence()
            [5, 2, 1, 1, 1, 0]

        ::

            sage: V = [2, 3, 5, 7, 8, 9, 10, 11]
            sage: E = [[], [8, 10], [11], [8, 11], [9], [], [], [2, 9, 10]]
            sage: g = DiGraph(dict(zip(V, E)))
            sage: g.in_degree_sequence()
            [2, 2, 2, 2, 1, 0, 0, 0]
        """
        return sorted(self.in_degree_iterator(), reverse=True)

    def out_degree(self, vertices=None, labels=False):
        """
        Same as degree, but for out degree.

        EXAMPLES::

            sage: D = DiGraph({0: [1,2,3], 1: [0,2], 2: [3], 3: [4], 4: [0,5], 5: [1]})
            sage: D.out_degree(vertices=[0, 1 ,2], labels=True)
            {0: 3, 1: 2, 2: 1}
            sage: D.out_degree()
            [3, 2, 1, 1, 2, 1]
            sage: D.out_degree(2)
            1
        """
        if vertices in self:
            return self._backend.out_degree(vertices)
        elif labels:
            return {v: d for v, d in self.out_degree_iterator(vertices, labels=labels)}
        else:
            return list(self.out_degree_iterator(vertices, labels=labels))

    def out_degree_iterator(self, vertices=None, labels=False):
        """
        Same as degree_iterator, but for out degree.

        EXAMPLES::

            sage: D = graphs.Grid2dGraph(2,4).to_directed()
            sage: for i in D.out_degree_iterator():
            ....:     print(i)
            3
            3
            2
            2
            3
            2
            2
            3
            sage: for i in D.out_degree_iterator(labels=True):
            ....:     print(i)
            ((0, 1), 3)
            ((1, 2), 3)
            ((0, 0), 2)
            ((0, 3), 2)
            ((1, 1), 3)
            ((1, 3), 2)
            ((1, 0), 2)
            ((0, 2), 3)
        """
        if vertices is None:
            vertices = self.vertex_iterator()
        if labels:
            for v in vertices:
                yield (v, self.out_degree(v))
        else:
            for v in vertices:
                yield self.out_degree(v)

    def out_degree_sequence(self):
        r"""
        Return the outdegree sequence of this digraph.

        EXAMPLES:

        The outdegree sequences of two digraphs::

            sage: g = DiGraph({1: [2, 5, 6], 2: [3, 6], 3: [4, 6], 4: [6], 5: [4, 6]})
            sage: g.out_degree_sequence()
            [3, 2, 2, 2, 1, 0]

        ::

            sage: V = [2, 3, 5, 7, 8, 9, 10, 11]
            sage: E = [[], [8, 10], [11], [8, 11], [9], [], [], [2, 9, 10]]
            sage: g = DiGraph(dict(zip(V, E)))
            sage: g.out_degree_sequence()
            [3, 2, 2, 1, 1, 0, 0, 0]
        """
        return sorted(self.out_degree_iterator(), reverse=True)

    def sources(self):
        r"""
        Return a list of sources of the digraph.

        OUTPUT:

        - list of the vertices of the digraph that have no edges going into them

        EXAMPLES::

            sage: G = DiGraph({1: {3: ['a']}, 2: {3: ['b']}})
            sage: G.sources()
            [1, 2]
            sage: T = DiGraph({1: {}})
            sage: T.sources()
            [1]
        """
        return [x for x in self if not self.in_degree(x)]

    def sinks(self):
        """
        Return a list of sinks of the digraph.

        OUTPUT:

        - list of the vertices of the digraph that have no edges beginning at them

        EXAMPLES::

            sage: G = DiGraph({1: {3: ['a']}, 2: {3: ['b']}})
            sage: G.sinks()
            [3]
            sage: T = DiGraph({1: {}})
            sage: T.sinks()
            [1]
        """
        return [x for x in self if not self.out_degree(x)]

    def degree_polynomial(self):
        r"""
        Return the generating polynomial of degrees of vertices in ``self``.

        This is the sum

        .. MATH::

            \sum_{v \in G} x^{\operatorname{in}(v)} y^{\operatorname{out}(v)},

        where ``in(v)`` and ``out(v)`` are the number of incoming and outgoing
        edges at vertex `v` in the digraph `G`.

        Because this polynomial is multiplicative for Cartesian product of
        digraphs, it is useful to help see if the digraph can be isomorphic to a
        Cartesian product.

        .. SEEALSO::

            :meth:`num_verts` for the value at `(x, y) = (1, 1)`

        EXAMPLES::

            sage: G = posets.PentagonPoset().hasse_diagram()
            sage: G.degree_polynomial()
            x^2 + 3*x*y + y^2

            sage: G = posets.BooleanLattice(4).hasse_diagram()
            sage: G.degree_polynomial().factor()
            (x + y)^4
        """
        from sage.rings.polynomial.polynomial_ring_constructor import PolynomialRing
        R = PolynomialRing(ZZ, 'x,y')
        x, y = R.gens()
        return R.sum(x ** self.in_degree(v) * y ** self.out_degree(v) for v in self)

    def feedback_edge_set(self, constraint_generation=True, value_only=False, solver=None, verbose=0):
        r"""
        Compute the minimum feedback edge set of a digraph (also called
        feedback arc set).

        The minimum feedback edge set of a digraph is a set of edges that
        intersect all the circuits of the digraph.  Equivalently, a minimum
        feedback arc set of a DiGraph is a set `S` of arcs such that the digraph
        `G - S` is acyclic. For more information, see the
        :wikipedia:`Feedback_arc_set`.

        INPUT:

        - ``value_only`` -- boolean (default: ``False``)

          - When set to ``True``, only the minimum cardinal of a minimum edge
            set is returned.

          - When set to ``False``, the ``Set`` of edges of a minimal edge set is
            returned.

        - ``constraint_generation`` -- boolean (default: ``True``); whether to
          use constraint generation when solving the Mixed Integer Linear
          Program.

        - ``solver`` -- string (default: ``None``); specify a Linear Program
          (LP) solver to be used. If set to ``None``, the default one is
          used. For more information on LP solvers and which default solver is
          used, see the method :meth:`solve
          <sage.numerical.mip.MixedIntegerLinearProgram.solve>` of the class
          :class:`MixedIntegerLinearProgram
          <sage.numerical.mip.MixedIntegerLinearProgram>`.

        - ``verbose`` -- integer (default: ``0``); sets the level of
          verbosity. Set to 0 by default, which means quiet.

        ALGORITHM:

        This problem is solved using Linear Programming, in two different
        ways. The first one is to solve the following formulation:

        .. MATH::

            \mbox{Minimize : }&\sum_{(u,v)\in G} b_{(u,v)}\\
            \mbox{Such that : }&\\
            &\forall (u,v)\in G, d_u-d_v+ n \cdot b_{(u,v)}\geq 0\\
            &\forall u\in G, 0\leq d_u\leq |G|\\

        An explanation:

        An acyclic digraph can be seen as a poset, and every poset has a linear
        extension. This means that in any acyclic digraph the vertices can be
        ordered with a total order `<` in such a way that if `(u,v) \in G`, then
        `u < v`.

        Thus, this linear program is built in order to assign to each vertex `v`
        a number `d_v \in [0,\dots,n-1]` such that if there exists an edge
        `(u, v) \in G` such that `d_v < d_u`, then the edge `(u,v)` is removed.

        The number of edges removed is then minimized, which is the objective.

        (Constraint Generation)

        If the parameter ``constraint_generation`` is enabled, a more efficient
        formulation is used :

        .. MATH::

            \mbox{Minimize : }&\sum_{(u,v)\in G} b_{(u,v)}\\
            \mbox{Such that : }&\\
            &\forall C\text{ circuits }\subseteq G, \sum_{uv\in C}b_{(u,v)}\geq 1\\

        As the number of circuits contained in a graph is exponential, this LP
        is solved through constraint generation. This means that the solver is
        sequentially asked to solved the problem, knowing only a portion of the
        circuits contained in `G`, each time adding to the list of its
        constraints the circuit which its last answer had left intact.

        EXAMPLES:

        If the digraph is created from a graph, and hence is symmetric (if `uv`
        is an edge, then `vu` is an edge too), then obviously the cardinality of
        its feedback arc set is the number of edges in the first graph::

            sage: cycle=graphs.CycleGraph(5)
            sage: dcycle=DiGraph(cycle)
            sage: cycle.size()
            5
            sage: dcycle.feedback_edge_set(value_only=True)
            5

        And in this situation, for any edge `uv` of the first graph, `uv` of
        `vu` is in the returned feedback arc set::

           sage: g = graphs.RandomGNP(5,.3)
           sage: dg = DiGraph(g)
           sage: feedback = dg.feedback_edge_set()
           sage: u,v,l = next(g.edge_iterator())
           sage: (u,v) in feedback or (v,u) in feedback
           True

        TESTS:

        Comparing with/without constraint generation. Also double-checks ticket
        :trac:`12833`::

            sage: for i in range(20):
            ....:     g = digraphs.RandomDirectedGNP(10, .3)
            ....:     x = g.feedback_edge_set(value_only=True)
            ....:     y = g.feedback_edge_set(value_only=True,
            ....:            constraint_generation=False)
            ....:     if x != y:
            ....:         print("Oh my, oh my !")
            ....:         break

        Loops are part of the feedback edge set (:trac:`23989`)::

            sage: D = digraphs.DeBruijn(2, 2)
            sage: D.loops(labels=None)
            [('11', '11'), ('00', '00')]
            sage: FAS = D.feedback_edge_set(value_only=False)
            sage: all(l in FAS for l in D.loops(labels=None))
            True
            sage: FAS2 =  D.feedback_edge_set(value_only=False, constraint_generation=False)
            sage: len(FAS) == len(FAS2)
            True

        Check that multi-edges are properly taken into account::

            sage: cycle = graphs.CycleGraph(5)
            sage: dcycle = DiGraph(cycle)
            sage: dcycle.feedback_edge_set(value_only=True)
            5
            sage: dcycle.allow_multiple_edges(True)
            sage: dcycle.add_edges(dcycle.edges())
            sage: dcycle.feedback_edge_set(value_only=True)
            10
            sage: dcycle.feedback_edge_set(value_only=True, constraint_generation=False)
            10

        Strongly connected components are well handled (:trac:`23989`)::

            sage: g = digraphs.Circuit(3) * 2
            sage: g.add_edge(0, 3)
            sage: g.feedback_edge_set(value_only=True)
            2
        """
        # It would be a pity to start a LP if the digraph is already acyclic
        if self.is_directed_acyclic():
            return 0 if value_only else []

        if self.has_loops():
            # We solve the problem on a copy without loops of the digraph
            D = DiGraph(self.edges(), multiedges=self.allows_multiple_edges(), loops=True)
            D.allow_loops(False)
            FAS = D.feedback_edge_set(constraint_generation=constraint_generation,
                                          value_only=value_only, solver=solver, verbose=verbose)
            if value_only:
                return FAS + self.number_of_loops()
            else:
                return FAS + self.loops(labels=None)

        if not self.is_strongly_connected():
            # If the digraph is not strongly connected, we solve the problem on
            # each of its strongly connected components

            FAS = 0 if value_only else []

            for h in self.strongly_connected_components_subgraphs():
                if value_only:
                    FAS += h.feedback_edge_set(constraint_generation=constraint_generation,
                                                value_only=True, solver=solver, verbose=verbose)
                else:
                    FAS.extend( h.feedback_edge_set(constraint_generation=constraint_generation,
                                                    value_only=False, solver=solver, verbose=verbose) )
            return FAS


        from sage.numerical.mip import MixedIntegerLinearProgram

        ########################################
        # Constraint Generation Implementation #
        ########################################
        if constraint_generation:

            p = MixedIntegerLinearProgram(constraint_generation=True,
                                          maximization=False, solver=solver)

            # An variable for each edge
            b = p.new_variable(binary=True)

            # Variables are binary, and their coefficient in the objective is
            # the number of occurence of the corresponding edge, so 1 if the
            # graph is simple
            p.set_objective( p.sum(b[u,v] for u,v in self.edge_iterator(labels=False)))

            p.solve(log=verbose)

            # For as long as we do not break because the digraph is acyclic....
            while True:

                # Building the graph without the edges removed by the LP
                h = DiGraph()
                for u,v in self.edge_iterator(labels=False):
                    if p.get_values(b[u,v]) < .5:
                        h.add_edge(u,v)

                # Is the digraph acyclic ?
                isok, certificate = h.is_directed_acyclic(certificate=True)

                # If so, we are done !
                if isok:
                    break

                # There is a circuit left. Let's add the corresponding
                # constraint !
                while not isok:

                    if verbose:
                        print("Adding a constraint on circuit : {}".format(certificate))

                    edges = zip(certificate, certificate[1:] + [certificate[0]])
                    p.add_constraint(p.sum(b[u, v] for u, v in edges), min=1)

                    # Is there another edge disjoint circuit ?
                    # for python3, we need to recreate the zip iterator
                    edges = zip(certificate, certificate[1:] + [certificate[0]])
                    h.delete_edges(edges)
                    isok, certificate = h.is_directed_acyclic(certificate=True)

                obj = p.solve(log=verbose)

            if value_only:
                return Integer(round(obj))

            else:
                # listing the edges contained in the MFAS
                return [(u, v) for u, v in self.edge_iterator(labels=False)
                        if p.get_values(b[u, v]) > .5]

        ######################################
        # Ordering-based MILP Implementation #
        ######################################
        else:
            p = MixedIntegerLinearProgram(maximization=False, solver=solver)

            b = p.new_variable(binary=True)
            d = p.new_variable(integer=True, nonnegative=True)

            n = self.order()

            for u,v in self.edge_iterator(labels=None):
                p.add_constraint(d[u] - d[v] + n * b[u,v], min=1)

            for v in self:
                p.add_constraint(d[v] <= n)

            p.set_objective(p.sum(b[u,v] for u,v in self.edge_iterator(labels=None)))

            if value_only:
                return Integer(round(p.solve(objective_only=True, log=verbose)))
            else:
                p.solve(log=verbose)

                b_sol = p.get_values(b)

                return [(u,v) for u,v in self.edge_iterator(labels=None) if b_sol[u,v]==1]

    ### Construction

    def reverse(self):
        """
        Return a copy of digraph with edges reversed in direction.

        EXAMPLES::

            sage: D = DiGraph({0: [1,2,3], 1: [0,2], 2: [3], 3: [4], 4: [0,5], 5: [1]})
            sage: D.reverse()
            Reverse of (): Digraph on 6 vertices
        """
        H = DiGraph(multiedges=self.allows_multiple_edges(), loops=self.allows_loops())
        H.add_vertices(self)
        H.add_edges((v, u, d) for u, v, d in self.edge_iterator())
        name = self.name()
        if name is None:
            name = ''
        H.name("Reverse of (%s)"%name)
        return H

    def reverse_edge(self, u, v=None, label=None, inplace=True, multiedges=None):
        """
        Reverse the edge from `u` to `v`.

        INPUT:

        - ``inplace`` -- boolean (default: ``True``); if ``False``, a new
          digraph is created and returned as output, otherwise ``self`` is
          modified.

        - ``multiedges`` -- boolean (default: ``None``); how to decide what
          should be done in case of doubt (for instance when edge `(1,2)` is to
          be reversed in a graph while `(2,1)` already exists):

          - If set to ``True``, input graph will be forced to allow parallel
            edges if necessary and edge `(1,2)` will appear twice in the graph.

          - If set to ``False``, only one edge `(1,2)` will remain in the graph
            after `(2,1)` is reversed. Besides, the label of edge `(1,2)` will
            be overwritten with the label of edge `(2,1)`.

          The default behaviour (``multiedges = None``) will raise an exception
          each time a subjective decision (setting ``multiedges`` to ``True`` or
          ``False``) is necessary to perform the operation.

        The following forms are all accepted:

        - D.reverse_edge( 1, 2 )
        - D.reverse_edge( (1, 2) )
        - D.reverse_edge( [1, 2] )
        - D.reverse_edge( 1, 2, 'label' )
        - D.reverse_edge( ( 1, 2, 'label') )
        - D.reverse_edge( [1, 2, 'label'] )
        - D.reverse_edge( ( 1, 2), label='label' )

        EXAMPLES:

        If ``inplace`` is ``True`` (default value), ``self`` is modified::

            sage: D = DiGraph([(0, 1 ,2)])
            sage: D.reverse_edge(0, 1)
            sage: D.edges()
            [(1, 0, 2)]

        If ``inplace`` is ``False``, ``self`` is not modified and a new digraph
        is returned::

            sage: D = DiGraph([(0, 1, 2)])
            sage: re = D.reverse_edge(0, 1, inplace=False)
            sage: re.edges()
            [(1, 0, 2)]
            sage: D.edges()
            [(0, 1, 2)]

        If ``multiedges`` is ``True``, ``self`` will be forced to allow parallel
        edges when and only when it is necessary::

            sage: D = DiGraph([(1, 2, 'A'), (2, 1, 'A'), (2, 3, None)])
            sage: D.reverse_edge(1, 2, multiedges=True)
            sage: D.edges()
            [(2, 1, 'A'), (2, 1, 'A'), (2, 3, None)]
            sage: D.allows_multiple_edges()
            True

        Even if ``multiedges`` is ``True``, ``self`` will not be forced to allow
        parallel edges when it is not necessary::

            sage: D = DiGraph( [(1, 2, 'A'), (2, 1, 'A'), (2, 3, None)] )
            sage: D.reverse_edge(2, 3, multiedges=True)
            sage: D.edges()
            [(1, 2, 'A'), (2, 1, 'A'), (3, 2, None)]
            sage: D.allows_multiple_edges()
            False

        If user specifies ``multiedges = False``, ``self`` will not be forced to
        allow parallel edges and a parallel edge will get deleted::

            sage: D = DiGraph( [(1, 2, 'A'), (2, 1, 'A'), (2, 3, None)] )
            sage: D.edges()
            [(1, 2, 'A'), (2, 1, 'A'), (2, 3, None)]
            sage: D.reverse_edge(1, 2, multiedges=False)
            sage: D.edges()
            [(2, 1, 'A'), (2, 3, None)]

        Note that in the following graph, specifying ``multiedges = False`` will
        result in overwriting the label of `(1, 2)` with the label of `(2, 1)`::

            sage: D = DiGraph( [(1, 2, 'B'), (2, 1, 'A'), (2, 3, None)] )
            sage: D.edges()
            [(1, 2, 'B'), (2, 1, 'A'), (2, 3, None)]
            sage: D.reverse_edge(2, 1, multiedges=False)
            sage: D.edges()
            [(1, 2, 'A'), (2, 3, None)]

        If input edge in digraph has weight/label, then the weight/label should
        be preserved in the output digraph.  User does not need to specify the
        weight/label when calling function::

            sage: D = DiGraph([[0, 1, 2], [1, 2, 1]], weighted=True)
            sage: D.reverse_edge(0, 1)
            sage: D.edges()
            [(1, 0, 2), (1, 2, 1)]
            sage: re = D.reverse_edge([1, 2], inplace=False)
            sage: re.edges()
            [(1, 0, 2), (2, 1, 1)]

        If ``self`` has multiple copies (parallel edges) of the input edge, only
        1 of the parallel edges is reversed::

            sage: D = DiGraph([(0, 1, '01'), (0, 1, '01'), (0, 1, 'cat'), (1, 2, '12')], weighted=True, multiedges=True)
            sage: re = D.reverse_edge([0, 1, '01'], inplace=False)
            sage: re.edges()
            [(0, 1, '01'), (0, 1, 'cat'), (1, 0, '01'), (1, 2, '12')]

        If ``self`` has multiple copies (parallel edges) of the input edge but
        with distinct labels and no input label is specified, only 1 of the
        parallel edges is reversed (the edge that is labeled by the first label
        on the list returned by :meth:`.edge_label`)::

            sage: D = DiGraph([(0, 1, 'A'), (0, 1, 'B'), (0, 1, 'mouse'), (0, 1, 'cat')], multiedges=true)
            sage: D.edge_label(0, 1)
            ['cat', 'mouse', 'B', 'A']
            sage: D.reverse_edge(0, 1)
            sage: D.edges()
            [(0, 1, 'A'), (0, 1, 'B'), (0, 1, 'mouse'), (1, 0, 'cat')]

        Finally, an exception is raised when Sage does not know how to choose
        between allowing multiple edges and losing some data::

            sage: D = DiGraph([(0, 1, 'A'), (1, 0, 'B')])
            sage: D.reverse_edge(0, 1)
            Traceback (most recent call last):
            ...
            ValueError: reversing the given edge is about to create two parallel
            edges but input digraph doesn't allow them - User needs to specify
            multiedges is True or False.

        The following syntax is supported, but note that you must use the
        ``label`` keyword::

            sage: D = DiGraph()
            sage: D.add_edge((1, 2), label='label')
            sage: D.edges()
            [(1, 2, 'label')]
            sage: D.reverse_edge((1, 2), label='label')
            sage: D.edges()
            [(2, 1, 'label')]
            sage: D.add_edge((1, 2), 'label')
            sage: D.edges()
            [(2, 1, 'label'), ((1, 2), 'label', None)]
            sage: D.reverse_edge((1, 2), 'label')
            sage: D.edges()
            [(2, 1, 'label'), ('label', (1, 2), None)]

        TESTS::

            sage: D = DiGraph([(0, 1, None)])
            sage: D.reverse_edge(0, 1, 'mylabel')
            Traceback (most recent call last):
            ...
            ValueError: input edge must exist in the digraph
        """
        # Assigns the expected values to u,v, and label depending on the input.
        if label is None:
            if v is None:
                try:
                    u, v, label = u
                except Exception:
                    try:
                        u, v = u
                    except Exception:
                        pass
        else:
            if v is None:
                try:
                    u, v = u
                except Exception:
                    pass

        if not self.has_edge(u,v,label):
            raise ValueError("input edge must exist in the digraph")

        tempG = self if inplace else copy(self)

        if label is None:
            if not tempG.allows_multiple_edges():
                label = tempG.edge_label(u, v)
            else:
                # If digraph has parallel edges for input edge, pick the first
                # from the labels on the list
                label = tempG.edge_label(u, v)[0]

        if ((not tempG.allows_multiple_edges()) and (tempG.has_edge(v, u))):
            # If user wants to force digraph to allow parallel edges
            if multiedges:
                tempG.allow_multiple_edges(True)
                tempG.delete_edge(u, v, label)
                tempG.add_edge(v, u, label)

            # If user does not want to force digraph to allow parallel edges, we
            # delete edge u to v and overwrite v,u with the label of u,v
            elif multiedges is False:
                tempG.delete_edge(u,v,label)
                tempG.set_edge_label(v,u,label)

            # User is supposed to specify multiedges True or False
            else:
                raise ValueError("reversing the given edge is about to "
                                 "create two parallel edges but input digraph "
                                 "doesn't allow them - User needs to specify "
                                 "multiedges is True or False.")
        else:
            tempG.delete_edge(u, v, label)
            tempG.add_edge(v, u, label)

        if not inplace:
            return tempG

    def reverse_edges(self, edges, inplace=True, multiedges=None):
        """
        Reverse a list of edges.

        INPUT:

        - ``edges`` -- a list of edges in the DiGraph.

        - ``inplace`` -- boolean (default: ``True``); if ``False``, a new
          digraph is created and returned as output, otherwise ``self`` is
          modified.

        - ``multiedges`` -- boolean (default: ``None``); if ``True``, input
          graph will be forced to allow parallel edges when necessary (for more
          information see the documentation of :meth:`~DiGraph.reverse_edge`)

        .. SEEALSO::

            :meth:`~DiGraph.reverse_edge` - Reverses a single edge.

        EXAMPLES:

        If ``inplace`` is ``True`` (default value), ``self`` is modified::

            sage: D = DiGraph({ 0: [1, 1, 3], 2: [3, 3], 4: [1, 5]}, multiedges=true)
            sage: D.reverse_edges([[0, 1], [0, 3]])
            sage: D.reverse_edges([(2, 3), (4, 5)])
            sage: D.edges()
            [(0, 1, None), (1, 0, None), (2, 3, None), (3, 0, None),
             (3, 2, None), (4, 1, None), (5, 4, None)]

        If ``inplace`` is ``False``, ``self`` is not modified and a new digraph
        is returned::

            sage: D = DiGraph([(0, 1, 'A'), (1, 0, 'B'), (1, 2, 'C')])
            sage: re = D.reverse_edges([(0, 1), (1, 2)],
            ....:                       inplace=False,
            ....:                       multiedges=True)
            sage: re.edges()
            [(1, 0, 'A'), (1, 0, 'B'), (2, 1, 'C')]
            sage: D.edges()
            [(0, 1, 'A'), (1, 0, 'B'), (1, 2, 'C')]
            sage: D.allows_multiple_edges()
            False
            sage: re.allows_multiple_edges()
            True

        If ``multiedges`` is ``True``, ``self`` will be forced to allow parallel
        edges when and only when it is necessary::

            sage: D = DiGraph([(1, 2, 'A'), (2, 1, 'A'), (2, 3, None)])
            sage: D.reverse_edges([(1, 2), (2, 3)], multiedges=True)
            sage: D.edges()
            [(2, 1, 'A'), (2, 1, 'A'), (3, 2, None)]
            sage: D.allows_multiple_edges()
            True

        Even if ``multiedges`` is ``True``, ``self`` will not be forced to allow
        parallel edges when it is not necessary::

            sage: D = DiGraph([(1, 2, 'A'), (2, 1, 'A'), (2, 3, None)])
            sage: D.reverse_edges([(2, 3)], multiedges=True)
            sage: D.edges()
            [(1, 2, 'A'), (2, 1, 'A'), (3, 2, None)]
            sage: D.allows_multiple_edges()
            False

        If ``multiedges`` is ``False``, ``self`` will not be forced to allow
        parallel edges and an edge will get deleted::

            sage: D = DiGraph([(1, 2), (2, 1)])
            sage: D.edges()
            [(1, 2, None), (2, 1, None)]
            sage: D.reverse_edges([(1, 2)], multiedges=False)
            sage: D.edges()
            [(2, 1, None)]

        If input edge in digraph has weight/label, then the weight/label should
        be preserved in the output digraph.  User does not need to specify the
        weight/label when calling function::

            sage: D = DiGraph([(0, 1, '01'), (1, 2, 1), (2, 3, '23')], weighted=True)
            sage: D.reverse_edges([(0, 1, '01'), (1, 2), (2, 3)])
            sage: D.edges()
            [(1, 0, '01'), (2, 1, 1), (3, 2, '23')]

        TESTS::

            sage: D = digraphs.Circuit(6)
            sage: D.reverse_edges(D.edges(), inplace=False).edges()
            [(0, 5, None), (1, 0, None), (2, 1, None),
             (3, 2, None), (4, 3, None), (5, 4, None)]

            sage: D = digraphs.Kautz(2, 3)
            sage: Dr = D.reverse_edges(D.edges(), inplace=False, multiedges=True)
            sage: Dr.edges() == D.reverse().edges()
            True
        """
        tempG = self if inplace else copy(self)
        for e in edges:
            tempG.reverse_edge(e,inplace=True,multiedges=multiedges)
        if not inplace:
            return tempG

    ### Paths and cycles iterators

    def _all_paths_iterator(self, vertex, ending_vertices=None,
                            simple=False, max_length=None, trivial=False):
        r"""
        Return an iterator over the paths of ``self`` starting with the
        given vertex.

        INPUT:

        - ``vertex`` -- the starting vertex of the paths

        - ``ending_vertices`` -- iterable (default: ``None``); allowed ending
          vertices of the paths. If ``None``, then all vertices are allowed.

        - ``simple`` -- boolean (default: ``False``); if set to ``True``, then
          only simple paths are considered. Simple paths are paths in which no
          two arcs share a head or share a tail, i.e. every vertex in the path
          is entered at most once and exited at most once.

        - ``max_length`` -- non negative integer (default: ``None``); the
          maximum length of the enumerated paths. If set to ``None``, then all
          lengths are allowed.

        - ``trivial`` - boolean (default: ``False``); if set to ``True``, then
          the empty paths are also enumerated.

        OUTPUT:

            iterator

        EXAMPLES::

            sage: g = DiGraph({'a': ['a', 'b'], 'b': ['c'], 'c': ['d'], 'd': ['c']}, loops=True)
            sage: pi = g._all_paths_iterator('a')
            sage: for _ in range(5): print(next(pi))
            ['a', 'a']
            ['a', 'b']
            ['a', 'a', 'a']
            ['a', 'a', 'b']
            ['a', 'b', 'c']

        ::

            sage: pi = g._all_paths_iterator('b')
            sage: for _ in range(5): print(next(pi))
            ['b', 'c']
            ['b', 'c', 'd']
            ['b', 'c', 'd', 'c']
            ['b', 'c', 'd', 'c', 'd']
            ['b', 'c', 'd', 'c', 'd', 'c']

        One may wish to enumerate simple paths, which are paths in which no two
        arcs share a head or share a tail, i.e. every vertex in the path is
        entered at most once and exited at most once. The result is always
        finite but may take a long time to compute::

            sage: pi = g._all_paths_iterator('a', simple=True)
            sage: list(pi)
            [['a', 'a'], ['a', 'b'], ['a', 'b', 'c'], ['a', 'b', 'c', 'd']]
            sage: pi = g._all_paths_iterator('d', simple=True)
            sage: list(pi)
            [['d', 'c'], ['d', 'c', 'd']]

        It is possible to specify the allowed ending vertices::

            sage: pi = g._all_paths_iterator('a', ending_vertices=['c'])
            sage: for _ in range(5): print(next(pi))
            ['a', 'b', 'c']
            ['a', 'a', 'b', 'c']
            ['a', 'a', 'a', 'b', 'c']
            ['a', 'b', 'c', 'd', 'c']
            ['a', 'a', 'a', 'a', 'b', 'c']
            sage: pi = g._all_paths_iterator('a', ending_vertices=['a', 'b'])
            sage: for _ in range(5): print(next(pi))
            ['a', 'a']
            ['a', 'b']
            ['a', 'a', 'a']
            ['a', 'a', 'b']
            ['a', 'a', 'a', 'a']

        One can bound the length of the paths::

            sage: pi = g._all_paths_iterator('d', max_length=3)
            sage: list(pi)
            [['d', 'c'], ['d', 'c', 'd'], ['d', 'c', 'd', 'c']]

        Or include the trivial empty path::

            sage: pi = g._all_paths_iterator('a', max_length=3, trivial=True)
            sage: list(pi)
            [['a'], ['a', 'a'], ['a', 'b'], ['a', 'a', 'a'], ['a', 'a', 'b'],
             ['a', 'b', 'c'], ['a', 'a', 'a', 'a'], ['a', 'a', 'a', 'b'],
             ['a', 'a', 'b', 'c'], ['a', 'b', 'c', 'd']]
        """
        if ending_vertices is None:
            ending_vertices = self
        if max_length is None:
            from sage.rings.infinity import Infinity
            max_length = Infinity
        if max_length < 1:
            return

        # Start with the empty path; we will try all extensions of it
        queue = []
        path = [vertex]

        if trivial and vertex in ending_vertices:
            yield path
        while True:
            # Build next generation of paths, one arc longer; max_length refers
            # to edges and not vertices, hence <= and not <
            if len(path) <= max_length:

                # We try all possible extensions
                if simple:
                    # We only keep simple extensions. An extension is simple iff
                    # the new vertex being entered has not previously occurred
                    # in the path, or has occurred but only been exited (i.e. is
                    # the first vertex in the path). In this latter case we must
                    # not exit the new vertex again, so we do not consider it
                    # for further extension, but just yield it immediately. See
                    # trac #12385.
                    for neighbor in self.neighbor_out_iterator(path[-1]):
                        if neighbor not in path:
                            queue.append(path + [neighbor])
                        elif ( neighbor == path[0] and
                               neighbor in ending_vertices ):
                            yield path + [neighbor]

                else:
                    # Non-simple paths requested: we add all of them
                    for neighbor in self.neighbor_out_iterator(path[-1]):
                        queue.append(path + [neighbor])

            if not queue:
                break
            path = queue.pop(0)     # get the next path

            if path[-1] in ending_vertices:
                yield path      # yield good path


    def all_paths_iterator(self, starting_vertices=None, ending_vertices=None,
                           simple=False, max_length=None, trivial=False):
        r"""
        Return an iterator over the paths of ``self``.

        The paths are enumerated in increasing length order.

        INPUT:

        - ``starting_vertices`` -- iterable (default: ``None``); vertices from
          which the paths must start. If ``None``, then all vertices of the
          graph can be starting points.

        - ``ending_vertices`` -- iterable (default: ``None``); allowed ending
          vertices of the paths. If ``None``, then all vertices are allowed.

        - ``simple`` -- boolean (default: ``False``); if set to ``True``, then
          only simple paths are considered. Simple paths are paths in which no
          two arcs share a head or share a tail, i.e. every vertex in the path
          is entered at most once and exited at most once.

        - ``max_length`` -- non negative integer (default: ``None``); the
          maximum length of the enumerated paths. If set to ``None``, then all
          lengths are allowed.

        - ``trivial`` - boolean (default: ``False``); if set to ``True``, then
          the empty paths are also enumerated.

        OUTPUT:

            iterator

        AUTHOR:

            Alexandre Blondin Masse

        EXAMPLES::

            sage: g = DiGraph({'a': ['a', 'b'], 'b': ['c'], 'c': ['d'], 'd': ['c']}, loops=True)
            sage: pi = g.all_paths_iterator()
            sage: for _ in range(7): print(next(pi))
            ['a', 'a']
            ['a', 'b']
            ['b', 'c']
            ['c', 'd']
            ['d', 'c']
            ['a', 'a', 'a']
            ['a', 'a', 'b']

        It is possible to precise the allowed starting and/or ending vertices::

            sage: pi = g.all_paths_iterator(starting_vertices=['a'])
            sage: for _ in range(5): print(next(pi))
            ['a', 'a']
            ['a', 'b']
            ['a', 'a', 'a']
            ['a', 'a', 'b']
            ['a', 'b', 'c']
            sage: pi = g.all_paths_iterator(starting_vertices=['a'], ending_vertices=['b'])
            sage: for _ in range(5): print(next(pi))
            ['a', 'b']
            ['a', 'a', 'b']
            ['a', 'a', 'a', 'b']
            ['a', 'a', 'a', 'a', 'b']
            ['a', 'a', 'a', 'a', 'a', 'b']

        One may prefer to enumerate only simple paths (see
        :meth:`all_simple_paths`)::

            sage: pi = g.all_paths_iterator(simple=True)
            sage: list(pi)
            [['a', 'a'], ['a', 'b'], ['b', 'c'], ['c', 'd'], ['d', 'c'],
             ['a', 'b', 'c'], ['b', 'c', 'd'], ['c', 'd', 'c'],
             ['d', 'c', 'd'], ['a', 'b', 'c', 'd']]

        Or simply bound the length of the enumerated paths::

            sage: pi = g.all_paths_iterator(starting_vertices=['a'], ending_vertices=['b', 'c'], max_length=6)
            sage: list(pi)
            [['a', 'b'], ['a', 'a', 'b'], ['a', 'b', 'c'],
             ['a', 'a', 'a', 'b'], ['a', 'a', 'b', 'c'],
             ['a', 'a', 'a', 'a', 'b'], ['a', 'a', 'a', 'b', 'c'],
             ['a', 'b', 'c', 'd', 'c'], ['a', 'a', 'a', 'a', 'a', 'b'],
             ['a', 'a', 'a', 'a', 'b', 'c'], ['a', 'a', 'b', 'c', 'd', 'c'],
             ['a', 'a', 'a', 'a', 'a', 'a', 'b'],
             ['a', 'a', 'a', 'a', 'a', 'b', 'c'],
             ['a', 'a', 'a', 'b', 'c', 'd', 'c'],
             ['a', 'b', 'c', 'd', 'c', 'd', 'c']]

        By default, empty paths are not enumerated, but it may be parametrized::

            sage: pi = g.all_paths_iterator(simple=True, trivial=True)
            sage: list(pi)
            [['a'], ['b'], ['c'], ['d'], ['a', 'a'], ['a', 'b'], ['b', 'c'],
             ['c', 'd'], ['d', 'c'], ['a', 'b', 'c'], ['b', 'c', 'd'],
             ['c', 'd', 'c'], ['d', 'c', 'd'], ['a', 'b', 'c', 'd']]
            sage: pi = g.all_paths_iterator(simple=True, trivial=False)
            sage: list(pi)
            [['a', 'a'], ['a', 'b'], ['b', 'c'], ['c', 'd'], ['d', 'c'],
             ['a', 'b', 'c'], ['b', 'c', 'd'], ['c', 'd', 'c'],
             ['d', 'c', 'd'], ['a', 'b', 'c', 'd']]
        """
        if starting_vertices is None:
            starting_vertices = self
        # We create one paths iterator per vertex
        # This is necessary if we want to iterate over paths
        # with increasing length
        vertex_iterators = {v: self._all_paths_iterator(v, ending_vertices=ending_vertices,
                                                            simple=simple, max_length=max_length,
                                                            trivial=trivial) for v in starting_vertices}
        paths = []
        for vi in vertex_iterators.values():
            try:
                path = next(vi)
                paths.append((len(path), path))
            except(StopIteration):
                pass
        # Since we always extract a shortest path, using a heap
        # can speed up the algorithm
        from heapq import heapify, heappop, heappush
        heapify(paths)
        while paths:
            # We choose the shortest available path
            _, shortest_path = heappop(paths)
            yield shortest_path
            # We update the path iterator to its next available path if it exists
            try:
                path = next(vertex_iterators[shortest_path[0]])
                heappush(paths, (len(path), path))
            except(StopIteration):
                pass

    def all_simple_paths(self, starting_vertices=None, ending_vertices=None,
                         max_length=None, trivial=False):
        r"""
        Return a list of all the simple paths of ``self`` starting with one of
        the given vertices.

        Simple paths are paths in which no two arcs share a head or share a
        tail, i.e. every vertex in the path is entered at most once and exited
        at most once.

        INPUT:

        - ``starting_vertices`` -- list (default: ``None``); vertices from which
          the paths must start. If ``None``, then all vertices of the graph can
          be starting points.

        - ``ending_vertices`` -- iterable (default: ``None``); allowed ending
          vertices of the paths. If ``None``, then all vertices are allowed.

        - ``max_length`` -- non negative integer (default: ``None``); the
          maximum length of the enumerated paths. If set to ``None``, then all
          lengths are allowed.

        - ``trivial`` - boolean (default: ``False``); if set to ``True``, then
          the empty paths are also enumerated.

        OUTPUT:

            list

        .. NOTE::

            Although the number of simple paths of a finite graph is always
            finite, computing all its paths may take a very long time.

        EXAMPLES::

            sage: g = DiGraph({'a': ['a', 'b'], 'b': ['c'], 'c': ['d'], 'd': ['c']}, loops=True)
            sage: g.all_simple_paths()
            [['a', 'a'], ['a', 'b'], ['b', 'c'], ['c', 'd'], ['d', 'c'],
             ['a', 'b', 'c'], ['b', 'c', 'd'], ['c', 'd', 'c'],
             ['d', 'c', 'd'], ['a', 'b', 'c', 'd']]

        One may compute all paths having specific starting and/or ending
        vertices::

            sage: g.all_simple_paths(starting_vertices=['a'])
            [['a', 'a'], ['a', 'b'], ['a', 'b', 'c'], ['a', 'b', 'c', 'd']]
            sage: g.all_simple_paths(starting_vertices=['a'], ending_vertices=['c'])
            [['a', 'b', 'c']]
            sage: g.all_simple_paths(starting_vertices=['a'], ending_vertices=['b', 'c'])
            [['a', 'b'], ['a', 'b', 'c']]

        It is also possible to bound the length of the paths::

            sage: g.all_simple_paths(max_length=2)
            [['a', 'a'], ['a', 'b'], ['b', 'c'], ['c', 'd'], ['d', 'c'],
             ['a', 'b', 'c'], ['b', 'c', 'd'], ['c', 'd', 'c'],
             ['d', 'c', 'd']]

        By default, empty paths are not enumerated, but this can be
        parametrized::

            sage: g.all_simple_paths(starting_vertices=['a'], trivial=True)
            [['a'], ['a', 'a'], ['a', 'b'], ['a', 'b', 'c'],
             ['a', 'b', 'c', 'd']]
            sage: g.all_simple_paths(starting_vertices=['a'], trivial=False)
            [['a', 'a'], ['a', 'b'], ['a', 'b', 'c'], ['a', 'b', 'c', 'd']]
        """
        return list(self.all_paths_iterator(starting_vertices=starting_vertices,
                                                ending_vertices=ending_vertices,
                                                simple=True, max_length=max_length,
                                                trivial=trivial))

    def _all_cycles_iterator_vertex(self, vertex, starting_vertices=None, simple=False,
                                    rooted=False, max_length=None, trivial=False,
                                    remove_acyclic_edges=True):
        r"""
        Return an iterator over the cycles of ``self`` starting with the given
        vertex.

        INPUT:

        - ``vertex`` -- the starting vertex of the cycle

        - ``starting_vertices`` -- iterable (default: ``None``); vertices from
          which the cycles must start. If ``None``, then all vertices of the
          graph can be starting points. This argument is necessary if ``rooted``
          is set to ``True``.

        - ``simple`` -- boolean (default: ``False``); if set to ``True``, then
          only simple cycles are considered. A cycle is simple if the only
          vertex occuring twice in it is the starting and ending one.

        - ``rooted`` -- boolean (default: ``False``); if set to False, then
          cycles differing only by their starting vertex are considered the same
          (e.g. ``['a', 'b', 'c', 'a']`` and ``['b', 'c', 'a',
          'b']``). Otherwise, all cycles are enumerated.

        - ``max_length`` -- non negative integer (default: ``None``); the
          maximum length of the enumerated paths. If set to ``None``, then all
          lengths are allowed.

        - ``trivial`` - boolean (default: ``False``); if set to ``True``, then
          the empty paths are also enumerated.

        - ``remove_acyclic_edges`` -- boolean (default: ``True``); whether
          acyclic edges must be removed from the graph.  Used to avoid
          recomputing it for each vertex

        OUTPUT:

            iterator

        EXAMPLES::

            sage: g = DiGraph({'a': ['a', 'b'], 'b': ['c'], 'c': ['d'], 'd': ['c']}, loops=True)
            sage: it = g._all_cycles_iterator_vertex('a', simple=False, max_length=None)
            sage: for i in range(5): print(next(it))
            ['a', 'a']
            ['a', 'a', 'a']
            ['a', 'a', 'a', 'a']
            ['a', 'a', 'a', 'a', 'a']
            ['a', 'a', 'a', 'a', 'a', 'a']
            sage: it = g._all_cycles_iterator_vertex('c', simple=False, max_length=None)
            sage: for i in range(5): print(next(it))
            ['c', 'd', 'c']
            ['c', 'd', 'c', 'd', 'c']
            ['c', 'd', 'c', 'd', 'c', 'd', 'c']
            ['c', 'd', 'c', 'd', 'c', 'd', 'c', 'd', 'c']
            ['c', 'd', 'c', 'd', 'c', 'd', 'c', 'd', 'c', 'd', 'c']

            sage: it = g._all_cycles_iterator_vertex('d', simple=False, max_length=None)
            sage: for i in range(5): print(next(it))
            ['d', 'c', 'd']
            ['d', 'c', 'd', 'c', 'd']
            ['d', 'c', 'd', 'c', 'd', 'c', 'd']
            ['d', 'c', 'd', 'c', 'd', 'c', 'd', 'c', 'd']
            ['d', 'c', 'd', 'c', 'd', 'c', 'd', 'c', 'd', 'c', 'd']

        It is possible to set a maximum length so that the number of cycles is
        finite::

            sage: it = g._all_cycles_iterator_vertex('d', simple=False, max_length=6)
            sage: list(it)
            [['d', 'c', 'd'], ['d', 'c', 'd', 'c', 'd'], ['d', 'c', 'd', 'c', 'd', 'c', 'd']]

        When ``simple`` is set to True, the number of cycles is finite since no vertex
        but the first one can occur more than once::

            sage: it = g._all_cycles_iterator_vertex('d', simple=True, max_length=None)
            sage: list(it)
            [['d', 'c', 'd']]

        By default, the empty cycle is not enumerated::

            sage: it = g._all_cycles_iterator_vertex('d', simple=True, trivial=True)
            sage: list(it)
            [['d'], ['d', 'c', 'd']]
        """
        if starting_vertices is None:
            starting_vertices = [vertex]
        # First enumerate the empty cycle
        if trivial:
            yield [vertex]
        # First we remove vertices and edges that are not part of any cycle
        if remove_acyclic_edges:
            sccs = self.strongly_connected_components()
            d = {}
            for id, component in enumerate(sccs):
                for v in component:
                    d[v] = id
            h = copy(self)
            h.delete_edges((u, v) for u, v in h.edge_iterator(labels=False) if d[u] != d[v])
        else:
            h = self
        queue = [[vertex]]
        if max_length is None:
            from sage.rings.infinity import Infinity
            max_length = Infinity
        while queue:
            path = queue.pop(0)
            # Checks if a cycle has been found
            if len(path) > 1 and path[0] == path[-1]:
                yield path
            # Makes sure that the current cycle is not too long
            # Also if a cycle has been encountered and only simple cycles are allowed,
            # Then it discards the current path
            if len(path) <= max_length and (not simple or path.count(path[-1]) == 1):
                for neighbor in h.neighbor_out_iterator(path[-1]):
                    # If cycles are not rooted, makes sure to keep only the minimum
                    # cycle according to the lexicographic order
                    if rooted or neighbor not in starting_vertices or path[0] <= neighbor:
                        queue.append(path + [neighbor])

    def all_cycles_iterator(self, starting_vertices=None, simple=False,
                            rooted=False, max_length=None, trivial=False):
        r"""
        Return an iterator over all the cycles of ``self`` starting with one of
        the given vertices.

        The cycles are enumerated in increasing length order.

        INPUT:

        - ``starting_vertices`` -- iterable (default: ``None``); vertices from
          which the cycles must start. If ``None``, then all vertices of the
          graph can be starting points. This argument is necessary if ``rooted``
          is set to ``True``.

        - ``simple`` -- boolean (default: ``False``); if set to ``True``, then
          only simple cycles are considered. A cycle is simple if the only
          vertex occuring twice in it is the starting and ending one.

        - ``rooted`` -- boolean (default: ``False``); if set to False, then
          cycles differing only by their starting vertex are considered the same
          (e.g. ``['a', 'b', 'c', 'a']`` and ``['b', 'c', 'a',
          'b']``). Otherwise, all cycles are enumerated.

        - ``max_length`` -- non negative integer (default: ``None``); the
          maximum length of the enumerated paths. If set to ``None``, then all
          lengths are allowed.

        - ``trivial`` - boolean (default: ``False``); if set to ``True``, then
          the empty paths are also enumerated.

        OUTPUT:

            iterator

        .. SEEALSO::

            - :meth:`all_simple_cycles`

        AUTHOR:

            Alexandre Blondin Masse

        EXAMPLES::

            sage: g = DiGraph({'a': ['a', 'b'], 'b': ['c'], 'c': ['d'], 'd': ['c']}, loops=True)
            sage: it = g.all_cycles_iterator()
            sage: for _ in range(7): print(next(it))
            ['a', 'a']
            ['a', 'a', 'a']
            ['c', 'd', 'c']
            ['a', 'a', 'a', 'a']
            ['a', 'a', 'a', 'a', 'a']
            ['c', 'd', 'c', 'd', 'c']
            ['a', 'a', 'a', 'a', 'a', 'a']

        There are no cycles in the empty graph and in acyclic graphs::

            sage: g = DiGraph()
            sage: it = g.all_cycles_iterator()
            sage: list(it)
            []
            sage: g = DiGraph({0:[1]})
            sage: it = g.all_cycles_iterator()
            sage: list(it)
            []

        It is possible to restrict the starting vertices of the cycles::

            sage: g = DiGraph({'a': ['a', 'b'], 'b': ['c'], 'c': ['d'], 'd': ['c']}, loops=True)
            sage: it = g.all_cycles_iterator(starting_vertices=['b', 'c'])
            sage: for _ in range(3): print(next(it))
            ['c', 'd', 'c']
            ['c', 'd', 'c', 'd', 'c']
            ['c', 'd', 'c', 'd', 'c', 'd', 'c']

        Also, one can bound the length of the cycles::

            sage: it = g.all_cycles_iterator(max_length=3)
            sage: list(it)
            [['a', 'a'], ['a', 'a', 'a'], ['c', 'd', 'c'],
             ['a', 'a', 'a', 'a']]

        By default, cycles differing only by their starting point are not all
        enumerated, but this may be parametrized::

            sage: it = g.all_cycles_iterator(max_length=3, rooted=False)
            sage: list(it)
            [['a', 'a'], ['a', 'a', 'a'], ['c', 'd', 'c'],
             ['a', 'a', 'a', 'a']]
            sage: it = g.all_cycles_iterator(max_length=3, rooted=True)
            sage: list(it)
            [['a', 'a'], ['a', 'a', 'a'], ['c', 'd', 'c'], ['d', 'c', 'd'],
             ['a', 'a', 'a', 'a']]

        One may prefer to enumerate simple cycles, i.e. cycles such that the only
        vertex occuring twice in it is the starting and ending one (see also
        :meth:`all_simple_cycles`)::

            sage: it = g.all_cycles_iterator(simple=True)
            sage: list(it)
            [['a', 'a'], ['c', 'd', 'c']]
            sage: g = digraphs.Circuit(4)
            sage: list(g.all_cycles_iterator(simple=True))
            [[0, 1, 2, 3, 0]]
        """
        if starting_vertices is None:
            starting_vertices = self
        # Since a cycle is always included in a given strongly connected
        # component, we may remove edges from the graph
        sccs = self.strongly_connected_components()
        d = {}
        for id, component in enumerate(sccs):
            for v in component:
                d[v] = id
        h = copy(self)
        h.delete_edges((u, v) for u, v in h.edge_iterator(labels=False) if d[u] != d[v])
        # We create one cycles iterator per vertex. This is necessary if we
        # want to iterate over cycles with increasing length.
        vertex_iterators = {v :h._all_cycles_iterator_vertex(v
                                        , starting_vertices=starting_vertices
                                        , simple=simple
                                        , rooted=rooted
                                        , max_length=max_length
                                        , trivial=trivial
                                        , remove_acyclic_edges=False
                                        ) for v in starting_vertices}
        cycles = []
        for vi in vertex_iterators.values():
            try:
                cycle = next(vi)
                cycles.append((len(cycle), cycle))
            except(StopIteration):
                pass
        # Since we always extract a shortest path, using a heap
        # can speed up the algorithm
        from heapq import heapify, heappop, heappush
        heapify(cycles)
        while cycles:
            # We choose the shortest available cycle
            _, shortest_cycle = heappop(cycles)
            yield shortest_cycle
            # We update the cycle iterator to its next available cycle if it
            # exists
            try:
                cycle = next(vertex_iterators[shortest_cycle[0]])
                heappush(cycles, (len(cycle), cycle))
            except(StopIteration):
                pass

    def all_simple_cycles(self, starting_vertices=None, rooted=False,
                          max_length=None, trivial=False):
        r"""
        Return a list of all simple cycles of ``self``.

        INPUT:

        - ``starting_vertices`` -- iterable (default: ``None``); vertices from
          which the cycles must start. If ``None``, then all vertices of the
          graph can be starting points. This argument is necessary if ``rooted``
          is set to ``True``.

        - ``rooted`` -- boolean (default: ``False``); if set to False, then
          cycles differing only by their starting vertex are considered the same
          (e.g. ``['a', 'b', 'c', 'a']`` and ``['b', 'c', 'a',
          'b']``). Otherwise, all cycles are enumerated.

        - ``max_length`` -- non negative integer (default: ``None``); the
          maximum length of the enumerated paths. If set to ``None``, then all
          lengths are allowed.

        - ``trivial`` - boolean (default: ``False``); if set to ``True``, then
          the empty paths are also enumerated.

        OUTPUT:

            list

        .. NOTE::

            Although the number of simple cycles of a finite graph is always
            finite, computing all its cycles may take a very long time.

        EXAMPLES::

            sage: g = DiGraph({'a': ['a', 'b'], 'b': ['c'], 'c': ['d'], 'd': ['c']}, loops=True)
            sage: g.all_simple_cycles()
            [['a', 'a'], ['c', 'd', 'c']]

        The directed version of the Petersen graph::

            sage: g = graphs.PetersenGraph().to_directed()
            sage: g.all_simple_cycles(max_length=4)
            [[0, 1, 0], [0, 4, 0], [0, 5, 0], [1, 2, 1], [1, 6, 1], [2, 3, 2],
             [2, 7, 2], [3, 8, 3], [3, 4, 3], [4, 9, 4], [5, 8, 5], [5, 7, 5],
             [6, 8, 6], [6, 9, 6], [7, 9, 7]]
            sage: g.all_simple_cycles(max_length=6)
            [[0, 1, 0], [0, 4, 0], [0, 5, 0], [1, 2, 1], [1, 6, 1], [2, 3, 2],
             [2, 7, 2], [3, 8, 3], [3, 4, 3], [4, 9, 4], [5, 8, 5], [5, 7, 5],
             [6, 8, 6], [6, 9, 6], [7, 9, 7], [0, 1, 2, 3, 4, 0],
             [0, 1, 2, 7, 5, 0], [0, 1, 6, 8, 5, 0], [0, 1, 6, 9, 4, 0],
             [0, 4, 9, 6, 1, 0], [0, 4, 9, 7, 5, 0], [0, 4, 3, 8, 5, 0],
             [0, 4, 3, 2, 1, 0], [0, 5, 8, 3, 4, 0], [0, 5, 8, 6, 1, 0],
             [0, 5, 7, 9, 4, 0], [0, 5, 7, 2, 1, 0], [1, 2, 3, 8, 6, 1],
             [1, 2, 7, 9, 6, 1], [1, 6, 8, 3, 2, 1], [1, 6, 9, 7, 2, 1],
             [2, 3, 8, 5, 7, 2], [2, 3, 4, 9, 7, 2], [2, 7, 9, 4, 3, 2],
             [2, 7, 5, 8, 3, 2], [3, 8, 6, 9, 4, 3], [3, 4, 9, 6, 8, 3],
             [5, 8, 6, 9, 7, 5], [5, 7, 9, 6, 8, 5], [0, 1, 2, 3, 8, 5, 0],
             [0, 1, 2, 7, 9, 4, 0], [0, 1, 6, 8, 3, 4, 0],
             [0, 1, 6, 9, 7, 5, 0], [0, 4, 9, 6, 8, 5, 0],
             [0, 4, 9, 7, 2, 1, 0], [0, 4, 3, 8, 6, 1, 0],
             [0, 4, 3, 2, 7, 5, 0], [0, 5, 8, 3, 2, 1, 0],
             [0, 5, 8, 6, 9, 4, 0], [0, 5, 7, 9, 6, 1, 0],
             [0, 5, 7, 2, 3, 4, 0], [1, 2, 3, 4, 9, 6, 1],
             [1, 2, 7, 5, 8, 6, 1], [1, 6, 8, 5, 7, 2, 1],
             [1, 6, 9, 4, 3, 2, 1], [2, 3, 8, 6, 9, 7, 2],
             [2, 7, 9, 6, 8, 3, 2], [3, 8, 5, 7, 9, 4, 3],
             [3, 4, 9, 7, 5, 8, 3]]

        The complete graph (without loops) on `4` vertices::

            sage: g = graphs.CompleteGraph(4).to_directed()
            sage: g.all_simple_cycles()
            [[0, 1, 0], [0, 2, 0], [0, 3, 0], [1, 2, 1], [1, 3, 1], [2, 3, 2],
             [0, 1, 2, 0], [0, 1, 3, 0], [0, 2, 1, 0], [0, 2, 3, 0],
             [0, 3, 1, 0], [0, 3, 2, 0], [1, 2, 3, 1], [1, 3, 2, 1],
             [0, 1, 2, 3, 0], [0, 1, 3, 2, 0], [0, 2, 1, 3, 0],
             [0, 2, 3, 1, 0], [0, 3, 1, 2, 0], [0, 3, 2, 1, 0]]

        If the graph contains a large number of cycles, one can bound the length
        of the cycles, or simply restrict the possible starting vertices of the
        cycles::

            sage: g = graphs.CompleteGraph(20).to_directed()
            sage: g.all_simple_cycles(max_length=2)
            [[0, 1, 0], [0, 2, 0], [0, 3, 0], [0, 4, 0], [0, 5, 0], [0, 6, 0],
             [0, 7, 0], [0, 8, 0], [0, 9, 0], [0, 10, 0], [0, 11, 0],
             [0, 12, 0], [0, 13, 0], [0, 14, 0], [0, 15, 0], [0, 16, 0],
             [0, 17, 0], [0, 18, 0], [0, 19, 0], [1, 2, 1], [1, 3, 1],
             [1, 4, 1], [1, 5, 1], [1, 6, 1], [1, 7, 1], [1, 8, 1], [1, 9, 1],
             [1, 10, 1], [1, 11, 1], [1, 12, 1], [1, 13, 1], [1, 14, 1],
             [1, 15, 1], [1, 16, 1], [1, 17, 1], [1, 18, 1], [1, 19, 1],
             [2, 3, 2], [2, 4, 2], [2, 5, 2], [2, 6, 2], [2, 7, 2], [2, 8, 2],
             [2, 9, 2], [2, 10, 2], [2, 11, 2], [2, 12, 2], [2, 13, 2],
             [2, 14, 2], [2, 15, 2], [2, 16, 2], [2, 17, 2], [2, 18, 2],
             [2, 19, 2], [3, 4, 3], [3, 5, 3], [3, 6, 3], [3, 7, 3], [3, 8, 3],
             [3, 9, 3], [3, 10, 3], [3, 11, 3], [3, 12, 3], [3, 13, 3],
             [3, 14, 3], [3, 15, 3], [3, 16, 3], [3, 17, 3], [3, 18, 3],
             [3, 19, 3], [4, 5, 4], [4, 6, 4], [4, 7, 4], [4, 8, 4], [4, 9, 4],
             [4, 10, 4], [4, 11, 4], [4, 12, 4], [4, 13, 4], [4, 14, 4],
             [4, 15, 4], [4, 16, 4], [4, 17, 4], [4, 18, 4], [4, 19, 4],
             [5, 6, 5], [5, 7, 5], [5, 8, 5], [5, 9, 5], [5, 10, 5],
             [5, 11, 5], [5, 12, 5], [5, 13, 5], [5, 14, 5], [5, 15, 5],
             [5, 16, 5], [5, 17, 5], [5, 18, 5], [5, 19, 5], [6, 7, 6],
             [6, 8, 6], [6, 9, 6], [6, 10, 6], [6, 11, 6], [6, 12, 6],
             [6, 13, 6], [6, 14, 6], [6, 15, 6], [6, 16, 6], [6, 17, 6],
             [6, 18, 6], [6, 19, 6], [7, 8, 7], [7, 9, 7], [7, 10, 7],
             [7, 11, 7], [7, 12, 7], [7, 13, 7], [7, 14, 7], [7, 15, 7],
             [7, 16, 7], [7, 17, 7], [7, 18, 7], [7, 19, 7], [8, 9, 8],
             [8, 10, 8], [8, 11, 8], [8, 12, 8], [8, 13, 8], [8, 14, 8],
             [8, 15, 8], [8, 16, 8], [8, 17, 8], [8, 18, 8], [8, 19, 8],
             [9, 10, 9], [9, 11, 9], [9, 12, 9], [9, 13, 9], [9, 14, 9],
             [9, 15, 9], [9, 16, 9], [9, 17, 9], [9, 18, 9], [9, 19, 9],
             [10, 11, 10], [10, 12, 10], [10, 13, 10], [10, 14, 10],
             [10, 15, 10], [10, 16, 10], [10, 17, 10], [10, 18, 10],
             [10, 19, 10], [11, 12, 11], [11, 13, 11], [11, 14, 11],
             [11, 15, 11], [11, 16, 11], [11, 17, 11], [11, 18, 11],
             [11, 19, 11], [12, 13, 12], [12, 14, 12], [12, 15, 12],
             [12, 16, 12], [12, 17, 12], [12, 18, 12], [12, 19, 12],
             [13, 14, 13], [13, 15, 13], [13, 16, 13], [13, 17, 13],
             [13, 18, 13], [13, 19, 13], [14, 15, 14], [14, 16, 14],
             [14, 17, 14], [14, 18, 14], [14, 19, 14], [15, 16, 15],
             [15, 17, 15], [15, 18, 15], [15, 19, 15], [16, 17, 16],
             [16, 18, 16], [16, 19, 16], [17, 18, 17], [17, 19, 17],
             [18, 19, 18]]
            sage: g = graphs.CompleteGraph(20).to_directed()
            sage: g.all_simple_cycles(max_length=2, starting_vertices=[0])
            [[0, 1, 0], [0, 2, 0], [0, 3, 0], [0, 4, 0], [0, 5, 0], [0, 6, 0],
             [0, 7, 0], [0, 8, 0], [0, 9, 0], [0, 10, 0], [0, 11, 0],
             [0, 12, 0], [0, 13, 0], [0, 14, 0], [0, 15, 0], [0, 16, 0],
             [0, 17, 0], [0, 18, 0], [0, 19, 0]]

        One may prefer to distinguish equivalent cycles having distinct starting
        vertices (compare the following examples)::

            sage: g = graphs.CompleteGraph(4).to_directed()
            sage: g.all_simple_cycles(max_length=2, rooted=False)
            [[0, 1, 0], [0, 2, 0], [0, 3, 0], [1, 2, 1], [1, 3, 1], [2, 3, 2]]
            sage: g.all_simple_cycles(max_length=2, rooted=True)
            [[0, 1, 0], [0, 2, 0], [0, 3, 0], [1, 0, 1], [1, 2, 1], [1, 3, 1],
             [2, 0, 2], [2, 1, 2], [2, 3, 2], [3, 0, 3], [3, 1, 3], [3, 2, 3]]
        """
        return list(self.all_cycles_iterator(starting_vertices=starting_vertices,
                                                 simple=True, rooted=rooted,
                                                 max_length=max_length, trivial=trivial))

    def path_semigroup(self):
        """
        The partial semigroup formed by the paths of this quiver.

        EXAMPLES::

            sage: Q = DiGraph({1: {2: ['a', 'c']}, 2: {3: ['b']}})
            sage: F = Q.path_semigroup(); F
            Partial semigroup formed by the directed paths of Multi-digraph on 3 vertices
            sage: list(F)
            [e_1, e_2, e_3, a, c, b, a*b, c*b]

        """
        from sage.quivers.path_semigroup import PathSemigroup
        return PathSemigroup(self)

    ### Directed Acyclic Graphs (DAGs)

    def topological_sort(self, implementation="default"):
        """
        Return a topological sort of the digraph if it is acyclic.

        If the digraph contains a directed cycle, a ``TypeError`` is raised. As
        topological sorts are not necessarily unique, different implementations
        may yield different results.

        A topological sort is an ordering of the vertices of the digraph such
        that each vertex comes before all of its successors. That is, if `u`
        comes before `v` in the sort, then there may be a directed path from `u`
        to `v`, but there will be no directed path from `v` to `u`.

        INPUT:

        - ``implementation`` -- string (default: ``"default"``); either use the
          default Cython implementation, or the default NetworkX library
          (``implementation = "NetworkX"``)

        .. SEEALSO::

            - :meth:`is_directed_acyclic` -- Tests whether a directed graph is
              acyclic (can also join a certificate -- a topological sort or a
              circuit in the graph).

        EXAMPLES::

            sage: D = DiGraph({0: [1, 2, 3], 4: [2, 5], 1: [8], 2: [7], 3: [7],
            ....:   5: [6, 7], 7: [8], 6: [9], 8: [10], 9: [10]})
            sage: D.plot(layout='circular').show()
            sage: D.topological_sort()
            [4, 5, 6, 9, 0, 1, 2, 3, 7, 8, 10]

        ::

            sage: D.add_edge(9, 7)
            sage: D.topological_sort()
            [4, 5, 6, 9, 0, 1, 2, 3, 7, 8, 10]

        Using the NetworkX implementation ::

            sage: list(D.topological_sort(implementation="NetworkX"))
            [4, 5, 6, 9, 0, 3, 2, 7, 1, 8, 10]

        ::

            sage: D.add_edge(7, 4)
            sage: D.topological_sort()
            Traceback (most recent call last):
            ...
            TypeError: digraph is not acyclic; there is no topological sort

        TESTS:

        A wrong value for the ``implementation`` keyword::

            sage: D.topological_sort(implementation = "cloud-reading")
            Traceback (most recent call last):
            ...
            ValueError: implementation must be set to one of "default" or "NetworkX"
        """
        if implementation == "default":
            b, ordering = self._backend.is_directed_acyclic(certificate = True)
            if b:
                return ordering
            else:
                raise TypeError('digraph is not acyclic; there is no topological sort')

        elif implementation == "NetworkX":
            import networkx
            S = networkx.topological_sort(self.networkx_graph(copy=False))
            if S is None:
                raise TypeError('digraph is not acyclic; there is no topological sort')
            else:
                return S

        else:
            raise ValueError("implementation must be set to one of \"default\" or \"NetworkX\"")

    def topological_sort_generator(self):
        """
        Return a list of all topological sorts of the digraph.

        If the digraph contains a directed cycle, a ``TypeError`` is raised.

        A topological sort is an ordering of the vertices of the digraph such
        that each vertex comes before all of its successors. That is, if u comes
        before v in the sort, then there may be a directed path from u to v, but
        there will be no directed path from v to u. See also
        :meth:`topological_sort`.

        AUTHORS:

        - Mike Hansen - original implementation

        - Robert L. Miller: wrapping, documentation

        REFERENCE:

        - [1] Pruesse, Gara and Ruskey, Frank. Generating Linear
          Extensions Fast. SIAM J. Comput., Vol. 23 (1994), no. 2, pp.
          373-386.

        EXAMPLES::

            sage: D = DiGraph({0: [1, 2], 1: [3], 2: [3, 4]})
            sage: D.plot(layout='circular').show()
            sage: D.topological_sort_generator()
            [[0, 1, 2, 3, 4], [0, 1, 2, 4, 3], [0, 2, 1, 3, 4], [0, 2, 1, 4, 3], [0, 2, 4, 1, 3]]

        ::

            sage: for sort in D.topological_sort_generator():
            ....:     for u, v in D.edge_iterator(labels=False):
            ....:         if sort.index(u) > sort.index(v):
            ....:             print("this should never happen")
        """
        from sage.graphs.linearextensions import LinearExtensions
        try:
            return LinearExtensions(self).list()
        except TypeError:
            raise TypeError('digraph is not acyclic; there is no topological sort (or there was an error in sage/graphs/linearextensions.py)')

    ### Visualization

    def layout_acyclic(self, rankdir="up", **options):
        """
        Return a ranked layout so that all edges point upward.

        To this end, the heights of the vertices are set according to the level
        set decomposition of the graph (see :meth:`.level_sets`).

        This is achieved by calling ``graphviz`` and ``dot2tex`` if available
        (see :meth:`.layout_graphviz`), and using a spring layout with fixed
        vertical placement of the vertices otherwise (see
        :meth:`.layout_acyclic_dummy` and
        :meth:`~sage.graphs.generic_graph.GenericGraph.layout_ranked`).

        Non acyclic graphs are partially supported by ``graphviz``, which then
        chooses some edges to point down.

        INPUT:

        - ``rankdir`` -- string (default: ``'up'``); indicates which direction
          the edges should point toward among ``'up'``, ``'down'``, ``'left'``,
          or ``'right'``

        - ``**options`` -- passed down to
          :meth:`~sage.graphs.generic_graph.GenericGraph.layout_ranked` or
          :meth:`~sage.graphs.generic_graph.GenericGraph.layout_graphviz`

        EXAMPLES::

            sage: H = DiGraph({0: [1, 2], 1: [3], 2: [3], 3: [], 5: [1, 6], 6: [2, 3]})

        The actual layout computed depends on whether dot2tex and graphviz are
        installed, so we don't test its relative values::

            sage: H.layout_acyclic()
            {0: [..., ...], 1: [..., ...], 2: [..., ...], 3: [..., ...], 5: [..., ...], 6: [..., ...]}

            sage: H = DiGraph({0: [1]})
            sage: pos = H.layout_acyclic(rankdir='up')
            sage: pos[1][1] > pos[0][1] + .5
            True
            sage: pos = H.layout_acyclic(rankdir='down')
            sage: pos[1][1] < pos[0][1] - .5
            True
            sage: pos = H.layout_acyclic(rankdir='right')
            sage: pos[1][0] > pos[0][0] + .5
            True
            sage: pos = H.layout_acyclic(rankdir='left')
            sage: pos[1][0] < pos[0][0] - .5
            True

        """
        if have_dot2tex():
            return self.layout_graphviz(rankdir=rankdir, **options)
        else:
            return self.layout_acyclic_dummy(rankdir=rankdir, **options)

    def layout_acyclic_dummy(self, heights=None, rankdir='up', **options):
        """
        Return a ranked layout so that all edges point upward.

        To this end, the heights of the vertices are set according to the level
        set decomposition of the graph (see :meth:`level_sets`). This is
        achieved by a spring layout with fixed vertical placement of the
        vertices otherwise (see :meth:`layout_acyclic_dummy` and
        :meth:`~sage.graphs.generic_graph.GenericGraph.layout_ranked`).

        INPUT:

        - ``rankdir`` -- string (default: ``'up'``); indicates which direction
          the edges should point toward among ``'up'``, ``'down'``, ``'left'``,
          or ``'right'``

        - ``**options`` -- passed down to
          :meth:`~sage.graphs.generic_graph.GenericGraph.layout_ranked`

        EXAMPLES::

            sage: H = DiGraph({0: [1, 2], 1: [3], 2: [3], 3: [], 5: [1, 6], 6: [2, 3]})
            sage: H.layout_acyclic_dummy()
            {0: [1.00..., 0], 1: [1.00..., 1], 2: [1.51..., 2], 3: [1.50..., 3], 5: [2.01..., 0], 6: [2.00..., 1]}

            sage: H = DiGraph({0: [1]})
            sage: H.layout_acyclic_dummy(rankdir='up')
            {0: [0.5..., 0], 1: [0.5..., 1]}
            sage: H.layout_acyclic_dummy(rankdir='down')
            {0: [0.5..., 1], 1: [0.5..., 0]}
            sage: H.layout_acyclic_dummy(rankdir='left')
            {0: [1, 0.5...], 1: [0, 0.5...]}
            sage: H.layout_acyclic_dummy(rankdir='right')
            {0: [0, 0.5...], 1: [1, 0.5...]}
            sage: H = DiGraph({0: [1, 2], 1: [3], 2: [3], 3: [1], 5: [1, 6], 6: [2, 3]})
            sage: H.layout_acyclic_dummy()
            Traceback (most recent call last):
            ...
            ValueError: `self` should be an acyclic graph

        """
        if heights is None:
            if not self.is_directed_acyclic():
                raise ValueError("`self` should be an acyclic graph")
            levels = self.level_sets()
            levels = [sorted(z) for z in levels]
            if rankdir=='down' or rankdir=='left':
                levels.reverse()
            heights = {i: levels[i] for i in range(len(levels))}
        positions = self.layout_ranked(heights=heights, **options)
        if rankdir == 'left' or rankdir == 'right':
            for coordinates in positions.values():
                coordinates.reverse()
        return positions

    def level_sets(self):
        r"""
        Return the level set decomposition of the digraph.

        OUTPUT:

        - a list of non empty lists of vertices of this graph

        The level set decomposition of the digraph is a list `l` such that the
        level `l[i]` contains all the vertices having all their predecessors in
        the levels `l[j]` for `j < i`, and at least one in level `l[i-1]`
        (unless `i = 0`).

        The level decomposition contains exactly the vertices not occuring in
        any cycle of the graph. In particular, the graph is acyclic if and only
        if the decomposition forms a set partition of its vertices, and we
        recover the usual level set decomposition of the corresponding poset.

        EXAMPLES::

            sage: H = DiGraph({0: [1, 2], 1: [3], 2: [3], 3: [], 5: [1, 6], 6: [2, 3]})
            sage: H.level_sets()
            [[0, 5], [1, 6], [2], [3]]

            sage: H = DiGraph({0: [1, 2], 1: [3], 2: [3], 3: [1], 5: [1, 6], 6: [2, 3]})
            sage: H.level_sets()
            [[0, 5], [6], [2]]

        This routine is mostly used for Hasse diagrams of posets::

            sage: from sage.combinat.posets.hasse_diagram import HasseDiagram
            sage: H = HasseDiagram({0: [1, 2], 1: [3], 2: [3], 3: []})
            sage: [len(x) for x in H.level_sets()]
            [1, 2, 1]

        ::

            sage: from sage.combinat.posets.hasse_diagram import HasseDiagram
            sage: H = HasseDiagram({0: [1, 2], 1: [3], 2: [4], 3: [4]})
            sage: [len(x) for x in H.level_sets()]
            [1, 2, 1, 1]

        Complexity: `O(n+m)` in time and `O(n)` in memory (besides the storage
        of the graph itself), where `n` and `m` are respectively the number of
        vertices and edges (assuming that appending to a list is constant time,
        which it is not quite).
        """
        in_degrees = self.in_degree(labels=True)
        level = [x for x in in_degrees if not in_degrees[x]]
        Levels = []
        while level:
            Levels.append(level)
            new_level = []
            for x in level:
                for y in self.neighbor_out_iterator(x):
                    in_degrees[y] -= 1
                    if not in_degrees[y]:
                        new_level.append(y)
            level = new_level
        return Levels


    def immediate_dominators(self, r, reverse=False):
        r"""
        Return the immediate dominators of all vertices reachable from `r`.

        A flowgraph `G = (V, A, r)` is a digraph where every vertex in `V` is
        reachable from a distinguished root vertex `r\in V`. In such digraph, a
        vertex `w` dominates a vertex `v` if every path from `r` to `v` includes
        `w`. Let `dom(v)` be the set of the vertices that dominate `v`.
        Obviously, `r` and `v`, the trivial dominators of `v`, are in
        `dom(v)`. For `v \neq r`, the immediate dominator of `v`, denoted by
        `d(v)`, is the unique vertex `w \neq v` that dominates `v` and is
        dominated by all the vertices in `dom(v)\setminus\{v\}`. The (immediate)
        dominator tree is a directed tree (or arborescence) rooted at `r` that
        is formed by the arcs `\{ (d(v), v)\mid v\in V\setminus\{r\}\}`.  See
        [Ge2005]_ for more details.

        This method implements the algorithm proposed in [CHK2001]_ which
        performs very well in practice, although its worst case time complexity
        is in `O(n^2)`.

        INPUT:

        - ``r`` -- a vertex of the digraph, the root of the immediate dominators
          tree

        - ``reverse`` -- boolean (default: ``False``); when set to ``True``, we
          consider the reversed digraph in which out-neighbors become the
          in-neighbors and vice-versa. This option is available only if the
          backend of the digraph is :mod:`~SparseGraphBackend`.

        OUTPUT: The (immediate) dominator tree rooted at `r`, encoded as a
        predecessor dictionary.

        EXAMPLES:

        The output encodes a tree rooted at `r`::

            sage: D = digraphs.Complete(4) * 2
            sage: D.add_edges([(0, 4), (7, 3)])
            sage: d = D.immediate_dominators(0)
            doctest:...: DeprecationWarning: immediate_dominators is now deprecated. Please use method dominator_tree instead.
            See https://trac.sagemath.org/25030 for details.
            sage: T = DiGraph([(d[u], u) for u in d if u != d[u]])
            sage: Graph(T).is_tree()
            True
            sage: all(T.in_degree(u) <= 1 for u in T)
            True

        In a strongly connected digraph, the result depends on the root::

            sage: D = digraphs.Circuit(5)
            sage: D.immediate_dominators(0)
            {0: 0, 1: 0, 2: 1, 3: 2, 4: 3}
            sage: D.immediate_dominators(1)
            {0: 4, 1: 1, 2: 1, 3: 2, 4: 3}

        The (immediate) dominator tree contains only reachable vertices::

            sage: P = digraphs.Path(5)
            sage: P.immediate_dominators(0)
            {0: 0, 1: 0, 2: 1, 3: 2, 4: 3}
            sage: P.immediate_dominators(3)
            {3: 3, 4: 3}

        Immediate dominators in the reverse digraph::

            sage: D = digraphs.Complete(5)+digraphs.Complete(4)
            sage: D.add_edges([(0, 5), (1, 6), (7, 2)])
            sage: idom = D.immediate_dominators(0, reverse=True)
            sage: idom
            {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 7, 6: 7, 7: 2, 8: 7}
            sage: D_reverse = D.reverse()
            sage: D_reverse.immediate_dominators(0) == idom
            True

        .. SEEALSO::

            - :wikipedia:`Dominator_(graph_theory)`
            - :meth:`~DiGraph.strong_articulation_points`
            - :meth:`~DiGraph.strongly_connected_components`

        TESTS:

        When `r` is not in the digraph::

            sage: DiGraph().immediate_dominators(0)
            Traceback (most recent call last):
            ...
            ValueError: the given root must be in the digraph

        The reverse option is available only when the backend of the digraph is
        :mod:`~SparseGraphBackend`::

            sage: H = DiGraph(D.edges(), data_structure='static_sparse')
            sage: H.immediate_dominators(0, reverse=True)
            Traceback (most recent call last):
            ...
            ValueError: the reverse option is not available for this digraph

        Comparison with the NetworkX method::

            sage: import networkx
            sage: D = digraphs.RandomDirectedGNP(20, 0.1)
            sage: d = D.immediate_dominators(0)
            sage: dx = networkx.immediate_dominators(D.networkx_graph(), 0)
            sage: all(d[i] == dx[i] for i in d) and all(d[i] == dx[i] for i in dx)
            True
        """
        deprecation(25030, "immediate_dominators is now deprecated."
                           " Please use method dominator_tree instead.")
        if r not in self:
            raise ValueError("the given root must be in the digraph")

        idom = {r: r}
        n = self.order()
        if reverse:
            from sage.graphs.base.sparse_graph import SparseGraphBackend
            if isinstance(self._backend, SparseGraphBackend):
                pre_order = list(self._backend.depth_first_search(r, reverse=True))
                number = {u: n-i for i, u in enumerate(pre_order)}
                neighbor_iterator = self.neighbor_out_iterator
            else:
                raise ValueError("the reverse option is not available for this digraph")
        else:
            pre_order = list(self.depth_first_search(r))
            number = {u: n-i for i, u in enumerate(pre_order)}
            neighbor_iterator = self.neighbor_in_iterator
        pre_order.pop(0)

        def intersect(u, v):
            while u != v:
                while number[u] < number[v]:
                    u = idom[u]
                while number[u] > number[v]:
                    v = idom[v]
            return u

        changed = True
        while changed:
            changed = False
            for u in pre_order:
                pred = [v for v in neighbor_iterator(u) if v in idom]
                if not pred:
                    continue
                else:
                    new_idom = pred[0]
                    for v in pred[1:]:
                        new_idom = intersect(new_idom, v)
                if not u in idom or idom[u] != new_idom:
                    idom[u] = new_idom
                    changed = True

        return idom


    def is_aperiodic(self):
        r"""
        Return whether the current ``DiGraph`` is aperiodic.

        A directed graph is aperiodic if there is no integer `k > 1` that
        divides the length of every cycle in the graph. See the
        :wikipedia:`Aperiodic_graph` for more information.

        EXAMPLES:

        The following graph has period ``2``, so it is not aperiodic::

            sage: g = DiGraph({0: [1], 1: [0]})
            sage: g.is_aperiodic()
            False

        The following graph has a cycle of length 2 and a cycle of length 3,
        so it is aperiodic::

            sage: g = DiGraph({0: [1, 4], 1: [2], 2: [0], 4: [0]})
            sage: g.is_aperiodic()
            True

        .. SEEALSO::

            :meth:`period`
        """
        import networkx
        return networkx.is_aperiodic(self.networkx_graph(copy=False))

    def period(self):
        r"""
        Return the period of the current ``DiGraph``.

        The period of a directed graph is the largest integer that divides the
        length of every cycle in the graph. See the :wikipedia:`Aperiodic_graph`
        for more information.

        EXAMPLES:

        The following graph has period ``2``::

            sage: g = DiGraph({0: [1], 1: [0]})
            sage: g.period()
            2

        The following graph has a cycle of length 2 and a cycle of length 3,
        so it has period ``1``::

            sage: g = DiGraph({0: [1, 4], 1: [2], 2: [0], 4: [0]})
            sage: g.period()
            1

        Here is an example of computing the period of a digraph which is not
        strongly connected. By definition, it is the :func:`gcd` of the periods
        of its strongly connected components::

            sage: g = DiGraph({-1: [-2], -2: [-3], -3: [-1],
            ....:     1: [2], 2: [1]})
            sage: g.period()
            1
            sage: sorted([s.period() for s
            ....:         in g.strongly_connected_components_subgraphs()])
            [2, 3]

        ALGORITHM:

        See the networkX implementation of ``is_aperiodic``, that is based on
        breadth first search.

        .. SEEALSO::

            :meth:`is_aperiodic`
        """
        from sage.arith.all import gcd

        g = 0

        for component in self.strongly_connected_components():
            levels = {s: None for s in component}
            vertices_in_scc = levels # considers level as a set
            s = component[0]
            levels[s] = 0
            this_level = [s]
            l = 1
            while this_level:
                next_level = []
                for u in this_level:
                    # we have levels[u] == l - 1
                    for v in self.neighbor_out_iterator(u):
                        # ignore edges leaving the component
                        if v not in vertices_in_scc:
                            continue
                        level_v = levels[v]
                        if level_v is not None: # Non-Tree Edge
                            g = gcd(g, l - level_v)
                            if g == 1:
                                return 1
                        else: # Tree Edge
                            next_level.append(v)
                            levels[v] = l
                this_level = next_level
                l += 1

        return g

    def flow_polytope(self, edges=None, ends=None):
        r"""
        Return the flow polytope of a digraph.

        The flow polytope of a directed graph is the polytope consisting of all
        nonnegative flows on the graph with a given set `S` of sources and a
        given set `T` of sinks.

        A *flow* on a directed graph `G` with a given set `S` of sources and a
        given set `T` of sinks means an assignment of a nonnegative real to each
        edge of `G` such that the flow is conserved in each vertex outside of
        `S` and `T`, and there is a unit of flow entering each vertex in `S` and
        a unit of flow leaving each vertex in `T`. These flows clearly form a
        polytope in the space of all assignments of reals to the edges of `G`.

        The polytope is empty unless the sets `S` and `T` are equinumerous.

        By default, `S` is taken to be the set of all sources (i.e., vertices of
        indegree `0`) of `G`, and `T` is taken to be the set of all sinks (i.e.,
        vertices of outdegree `0`) of `G`. If a different choice of `S` and `T`
        is desired, it can be specified using the optional ``ends`` parameter.

        The polytope is returned as a polytope in `\RR^m`, where `m` is the
        number of edges of the digraph ``self``. The `k`-th coordinate of a
        point in the polytope is the real assigned to the `k`-th edge of
        ``self``. The order of the edges is the one returned by
        ``self.edges()``. If a different order is desired, it can be specified
        using the optional ``edges`` parameter.

        The faces and volume of these polytopes are of interest. Examples of
        these polytopes are the Chan-Robbins-Yuen polytope and the
        Pitman-Stanley polytope [PitSta]_.

        INPUT:

        - ``edges`` -- (optional, default: ``self.edges()``) a list or tuple of
          all edges of ``self`` (each only once). This determines which
          coordinate of a point in the polytope will correspond to which edge of
          ``self``. It is also possible to specify a list which contains not all
          edges of ``self``; this results in a polytope corresponding to the
          flows which are `0` on all remaining edges. Notice that the edges
          entered here must be in the precisely same format as outputted by
          ``self.edges()``; so, if ``self.edges()`` outputs an edge in the form
          ``(1, 3, None)``, then ``(1, 3)`` will not do!

        - ``ends`` -- (optional, default: ``(self.sources(), self.sinks())``) a
          pair `(S, T)` of an iterable `S` and an iterable `T`.

        .. NOTE::

            Flow polytopes can also be built through the ``polytopes.<tab>``
            object::

                sage: polytopes.flow_polytope(digraphs.Path(5))
                A 0-dimensional polyhedron in QQ^4 defined as the convex hull of 1 vertex

        EXAMPLES:

        A commutative square::

            sage: G = DiGraph({1: [2, 3], 2: [4], 3: [4]})
            sage: fl = G.flow_polytope(); fl
            A 1-dimensional polyhedron in QQ^4 defined as the convex hull
            of 2 vertices
            sage: fl.vertices()
            (A vertex at (0, 1, 0, 1), A vertex at (1, 0, 1, 0))

        Using a different order for the edges of the graph::

            sage: fl = G.flow_polytope(edges=G.edges(key=lambda x: x[0] - x[1])); fl
            A 1-dimensional polyhedron in QQ^4 defined as the convex hull of 2 vertices
            sage: fl.vertices()
            (A vertex at (0, 1, 1, 0), A vertex at (1, 0, 0, 1))

        A tournament on 4 vertices::

            sage: H = digraphs.TransitiveTournament(4)
            sage: fl = H.flow_polytope(); fl
            A 3-dimensional polyhedron in QQ^6 defined as the convex hull
            of 4 vertices
            sage: fl.vertices()
            (A vertex at (0, 0, 1, 0, 0, 0),
             A vertex at (0, 1, 0, 0, 0, 1),
             A vertex at (1, 0, 0, 0, 1, 0),
             A vertex at (1, 0, 0, 1, 0, 1))

        Restricting to a subset of the edges::

            sage: fl = H.flow_polytope(edges=[(0, 1, None), (1, 2, None),
            ....:                             (2, 3, None), (0, 3, None)])
            sage: fl
            A 1-dimensional polyhedron in QQ^4 defined as the convex hull
            of 2 vertices
            sage: fl.vertices()
            (A vertex at (0, 0, 0, 1), A vertex at (1, 1, 1, 0))

        Using a different choice of sources and sinks::

            sage: fl = H.flow_polytope(ends=([1], [3])); fl
            A 1-dimensional polyhedron in QQ^6 defined as the convex hull
            of 2 vertices
            sage: fl.vertices()
            (A vertex at (0, 0, 0, 1, 0, 1), A vertex at (0, 0, 0, 0, 1, 0))
            sage: fl = H.flow_polytope(ends=([0, 1], [3])); fl
            The empty polyhedron in QQ^6
            sage: fl = H.flow_polytope(ends=([3], [0])); fl
            The empty polyhedron in QQ^6
            sage: fl = H.flow_polytope(ends=([0, 1], [2, 3])); fl
            A 3-dimensional polyhedron in QQ^6 defined as the convex hull
            of 5 vertices
            sage: fl.vertices()
            (A vertex at (0, 0, 1, 1, 0, 0),
             A vertex at (0, 1, 0, 0, 1, 0),
             A vertex at (1, 0, 0, 2, 0, 1),
             A vertex at (1, 0, 0, 1, 1, 0),
             A vertex at (0, 1, 0, 1, 0, 1))
            sage: fl = H.flow_polytope(edges=[(0, 1, None), (1, 2, None),
            ....:                             (2, 3, None), (0, 2, None),
            ....:                             (1, 3, None)],
            ....:                      ends=([0, 1], [2, 3])); fl
            A 2-dimensional polyhedron in QQ^5 defined as the convex hull
            of 4 vertices
            sage: fl.vertices()
            (A vertex at (0, 0, 0, 1, 1),
             A vertex at (1, 2, 1, 0, 0),
             A vertex at (1, 1, 0, 0, 1),
             A vertex at (0, 1, 1, 1, 0))

        A digraph with one source and two sinks::

            sage: Y = DiGraph({1: [2], 2: [3, 4]})
            sage: Y.flow_polytope()
            The empty polyhedron in QQ^3

        A digraph with one vertex and no edge::

            sage: Z = DiGraph({1: []})
            sage: Z.flow_polytope()
            A 0-dimensional polyhedron in QQ^0 defined as the convex hull
            of 1 vertex

        REFERENCES:

        .. [PitSta] Jim Pitman, Richard Stanley, "A polytope related to
           empirical distributions, plane trees, parking functions, and
           the associahedron", :arxiv:`math/9908029`
        """
        from sage.geometry.polyhedron.constructor import Polyhedron
        if edges is None:
            edges = self.edges()
        ineqs = [[0] + [Integer(j == u) for j in edges]
                 for u in edges]

        eqs = []
        for u in self:
            ins = self.incoming_edges(u)
            outs = self.outgoing_edges(u)
            eq = [Integer(j in ins) - Integer(j in outs) for j in edges]

            const = 0
            if ends is None:
                if not ins:  # sources (indegree 0)
                    const += 1
                if not outs:  # sinks (outdegree 0)
                    const -= 1
            else:
                if u in ends[0]:  # chosen sources
                    const += 1
                if u in ends[1]:  # chosen sinks
                    const -= 1

            eq = [const] + eq
            eqs.append(eq)

        return Polyhedron(ieqs=ineqs, eqns=eqs)

    def is_tournament(self):
        r"""
        Check whether the digraph is a tournament.

        A tournament is a digraph in which each pair of distinct vertices is
        connected by a single arc.

        EXAMPLES::

            sage: g = digraphs.RandomTournament(6)
            sage: g.is_tournament()
            True
            sage: u,v = next(g.edge_iterator(labels=False))
            sage: g.add_edge(v, u)
            sage: g.is_tournament()
            False
            sage: g.add_edges([(u, v), (v, u)])
            sage: g.is_tournament()
            False

        .. SEEALSO::

            - :wikipedia:`Tournament_(graph_theory)`
            - :meth:`~sage.graphs.digraph_generators.DiGraphGenerators.RandomTournament`
            - :meth:`~sage.graphs.digraph_generators.DiGraphGenerators.TransitiveTournament`
        """
        self._scream_if_not_simple()

        if self.size() != self.order() * (self.order() - 1) // 2:
            return False

        import itertools
        return not any(self.has_edge(u, v) == self.has_edge(v, u)
                           for u,v in itertools.combinations(self, 2))

    # Aliases to functions defined in other modules
    from sage.graphs.comparability import is_transitive
    from sage.graphs.base.static_sparse_graph import tarjan_strongly_connected_components as strongly_connected_components
    from sage.graphs.connectivity import is_strongly_connected
    from sage.graphs.connectivity import strongly_connected_components_digraph
    from sage.graphs.connectivity import strongly_connected_components_subgraphs
    from sage.graphs.connectivity import strongly_connected_component_containing_vertex
    from sage.graphs.connectivity import strong_articulation_points
