from automatas import NFA, DFA
from structures import SyntaxTree

# operators and precedence
OPERATORS = {
    '|': 1,
    '^': 2,
    '*': 3,
    '?': 3,
    '+': 3
}

# epsilon char
EPSILON = 'ε'

# Regex expression
#REGEX = '(a|b)*((a|(bb))*ε)'
#REGEX = '(a|b)b'
#REGEX = '(a|b)a?'
#REGEX = '(aa|b)+'
#REGEX = '(a|b)*abb'
#REGEX = '(a|b)*a(a|b)(a|b)'
REGEX = '(0|1)1*(0|1)'

## Syntax tree construction
# generate tree from regex
tree = SyntaxTree(OPERATORS, REGEX)


## Regex to NFA conversion (via Thompson)
# build NFA from generated tree
nfa = NFA(tree.symbols, tree)
nfa.thompson()

# graph resulting NFA
nfa.graph_automata()


## NFA to DFA conversion (via Subset)
# instantiate DFA and call subset method 
dfa = DFA(nfa)
dfa.subset()

# graph resulting DFA
dfa.graph_automata(mapping=dfa.state_mapping)


## Regex to DFA using direct method
# tree for direct build
hash_tree = SyntaxTree(OPERATORS, REGEX + "#", direct=True)

# get nodes for computing nullable, firstpos, lastpos and followpos
nodes = hash_tree.traverse_postorder(hash_tree.root, full=True)

# instantiate dfa object
direct_dfa = DFA(syntax_tree=hash_tree, direct=True, nodes=nodes)

# call direct method
direct_dfa.direct()

# graph resulting DFA
direct_dfa.graph_automata(mapping=direct_dfa.state_mapping)