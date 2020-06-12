@builtin "number.ne" 
imp -> conj "==>" disj
conj -> rel "/\\" conj
conj -> rel
disj -> eq "\\/" disj
rel -> ineq | eq
ineq -> term "/=" term
eq -> term "=" term
term -> sum
sum -> product
sum -> sum "+" product
sum -> sum "-" product
product -> atom
product -> product "*" atom
product -> product "/" int
atom -> int
atom -> "-" atom
atom -> [a-z]
atom -> "(" sum ")"
atom -> atom "^" int