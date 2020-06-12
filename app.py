from flask import Flask
from flask import request
from datetime import datetime
from sympy import symbols, groebner
from lark import Lark, Transformer, v_args

app = Flask(__name__, static_url_path = "", static_folder="static")

header = r"""
<!DOCTYPE html>
<html>
<head>
<title>Gröbner Basis</title>
<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css" integrity="sha384-9aIt2nRpC12Uk9gS9baDl411NQApFmC26EwAOH8WgZl5MYYxFfc+NcPb1dKGj7Sk" crossorigin="anonymous">
<link rel = "stylesheet" href = "./style.css">
</head>
<body>
<div id = "wrapper">
<h1>&#x2102;omplex Decisions</h1>
"""

footer = r"""
<h2>Examples</h2>
<ul>
<li> <a href = "/?formula=x+%3D+2+%2F%5C+y+%3D+3+%3D%3D>+x+%2B+y+%3D+5">2+3 = 5</a>
<li> <a href = "/?formula=a%5E2+%3D+2+%2F%5C+x%5E2%2Ba*x+%2B+1+%3D+0+%3D%3D>+x%5E4+%2B+1+%3D+0">Complex Roots</a>
<li> <a href = "/?formula=a*x%5E2%2Bb*x%2Bc+%3D+0+%2F%5C+a*y%5E2%2Bb*y%2Bc+%3D+0+%2F%5C+x+%2F%3D+y+%3D%3D>+a*x*y+%3D+c">Vieta I</a>
<li> <a href = "/?formula=a*x%5E2%2Bb*x%2Bc+%3D+0+%2F%5C+a*y%5E2%2Bb*y%2Bc+%3D+0+%2F%5C+x+%2F%3D+y+%3D%3D>+a*%28x%2By%29+%3D+-b">Vieta II</a>
<li> <a href = "/?formula=a*c+%3D+1%2Bb+%2F%5C+b*d+%3D+1%2Bc+%2F%5C+c*e+%3D+1%2Bd+%2F%5C+d*f+%3D+1%2Be+%2F%5C+a+%2F%3D+0+%2F%5C+b+%2F%3D+0+%3D%3D>+a+%3D+f">Period = 5</a>
<li> <a href = "/?formula=a*x+%3D+0+%3D%3D>+a+%3D+0+%5C%2F+x+%3D+0">Integral I</a>
<li> <a href = "/?formula=a*x+%3D+0++%2F%5C+a+%2F%3D+0+%3D%3D>+x+%3D+0">Integral II</a>
<li> <a href = "/?formula=x%5E5%2Bx%5E4%2B1%3D0+%3D%3D>+x%5E2%2Bx%2B1+%3D+0+%5C%2F+x%5E3-x%2B1+%3D+0">Factor </a>
<li> <a href = "/?formula=x+%3D+0++%3D%3D>++x+%3D+1">non-sense</a>

</ul>
</div>
<script src = "app.js"></script>
</body>
</html>
"""


def wrap(content):
    return header + content + footer




calc_grammar = r"""
    imp:  conj "==>" disj -> imp
    conj: [rel ("/\\" rel)*] -> conj
    disj: [eq ("\\/" eq)*] -> disj
    ?rel : ineq
        | eq
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

    univ_parser = Lark(calc_grammar, parser='lalr', transformer=transformer, start = "imp")

    formula = request.args.get("formula")

    if formula == "":
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
        return wrap(f"""
       
<div id = "result" class = "{suc_class}">
<form action = "/">
    <div>
<div id = "quant">&#x2200; <span id = "qvars"></span> .
</div>
<div id = "input"><input type = "text" id = "formula" name = "formula" value = "{formula}"></div>
</div>
</form>
<p> Gröbner-Basis: {basis}</p>
<h1>{ev}</h1>
</div>
        """)
    except Exception as err:
        return wrap("""
        <form action = "/">
        <input style="width:800px" type = "text" id = "formula" name = "formula" value = "{raw}">
        </form>
        <p>
        {err}
        <p>
        """.format(raw = formula, err = err))
if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
