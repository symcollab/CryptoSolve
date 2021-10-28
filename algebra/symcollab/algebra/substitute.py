"""
This module is responsible for describing substitutions
which are mappings between variables and terms, as well
as the application of them.
"""
from typing import List, Set, Tuple
from copy import deepcopy
from .term import Variable, Constant, FuncTerm, Term

__all__ = ['SortMismatch', 'SubstituteTerm']

class SortMismatch(Exception):
    """Raise when there is a sort mismatch."""

class SubstituteTerm:
    """
    Represents a substitution from variables to terms.

    Examples
    --------
    >>> from symcollab.algebra import *
    >>> x = Variable("x")
    >>> a = Constant("a")
    >>> sigma = SubstituteTerm()
    >>> sigma.add(x, a)
    >>> x * sigma
    a
    """
    def __init__(self):
        self.subs: Set[Tuple[Variable, Term]] = set()

    def add(self, variable: Variable, term: Term):
        """
        Adds a mapping from a variable to a term

        Parameters
        ----------
        variable : Variable
            The variable to replace
        term : Term
            The term to replace the variable with.

        Examples
        --------
        >>> from symcollab.algebra import *
        >>> x = Variable("x")
        >>> a = Constant("a")
        >>> sigma = SubstituteTerm()
        >>> sigma.add(x, a)
        >>> print(sigma)
        { x -> a }
        """
        assert isinstance(variable, Variable)
        assert isinstance(term, Constant) or \
            isinstance(term, FuncTerm) or \
            isinstance(term, Variable)

        if variable.sort != term.sort:
            raise SortMismatch("Substitution must preserve sorts.")

        # Check to see if what we're adding already exists
        # in the substitution set
        for sub_var, sub_term in self.subs:
            if sub_var == variable and term != sub_term:
                raise ValueError(f"{variable} already exists in the substitution set")

        self.subs.add((variable, term))

    def remove(self, variable: Variable):
        """Removes a mapping from a variable"""
        # The removal technique consists of creating a set
        # that contains what you want to remove
        # and then do set subtraction
        to_remove = {}
        for sub_var, sub_term in self.subs:
            if sub_var == variable:
                to_remove = {(sub_var, sub_term)}
        self.subs = self.subs - to_remove

    def replace(self, variable: Variable, term: Term):
        """Replaces a mapping from a variable with another term"""
        assert isinstance(variable, Variable)
        assert isinstance(term, Constant) or \
            isinstance(term, FuncTerm) or \
            isinstance(term, Variable)
        self.remove(variable)
        # We don't have to call self.add as we already
        # ensured that the item is removed
        self.subs.add((variable, term))

    def domain(self) -> List[Variable]:
        """
        Grabs the domain (the left side) of the substitutions.

        Warning: Do not pair this call with range as ordering is not guarenteed.
        """
        return [m[0] for m in self.subs]

    def range(self) -> List[Term]:
        """
        Grabs the range (the right side) of the substitutions.

        Warning: Do not pair this call with domain as ordering is not guarenteed.
        """
        return [m[1] for m in self.subs]

    def __len__(self):
        return len(self.subs)

    def __deepcopy__(self, memo):
        subs = set()
        for variable, term in self.subs:
            new_variable = deepcopy(variable)
            new_term = deepcopy(term)
            subs.add((new_variable, new_term))
        subterm = SubstituteTerm()
        subterm.subs = subs
        return subterm

    def __str__(self):
        if len(self.subs) == 0:
            return "{}"
        if len(self.subs) == 1:
            variable, term = self.subs.pop()
            self.subs.add((variable, term))
            return "{ %s ↦ %s }" % (str(variable), str(term))
        str_repr = "{\n"
        i = 1
        if len(self.subs) < 9:
            sorted_subs = sorted(self.subs, key=lambda k: k[0].symbol)
            for variable, term in sorted_subs:
                str_repr += "  " + str(variable) + " ↦ " + str(term)
                str_repr += ",\n" if i < len(self.subs) else ""
                i += 1
        else:
            subs_str = self._subSort(self.subs)
            for string in subs_str:
                str_repr += string
                print(string)
                str_repr += ",\n" if i < len(self.subs) else ""
                i += 1
        str_repr += "\n}"
        return str_repr

    def _applysub(self, term: Term) -> Term:
        """Apply a substitution to a term"""
        assert isinstance(term, (Constant, Variable, FuncTerm))
        new_term = deepcopy(term)
        new_term = self._termSubstituteHelper(new_term)
        return new_term

    def __rmul__(self, term: Term) -> Term:
        return self._applysub(term)

    # Franz Baader and Wayne Snyder. Unification Theory. Handbook of Automated Reasoning, 2001.
    def __mul__(self, theta):
        """
        Combine two substitutions
        Source: Franz Baader and Wayne Snyder.
        Unification Theory. Handbook of Automated Reasoning, 2001
        """
        if not isinstance(theta, SubstituteTerm):
            raise ValueError(
                "Expected a substitution to the right of *, \
                perhaps you meant to apply substitution on a term? \
                If so, swap the arguments."
            )

        # If our substitution is empty, then return theta
        if len(self.subs) == 0:
            return deepcopy(theta)

        v, t = zip(*self.subs)
        # Apply theta to every term in its range
        t = tuple(map(theta, t))
        sigma1 = SubstituteTerm()
        sigma1.subs = set(zip(v, t))

        # Remove any binding x->t where x in Dom(sigma)
        theta1 = deepcopy(theta)
        theta_dom = theta1.domain()
        for vt in v:
            if vt in theta_dom:
                theta1.remove(vt)

        # Remove trival bindings
        for vt, tt in zip(v, t):
            if vt == tt:
                sigma1.remove(vt)

        # Union the two substitution sets
        result = SubstituteTerm()
        result.subs = sigma1.subs | theta1.subs
        return result

    def __call__(self, term: Term) -> Term:
        """Apply substitution to term."""
        return self._applysub(term)

    def _termSubstituteHelper(self, term: Term) -> Term:
        # If there is nothing in the substitution set, return the same term
        if len(self.subs) == 0:
            return term

        # Recurse down if term is a FuncTerm
        if isinstance(term, FuncTerm):
            new_arguments = [
                self._termSubstituteHelper(t)
                for t in term.arguments
            ]
            term.arguments = new_arguments
            return term

            # Note: Can't do the below because it simplifies with xor
            # which breaks some of the crypto procedures.
            # return term.function(*new_arguments)

        # If term is a variable in the substitution
        # then return its substitute
        if isinstance(term, Variable):
            for sub_var, sub_term in self.subs:
                if term == sub_var:
                    return deepcopy(sub_term)

        return term

    def _subSort(self, subs: Set) -> list:
        #creates an ordered list of formatted strings from the substitutions
        #only using this method when the list of substitions is longer than 9,
        #because thats where the issue occurs, everywhere else its fine
        unsorted_list = list(subs)
        sorted_list = [None] * len(subs)
        for variable, term in unsorted_list:
            var = str(variable)
            index = int(var[2:len(var)])
            sorted_list[index-1] = str(variable) + " ↦ " + str(term)
        return sorted_list




