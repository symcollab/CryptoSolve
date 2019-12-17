#E_AC unification 
#cite the E_AC paper

#############################################
#Theory:                                    #
#                                           #
# exp(exp(x, y), z) = exp(x, f(y, z))       #
# exp(g(x, y), z) = g(exp(x, z), exp(y, z)) #
# f is AC                                   #
#############################################

#!/usr/bin/env python3
from algebra import *
from Unification import *
from itertools import combinations


def eac_unif(U: set):
	
	
	var_count = [0]
	
	#First call flat
	U2 = flat(U)
	
	#Get the set of variables from the equations
	var_set = set()
	for e in U2:
		var_set = var_set.union(get_vars(e.left_side))
		var_set = var_set.union(get_vars(e.right_side))
	
	#print(var_set)
	#Generate the set of partitions 
	#To-Do
	
	
	
	
	#################################################
	# Composite Rules                               #
	#################################################
	
	#rule c1, i*a*
	Utemp = set()
	while Utemp != U2:
		Utemp = U2
		U2 = rule_i(U2, var_count)
	
	Utemp = set()
	while Utemp != U2:
		Utemp = U2
		U2 = rule_a(U2)
	
	print(U2)
	
	#rule c2, [b + c + d]a*
	U2 = rule_b_c(U2)
	U2 = rule_d(U2)
	Utemp = set()
	while Utemp != U2:
		Utemp = U2
		U2 = rule_a(U2)
		
	print(U2)
	
	#rule c3, [b + c + d]*a*i*e[b + c + d]*a*
	U2 = rule_b_c(U2)
	U2 = rule_d(U2)
	
	Utemp = set()
	while Utemp != U2:
		Utemp = U2
		U2 = rule_a(U2)
		
	Utemp = set()
	while Utemp != U2:
		Utemp = U2
		U2 = rule_i(U2, var_count)
	
	U2 = rule_e(U2, var_count)
	
	Utemp = set()
	while Utemp != U2:
		Utemp = U2
		U2 = rule_b_c(U2)
		U2 = rule_d(U2)
	
	Utemp = set()
	while Utemp != U2:
		Utemp = U2
		U2 = rule_a(U2)
	
	print(U2)
	
	#rule c4, (i*[b + c + d]*a*)*(f + g + h)a*
	Utemp2 = set()
	while Utemp2 != U2:
		Utemp2 = U2
		Utemp = set()
		while Utemp != U2:
			Utemp = U2
			U2 = rule_i(U2, var_count)
		Utemp = set()
		while Utemp != U2:
			Utemp = U2
			U2 = rule_b_c(U2)
			U2 = rule_d(U2)
		Utemp = set()
		while Utemp != U2:
			Utemp = U2
			U2 = rule_a(U2)
	U2 = rule_f(U2, var_count)
	U2 = rule_g(U2)
	U2 = rule_h(U2, var_count)
	Utemp = set()
	while Utemp != U2:
		Utemp = U2
		U2 = rule_a(U2)
	
	
	
	################################################
	# Call AC-unification                          #
	################################################
	
	#first get just the f-terms
	f_terms = set()
	for e in U2:
		if isinstance(e.right_side, FuncTerm) and str(e.right_side.function) == "f":
			f_terms.add(e)
	print("F-terms")
	print(f_terms)
	delta = SubstituteTerm()
	
	#call ac-unif
	delta=ac_unify(f_terms)
	print(delta)
	
	
	return U2
	
def rule_a(U2: set):
	#Rule (a)
	for e in list(U2):
		if isinstance(e.right_side, Variable) and isinstance(e.left_side, Variable):
			sigma = SubstituteTerm()
			sigma.add(e.left_side, e.right_side)
			for e2 in list(U2):
				if (isinstance(e2.left_side, FuncTerm) or isinstance(e2.left_side, Variable)):
					e2.left_side = e2.left_side * sigma
				if (isinstance(e2.right_side, FuncTerm) or isinstance(e2.right_side, Variable)):
					e2.right_side = e2.right_side * sigma
			U2.remove(e)
	return U2
					
def rule_b_c(U2: set):
	#Rule (b) and (c)
	#exp terms with the same base or the same exp
	Uremove = set()
	Utemp = U2
	for e in list(U2):
		if isinstance(e.right_side, FuncTerm) and str(e.right_side.function) == "exp":
			Utemp = Utemp - {e}
			for e2 in list(Utemp):
				if isinstance(e2.right_side, FuncTerm):
					if e2.left_side == e.left_side and str(e2.right_side.function) == "exp" and e2 not in Uremove:
						if e.right_side.arguments[0] == e2.right_side.arguments[0]:
							# rule (b)
							print("In rule B")
							e3 = Equation(e.right_side.arguments[1], e2.right_side.arguments[1])
							U2.add(e3)
							U2 = U2 - {e2}
							Uremove.add(e2)
					else:
						if e.right_side.arguments[1] == e2.right_side.arguments[1]:
							# rule (c)
							print("In rule C")
							e3 = Equation(e.right_side.arguments[0], e2.right_side.arguments[0])
							U2.add(e3)
							U2 = U2 - {e2}
							Uremove.add(e2)
	return U2
	
	
def rule_d(U2: set):
	#Rule (d)
	#two g-terms
	Uremove=set()
	Utemp=set()
	Utemp = U2
	for e in list(U2):
		if isinstance(e.right_side, FuncTerm) and str(e.right_side.function) == "g":
			Utemp = Utemp - {e}
			for e2 in list(Utemp):
				if isinstance(e2.right_side, FuncTerm):
					if e2.left_side == e.left_side and str(e2.right_side.function) == "g" and e2 not in Uremove:
						e4 = Equation(e.right_side.arguments[1], e2.right_side.arguments[1])
						e5 = Equation(e.right_side.arguments[0], e2.right_side.arguments[0])
						U2.add(e4)
						U2.add(e5)
						Uremove.add(e2)
						
	return U2
	
	
	
def rule_e(U2: set, var_count):
	#Rule (e) 
	# exp and a g term
	Uremove=set()
	Utemp=set()
	Utemp = U2
	for e in list(U2):
		if isinstance(e.right_side, FuncTerm) and str(e.right_side.function) == "exp":
			for e2 in list(U2):
				if isinstance(e2.right_side, FuncTerm):
					if e2.left_side == e.left_side and str(e2.right_side.function) == "g" and e2 not in Uremove:
						#create three new equations
						var1 = str()
						var1 = 'v_'+str(var_count[0])
						var_count[0] = var_count[0] + 1
						var2 = str()
						var2 = 'v_'+str(var_count[0])
						var_count[0] = var_count[0] + 1
						var1 = Variable(var1)
						var2 = Variable(var2)
						t1 = FuncTerm(e2.right_side.function, [var1, var1])
						t2 = FuncTerm(e.right_side.function, [var1, e.right_side.arguments[1]])
						t3 = FuncTerm(e.right_side.function, [var2, e.right_side.arguments[1]])
						add1 = Equation(e.right_side.arguments[0], t1)
						add2 = Equation(e2.right_side.arguments[0], t2)
						add3 = Equation(e2.right_side.arguments[1], t3)
						U2.add(add1)
						U2.add(add2)
						U2.add(add3)
						Uremove.add(e2)
						U2.remove(e2)
	return U2
	
def rule_i(U2: set, var_count):
	#Rule (i), fourth of 4 exp = exp rules
	Uremove=set()
	U3=Utemp=set()
	Utemp=U3=U2
	for e in list(U2):
		if isinstance(e.right_side, FuncTerm) and str(e.right_side.function) == "exp":
			U3 = U3 - {e}
			for e2 in list(U3):
				if isinstance(e2.right_side, FuncTerm):
					if e2.left_side != e.left_side and str(e2.right_side.function) == "exp" and e2 not in Uremove:
						#create three new equations
						F = Function("f", 2)
						var1 = str()
						var1 = 'v_'+str(var_count[0]) 
						var_count[0] = var_count[0] + 1
						var1 = Variable(var1) #Z
						t1 = FuncTerm(e.right_side.function, [e2.right_side.arguments[0], var1])
						t2 = FuncTerm(F, [e2.right_side.arguments[1], e.right_side.arguments[1]])
						add1 = e2
						add2 = Equation(e.left_side, t1)
						add3 = Equation(var1, t2)
						Utemp.add(add1)
						Utemp.add(add2)
						Utemp.add(add3)
						Uremove.add(e2)
						Uremove.add(e)
						#U2.remove(e2)
						U2.remove(e)
	U2 = U2.union(Utemp)
	return U2
	
def rule_f(U2: set, var_count):
	#Rule (f), first of 4 exp = exp rules
	Uremove=set()
	U3=Utemp=set()
	Utemp=U3=U2
	print(U2)
	for e in list(U2):
		if isinstance(e.right_side, FuncTerm) and str(e.right_side.function) == "exp":
			U3 = U3 - {e}
			for e2 in list(U3):
				if isinstance(e2.right_side, FuncTerm):
					if e2.left_side == e.left_side and str(e2.right_side.function) == "exp" and e2 not in Uremove:
						#create three new equations
						F = Function("f", 2)
						var1 = str()
						var1 = 'v_'+str(var_count[0]) 
						var_count[0] = var_count[0] + 1
						var1 = Variable(var1) #Z
						t1 = FuncTerm(F, [var1, e.right_side.arguments[1]])
						t2 = FuncTerm(e.right_side.function, [e2.right_side.arguments[0], var1])
						add1 = e2
						add2 = Equation(e2.right_side.arguments[1], t1)
						add3 = Equation(e.right_side.arguments[0], t2)
						Utemp.add(add1)
						Utemp.add(add2)
						Utemp.add(add3)
						Uremove.add(e2)
						Uremove.add(e)
						#U2.remove(e2)
						U2.remove(e)
	U2 = U2.union(Utemp)
	return U2
	
def rule_h(U2: set, var_count):
	#Rule (h), third of 4 exp = exp rules
	Uremove=set()
	U3=Utemp=set()
	Utemp=U3=U2
	for e in list(U2):
		if isinstance(e.right_side, FuncTerm) and str(e.right_side.function) == "exp":
			U3 = U3 - {e}
			for e2 in list(U3):
				if isinstance(e2.right_side, FuncTerm):
					if e2.left_side == e.left_side and str(e2.right_side.function) == "exp" and e2 not in Uremove:
						#create three new equations
						u=e2.left_side
						F = Function("f", 2)
						var1 = str()
						var1 = 'v_'+str(var_count[0]) 
						var_count[0] = var_count[0] + 1
						var2 = str()
						var2 = 'v_'+str(var_count[0])
						var_count[0] = var_count[0] + 1
						var3 = str()
						var3 = 'v_'+str(var_count[0])
						var_count[0] = var_count[0] + 1
						var4 = str()
						var4 = 'v_'+str(var_count[0])
						var_count[0] = var_count[0] + 1
						var1 = Variable(var1) #W'
						var2 = Variable(var2) #Y'
						var3 = Variable(var3) #Z
						var4 = Variable(var4) #L
						t1 = FuncTerm(e.right_side.function, [var3, var4])
						t2 = FuncTerm(e.right_side.function, [var3, var2])
						t3 = FuncTerm(e.right_side.function, [var3, var1])
						t4 = FuncTerm(F, [e.right_side.arguments[1], var2])
						t5 = FuncTerm(F, [e2.right_side.arguments[1], var1])
						add1 = Equation(u, t1)
						add2 = Equation(e.right_side.arguments[0], t2)
						add3 = Equation(e2.right_side.arguments[0], t3)
						add4 = Equation(var4, t4)
						add5 = Equation(var4, t5)
						Utemp.add(add1)
						Utemp.add(add2)
						Utemp.add(add3)
						Utemp.add(add4)
						Utemp.add(add5)
						Uremove.add(e2)
						Uremove.add(e)
						U2.remove(e2)
						U2.remove(e)
	U2 = U2.union(Utemp)
	return U2
	
def rule_g(U2: set):
	#Rule (g), second of 4 exp = exp rules
	Utemp=set()
	Utemp = U2
	Uremove=set()
	for e in list(U2):
		if isinstance(e.right_side, FuncTerm) and str(e.right_side.function) == "exp":
			Utemp = Utemp - {e}
			for e2 in list(Utemp):
				if isinstance(e2.right_side, FuncTerm):
					if e2.left_side == e.left_side and str(e2.right_side.function) == "exp" and e2 not in Uremove:
						e4 = Equation(e.right_side.arguments[1], e2.right_side.arguments[1])
						e5 = Equation(e.right_side.arguments[0], e2.right_side.arguments[0])
						U2.add(e4)
						U2.add(e5)
						Uremove.add(e2)
						U2.remove(e2)
	return U2



