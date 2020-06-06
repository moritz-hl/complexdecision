import sympy

a, b, c, x, y = sympy.symbols('a b c x y')
z_1, z_2 = sympy.symbols('z l')

def neg(tm, z):
    return 1-tm*z

basis = sympy.groebner([a*x**2+b*x+c, a*y**2+b*y+c, neg(x-y, z_1), neg(a*x*y-c, z_2)], [a, b, c, x, y, z_1, z_2], order = 'grevlex')

print(basis)
print(1 in basis)

from lark import Lark
parser = Lark(open('univ.lark'),  start = "formula")
