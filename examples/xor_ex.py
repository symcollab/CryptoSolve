#!/usr/bin/env python3
from symcollab.algebra import *
from symcollab.xor import *

a = Constant("a")
b = Constant("b")
c = Constant("c")
x = Variable("x")
y = Variable("y")
z = Variable("z")

print("xor(a,b,x,x,y,a,c) =", end = " ")
print(xor(a, b, x, x, y, a, c))