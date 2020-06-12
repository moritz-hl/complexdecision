from flask import Flask
from flask import request
from datetime import datetime
from sympy import symbols, groebner
from lark import Lark, Transformer, v_args

from static import *

app = Flask(__name__, static_url_path = "", static_folder="static")

@v_args(inline=True)
class UnivTree(Transformer):
    from operator import add, sub, mul, truediv as div, neg
    number = int

    def __init__(self):
        self.vars = set()
        self.helpers = 0

    def imp(self, left, right):
        return (left, right)

    def conj(self, *args):
        return list(args)

    def var(self, name):
        self.vars.add(symbols(name))
        return symbols(name)
    
    def eq(self, left, right):
        return left-right
    
    def ineq(self, left, right):
        helper = symbols("z" + str(self.helpers))
        self.helpers += 1
        self.vars.add(helper)
        return helper*(left-right)-1
    
    def power(self, base, exp):
        return base ** exp

    def disj(self, *args):
        result = 1
        print(args)
        for arg in args:
            print(arg)
            if arg:
                result *= arg
        print(result)
        return result

def neg(tm, z):
    return 1-tm*z

@app.route('/')
def homepage():
    transformer = UnivTree()

    univ_parser = Lark(open("grammar.lark"), parser='lalr', transformer=transformer, start = "imp")

    formula = request.args.get("formula")

    if not formula:
        formula = "x=y==>y=x"
    
    try:
        parse = univ_parser.parse

        parsed = parse(formula)

        z = symbols("zz")

        basis = list(groebner(parsed[0] + [neg(parsed[1], z)], list(transformer.vars) + [z], order = "grevlex"))
        ev = 1 in basis

        suc_class = "true"
        if not ev:
            suc_class = "false"
        return pos_out(suc_class, formula, basis, ev)

    except Exception as err:
        return err_out(formula, err)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)