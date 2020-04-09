import random
#from generator import MOE_Generator
from moe import *
from algebra import *
from functools import reduce

class FilteredMOEGenerator:
    '''
    Class for using the MOE_Generator to generate MOEs and filter out those that don't satisfy certain conditions.
    
    '''
    def __init__(self, max_history:int=2, max_f_depth:int=3, must_start_with_IV:bool=False, must_have_chaining:bool=False):
        self.max_history = max_history #maximum x for every i-x
        self.max_f_depth = max_f_depth #maximum number of nested f's
        self.must_start_with_IV = must_start_with_IV
        self.must_have_chaining = must_have_chaining
        self.memo = [] #stores all previous valid MOEs
        self.filtered_it=self._construct_iter()
    
    '''recursively check f nestings'''
    def _check_f_depth(self, t, depth_level=0):
        if isinstance(t, Variable) or isinstance(t, Constant) or isinstance(t, Function):
            return depth_level
        max_depth = 0
        for ti in t.arguments:
            max_depth = max(max_depth, depth(ti, depth_level + int(t.symbol == "f")))
        return max_depth
    
    '''check chaining'''
    def _satisfies_chaining(self, term):
        if not self.must_have_chaining:
            return True
        for a in range(self.max_history):
            if Variable("C_{i-" + str(a+1) + "}") in term:
                return True
        return False
    
    '''Retrieve the next valid MOE and store it in the memo'''
    def __next__(self):
        next_moe = next(self.filtered_it)
        self.memo.append(next_moe)
        return next_moe
    
    '''
    Construct the filtered iterable that generates new MOEs
    This is its own function just in case it needs to be called in multiple places, but that seems unlikely.
    '''
    def _construct_iter(self):
        #make functions to put in filter to generate iterable
        #function for checking if an moe starts with the IV
        c_iv = lambda t : (Constant("r") in t) if self.must_start_with_IV else True
        #function that checks if you've seen it before
        c_not_seen = lambda t: (t not in self.memo)
        #combined conditions
        conditions = lambda t : c_not_seen(t) and c_iv(t) and self._satisfies_chaining(t)  and self._check_f_depth(t) <= self.max_f_depth
        return iter(filter(conditions, MOE_Generator(self.max_history)))





