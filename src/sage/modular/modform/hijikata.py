#########################################################################
#       Copyright (C) 2012 William Stein <wstein@gmail.com>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#
#                  http://www.gnu.org/licenses/
#########################################################################

r"""
Hijikata trace formula

Compute the trace `tr(T_n)` of the `n`th Hecke operator
acting on `S_k(\Gamma_0(N))`, for any `n \geq 1`,
except if `n|N`,  in which case `n` must be prime.

AUTHORS:

- William A. Stein (February 5, 2012)

"""

from sage.rings.all import ZZ, QQ, QuadraticField, euler_phi
from sage.functions.all import ceil, sign
from sage.misc.all import round, prod
from sage.libs.pari.all import pari
from sage.matrix.all import zero_matrix

def w(d):
    if d == -4:
        return 2
    elif d == -3:
        return 3
    else:
        return 1

def tof(a):
    t = prod(p**((e-(e%2))//2) for p,e in a.factor())
    if ZZ(a/t**2) % 4 == 1:
        return t
    else:
        return ZZ(t/2)

def mu(N):
    return N * prod(1+1/p for p in N.prime_divisors())

def sig(n, N):
    if N % n == 0:
        return n
    else:
        return prod( (1 - p**(e+1)) / (1-p) for p,e in n.factor())

def quadpoints(s, n, p, v):
    # WARNING: This is a very very stupid algorithm!
    pv = p**v
    return [x for x in range(pv) if (x**2 - s*x + n)%pv == 0]

def A(s, f, n, p, v):
    rho = ZZ(f).valuation(p)
    sr = set([x % p**(v+rho) for x in quadpoints(s, n, p, v+2*rho)])
    return len([x for x in sr if
                (2*x - s)%(p**rho) == 0 \
                and ((n != p) or ((n == p) and x%p != 0))])

def B(s, f, n, p, v):
    rho = ZZ(f).valuation(p)
    return len(set([x % p**(v+rho) for x in quadpoints(s, n, p, v+2*rho+1)]))

def cp(s, f, n, p, v):
    ans = A(s, f, n, p, v)
    if ZZ((s**2 - 4*n)/f**2) % p == 0:
        ans += B(s, f, n, p, v)
    return ans

def c(s, f, n, N):
    return prod(cp(s, f, n, p, e) for p,e in N.factor())

def type_p(n, k, N):
    if n.is_square():
        s = ZZ(int((4*n).sqrt()))
        return ZZ(1)/4 * (s/2) * n**((k//2) - 1) * (c(s,1,n,N) + (-1)**k * c(-s,1,n,N))
    else:
        return 0

def absxy(s, n, k, N):
    t = ZZ(int((s**2 - 4*n).sqrt()))
    x = (s - t)/2
    y = (s + t)/2
    return (min(abs(x), abs(y))**(k-1) / abs(x-y)) * sign(x)**k * \
           sum([ZZ(1)/2*euler_phi(ZZ(t/f))*c(s, f, n, N) for f in t.divisors()])

def type_h(n, k, N):
    start = int(ceil(2*n.sqrt()))
    if n.is_square():
        start += 1
    return sum([QQ(absxy(s, n, k, N) + absxy(-s, n, k, N)) for
                s in range(start, 4*n+1) if (s**2 - 4*n).is_square()])

def classno(d, proof=True):
    """Return the class number of the order of discriminant d."""
    # There is currently no qfbclassno method in gen.pyx, hence the string.
    return ZZ(pari('qfbclassno(%s,%s)'%(d, 1 if proof else 0)))

def xy(s, n, k, N):
    K = QuadraticField(s**2 - 4*n)
    a = K.gen()
    # x and y are the solutions to X^2 - s*X + n = 0.
    x = (s + a)/2; y = (s - a)/2
    return QQ(
        ZZ(1)/2 * (x**(k-1) - y**(k-1)) / (x - y)
          * sum(classno(ZZ((s**2 - 4*n)/f**2)) / w((s**2 - 4*n)/f**2) * c(s,f,n,N)
                for f in tof(s**2 - 4*n).divisors()))

def type_e(n, k, N):
    r = int(2*n.sqrt())
    if n.is_square():
        r -= 1
    # return sum([xy(s, n, k, N) for s in range(-r, r+1)])
    # WARNING: I *conjecture* that the sum below is the same as the one
    # that I commented out above.
    return xy(0, n, k, N) + 2*sum(xy(s, n, k, N) for s in range(1, r+1))

def sum_s(n, k, N):
    return type_p(n, k, N) + type_h(n, k, N) + type_e(n, k, N)

def test_trace_hecke_operator(n_range, k_range, N_range, verbose=True):
    """
    Verify that the trace_hecke_operator command gives the same output
    as the trace computed using modular symbols.  If not, a RuntimeError
    exception is raised.

    INPUT:

    - ``n_range`` -- list of indexes `n` for which the Hecke operator `T_n`
      is computed when `n` is either prime or `n` is coprime to the level
    - ``k_range`` -- list of weights; odd weights are ignored (since
      trace is always 0)
    - ``N_range`` -- list levels
    - ``verbose`` -- bool (default: True); if True print level and weight

    EXAMPLES::

    Test that level 1 traces are correct::
    
        sage: hijikata.test_trace_hecke_operator([1..20], [2, 4, .., 50], [1], verbose=False)

    Test levels up to 32 and weights 2,4::
    
        sage: hijikata.test_trace_hecke_operator([1..20], [2, 4], [1..32], verbose=False)
    """
    from sage.modular.modsym.all import ModularSymbols
    for N in N_range:
        for k in k_range:
            if k % 2 == 0:
                if verbose:
                    print "(N, k) =", (N,k),
                S = ModularSymbols(N,k,sign=1).cuspidal_submodule()
                for n in n_range:
                    n = ZZ(n)
                    if n.gcd(N) == 1 or n.is_prime():
                        if S.hecke_operator(n).trace() != trace_hecke_operator(n, k, N):
                            raise RuntimeError("trace_hecke_operator(n=%s,k=%s,N=%s) disagrees with modular symbols trace"%(n,k,N))
                if verbose: print " (good)"

def trace_hecke_operator(n, k, N=1):
    r"""
    Return the trace of the Hecke operator `T_n` on
    `S_k(\Gamma_0(N)))`.  The only constraint on `n` is that if
    `GCD(n,N) \neq 1`, then `n` must be prime.

    INPUT:

    - `n` -- positive integer
    - `k` -- integer at least 2
    - `N` -- positive integer

    OUTPUT:

    - rational number

    EXAMPLES::

    We compute the trace of the first few Hecke operators on level 1
    weight 12::

        sage: hijikata.trace_hecke_operator(1, 12)
        1
        sage: v = [hijikata.trace_hecke_operator(n, 12) for n in [1..30]]
        sage: v[:10]
        [1, -24, 252, -1472, 4830, -6048, -16744, 84480, -113643, -115920]
        sage: list(delta_qexp(31))[1:] == v
        True

    We can compute dimensions using the trace formula::

        sage: hijikata.trace_hecke_operator(1, 20000)
        1666
        sage: dimension_cusp_forms(1, 20000)
        1666    
        sage: hijikata.trace_hecke_operator(1, 2000, 11)
        1998
        sage: dimension_cusp_forms(11, 2000)
        1998

    An advantage of the trace formula is that can quickly compute
    traces of operators that one couldn't do using other techniques
    like modular symbols.  For example, here we instantly compute the
    trace of `T_2` on `S_{20000}(\Gamma_0(19))`::
    
        sage: t = hijikata.trace_hecke_operator(2, 20000, 19)
        sage: t.valuation(2)
        1    
    """
    n = ZZ(n); k=ZZ(k); N=ZZ(N)
    if n.gcd(N) != 1 and not n.is_prime():
        raise ValueError, "n must be prime when n and N are not coprime"

    if k%2 != 0:
        return 0
    if k == 2:
        t = sig(n, N)
    else:
        t = 0
    t += -sum_s(n, k, N)
    if n.is_square():
        t += (k-1)*mu(N) / 12 * n**((k//2) - 1)
    return t

def trace_modular_form(k, prec):
    r"""
    Return the trace modular form sum `Tr(T_n) q^n` to absolute
    precision prec, where `T_n` is the `n`th Hecke operator on
    `S_k(SL_2(Z))`.  The complexity is almost entirely a function of
    prec, but not of `k`.

    INPUT:

    - `k` -- positive integer
    - ``prec`` -- positive integer

    EXAMPLES::

        sage: hijikata.trace_modular_form(12, 6)
        q - 24*q^2 + 252*q^3 - 1472*q^4 + 4830*q^5 + O(q^6)
        sage: hijikata.trace_modular_form(24, 6)
        2*q + 1080*q^2 + 339480*q^3 + 25326656*q^4 + 73069020*q^5 + O(q^6)    
    """
    R = QQ[['q']]
    return R([0] + [trace_hecke_operator(n, k, 1) for n in range(1, prec)], prec)

def Tp(p, r, k, f):
    if r > 1:
        return Tp(p, 1, k, Tp(p, r-1, k, f)) - p**(k-1)*Tp(p, r-2, k, f)
    if r == 1:
        R = QQ[['q']]
        q = R.gen()
        prec = int(((f.prec()-1)/p) + 1)
        return R(sum(f[n*p]*q**n + p**(k-1)*f[n]*q**(n*p) for n in range(1, prec)), prec)
    if r == 0:
        return f

def hecke_operator(n, k, f):
    n = ZZ(n)
    for p, e in n.factor():
        f = Tp(p, e, k, f)
    return f

def trace_formula_basis(k, prec):
    """
    EXAMPLES::

        sage: hijikata.trace_formula_basis(24, 6)
        [2*q + 1080*q^2 + 339480*q^3 + 25326656*q^4 + 73069020*q^5 + O(q^6), 1080*q + 42103872*q^2 + O(q^3)]    

    Double check the claimed result above to higher precision::
    
        sage: B = [vector(QQ,f.qexp(10)) for f in CuspForms(1, 24).basis()]
        sage: C = [vector(QQ, f.padded_list(10)) for f in hijikata.trace_formula_basis(24, 21)]
        sage: span(B) == span(C)
        True    
    """
    f = trace_modular_form(k, prec)
    d = ZZ(f[1])  # the dimension
    return [hecke_operator(n, k, f) for n in range(1, d+1)]

def basis_matrix(B):
    d = len(B)
    I = zero_matrix(QQ, d)
    for r in range(d):
        for c in range(d):
            I[r,c] = B[r][c+1]
    return I

def hecke_operator_matrix(k, n):
    """
    EXAMPLES::

        sage: hijikata.hecke_operator_matrix(24, 2)
        [       0 20468736]
        [       1     1080]
        sage: hijikata.hecke_operator_matrix(24, 2).fcp()
        x^2 - 1080*x - 20468736
        sage: CuspForms(1, 24).hecke_polynomial(2)
        x^2 - 1080*x - 20468736
    """
    from sage.modular.dims import dimension_cusp_forms
    d = dimension_cusp_forms(1, k)
    B = trace_formula_basis(k, n*d**2 + 1)
    return hecke_operator_matrix_wrt_basis(k, n, B)

def hecke_operator_matrix_wrt_basis(k, n, B):
    d = len(B)
    I = basis_matrix(B)**(-1)
    A = []
    for j in range(d):
        g = hecke_operator(n, k, B[j])
        A.append([g[i] for i in range(1, d+1)])
    A = I.parent()(A)
    return I*A


                   
