from flask import Flask
from flask import request
from datetime import datetime
from sympy import symbols, groebner
from lark import Lark, Transformer, v_args

app = Flask(__name__)




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




@app.route('/')
def homepage():
    transformer = UnivTree()

    univ_parser = Lark(calc_grammar, parser='lalr', transformer=transformer, start = "imp")
    parse = univ_parser.parse

    formula = request.args.get("formula")
    parsed = parse(formula)

    basis = groebner(parsed[0], list(transformer.vars), order = "grevlex")
    ev = 1 in basis
    return """
    <h1>Gröbner</h1>
    <form action = "/">
    <input style="width:800px" type = "text" id = "formula" name = "formula" value = "{raw}">
    </form>
    <p>Formula: {getp}</p>
    <p> Basis: {basis}</p>
    <p>Wahr: {ev} </p>
    """.format(raw = formula, getp = parsed, basis = basis, ev = ev)
if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)

