"""
UNFINISHED
An implementation of Algebraic Fields. This module can use some rework
to utilize the sort attribute in the algebra module.

See nat.py for a more modern take of implementing a theory.
"""
from algebra import Constant, Function, Term, Variable
from rewrite import RewriteRule, RewriteSystem, normal
from .rings import Ring

# TODO: Capture the commutative property of addition & multiplication
# TODO: Make sure zero is noninvertible

class Field:
    """
    A field is a ring with every nonzero element
    having a multiplicative inverse.
    """
    @staticmethod
    def create_rules(add: Function, mul: Function, negation: Function, inverse: Function, zero: Constant, unity: Constant):
        """Create the set of rewrite rules that characterizes an algebraic field."""
        x = Variable("x") ; y = Variable("y") ; z = Variable("z")
        # Union Ring rules and new ring rules
        return Ring.create_rules(add, mul, negation, zero) | {
            ## One and Zero
            # 1 * 0 -> 0
            RewriteRule(mul(unity, zero), zero),
            # 0 * 1 -> 0
            RewriteRule(mul(zero, unity), zero),
            # 1 + 0 -> 1
            RewriteRule(add(unity, zero), unity),
            # 0 + 1 -> 1
            RewriteRule(add(zero, unity), unity),
            ## Unity Rules
            # 1 * x → x
            RewriteRule(mul(unity, x), x),
            # x * 1 → x
            RewriteRule(mul(x, unity), x),
            # -1 * x → -x
            RewriteRule(mul(negation(unity), x), negation(x)),
            # x * -1 → -x
            RewriteRule(mul(x, negation(unity)), negation(x)),
            # x * i(x) → 1
            RewriteRule(mul(x, inverse(x)), unity),
            # i(x) * x → 1
            RewriteRule(mul(inverse(x), x), unity),
            ## Inverse Rules
            # i(i(x)) → x
            RewriteRule(inverse(inverse(x)), x),
            # i(x * y) → i(y) * i(x)
            RewriteRule(inverse(mul(x, y)), mul(inverse(y), inverse(x))),
            ## Interplay between associativity and inverses
            # x * (i(x) * y) → y
            RewriteRule(mul(x, mul(inverse(x), y)), y),
            # i(x) * (x * y) → y
            RewriteRule(mul(inverse(x), mul(x, y)), y)
        }

    def __init__(self, add: Function, mul: Function, negation: Function, inverse: Function, zero: Constant, unity: Constant):
        self.add = add
        self.mul = mul
        self.inverse = inverse
        self.negation = negation
        self.zero = zero
        self.unity = unity
        self.rewrite_rules = Field.create_rules(add, mul, negation, inverse, zero, unity)

    def normal(self, element: Term):
        """Normal form of a field term."""
        return normal(element, RewriteSystem(self.rewrite_rules))
