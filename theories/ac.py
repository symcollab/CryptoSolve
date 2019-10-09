#!/usr/bin/env python3
import typing
from typing import Union, Any, Optional
from copy import deepcopy
from algebra import *
from collections import Counter
from rewrite import *

#
## Associative Functions
#

class AFunction(Function):
    def __init__(self, symbol : str, arity : int):
        assert arity > 0
        super().__init__(symbol, arity)
    def __call__(self, *args, simplify = True):
        term = ATerm(self, tuple(args[:self.arity]))
        for i in range(self.arity, len(args), self.arity - 1):
            l = args[i:(i + self.arity - 1)]
            term = ATerm(self, (term, *l))
        return term


def _flatten_sublist(l):
    new_list = []
    for li in l:
        if hasattr(li, '__iter__'):
            new_list.extend(li)
        else:
            new_list.append(li)
    return new_list

class ATerm(FuncTerm):
    def __init__(self, function : Function, args):
        super().__init__(function, args)
    def flatten(self):
        terms = []
        for t in self.arguments:
            if isinstance(t, ATerm) and t.function == self.function:
                sublist = list(map(lambda t: t.flatten() if isinstance(t, ATerm) else t, t.arguments))
                terms += _flatten_sublist(sublist)
            else:
                terms += [t]
        return terms
    def __eq__(self, x):
        return isinstance(x, ATerm) and self.function == x.function and self.flatten() == x.flatten()
    def __hash__(self):
        return super().__hash__()


#
## Commutative Functions
#

class CFunction(Function):
    def __init__(self, symbol : str, arity : int):
        super().__init__(symbol, arity)
    def __call__(self, *args):
        return CTerm(self, args)


class CTerm(FuncTerm):
    def __init__(self, function : Function, args):
        super().__init__(function, args)
    def __eq__(self, x):
        return isinstance(x, CTerm) and self.function == x.function and Counter(self.arguments) == Counter(x.arguments)
    def __hash__(self):
        return super().__hash__()

#
## Associative-Commutative Functions
#

class ACFunction(AFunction, CFunction):
    def __init__(self, symbol : str, arity : int):
        super().__init__(symbol, arity)
    def __call__(self, *args):
        term = ACTerm(self, tuple(args[:self.arity]))
        for i in range(self.arity, len(args), self.arity - 1):
            l = args[i:(i + self.arity - 1)]
            term = ACTerm(self, (term, *l))
        return term


class ACTerm(ATerm, CTerm):
    def __init__(self, function : Function, args):
        super().__init__(function, args)
    def __eq__(self, x):
        return isinstance(x, ACTerm) and self.function == x.function and Counter(self.flatten()) == Counter(x.flatten())
    def __hash__(self):
        return super().__hash__()

# 
## Idempotence Functions
#

class IFunction(Function):
    def __init__(self, symbol : str, arity : int):
        super().__init__(symbol, arity)
    def __call__(self, *args):
        term = ITerm(self, args)
        x = Variable("x")
        f = Function(self.symbol, self.arity)
        r = RewriteRule(f(x,x), x)
        return r.apply(term)


class ITerm(FuncTerm):
    def __init__(self, function : Function, args):
        super().__init__(function, args)
    def __eq__(self, x):
        return isinstance(x, ITerm) and self.function == x.function and self.arguments == x.arguments
    def __hash__(self):
        return super().__hash__()