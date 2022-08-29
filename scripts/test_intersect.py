#%%
# Import Dependencies

from sympy import Symbol, simplify, expand
from sympy.solvers.solvers import solve

ya = Symbol('ya', real=True)
za = Symbol('za', real=True)
va = Symbol('va', real=True)
wa = Symbol('wa', real=True)
la = Symbol('la', real=True)

yb = Symbol('yb', real=True)
zb = Symbol('zb', real=True)
vb = Symbol('vb', real=True)
wb = Symbol('wb', real=True)
lb = Symbol('lb', real=True)

eqy = ya+la*va-yb-lb*vb
eqz = za+la*wa-zb-lb*wb

print('eqy = {:}'.format(eqy))
print('eqz = {:}'.format(eqz))

lares = solve(eqy, la)[0]

print('lares = {:}'.format(lares))

eqz = simplify(expand(eqz.subs(la, lares)))

print('eqz = {:}'.format(eqz))

lbres = solve(eqz, lb)[0]

print('lbres = {:}'.format(lbres))

yf = yb+lbres*vb
zf = zb+lbres*wb

print('yf = {:}'.format(yf))
print('zf = {:}'.format(zf))
