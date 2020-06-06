from sympy import symbols, groebner
from lark import Lark, Transformer, v_args

calc_grammar = r"""
    imp:  conj "==>" eq -> imp
    conj: [eq ("/\\" eq)*] -> conj
    ?ineq: term "/=" term -> ineq
    ?eq: term "=" term -> eq
    ?term: sum
    ?sum: product
        | sum "+" product   -> add
        | sum "-" product   -> sub
    ?product: atom
        | product "*" atom  -> mul
        | product "/" num  -> div
    ?atom: NUMBER           -> number
         | "-" atom         -> neg
         | NAME             -> var
         | "(" sum ")"
         | atom "^" num  -> power
    ?num: NUMBER           -> number
    %import common.CNAME -> NAME
    %import common.NUMBER
    %import common.WS_INLINE
    %ignore WS_INLINE
"""

@v_args(inline=True)    # Affects the signatures of the methods
class UnivTree(Transformer):
    from operator import add, sub, mul, truediv as div, neg
    number = int

    def __init__(self):
        self.vars = set()

    def imp(self, left, right):
        return (left, right)

    def conj(self, *args):
        return list(args)

    def var(self, name):
        self.vars.add(symbols(name))
        return symbols(name)
    
    def eq(self, left, right):
        return left-right
    
    def power(self, base, exp):
        return base ** exp


transformer = UnivTree()

univ_parser = Lark(calc_grammar, parser='lalr', transformer=transformer, start = "imp")
parse = univ_parser.parse
parseRes = parse(r"a*xx^2+b*xx+c = 0 /\ b = 0 /\ c = 0 /\ 1-xx*zz=0 /\ 1-a*z = 0 ==> 1 = 0")

print(parseRes)
print(transformer.vars)

print(parseRes[1])

basis = groebner(parseRes[0], list(transformer.vars), order = "grevlex")

print(basis)
print(1 in basis)