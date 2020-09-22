"""
This module is responsible for rewrite systems,
a set of rewrite rules and operations on them.
"""
from copy import deepcopy
from typing import Set, Optional
from algebra import Term
from .rule import RewriteRule

__all__ = ['RewriteSystem', 'normal']

class RewriteSystem:
    """
    A set of rewrite rules.
    Used primarily to hold properties of a rewrite system.
    """
    def __init__(self, rules: Set[RewriteRule]):
        self.rules = rules

    def append(self, rule):
        """Add a single rule to the rewrite system"""
        self.rules.append(rule)

    def extend(self, system):
        """Add a list of rules to a rewrite system"""
        self.rules.extend(system.rules)

    def __iter__(self):
        return iter(self.rules)

    def __repr__(self):
        if len(self.rules) == 0:
            return "{}"
        if len(self.rules) == 1:
            return "{ %s }" % (str(self.rules[0]))
        str_repr = "{\n"
        i = 1
        for i, rule in enumerate(self.rules):
            str_repr += "  " + str(rule)
            str_repr += ",\n" if i < len(self.rules) else ""
            i += 1
        str_repr += "\n}"
        return str_repr

def normal(element: Term, rewrite_rules: RewriteSystem, bound: int = -1) -> Optional[Term]:
    """
    Returns the normal form of an element
    given a set of convergent term rewrite rules.

    Notes
    -----
    If the set of rewrite rules aren't convergent,
    then it is possible that this function won't terminate.

    Parameters
    ----------
    element : Term
      The term to check the normal form for.
    rewrite_rules : RewriteSystem
      Possible rules to apply.
    bound : int
      Applies up to 'bound' rewrite rules. Set to -1 in order to have no bound.
    """
    element = deepcopy(element)
    element_changed = True
    iteration = 0
    # We keep on going until the element stops changing
    while element_changed:
        element_changed = False
        # Check to see if we went passed our bound
        if bound != -1 and iteration > bound:
            return None

        # Apply the first rewrite rule that works
        for rule in rewrite_rules:
            new_elements = rule.apply(element)
            if new_elements is not None:
                element = next(iter(new_elements.values()))
                element_changed = True
                break
        iteration += 1

    return element
