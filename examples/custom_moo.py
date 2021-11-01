#Table 2
##MOO One 

###Import the Libraries
from symcollab.moe.generator import MOOGenerator
from symcollab.moe.custom import CustomMOO
from symcollab.moe.check import moo_check
from symcollab.Unification.constrained.p_unif import p_unif
from symcollab.algebra import *
from symcollab.xor import *

###Create the variables for the MOO Def
P = Variable("P[i]")
C1 = Variable("C[i-1]")
f =Function("f", 1)

###Create the recursive Def
t = xor(f(xor(P, f(C1))), f(C1))
###Check the def 
print(t)

###Use the CustomMOO() function to create the base case
tm = CustomMOO(t)

###Run the security check
M=moo_check(tm.name, 'every', XOR_rooted_security, 3, True, True)

###Check Results
M.secure

############################################################
##MOO Two

###Import the Libraries
from symcollab.moe.generator import MOOGenerator
from symcollab.moe.custom import CustomMOO
from symcollab.moe.check import moo_check
from symcollab.Unification.constrained.p_unif import p_unif
from symcollab.algebra import *
from symcollab.xor import *

###Create the variables for the MOO Def
P = Variable("P[i]")
C1 = Variable("C[i-1]")
f =Function("f", 1)

###Create the recursive Def
t = f(xor(xor(P, f(C1)), f(P)))
###Check the def 
print(t)

###Use the CustomMOO() function to create the base case
tm = CustomMOO(t)

###Run the security check
M=moo_check(tm.name, 'every', p_unif, 3, True, True)


###Check Results
M.secure

############################################################
##MOO Three

###Import the Libraries
from symcollab.moe.generator import MOOGenerator
from symcollab.moe.custom import CustomMOO
from symcollab.moe.check import moo_check
from symcollab.Unification.constrained.p_unif import p_unif
from symcollab.algebra import *
from symcollab.xor import *

###Create the variables for the MOO Def
P = Variable("P[i]")
C1 = Variable("C[i-1]")
f =Function("f", 1)

###Create the recursive Def
t = xor(f(xor(f(P), C1)),f(xor(f(P), f(C1))))
###Check the def 
print(t)

###Use the CustomMOO() function to create the base case
tm = CustomMOO(t)

###Run the security check
M=moo_check(tm.name, 'every', XOR_rooted_security, 3, True, True)

###Check Results
M.secure

