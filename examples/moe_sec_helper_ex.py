"""
Examples from Hai's presentation on May 23rd 2020
"""
from algebra import Function, Variable, Constant
from xor import xor
from xor.structure import Zero
from moe.moe_sec_helper import moe_syntactic_condition, moe_syn_security, \
    moe_has_random, moe_f_depth


f = Function("f", 1)
r = Constant("r")
x = Variable("x")
x2 = Variable("x2")
zero = Zero()


print("Example 1.")
t1 = moe_f_depth(
    f(f(r))
)
print(f"f_depth(f(f(r))) = {t1}")
print("")


print("Example 2.")
t2 = moe_f_depth(
    xor(
        f(f(r)),
        f(r)
    )
)
print(f"f_depth(f(f(r)) ⊕ f(r)) = {t2}")
print("")


print("Example 3.")
possible_subs1 = dict()
possible_subs1[x] = [r, f(r)]
t3 = moe_f_depth(
    xor(f(r), x),
    possible_subs1
)
print(f"If {x} maps to {r} or {f(r)}...")
print(f"f_depth(f(r) ⊕ x) = {t3}")
print("")


print("Example 4.")
possible_subs2 = dict()
possible_subs2[x] = [r, zero]
t4 = moe_f_depth(
    xor(f(r), x),
    possible_subs2
)
print(f"If {x} maps to {r} or {zero}...")
print(f"f_depth(f(r) ⊕ x) = {t4}")
print("")


print("Example 5.")
possible_subs3 = dict()
possible_subs3[x] = [r]
possible_subs3[x2] = [r, f(zero)]
t5 = moe_f_depth(
    xor(
        f(xor(
            f(zero),
            x,
            r
        )),
        x2
    ),
    possible_subs3
)
print(f"If {x} maps to {r}")
print(f"and {x2} maps to {r} and {f(zero)}...")
print(f"f_depth(f(f(0) ⊕ x1 ⊕ r) ⊕ x2) = {t5}")
print("")


print("Example 6.")
t6 = moe_has_random(f(r))
print(f"has_randomness(f(r)) is {t6}")
print("")


print("Example 7.")
t7 = moe_has_random(xor(f(r), f(r)))
print(f"has_randomness(f(r) ⊕ f(r)) is {t7}")
print("")


print("Example 8.")
possible_subs4 = dict()
possible_subs4[x] = [r, f(r)]
t7 = moe_has_random(
    xor(f(r), x),
    possible_subs4
)
print(f"If {x} maps to {r} or {f(r)}...")
print(f"has_randomness(f(r) ⊕ x) is {t7}")
print("")


print("Example 9.")
possible_subs5 = dict()
possible_subs5[x] = [r, zero]
t9 = moe_has_random(
    xor(f(r), x),
    possible_subs5
)
print(f"If {x} maps to {r} or {zero}...")
print(f"has_randomness(f(r) ⊕ x) is {t9}")
print("")


print("Example 10.")
last_block1 = r
block1 = xor(
    f(f(last_block1)),
    x
)
t10 = moe_syntactic_condition(last_block1, block1)
print(f"satisfies_syn_cond(f(f(C[i-1])) ⊕ x) is {t10}")
print("")


print("Example 11.")
last_block2 = r
block2 = f(
    xor(
        f(last_block2),
        x
    )
)
t11 = moe_syntactic_condition(last_block2, block2)
print(f"satisfies_syn_cond(f( f(C[i-1]) ⊕ x )) is {t11}")
