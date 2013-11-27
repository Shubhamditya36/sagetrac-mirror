
## -*- encoding: utf-8 -*-
"""
This file (./linalg_doctest.sage) was *autogenerated* from ./linalg.tex,
with sagetex.sty version 2011/05/27 v2.3.1.
It contains the contents of all the sageexample environments from this file.
You should be able to doctest this file with:
sage -t ./linalg_doctest.sage
It is always safe to delete this file; it is not used in typesetting your
document.

Sage example in ./linalg.tex, line 136::

    sage: MS = MatrixSpace(ZZ,2,3); MS
    Full MatrixSpace of 2 by 3 dense matrices over Integer Ring
    sage: VS = VectorSpace(GF(3^2,'x'),3); VS
    Vector space of dimension 3 over Finite Field in x of size 3^2

Sage example in ./linalg.tex, line 148::

    sage: MatrixSpace(ZZ,2,3).basis()
    [
    [1 0 0]  [0 1 0]  [0 0 1]  [0 0 0]  [0 0 0]  [0 0 0]
    [0 0 0], [0 0 0], [0 0 0], [1 0 0], [0 1 0], [0 0 1]
    ]

Sage example in ./linalg.tex, line 190::

    sage: A = matrix(GF(11), 2, 2, [1,0,0,2])
    sage: B = matrix(GF(11), 2, 2, [0,1,1,0])
    sage: MG = MatrixGroup([A,B])
    sage: MG.cardinality()
    200
    sage: identity_matrix(GF(11),2) in MG
    True

Sage example in ./linalg.tex, line 226::

    sage: MS = MatrixSpace(ZZ,2,3); A = MS([1,2,3,4,5,6]); A
    [1 2 3]
    [4 5 6]

Sage example in ./linalg.tex, line 247::

    sage: a = matrix(); a.parent()
    Full MatrixSpace of 0 by 0 dense matrices over Integer Ring

Sage example in ./linalg.tex, line 263::

    sage: a = matrix(GF(8,'x'),3,4); a.parent()
    Full MatrixSpace of 3 by 4 dense matrices over Finite Field
    in x of size 2^3

Sage example in ./linalg.tex, line 274::

    sage: g = graphs.PetersenGraph()
    sage: m = matrix(g); m; m.parent()
    [0 1 0 0 1 1 0 0 0 0]
    [1 0 1 0 0 0 1 0 0 0]
    [0 1 0 1 0 0 0 1 0 0]
    [0 0 1 0 1 0 0 0 1 0]
    [1 0 0 1 0 0 0 0 0 1]
    [1 0 0 0 0 0 0 1 1 0]
    [0 1 0 0 0 0 0 0 1 1]
    [0 0 1 0 0 1 0 0 0 1]
    [0 0 0 1 0 1 1 0 0 0]
    [0 0 0 0 1 0 1 1 0 0]
    Full MatrixSpace of 10 by 10 dense matrices over Integer Ring

Sage example in ./linalg.tex, line 295::

    sage: A = matrix([[1,2],[3,4]])
    sage: block_matrix([[A,-A],[2*A, A^2]])
    [ 1  2|-1 -2]
    [ 3  4|-3 -4]
    [-----+-----]
    [ 2  4| 7 10]
    [ 6  8|15 22]

Sage example in ./linalg.tex, line 320::

    sage: A = matrix([[1,2,3],[4,5,6]])
    sage: block_matrix([1,A,0,0,-A,2], ncols=3)
    [ 1  0| 1  2  3| 0  0]
    [ 0  1| 4  5  6| 0  0]
    [-----+--------+-----]
    [ 0  0|-1 -2 -3| 2  0]
    [ 0  0|-4 -5 -6| 0  2]

Sage example in ./linalg.tex, line 346::

    sage: A = matrix([[1,2,3],[0,1,0]])
    sage: block_diagonal_matrix(A, A.transpose())
    [1 2 3|0 0]
    [0 1 0|0 0]
    [-----+---]
    [0 0 0|1 0]
    [0 0 0|2 1]
    [0 0 0|3 0]

Sage example in ./linalg.tex, line 397::

    sage: A = matrix(3,3,range(9))
    sage: A[:,1] = vector([1,1,1]); A
    [0 1 2]
    [3 1 5]
    [6 1 8]

Sage example in ./linalg.tex, line 414::

    sage: A[::-1], A[:,::-1], A[::2,-1]
    (
    [6 1 8]  [2 1 0]
    [3 1 5]  [5 1 3]  [2]
    [0 1 2], [8 1 6], [8]
    )

Sage example in ./linalg.tex, line 446::

    sage: A = matrix(ZZ,4,4,range(16)); A
    [ 0  1  2  3]
    [ 4  5  6  7]
    [ 8  9 10 11]
    [12 13 14 15]


Sage example in ./linalg.tex, line 462::

    sage: A.matrix_from_rows_and_columns([0,2,3],[1,2])
    [ 1  2]
    [ 9 10]
    [13 14]

Sage example in ./linalg.tex, line 505::

    sage: MS = MatrixSpace(GF(3),2,3)
    sage: MS.base_extend(GF(9,'x'))
    Full MatrixSpace of 2 by 3 dense matrices over Finite Field
    in x of size 3^2
    sage: MS = MatrixSpace(ZZ,2,3)
    sage: MS.change_ring(GF(3))
    Full MatrixSpace of 2 by 3 dense matrices over Finite Field of size 3

Sage example in ./linalg.tex, line 896::

    sage: a = matrix(GF(7),4,3,[6,2,2,5,4,4,6,4,5,5,1,3]); a
    [6 2 2]
    [5 4 4]
    [6 4 5]
    [5 1 3]

Sage example in ./linalg.tex, line 910::

    sage: u = copy(identity_matrix(GF(7),4)); u[1:,0] = -a[1:,0]/a[0,0]
    sage: u, u*a
    (
    [1 0 0 0]  [6 2 2]
    [5 1 0 0]  [0 0 0]
    [6 0 1 0]  [0 2 3]
    [5 0 0 1], [0 4 6]
    )

Sage example in ./linalg.tex, line 932::

    sage: v = copy(identity_matrix(GF(7),4)); v.swap_rows(1,2)
    sage: b = v*u*a; v, b
    (
    [1 0 0 0]  [6 2 2]
    [0 0 1 0]  [0 2 3]
    [0 1 0 0]  [0 0 0]
    [0 0 0 1], [0 4 6]
    )

Sage example in ./linalg.tex, line 954::

    sage: w = copy(identity_matrix(GF(7),4))
    sage: w[2:,1] = -b[2:,1]/b[1,1]; w, w*b
    (
    [1 0 0 0]  [6 2 2]
    [0 1 0 0]  [0 2 3]
    [0 0 1 0]  [0 0 0]
    [0 5 0 1], [0 0 0]
    )

Sage example in ./linalg.tex, line 1024::

    sage: A = matrix(GF(7),4,5,[4,4,0,2,4,5,1,6,5,4,1,1,0,1,0,5,1,6,6,2])
    sage: A, A.echelon_form()
    (
    [4 4 0 2 4]  [1 0 5 0 3]
    [5 1 6 5 4]  [0 1 2 0 6]
    [1 1 0 1 0]  [0 0 0 1 5]
    [5 1 6 6 2], [0 0 0 0 0]
    )

Sage example in ./linalg.tex, line 1147::

    sage: a = matrix(ZZ, 4, 6, [2,1,2,2,2,-1,1,2,-1,2,1,-1,2,1,-1,\
    ....:              -1,2,2,2,1,1,-1,-1,-1]); a.echelon_form()
    [ 1  2  0  5  4 -1]
    [ 0  3  0  2 -6 -7]
    [ 0  0  1  3  3  0]
    [ 0  0  0  6  9  3]

Sage example in ./linalg.tex, line 1163::

    sage: a.base_extend(QQ).echelon_form()
    [   1    0    0    0  5/2 11/6]
    [   0    1    0    0   -3 -8/3]
    [   0    0    1    0 -3/2 -3/2]
    [   0    0    0    1  3/2  1/2]

Sage example in ./linalg.tex, line 1189::

    sage: A = matrix(ZZ,4,5,[4,4,0,2,4,5,1,6,5,4,1,1,0,1,0,5,1,6,6,2])
    sage: H, U = A.echelon_form(transformation=True); H, U
    (
    [ 1  1  0  0  2]  [ 0  1  1 -1]
    [ 0  4 -6  0 -4]  [ 0 -1  5  0]
    [ 0  0  0  1 -2]  [ 0 -1  0  1]
    [ 0  0  0  0  0], [ 1 -2 -4  2]
    )

Sage example in ./linalg.tex, line 1250::

    sage: A = matrix(ZZ, 4, 5,\
    ....:            [-1,-1,-1,-2,-2,-2,1,1,-1,2,2,2,2,2,-1,2,2,2,2,2])
    sage: S,U,V = A.smith_form(); S,U,V
    (
                                [ 0 -2 -1 -5  0]
    [1 0 0 0 0]  [ 1  0  0  0]  [ 1  0  1 -1 -1]
    [0 1 0 0 0]  [ 0  0  1  0]  [ 0  0  0  0  1]
    [0 0 3 0 0]  [-2  1  0  0]  [-1  2  0  5  0]
    [0 0 0 6 0], [ 0  0 -2 -1], [ 0 -1  0 -2  0]
    )

Sage example in ./linalg.tex, line 1284::

    sage: A.elementary_divisors()
    [1, 1, 3, 6]
    sage: S == U*A*V
    True

Sage example in ./linalg.tex, line 1329::

    sage: B = matrix(GF(7),5,4,[4,5,1,5,4,1,1,1,0,6,0,6,2,5,1,6,4,4,0,2])
    sage: B.transpose().echelon_form()
    [1 0 5 0 3]
    [0 1 2 0 6]
    [0 0 0 1 5]
    [0 0 0 0 0]

Sage example in ./linalg.tex, line 1344::

    sage: B.pivot_rows()
    (0, 1, 3)
    sage: B.transpose().pivots() == B.pivot_rows()
    True

Sage example in ./linalg.tex, line 1381::

    sage: R.<x> = PolynomialRing(GF(5),'x')
    sage: A = random_matrix(R,2,3); A                    # random
    [      3*x^2 + x       x^2 + 2*x       2*x^2 + 2]
    [    x^2 + x + 2 2*x^2 + 4*x + 3   x^2 + 4*x + 3]

Sage example in ./linalg.tex, line 1393::

    sage: b = random_matrix(R,2,1); b                    # random
    [  4*x^2 + 1]
    [3*x^2 + 2*x]

Sage example in ./linalg.tex, line 1404::

    sage: A.solve_right(b)                               # random
    [(4*x^3 + 2*x + 4)/(3*x^3 + 2*x^2 + 2*x)]
    [  (3*x^2 + 4*x + 3)/(x^3 + 4*x^2 + 4*x)]
    [                                      0]

Sage example in ./linalg.tex, line 1418::

    sage: A.solve_right(b) == A\b
    True

Sage example in ./linalg.tex, line 1449::

    sage: a = matrix(QQ,3,5,[2,2,-1,-2,-1,2,-1,1,2,-1/2,2,-2,-1,2,-1/2])
    sage: a.image()
    Vector space of degree 5 and dimension 3 over Rational Field
    Basis matrix:
    [     1      0      0    1/4 -11/32]
    [     0      1      0     -1   -1/8]
    [     0      0      1    1/2   1/16]
    sage: a.right_kernel()
    Vector space of degree 5 and dimension 2 over Rational Field
    Basis matrix:
    [    1     0     0  -1/3   8/3]
    [    0     1  -1/2 11/12   2/3]

Sage example in ./linalg.tex, line 1472::

    sage: a = matrix(ZZ,5,3,[1,1,122,-1,-2,1,-188,2,1,1,-10,1,-1,-1,-1])
    sage: a.kernel()
    Free module of degree 5 and rank 2 over Integer Ring
    Echelon basis matrix:
    [   1  979  -11 -279  811]
    [   0 2079  -22 -569 1488]
    sage: b = a.base_extend(QQ)
    sage: b.kernel()
    Vector space of degree 5 and dimension 2 over Rational Field
    Basis matrix:
    [        1         0  -121/189 -2090/189   6949/63]
    [        0         1    -2/189 -569/2079   496/693]
    sage: b.integer_kernel()
    Free module of degree 5 and rank 2 over Integer Ring
    Echelon basis matrix:
    [   1  979  -11 -279  811]
    [   0 2079  -22 -569 1488]

Sage example in ./linalg.tex, line 1684::

    sage: A = matrix(GF(97), 4, 4,\
    ....:            [86,1,6,68,34,24,8,35,15,36,68,42,27,1,78,26])
    sage: e1 = identity_matrix(GF(97),4)[0]
    sage: U = matrix(A.transpose().maxspin(e1)).transpose()
    sage: F = U^-1*A*U; F
    [ 0  0  0 83]
    [ 1  0  0 77]
    [ 0  1  0 20]
    [ 0  0  1 10]

Sage example in ./linalg.tex, line 1703::

    sage: K.<x> = GF(97)[]
    sage: P = x^4-sum(F[i,3]*x^i for i in range(4)); P
    x^4 + 87*x^3 + 77*x^2 + 20*x + 14

Sage example in ./linalg.tex, line 1709::

    sage: P == A.charpoly()
    True

Sage example in ./linalg.tex, line 1813::

    sage: A = matrix(ZZ,8,[[6,0,-2,4,0,0,0,-2],[14,-1,0,6,0,-1,-1,1],\
    ....:                  [2,2,0,1,0,0,1,0],[-12,0,5,-8,0,0,0,4],\
    ....:                  [0,4,0,0,0,0,4,0],[0,0,0,0,1,0,0,0],\
    ....:                  [-14,2,0,-6,0,2,2,-1],[-4,0,2,-4,0,0,0,4]])
    sage: A.frobenius()
    [0 0 0 4 0 0 0 0]
    [1 0 0 4 0 0 0 0]
    [0 1 0 1 0 0 0 0]
    [0 0 1 0 0 0 0 0]
    [0 0 0 0 0 0 4 0]
    [0 0 0 0 1 0 0 0]
    [0 0 0 0 0 1 1 0]
    [0 0 0 0 0 0 0 2]

Sage example in ./linalg.tex, line 1845::

    sage: A.frobenius(1)
    [x^4 - x^2 - 4*x - 4, x^3 - x^2 - 4, x - 2]

Sage example in ./linalg.tex, line 1851::

    sage: F,K = A.frobenius(2)
    sage: K
    [     1    -1/2    1/16   15/64   3/128    7/64  -23/64  43/128]
    [     0       0   -5/64 -13/128 -15/256  17/128  -7/128  53/256]
    [     0       0   9/128 -11/128  -7/128   -1/32   5/128    5/32]
    [     0       0  -5/128       0   7/256  -7/128   -1/64   9/256]
    [     0       1    1/16    5/32  -17/64   -1/32   31/32  -21/64]
    [     0       0    1/32    5/64  31/128  -17/64   -1/64 -21/128]
    [     0       0    1/32    5/64  -1/128   15/64   -1/64 -21/128]
    [     0       0       1     5/2    -1/4    -1/2    -1/2   -21/4]

Sage example in ./linalg.tex, line 1877::

    sage: K^-1*F*K == A
    True

Sage example in ./linalg.tex, line 1905::

    sage: S.<x> = QQ[]
    sage: B = x*identity_matrix(8) - A
    sage: B.elementary_divisors()
    [1, 1, 1, 1, 1, x - 2, x^3 - x^2 - 4, x^4 - x^2 - 4*x - 4]

Sage example in ./linalg.tex, line 1913::

    sage: A.frobenius(1)
    [x^4 - x^2 - 4*x - 4, x^3 - x^2 - 4, x - 2]

Sage example in ./linalg.tex, line 1981::

    sage: A = matrix(GF(7),4,[5,5,4,3,0,3,3,4,0,1,5,4,6,0,6,3])
    sage: A.eigenvalues()
    [4, 1, 2, 2]
    sage: A.eigenvectors_right()
    [(4, [
    (1, 5, 5, 1)
    ], 1), (1, [
    (0, 1, 1, 4)
    ], 1), (2, [
    (1, 3, 0, 1),
    (0, 0, 1, 1)
    ], 2)]
    sage: A.eigenspaces_right()
    [
    (4, Vector space of degree 4 and dimension 1 over Finite Field
    of size 7
    User basis matrix:
    [1 5 5 1]),
    (1, Vector space of degree 4 and dimension 1 over Finite Field
    of size 7
    User basis matrix:
    [0 1 1 4]),
    (2, Vector space of degree 4 and dimension 2 over Finite Field
    of size 7
    User basis matrix:
    [1 3 0 1]
    [0 0 1 1])
    ]

Sage example in ./linalg.tex, line 2019::

    sage: A.eigenmatrix_right()
    (
    [4 0 0 0]  [1 0 1 0]
    [0 1 0 0]  [5 1 3 0]
    [0 0 2 0]  [5 1 0 1]
    [0 0 0 2], [1 4 1 1]
    )

Sage example in ./linalg.tex, line 2144::

    sage: A = matrix(ZZ,4,[3,-1,0,-1,0,2,0,-1,1,-1,2,0,1,-1,-1,3])
    sage: A.jordan_form()
    [3|0|0 0]
    [-+-+---]
    [0|3|0 0]
    [-+-+---]
    [0|0|2 1]
    [0|0|0 2]

Sage example in ./linalg.tex, line 2163::

    sage: J,U = A.jordan_form(transformation=True)
    sage: U^-1*A*U == J
    True
"""
# This file was *autogenerated* from the file linalg_doctest.sage.
