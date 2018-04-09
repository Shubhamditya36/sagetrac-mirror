# distutils: language = c++
"""
SCIP Backend

AUTHORS:

- Nathann Cohen (2010-10): generic backend
- Matthias Koeppe (2017): stubs
- Moritz Firsching (2018-04): rest
"""

#*****************************************************************************
#       Copyright (C) 2010 Nathann Cohen <nathann.cohen@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#                  http://www.gnu.org/licenses/
#*****************************************************************************
from __future__ import print_function

from os import sys
from os.path import splitext
from sage.ext.memory_allocator cimport MemoryAllocator
from sage.numerical.mip import MIPSolverException
from libc.float cimport DBL_MAX
from libc.limits cimport INT_MAX
from pyscipopt import Model

cdef class SCIPBackend(GenericBackend):

    """
    MIP Backend that uses the SCIP solver.

    TESTS:

    General backend testsuite::

        sage: p = MixedIntegerLinearProgram(solver="SCIP")
        sage: TestSuite(p.get_backend()).run(skip="_test_pickling")
    """

    def __cinit__(self, maximization = True):
        """
        Constructor

        EXAMPLE::

            sage: p = MixedIntegerLinearProgram(solver="SCIP")
        """
        self.model = Model('')
        if maximization:
            self.set_sense(1)
        else:
            self.set_sense(-1)


    cpdef int add_variable(self, lower_bound=0.0, upper_bound=None, binary=False, continuous=False, integer=False, obj=0.0, name=None) except -1:
        """
        Add a variable.

        This amounts to adding a new column to the matrix. By default,
        the variable is both positive, real and the coefficient in the
        objective function is 0.0.

        INPUT:

        - ``lower_bound`` - the lower bound of the variable (default: 0)

        - ``upper_bound`` - the upper bound of the variable (default: ``None``)

        - ``binary`` - ``True`` if the variable is binary (default: ``False``).

        - ``continuous`` - ``True`` if the variable is binary (default: ``True``).

        - ``integer`` - ``True`` if the variable is binary (default: ``False``).

        - ``obj`` - (optional) coefficient of this variable in the objective function (default: 0.0)

        - ``name`` - an optional name for the newly added variable (default: ``None``).

        OUTPUT: The index of the newly created variable

        EXAMPLE::

            sage: from sage.numerical.backends.generic_backend import get_solver
            sage: p = get_solver(solver = "SCIP")
            sage: p.ncols()
            0
            sage: p.add_variable()
            0
            sage: p.ncols()
            1
            sage: p.add_variable(binary=True)
            1
            sage: p.add_variable(lower_bound=-2.0, integer=True)
            2
            sage: p.add_variable(continuous=True, integer=True)
            Traceback (most recent call last):
            ...
            ValueError: ...
            sage: p.add_variable(name='x', obj=1.0)
            3
            sage: p.col_name(3)
            u'x'
            sage: p.objective_coefficient(3)
            1.0
        """
        if self.model.getStatus() != 'unknown':
            self.model.freeTransform()
        cdef int vtype = int(bool(binary)) + int(bool(continuous)) + int(bool(integer))
        if  vtype == 0:
            continuous = True
        elif vtype != 1:
            raise ValueError("Exactly one parameter of 'binary', 'integer' and 'continuous' must be 'True'.")

        if name==None:
            vname=''
        else:
            assert(type(name)==str)
            vname=name
        if continuous:
            vtypestr = 'C'
        if binary:
            vtypestr = 'B'
        if integer:
            vtypestr = 'I'
        # the following two lines can be removed, once this bug is fixed: https://github.com/SCIP-Interfaces/PySCIPOpt/issues/145
        if lower_bound==None:
            lower_bound = -self.model.infinity()

        self.model.addVar(name=vname, vtype=vtypestr, ub=upper_bound, lb=lower_bound, obj=obj, pricedVar = False)
        return self.ncols() - 1


    cpdef set_variable_type(self, int variable, int vtype):
        """
        Set the type of a variable

        INPUT:

        - ``variable`` (integer) -- the variable's id

        - ``vtype`` (integer) :

            *  1  Integer
            *  0  Binary
            * -1  Real

        EXAMPLE::

            sage: from sage.numerical.backends.generic_backend import get_solver
            sage: p = get_solver(solver = "SCIP")
            sage: p.ncols()
            0
            sage: p.add_variable()
            0
            sage: p.set_variable_type(0,1)
            sage: p.is_variable_integer(0)
            True
        """
        if self.model.getStatus() != 'unknown':
            self.model.freeTransform()
        vtypenames = {1:'I', 0:'B', -1:'C'}
        self.model.chgVarType(var = self.model.getVars()[variable], vtype = vtypenames[vtype])

    cpdef set_sense(self, int sense):
        """
        Set the direction (maximization/minimization).

        INPUT:

        - ``sense`` (integer) :

            * +1 => Maximization
            * -1 => Minimization

        EXAMPLE::

            sage: from sage.numerical.backends.generic_backend import get_solver
            sage: p = get_solver(solver = "SCIP")
            sage: p.is_maximization()
            True
            sage: p.set_sense(-1)
            sage: p.is_maximization()
            False
        """
        if self.model.getStatus() != 'unknown':
            self.model.freeTransform()
        if sense == 1:
            self.model.setMaximize()
        elif sense == -1:
            self.model.setMinimize()
        else:
            raise AssertionError("sense must be either 1 or -1")

    cpdef objective_coefficient(self, int variable, coeff=None):
        """
        Set or get the coefficient of a variable in the objective function

        INPUT:

        - ``variable`` (integer) -- the variable's id

        - ``coeff`` (double) -- its coefficient or ``None`` for
          reading (default: ``None``)

        EXAMPLE::

            sage: from sage.numerical.backends.generic_backend import get_solver
            sage: p = get_solver(solver = "SCIP")
            sage: p.add_variable()
            0
            sage: p.objective_coefficient(0)
            0.0
            sage: p.objective_coefficient(0,2)
            sage: p.objective_coefficient(0)
            2.0
        """
        if self.model.getStatus() != 'unknown':
            self.model.freeTransform()
        if coeff==None:
            return self.model.getVars()[variable].getObj()
        else:
            objexpr = self.model.getObjective()
            var = self.model.getVars()[variable]
            linfun = sum([e*c for e,c in objexpr.terms.iteritems() if e!=var]) + var*coeff
            self.model.setObjective(linfun, sense = self.model.getObjectiveSense())

    cpdef problem_name(self, char * name = NULL):
        """
        Return or define the problem's name

        INPUT:

        - ``name`` (``char *``) -- the problem's name. When set to
          ``NULL`` (default), the method returns the problem's name.

        EXAMPLE::

            sage: from sage.numerical.backends.generic_backend import get_solver
            sage: p = get_solver(solver = "SCIP")
            sage: p.problem_name("Nomen est omen")
            Traceback (most recent call last):
            ...
            NotImplementedError: Cannot return or define problem name for SCIP problem
        """
        #if name is NULL:
        #    return self.model.getProbName()
        #else:
        raise NotImplementedError("Cannot return or define problem name for SCIP problem")

    cpdef set_objective(self, list coeff, d = 0.0):
        """
        Set the objective function.

        INPUT:

        - ``coeff`` - a list of real values, whose ith element is the
          coefficient of the ith variable in the objective function.

        - ``d`` (double) -- the constant term in the linear function (set to `0` by default)

        EXAMPLE::

            sage: from sage.numerical.backends.generic_backend import get_solver
            sage: p = get_solver(solver = "SCIP")
            sage: p.add_variables(5)
            4
            sage: p.set_objective([1, 1, 2, 1, 3])
            sage: map(lambda x :p.objective_coefficient(x), range(5))
            [1.0, 1.0, 2.0, 1.0, 3.0]
        """
        if self.model.getStatus() != 'unknown':
            self.model.freeTransform()
        linfun = sum([c*x for c,x in zip(coeff, self.model.getVars())]) + d
        self.model.setObjective(linfun, sense = self.model.getObjectiveSense())

    cpdef set_verbosity(self, int level):
        """
        Set the verbosity level

        INPUT:

        - ``level`` (integer) -- From 0 (no verbosity) to 3.

        EXAMPLE::

            sage: from sage.numerical.backends.generic_backend import get_solver
            sage: p = get_solver(solver = "SCIP")
            sage: p.set_verbosity(2)

        """
        NotImplementedError()

    cpdef remove_constraint(self, int i):
        r"""
        Remove a constraint from self.

        INPUT:

        - ``i`` -- index of the constraint to remove

        EXAMPLE::

            sage: p = MixedIntegerLinearProgram(solver='SCIP')
            sage: x, y = p['x'], p['y']
            sage: p.add_constraint(2*x + 3*y <= 6)
            sage: p.add_constraint(3*x + 2*y <= 6)
            sage: p.add_constraint(x >= 0)
            sage: p.set_objective(x + y + 7)
            sage: p.set_integer(x); p.set_integer(y)
            sage: p.solve()
            9.0
            sage: p.remove_constraint(0)
            sage: p.solve()
            10.0

        Removing fancy constraints does not make Sage crash::

            sage: MixedIntegerLinearProgram(solver = "SCIP").remove_constraint(-2)
            Traceback (most recent call last):
            ...
            ValueError: The constraint's index i must satisfy 0 <= i < number_of_constraints
        """
        if i < 0 or i >= self.nrows():
            raise ValueError("The constraint's index i must satisfy 0 <= i < number_of_constraints")
        if self.model.getStatus() != 'unknown':
            self.model.freeTransform()
        self.model.delCons(self.model.getConss()[i])

    cpdef add_linear_constraint(self, coefficients, lower_bound, upper_bound, name=None):
        """
        Add a linear constraint.

        INPUT:

        - ``coefficients`` an iterable with ``(c,v)`` pairs where ``c``
          is a variable index (integer) and ``v`` is a value (real
          value).

        - ``lower_bound`` - a lower bound, either a real value or ``None``

        - ``upper_bound`` - an upper bound, either a real value or ``None``

        - ``name`` - an optional name for this row (default: ``None``)

        EXAMPLES::

            sage: from sage.numerical.backends.generic_backend import get_solver
            sage: p = get_solver(solver = "SCIP")
            sage: p.add_variables(5)
            4
            sage: p.add_linear_constraint( zip(range(5), range(5)), 2.0, 2.0)
            sage: p.row_bounds(0)
            (2.0, 2.0)
            sage: p.add_linear_constraint( zip(range(5), range(5)), 1.0, 1.0, name='foo')
            sage: p.row_name(1)
            u'foo'
        """
        if self.model.getStatus() != 'unknown':
            self.model.freeTransform()
        mvars = self.model.getVars()
        from pyscipopt.scip import quicksum
        linfun = quicksum([v*mvars[c] for c,v in coefficients])
        #we introduced patch 0001 for pyscipopt, in order to handle the case
        #when linfun is an empty expression.
        if name==None:
            name=''

        if lower_bound is None:
            lower_bound = -self.model.infinity()
        if upper_bound is None:
            upper_bound = self.model.infinity()

        cons = lower_bound <= (linfun <= upper_bound)
        self.model.addCons(cons, name=name)

    cpdef row(self, int index):
        r"""
        Return a row

        INPUT:

        - ``index`` (integer) -- the constraint's id.

        OUTPUT:

        A pair ``(indices, coeffs)`` where ``indices`` lists the
        entries whose coefficient is nonzero, and to which ``coeffs``
        associates their coefficient on the model of the
        ``add_linear_constraint`` method.

        EXAMPLE::


            sage: from sage.numerical.backends.generic_backend import get_solver
            sage: p = get_solver(solver = "SCIP")
            sage: p.add_variables(5)
            4
            sage: p.add_linear_constraint(zip(range(5), range(5)), 2, 2)
            sage: p.row(0)
            Traceback (most recent call last):
            ...
            NotImplementedError: SCIP backend doesn't provide the row
            sage: p.row_bounds(0)
            (2.0, 2.0)
        """
        #This could be fixed as soon as pyscipopt provides a way to get back
        #the expression (not lhs or rhs, but middle) of a constraint.
        raise NotImplementedError("SCIP backend doesn't provide the row")

    cpdef row_bounds(self, int index):
        """
        Return the bounds of a specific constraint.

        INPUT:

        - ``index`` (integer) -- the constraint's id.

        OUTPUT:

        A pair ``(lower_bound, upper_bound)``. Each of them can be set
        to ``None`` if the constraint is not bounded in the
        corresponding direction, and is a real value otherwise.

        EXAMPLE::

            sage: from sage.numerical.backends.generic_backend import get_solver
            sage: p = get_solver(solver = "SCIP")
            sage: p.add_variables(5)
            4
            sage: p.add_linear_constraint(zip(range(5), range(5)), 2, 2)
            sage: p.row_bounds(0)
            (2.0, 2.0)
        """
        cons = self.model.getConss()[index]
        lhs = self.model.getLhs(cons)
        rhs = self.model.getRhs(cons)
        if lhs == -self.model.infinity():
            lhs = None
        if rhs == self.model.infinity():
            rhs = None
        return (lhs, rhs)

    cpdef col_bounds(self, int index):
        """
        Return the bounds of a specific variable.

        INPUT:

        - ``index`` (integer) -- the variable's id.

        OUTPUT:

        A pair ``(lower_bound, upper_bound)``. Each of them can be set
        to ``None`` if the variable is not bounded in the
        corresponding direction, and is a real value otherwise.

        EXAMPLE::

            sage: from sage.numerical.backends.generic_backend import get_solver
            sage: p = get_solver(solver = "SCIP")
            sage: p.add_variable()
            0
            sage: p.col_bounds(0)
            (0.0, None)
            sage: p.variable_upper_bound(0, 5)
            sage: p.col_bounds(0)
            (0.0, 5.0)
        """
        var = self.model.getVars()[index]
        lb = var.getLbOriginal()
        if lb == -self.model.infinity():
            lb = None
        ub = var.getUbOriginal()
        if ub == self.model.infinity():
            ub = None
        return (lb, ub)


    cpdef add_col(self, list indices, list coeffs):
        """
        Add a column.

        INPUT:

        - ``indices`` (list of integers) -- this list constains the
          indices of the constraints in which the variable's
          coefficient is nonzero

        - ``coeffs`` (list of real values) -- associates a coefficient
          to the variable in each of the constraints in which it
          appears. Namely, the ith entry of ``coeffs`` corresponds to
          the coefficient of the variable in the constraint
          represented by the ith entry in ``indices``.

        .. NOTE::

            ``indices`` and ``coeffs`` are expected to be of the same
            length.

        EXAMPLE::

            sage: from sage.numerical.backends.generic_backend import get_solver
            sage: p = get_solver(solver = "SCIP")
            sage: p.ncols()
            0
            sage: p.nrows()
            0
            sage: p.add_linear_constraints(5, 0, None)
            sage: p.add_col(range(5), range(5))
            sage: p.nrows()
            5
        """
        mcons = self.model.getConss()
        #after update of
        index = self.add_variable(lower_bound=-self.model.infinity())
        var = self.model.getVars()[index]

        for i,coeff in zip(indices, coeffs):
            self.model.addConsCoeff(var=var, cons=mcons[i], coeff=coeff)

    cpdef int solve(self) except -1:
        """
        Solve the problem.

        Sage uses SCIP's implementation of the branch-and-cut algorithm
        to solve the mixed-integer linear program.
        (If all variables are continuous, the algorithm reduces to solving the
        linear program by the simplex method.)

        EXAMPLE::

            sage: lp = MixedIntegerLinearProgram(solver = 'SCIP', maximization = False)
            sage: x, y = lp[0], lp[1]
            sage: lp.add_constraint(-2*x + y <= 1)
            sage: lp.add_constraint(x - y <= 1)
            sage: lp.add_constraint(x + y >= 2)
            sage: lp.set_objective(x + y)
            sage: lp.set_integer(x)
            sage: lp.set_integer(y)
            sage: lp.solve()
            2.0
            sage: lp.get_values([x, y])
            [1.0, 1.0]

        .. NOTE::

            This method raises ``MIPSolverException`` exceptions when
            the solution can not be computed for any reason (none
            exists, or the LP solver was not able to find it, etc...)

        EXAMPLE::

            sage: from sage.numerical.backends.generic_backend import get_solver
            sage: p = get_solver(solver = "SCIP")
            sage: p.add_linear_constraints(5, 0, None)
            sage: p.add_col(range(5), range(5))
            sage: p.solve()
            0
            sage: p.objective_coefficient(0,1)
            sage: p.solve()
            Traceback (most recent call last):
            ...
            MIPSolverException: ...

        EXAMPLE::

            sage: lp = MixedIntegerLinearProgram(solver = "SCIP")
            sage: v = lp.new_variable(nonnegative=True)
            sage: lp.add_constraint(v[1] +v[2] -2.0 *v[3], max=-1.0)
            sage: lp.add_constraint(v[0] -4.0/3 *v[1] +1.0/3 *v[2], max=-1.0/3)
            sage: lp.add_constraint(v[0] +0.5 *v[1] -0.5 *v[2] +0.25 *v[3], max=-0.25)
            sage: lp.solve()
            0.0

        Solving a LP within the acceptable gap. No exception is raised, even if
        the result is not optimal. To do this, we try to compute the maximum
        number of disjoint balls (of diameter 1) in a hypercube::

            sage: g = graphs.CubeGraph(9)
            sage: p = MixedIntegerLinearProgram(solver = "SCIP")
            sage: p.solver_parameter("limits/absgap", 1000)
            sage: b = p.new_variable(binary=True)
            sage: p.set_objective(p.sum(b[v] for v in g))
            sage: for v in g:
            ....:     p.add_constraint(b[v]+p.sum(b[u] for u in g.neighbors(v)) <= 1)
            sage: p.add_constraint(b[v] == 1) # Force an easy non-0 solution
            sage: p.solve() # rel tol 100
            1

        Same, now with a time limit::

            sage: p.solver_parameter("limits/absgap", 1)
            sage: p.solver_parameter("timelimit",1)
            sage: p.solve() # rel tol 1
            1
        """
        self.model.hideOutput()
        self.model.optimize()

        status = self.model.getStatus()

        if status=='unbounded':
            raise MIPSolverException("SCIP : Solution is unbounded")
        elif status=='infeasible':
            raise MIPSolverException("SCIP : There is no feasible solution")
        #elif status=='timelimit':
        #    raise MIPSolverException("SCIP : Time limit reached")
        return 0

    cpdef get_objective_value(self):
        """
        Returns the value of the objective function.

        .. NOTE::

           Behaviour is undefined unless ``solve`` has been called before.

        EXAMPLE::

            sage: from sage.numerical.backends.generic_backend import get_solver
            sage: p = get_solver(solver = "SCIP")
            sage: p.add_variables(2)
            1
            sage: p.add_linear_constraint([[0, 1], [1, 2]], None, 3)
            sage: p.set_objective([2, 5])
            sage: p.solve()
            0
            sage: p.get_objective_value()
            7.5
            sage: p.get_variable_value(0) # abs tol 1e-15
            0.0
            sage: p.get_variable_value(1)
            1.5
        """
        return self.model.getObjVal()

    cpdef best_known_objective_bound(self):
        r"""
        Return the value of the currently best known bound.

        This method returns the current best upper (resp. lower) bound on the
        optimal value of the objective function in a maximization
        (resp. minimization) problem. It is equal to the output of
        :meth:`get_objective_value` if the MILP found an optimal solution, but
        it can differ if it was interrupted manually or after a time limit (cf
        :meth:`solver_parameter`).

        .. NOTE::

           Has no meaning unless ``solve`` has been called before.

        EXAMPLE::

        """
        return self.model.getPrimalbound()

    cpdef get_relative_objective_gap(self):
        r"""
        Return the relative objective gap of the best known solution.

        For a minimization problem, this value is computed by
        `(\texttt{bestinteger} - \texttt{bestobjective}) / (1e-10 +
        |\texttt{bestobjective}|)`, where ``bestinteger`` is the value returned
        by :meth:`get_objective_value` and ``bestobjective`` is the value
        returned by :meth:`best_known_objective_bound`. For a maximization
        problem, the value is computed by `(\texttt{bestobjective} -
        \texttt{bestinteger}) / (1e-10 + |\texttt{bestobjective}|)`.

        .. NOTE::

           Has no meaning unless ``solve`` has been called before.

        EXAMPLE::


        TESTS:

        Just make sure that the variable *has* been defined, and is not just
        undefined::

        """
        return self.model.getGap()

    cpdef get_variable_value(self, int variable):
        """
        Returns the value of a variable given by the solver.

        .. NOTE::

           Behaviour is undefined unless ``solve`` has been called before.

        EXAMPLE::

            sage: from sage.numerical.backends.generic_backend import get_solver
            sage: p = get_solver(solver = "SCIP")
            sage: p.add_variables(2)
            1
            sage: p.add_linear_constraint([[0, 1], [1, 2]], None, 3)
            sage: p.set_objective([2, 5])
            sage: p.solve()
            0
            sage: p.get_objective_value()
            7.5
            sage: p.get_variable_value(0) # abs tol 1e-15
            0.0
            sage: p.get_variable_value(1)
            1.5
        """
        return self.model.getVal(self.model.getVars()[variable])

    cpdef get_row_prim(self, int i):
        r"""
        Returns the value of the auxiliary variable associated with i-th row.

        .. NOTE::

           Behaviour is undefined unless ``solve`` has been called before.

        EXAMPLE::

            sage: from sage.numerical.backends.generic_backend import get_solver
            sage: lp = get_solver(solver = "SCIP")
            sage: lp.add_variables(3)
            2
            sage: lp.add_linear_constraint(zip([0, 1, 2], [8, 6, 1]), None, 48)
            sage: lp.add_linear_constraint(zip([0, 1, 2], [4, 2, 1.5]), None, 20)
            sage: lp.add_linear_constraint(zip([0, 1, 2], [2, 1.5, 0.5]), None, 8)
            sage: lp.set_objective([60, 30, 20])
            sage: lp.solve()
            0
            sage: lp.get_objective_value()
            280.0
            sage: lp.get_row_prim(0)
            24.0
            sage: lp.get_row_prim(1)
            20.0
            sage: lp.get_row_prim(2)
            8.0
        """
        return self.model.getActivity(self.model.getConss()[i])


    cpdef int ncols(self):
        """
        Return the number of columns/variables.

        EXAMPLE::

            sage: from sage.numerical.backends.generic_backend import get_solver
            sage: p = get_solver(solver = "SCIP")
            sage: p.ncols()
            0
            sage: p.add_variables(2)
            1
            sage: p.ncols()
            2
        """
        return len(self.model.getVars())

    cpdef int nrows(self):
        """
        Return the number of rows/constraints.

        EXAMPLE::

            sage: from sage.numerical.backends.generic_backend import get_solver
            sage: p = get_solver(solver = "SCIP")
            sage: p.nrows()
            0
            sage: p.add_linear_constraints(2, 2, None)
            sage: p.nrows()
            2
        """
        return len(self.model.getConss())

    cpdef col_name(self, int index):
        """
        Return the ``index``th col name

        INPUT:

        - ``index`` (integer) -- the col's id

        EXAMPLE::

            sage: from sage.numerical.backends.generic_backend import get_solver
            sage: p = get_solver(solver = "SCIP")
            sage: p.add_variable(name='I am a variable')
            0
            sage: p.col_name(0)
            u'I am a variable'
        """
        return self.model.getVars()[index].name

    cpdef row_name(self, int index):
        """
        Return the ``index`` th row name

        INPUT:

        - ``index`` (integer) -- the row's id

        EXAMPLE::

            sage: from sage.numerical.backends.generic_backend import get_solver
            sage: p = get_solver(solver = "SCIP")
            sage: p.add_linear_constraints(1, 2, None, names=['Empty constraint 1'])
            sage: p.row_name(0)
            u'Empty constraint 1'
        """
        return self.model.getConss()[index].name

    cpdef bint is_variable_binary(self, int index):
        """
        Test whether the given variable is of binary type.

        INPUT:

        - ``index`` (integer) -- the variable's id

        EXAMPLE::

            sage: from sage.numerical.backends.generic_backend import get_solver
            sage: p = get_solver(solver = "SCIP")
            sage: p.ncols()
            0
            sage: p.add_variable()
            0
            sage: p.set_variable_type(0,0)
            sage: p.is_variable_binary(0)
            True

        """
        return self.model.getVars()[index].vtype() == 'BINARY'

    cpdef bint is_variable_integer(self, int index):
        """
        Test whether the given variable is of integer type.

        INPUT:

        - ``index`` (integer) -- the variable's id

        EXAMPLE::

            sage: from sage.numerical.backends.generic_backend import get_solver
            sage: p = get_solver(solver = "SCIP")
            sage: p.ncols()
            0
            sage: p.add_variable()
            0
            sage: p.set_variable_type(0,1)
            sage: p.is_variable_integer(0)
            True
        """
        return self.model.getVars()[index].vtype() == 'INTEGER'


    cpdef bint is_variable_continuous(self, int index):
        """
        Test whether the given variable is of continuous/real type.

        INPUT:

        - ``index`` (integer) -- the variable's id

        EXAMPLE::

            sage: from sage.numerical.backends.generic_backend import get_solver
            sage: p = get_solver(solver = "SCIP")
            sage: p.ncols()
            0
            sage: p.add_variable()
            0
            sage: p.is_variable_continuous(0)
            True
            sage: p.set_variable_type(0,1)
            sage: p.is_variable_continuous(0)
            False

        """
        return self.model.getVars()[index].vtype() == 'CONTINUOUS'


    cpdef bint is_maximization(self):
        """
        Test whether the problem is a maximization

        EXAMPLE::

            sage: from sage.numerical.backends.generic_backend import get_solver
            sage: p = get_solver(solver = "SCIP")
            sage: p.is_maximization()
            True
            sage: p.set_sense(-1)
            sage: p.is_maximization()
            False
        """
        return self.model.getObjectiveSense() != 'minimize'

    cpdef variable_upper_bound(self, int index, value = False):
        """
        Return or define the upper bound on a variable

        INPUT:

        - ``index`` (integer) -- the variable's id

        - ``value`` -- real value, or ``None`` to mean that the
          variable has not upper bound. When set to ``False``
          (default), the method returns the current value.

        EXAMPLE::

            sage: from sage.numerical.backends.generic_backend import get_solver
            sage: p = get_solver(solver = "SCIP")
            sage: p.add_variable()
            0
            sage: p.col_bounds(0)
            (0.0, None)
            sage: p.variable_upper_bound(0, 5)
            sage: p.col_bounds(0)
            (0.0, 5.0)

        TESTS:

        :trac:`14581`::

            sage: P = MixedIntegerLinearProgram(solver="SCIP")
            sage: x = P["x"]
            sage: P.set_max(x, 0)
            sage: P.get_max(x)
            0.0

        Check that :trac:`10232` is fixed::

            sage: p = get_solver(solver="SCIP")
            sage: p.variable_upper_bound(2)
            Traceback (most recent call last):
            ...
            ValueError: The variable's id must satisfy 0 <= id < number_of_variables
            sage: p.variable_upper_bound(3, 5)
            Traceback (most recent call last):
            ...
            ValueError: The variable's id must satisfy 0 <= id < number_of_variables

            sage: p.add_variable()
            0
            sage: p.variable_upper_bound(0, 'hey!')
            Traceback (most recent call last):
            ...
            TypeError: a float is required
        """
        if index < 0 or index >= self.ncols():
            raise ValueError("The variable's id must satisfy 0 <= id < number_of_variables")
        var = self.model.getVars()[index]
        if value is False:
            return var.getUbOriginal()
        else:
            self.model.chgVarUb(var = var, ub = value)


    cpdef variable_lower_bound(self, int index, value = False):
        """
        Return or define the lower bound on a variable

        INPUT:

        - ``index`` (integer) -- the variable's id

        - ``value`` -- real value, or ``None`` to mean that the
          variable has not lower bound. When set to ``False``
          (default), the method returns the current value.

        EXAMPLE::

            sage: from sage.numerical.backends.generic_backend import get_solver
            sage: p = get_solver(solver = "SCIP")
            sage: p.add_variable()
            0
            sage: p.col_bounds(0)
            (0.0, None)
            sage: p.variable_lower_bound(0, 5)
            sage: p.col_bounds(0)
            (5.0, None)

        TESTS:

        :trac:`14581`::

            sage: P = MixedIntegerLinearProgram(solver="SCIP")
            sage: x = P["x"]
            sage: P.set_min(x, 5)
            sage: P.set_min(x, 0)
            sage: P.get_min(x)
            0.0

        Check that :trac:`10232` is fixed::

            sage: p = get_solver(solver="SCIP")
            sage: p.variable_lower_bound(2)
            Traceback (most recent call last):
            ...
            ValueError: The variable's id must satisfy 0 <= id < number_of_variables
            sage: p.variable_lower_bound(3, 5)
            Traceback (most recent call last):
            ...
            ValueError: The variable's id must satisfy 0 <= id < number_of_variables

            sage: p.add_variable()
            0
            sage: p.variable_lower_bound(0, 'hey!')
            Traceback (most recent call last):
            ...
            TypeError: a float is required
        """
        if index < 0 or index >= self.ncols():
            raise ValueError("The variable's id must satisfy 0 <= id < number_of_variables")
        var = self.model.getVars()[index]
        if value is False:
            return var.getLbOriginal()
        else:
            self.model.chgVarLb(var = var, lb = value)

    cpdef write_cip(self, char * filename):
        """
        Write the problem to a .cip file

        INPUT:

        - ``filename`` (string)

        EXAMPLE::

            sage: from sage.numerical.backends.generic_backend import get_solver
            sage: p = get_solver(solver = "SCIP")
            sage: p.add_variables(2)
            1
            sage: p.add_linear_constraint([[0, 1], [1, 2]], None, 3)
            sage: p.set_objective([2, 5])
            sage: p.write_cip(os.path.join(SAGE_TMP, "lp_problem.cip"))
            wrote original problem to file ...
        """
        self.model.writeProblem(filename)

    cpdef write_lp(self, char * filename):
        """
        Write the problem to a .lp file

        INPUT:

        - ``filename`` (string)

        EXAMPLE::

            sage: from sage.numerical.backends.generic_backend import get_solver
            sage: p = get_solver(solver = "SCIP")
            sage: p.add_variables(2)
            1
            sage: p.add_linear_constraint([[0, 1], [1, 2]], None, 3)
            sage: p.set_objective([2, 5])
            sage: p.write_lp(os.path.join(SAGE_TMP, "lp_problem.lp"))
            wrote original problem to file ...
        """
        filenamestr = filename
        fname, fext = splitext(filenamestr)

        if fext.lower() != 'lp':
            filenamestr = filename + '.lp'

        self.model.writeProblem(filenamestr)


    cpdef write_mps(self, char * filename, int modern):
        """
        Write the problem to a .mps file

        INPUT:

        - ``filename`` (string)

        EXAMPLE::

            sage: from sage.numerical.backends.generic_backend import get_solver
            sage: p = get_solver(solver = "SCIP")
            sage: p.add_variables(2)
            1
            sage: p.add_linear_constraint([[0, 1], [1, 2]], None, 3)
            sage: p.set_objective([2, 5])
            sage: p.write_mps(os.path.join(SAGE_TMP, "lp_problem.mps"), 2)
            wrote original problem to file ...
        """
        filenamestr = filename
        fname, fext = splitext(filenamestr)

        if fext.lower() != 'mps':
            filenamestr = filename + '.mps'

        self.model.writeProblem(filenamestr)


    cpdef __copy__(self):
        """
        Returns a copy of self.

        EXAMPLE::

            sage: from sage.numerical.backends.generic_backend import get_solver
            sage: p = MixedIntegerLinearProgram(solver = "SCIP")
            sage: b = p.new_variable()
            sage: p.add_constraint(b[1] + b[2] <= 6)
            sage: p.set_objective(b[1] + b[2])
            sage: copy(p)
            Traceback (most recent call last):
            ...
            NotImplementedError: copying not yet implemented

        """
        raise NotImplementedError("copying not yet implemented")

    cpdef solver_parameter(self, name, value = None):
        """
        Return or define a solver parameter

        INPUT:

        - ``name`` (string) -- the parameter

        - ``value`` -- the parameter's value if it is to be defined,
          or ``None`` (default) to obtain its current value.

        """
        if value is not None:
            if name.lower() == 'timelimit':
                self.model.setRealParam("limits/time", float(value))
                return


            try:
                self.model.setIntParam(name, int(value))
                return
            except KeyError:
                raise
            except LookupError or ValueError:
                pass

            try:
                self.model.setBoolParam(name, bool(value))
                return
            except LookupError or ValueError:
                pass

            try:
                self.model.setRealParam(name, float(value))
                return
            except LookupError or ValueError:
                pass

            try:
                self.model.setLongintParam(name, long(value))
                return
            except LookupError or ValueError:
                pass

            try:
                self.model.setCharParam(name, str(value))
                return
            except LookupError or ValueError:
                pass

            try:
                self.model.setStringParam(name, str(value))
                return
            except LookupError or ValueError:
                pass

