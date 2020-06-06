from flask import Flask
from flask import request
from datetime import datetime
from sympy import symbols, groebner
from lark import Lark, Transformer, v_args

app = Flask(__name__, static_url_path = "", static_folder="static")

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


header = """
<!DOCTYPE html>
<html>
<head>
<title>Gröbner Basis</title>
<link rel = "stylesheet" href = "./style.css">
</head>
<body>
"""

footer = """
<h2>Examples</h2>
<ul>
<li> <a href = "/?formula=x+%3D+2+%2F%5C+y+%3D+3+%3D%3D>+x+%2By+%3D+5">2+3 = 5</a>
<li> <a href = "/?formula=a%5E2+%3D+2+%2F%5C+x%5E2%2Ba*x+%2B+1+%3D+0+%3D%3D>+x%5E4+%2B+1+%3D+0">Complex Roots</a>
<li> <a href = "/?formula=a*x%5E2%2Bb*x%2Bc+%3D+0+%2F%5C+a*y%5E2%2Bb*y%2Bc+%3D+0+%2F%5C+1-%28x-y%29*z+%3D+0+%3D%3D>+a*x*y+%3D+c">Vieta I</a>
<li> <a href = "/?formula=a*x%5E2%2Bb*x%2Bc+%3D+0+%2F%5C+a*y%5E2%2Bb*y%2Bc+%3D+0+%2F%5C+1-%28x-y%29*z+%3D+0+%3D%3D>+a*%28x%2By%29+%3D+-b">Vieta II</a>
<li> <a href = "/?formula=x+%3D+0++%3D%3D>++x+%3D+1">non-sense</a>
</ul>
</body>
</html>
"""


def wrap(content):
    return header + content + footer

@v_args(inline=True)
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


def neg(tm, z):
    return 1-tm*z

@app.route('/')
def homepage():
    transformer = UnivTree()

    univ_parser = Lark(calc_grammar, parser='lalr', transformer=transformer, start = "imp")

    formula = request.args.get("formula")
    

    try:
        parse = univ_parser.parse

        parsed = parse(formula)

        z = symbols("z1")

        basis = list(groebner(parsed[0] + [neg(parsed[1], z)], list(transformer.vars) + [z], order = "grevlex"))
        ev = 1 in basis

        suc_class = "true"
        if not ev:
            suc_class = "false"
        return wrap("""
        <h1>Gröbner</h1>
        <div id = "wrapper" class = "{cls}">
        <form action = "/">
        <input style="width:800px" type = "text" id = "formula" name = "formula" value = "{raw}">
        </form>
        <p>Formula: {getp}</p>
        <p> Gröbner-Basis: {basis}</p>
        <p>Wahr: {ev} </p>
        </div>
        """.format(raw = formula, getp = parsed, basis = basis, ev = ev, cls = suc_class))
    except Exception as err:
        return wrap("""
        <h1>An error occured</h1>
        <form action = "/">
        <input style="width:800px" type = "text" id = "formula" name = "formula" value = "{raw}">
        </form>
        <p>
        {err}
        <p>
        """.format(raw = formula, err = err))
if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
