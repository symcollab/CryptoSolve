"""
Module used to create custom modes of operation.
"""
from algebra import Constant, SubstituteTerm, get_vars
from .moo import MOO

__all__ = ['CustomMOO']

class CustomMOO:
    """Create and register a custom mode of operation from a term."""
    def __init__(self, term):
        self.term = term
        self.name = str(term)
        MOO.register(self.name, self.__call__)

    def __call__(self, iteration, nonces, P, C):
        IV = nonces[0]
        i = iteration - 1
        # Create substitution between symbolic plain and cipher texts
        # and the symbolic instantiations of them in MOESession
        sigma = SubstituteTerm()
        subterms = get_vars(self.term)
        for subterm in subterms:
            if subterm.symbol[0] == "P":
                if '-' not in subterm.symbol:
                    # Assume we mean current plaintext
                    sigma.add(subterm, P[-1])
                else:
                    j = int(subterm.symbol[4:-1])
                    if j > i:
                        # If we request for a cipher block that doesn't exist yet
                        # due to the current session length
                        # then map the subterm to a different nounce
                        sigma.add(subterm, Constant(IV.symbol + f"_{j}"))
                    else:
                        sigma.add(subterm, P[-j])
            elif subterm.symbol[0] == "C":
                j = int(subterm.symbol[5:-1])
                if j > i:
                    # If we request for a cipher block that doesn't exist yet
                    # due to the current session length
                    # then map the subterm to a different nounce
                    sigma.add(subterm, Constant(IV.symbol + f"_{j}"))
                else:
                    sigma.add(subterm, C[-j])
        return self.term * sigma
