from automatas import NFA, DFA
from structures import SyntaxTree

OPERATORS = {
    '|': 1,
    '^': 2,
    '*': 3,
    '?': 3,
    '+': 3
}

EPSILON = 'ε'

#REGEX = '(a|b)*((a|(bb))*ε)'
#REGEX = '(a|b)b'
#REGEX = '(a|b)a?'
#REGEX = '(aa|b)+'
REGEX = '(a|b)*abb'
#REGEX = '(a|b)*a(a|b)(a|b)'
#REGEX = '(0|1)1*(0|1)'

# generate tree from regex
#tree = SyntaxTree(OPERATORS, REGEX)

# build NFA from generated tree (via Thompson)
#nfa = NFA(tree.symbols, tree)
#nfa.thompson()

#nfa.graph_automata()

# convert NFA to DFA (via Subset)
#dfa = DFA(nfa)
#dfa.subset()

#dfa.graph_automata(mapping=dfa.state_mapping)

# tree for direct build
hash_tree = SyntaxTree(OPERATORS, REGEX + "#", direct=True)
nodes = hash_tree.traverse_postorder(hash_tree.root, full=True)

direct_dfa = DFA(syntax_tree=hash_tree, direct=True, nodes=nodes)

direct_dfa.direct()

direct_dfa.graph_automata(mapping=direct_dfa.state_mapping)