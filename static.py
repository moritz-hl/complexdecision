
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
<li> <a href = "http://localhost:5000/?formula=a*c+%3D+1%2Bb+%2F%5C+b*d+%3D+1%2Bc+%2F%5C+c*e+%3D+1%2Bd+%2F%5C+d*f+%3D+1%2Be+%2F%5C+a+%2F%3D+0+%2F%5C+b+%2F%3D+0+%2F%5C+c%2F%3D+0+%2F%5C+d+%2F%3D+0%3D%3D%3E+a+%3D+f">Period = 5</a>
<li> <a href = "/?formula=a*x+%3D+0+%3D%3D>+a+%3D+0+%5C%2F+x+%3D+0">Integral I</a>
<li> <a href = "/?formula=a*x+%3D+0++%2F%5C+a+%2F%3D+0+%3D%3D>+x+%3D+0">Integral II</a>
<li> <a href = "/?formula=x%5E5%2Bx%5E4%2B1%3D0+%3D%3D>+x%5E2%2Bx%2B1+%3D+0+%5C%2F+x%5E3-x%2B1+%3D+0">Factor </a>
<li> <a href = "/?formula=x+%3D+0++%3D%3D>++x+%3D+1">non-sense</a>

</ul>
<a href = "/railroad.html">Syntax</a>
</div>
<script src = "app.js"></script>
</body>
</html>
"""

def wrap(content):
    return header + content + footer

def pos_out(suc_class, formula, basis, ev):
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

def err_out(formula, err):
    return wrap("""
        <form action = "/">
        <input style="width:800px" type = "text" id = "formula" name = "formula" value = "{raw}">
        </form>
        <p>
        {err}
        <p>
        """.format(raw = formula, err = err))