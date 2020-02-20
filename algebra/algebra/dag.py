from .term import Term, FuncTerm, Function, Variable
import matplotlib.pyplot as plt # type: ignore
import networkx as nx # type: ignore
from typing import Dict, Tuple, Union

##
# Small Essay:
##
# A term DAG is a term that is represented by a directed acyclic graph.
# You can think of this as a tree. At the top of the tree is the outermost function/variable/constant
# For each argument that a function has, it will point an array from that function to the argument
# One of the goals of this sub-library is to have the structured be shared in the TermDAG such that every subterm only appears once.


#
## Directed Acyclic Graphs
#
class TermDAG:
    def __init__(self, term: Term):
        """Create a directed acyclic graph from a term"""
        # Our DAG is an ordered graph because the edges are directional
        # It is considered a MultiGraph due to our structured sharing. 
        # One of the consequences is that finding the parent of a node is ambiguous
        self.dag = nx.OrderedMultiGraph()
        self.term = term
        self.edge_labels : Dict[Tuple[Term, Term], str] = {}
        self.node_labels : Dict[Term, Union[Variable, Function]] = {}
        self.dag.add_node(term)
        # If the term we're starting out from is just a variable or constant, then we just make a single node graph
        # Otherwise, we'll need to start recursing down the arguments and add edges to each one...
        if isinstance(term, FuncTerm):
            self.node_labels[term] = term.function
            # Go through each of the arguments and add it to the graph
            for index, t in enumerate(term.arguments):
                self._appendTermDAG(term, t, edge_label = str(index))
        else:
            self.node_labels[term] = term

    def _appendTermDAG(self, last_term : Term, term : Term, edge_label = ""):
        # Annotate edges with argument number
        # If there is already a label, then append the new label
        if (last_term, term) in self.edge_labels and self.edge_labels[(last_term, term)] != edge_label:
            self.edge_labels[(last_term, term)] = self.edge_labels[(last_term, term)] + ", " + edge_label
        else:
            self.edge_labels[(last_term, term)] = edge_label
        
        self.dag.add_edge(last_term, term)
        if isinstance(term, FuncTerm):
            # Go through each of the function arguments and add a directed edge to it
            for index, t in enumerate(term.arguments):
                self._appendTermDAG(term, t, edge_label = str(index))
            self.node_labels[term] = term.function
        else:
            self.node_labels[term] = term

    def show(self):
        """Plot the directed acyclic graph of the TermDAG"""
        fig = plt.figure()
        pos = nx.spring_layout(self.dag)
        # The first node will be colored differently to signify the start of the DAG
        nx.draw(self.dag, pos, font_weight = 'bold', node_size = 600, font_size = 30, node_color = ['#a8c74d'] + ['#1f78b4' for i in range(len(self.dag.nodes) - 1)])
        # Add both the node labels and edge labels
        nx.draw_networkx_labels(self.dag, pos, labels = self.node_labels)
        nx.draw_networkx_edge_labels(self.dag, pos, edge_labels=self.edge_labels)
        fig.suptitle(self.term)
        plt.show()
    
    def df_edge_traversal(self):
        """Depth-first traversal of the edges"""
        return nx.dfs_edges(self.dag, source = list(self.dag.node)[0])
    def df_node_traversal(self):
        """Depth-first traversal of the nodes"""
        return nx.dfs_tree(self.dag, source = list(self.dag.node)[0])
    def bs_edge_traversal(self):
        """Breadth-first traversal of the edges"""
        return nx.bfs_edges(self.dag, source = list(self.dag.node)[0])
    def bs_node_traversal(self):
        """Breadth-frist traversal of the nodes"""
        return nx.bfs_tree(self.dag, source = list(self.dag.node)[0])
    
    def parents(self, term):
        """Parents of a term in the TermDAG"""
        if term in self.dag.node:
            return self.dag.predecessors(term)
        else:
            return []