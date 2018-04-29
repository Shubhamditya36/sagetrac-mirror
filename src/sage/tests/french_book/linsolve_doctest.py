## -*- encoding: utf-8 -*-
r"""
This file (./linsolve_doctest.sage) was *autogenerated* from ./linsolve.tex,
with sagetex.sty version 2011/05/27 v2.3.1.
It contains the contents of all the sageexample environments from this file.
You should be able to doctest this file with:
sage -t ./linsolve_doctest.sage
It is always safe to delete this file; it is not used in typesetting your
document.

Sage example in ./linsolve.tex, line 235::

  sage: def cond_hilbert(n):
  ....:     A = matrix(QQ, [[1/(i+j-1) for j in [1..n]] for i in [1..n]])
  ....:     return A.norm(Infinity) * (A^-1).norm(Infinity)

Sage example in ./linsolve.tex, line 269::

  sage: n = 8
  sage: x = vector(QQ,[1 for i in range(0,n)])
  sage: A = matrix(QQ, [[1/(i+j-1) for j in [1..n]] for i in [1..n]])
  sage: y = A*x
  sage: A[n-1,n-1] = (1/(2*n-1))*(1+1/(10^5)) # perturbe la matrice
  sage: sol = A\y
  sage: diff = max(float(sol[i]-x[i]) for i in range(0,n))

Sage example in ./linsolve.tex, line 313::

  sage: n = 8
  sage: A = matrix(RR, [[1/(i+j-1) for j in [1..n]] for i in [1..n]])
  sage: x = vector(RR, [1 for i in range(0,n)])
  sage: y = A*x
  sage: s = A.solve_right(y)
  sage: diff = [float(s[i]-x[i]) for i in range(0,n)]

Sage example in ./linsolve.tex, line 422::

  sage: n = 20; cout = (n+1)*factorial(n); cout
  51090942171709440000

Sage example in ./linsolve.tex, line 433::

  sage: v = 3*10^9
  sage: print("%3.3f" % float(cout/v/3600/24/365))
  540.028

Sage example in ./linsolve.tex, line 502::

  sage: A = matrix(RDF, [[-1,2],[3,4]])
  sage: b = vector(RDF, [2,3])
  sage: x = A\b; x  # rel tol 3e-15
  (-0.20000000000000018, 0.9000000000000001)

Sage example in ./linsolve.tex, line 512::

  sage: x = A.solve_right(b)

Sage example in ./linsolve.tex, line 520::

  sage: A = matrix(RDF, [[-1,2],[3,4]])
  sage: P, L, U = A.LU()

Sage example in ./linsolve.tex, line 561::

  sage: A = random_matrix(RDF, 1000)
  sage: b = vector(RDF, range(1000))

Sage example in ./linsolve.tex, line 600::

  sage: m = random_matrix(RDF, 10)
  sage: A = transpose(m)*m
  sage: C = A.cholesky()

Sage example in ./linsolve.tex, line 655::

  sage: A = random_matrix(RDF,6,5)
  sage: Q, R = A.QR()

Sage example in ./linsolve.tex, line 786::

  sage: A = matrix(RDF, [[1,3,2],[1,4,2],[0,5,2],[1,3,2]])
  sage: b = vector(RDF, [1,2,3,4])
  sage: Z = transpose(A)*A
  sage: C = Z.cholesky()
  sage: R = transpose(A)*b
  sage: Z.solve_right(R)  # rel tol 1e-13
  (-1.5000000000000044, -0.5000000000000009, 2.750000000000003)

Sage example in ./linsolve.tex, line 822::

  sage: A = matrix(RDF, [[1,3,2],[1,4,2],[0,5,2],[1,3,2]])
  sage: b = vector(RDF, [1,2,3,4])
  sage: Q, R = A.QR()
  sage: R1 = R[0:3,0:3]
  sage: b1 = transpose(Q)*b
  sage: c = b1[0:3]
  sage: R1.solve_right(c)  # rel tol 2e-14
  (-1.499999999999999, -0.49999999999999867, 2.7499999999999973)

Sage example in ./linsolve.tex, line 834::

  sage: Z = A.transpose()*A
  sage: Z.norm(Infinity)*(Z^-1).norm(Infinity)  # rel tol 1e-14
  1992.3750000000084

Sage example in ./linsolve.tex, line 876::

  sage: A = matrix(RDF, [[1,3,2],[1,3,2],[0,5,2],[1,3,2]])
  sage: b = vector(RDF, [1,2,3,4])
  sage: U, Sig, V = A.SVD()
  sage: m = A.ncols()
  sage: x = vector(RDF, [0]*m)
  sage: lamb = vector(RDF, [0]*m)
  sage: for i in range(0,m):
  ....:     s = Sig[i,i]
  ....:     if s < 1e-12:
  ....:        break
  ....:     lamb[i] = U.column(i)*b / s
  sage: x = V*lamb; x  # rel tol 1e-14
  (0.2370370370370367, 0.4518518518518521, 0.3703703703703702)

Sage example in ./linsolve.tex, line 968::

  sage: A = matrix(RDF, [[1,2],[3,4],[5,6],[7,8]])

Sage example in ./linsolve.tex, line 974::

  sage: th = 0.7
  sage: R = matrix(RDF, [[cos(th),sin(th)],[-sin(th),cos(th)]])
  sage: B = (A + 0.1*random_matrix(RDF,4,2)) * transpose(R)

Sage example in ./linsolve.tex, line 1189::

  sage: A = matrix(RDF, [[1,3,2],[1,2,3],[0,5,2]])

Sage example in ./linsolve.tex, line 1382::

  sage: def pol2companion(p):
  ....:     n = len(p)
  ....:     m = matrix(RDF,n)
  ....:     for i in range(1,n):
  ....:         m[i,i-1]=1
  ....:     for i in range(0,n):
  ....:         m[i,n-1]=-p[i]
  ....:     return m

Sage example in ./linsolve.tex, line 1392::

  sage: q = [1,-1,2,3,5,-1,10,11]
  sage: comp = pol2companion(q); comp
  [  0.0   0.0   0.0   0.0   0.0   0.0   0.0  -1.0]
  [  1.0   0.0   0.0   0.0   0.0   0.0   0.0   1.0]
  [  0.0   1.0   0.0   0.0   0.0   0.0   0.0  -2.0]
  [  0.0   0.0   1.0   0.0   0.0   0.0   0.0  -3.0]
  [  0.0   0.0   0.0   1.0   0.0   0.0   0.0  -5.0]
  [  0.0   0.0   0.0   0.0   1.0   0.0   0.0   1.0]
  [  0.0   0.0   0.0   0.0   0.0   1.0   0.0 -10.0]
  [  0.0   0.0   0.0   0.0   0.0   0.0   1.0 -11.0]
  sage: racines = comp.eigenvalues(); racines  # abs tol 1e-10
  [0.347521510119 + 0.566550553398*I,
   0.347521510119 - 0.566550553398*I,
   0.345023776962 + 0.439908702386*I,
   0.345023776962 - 0.439908702386*I,
   -0.517257614325 + 0.512958206789*I,
   -0.517257614325 - 0.512958206789*I,
   -1.36699716455,
   -9.98357818097]

Sage example in ./linsolve.tex, line 1515::

  sage: def eval(P,x):
  ....:     if len(P) == 0:
  ....:         return 0
  ....:     else:
  ....:         return P[0]+x*eval(P[1:],x)

Sage example in ./linsolve.tex, line 1523::

  sage: def pscal(P,Q,lx):
  ....:     return float(sum(eval(P,s)*eval(Q,s) for s in lx))

Sage example in ./linsolve.tex, line 1528::

  sage: def padd(P,a,Q):
  ....:     for i in range(0,len(Q)):
  ....:         P[i] += a*Q[i]

Sage example in ./linsolve.tex, line 1536::

  sage: class BadParamsforOrthop(Exception):
  ....:     def __init__(self, degreplusun, npoints):
  ....:         self.deg = degreplusun
  ....:         self.np = npoints
  ....:     def __str__(self):
  ....:         return "degre: " + str(self.deg) + \
  ....:                " nb. points: " + repr(self.np)

Sage example in ./linsolve.tex, line 1546::

  sage: def orthopoly(n,x):
  ....:     if n > len(x):
  ....:         raise BadParamsforOrthop(n-1, len(x))
  ....:     orth = [[1./sqrt(float(len(x)))]]
  ....:     for p in range(1,n):
  ....:         nextp = copy(orth[p-1])
  ....:         nextp.insert(0,0)
  ....:         s = []
  ....:         for i in range(p-1,max(p-3,-1),-1):
  ....:             s.append(pscal(nextp, orth[i], x))
  ....:         j = 0
  ....:         for i in range(p-1,max(p-3,-1),-1):
  ....:             padd(nextp, -s[j], orth[i])
  ....:             j += 1
  ....:         norm = sqrt(pscal(nextp, nextp, x))
  ....:         nextpn = [nextp[i]/norm for i in range(len(nextp))]
  ....:         orth.append(nextpn)
  ....:     return orth

"""
# This file was *autogenerated* from the file linsolve_doctest.sage.