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

# string to evaluate
STRING = 'aabbbbbaabaaaaaaaabb'

# Regex expression
#REGEX = '(a|b)*((a|(bb))*ε)'
#REGEX = '(a|b)b'
#REGEX = '(a|b)a?'
#REGEX = '(aa|b)+'
#REGEX = '(a|b)*abb'
REGEX = '(a|b)*a(a|b)(a|b)'
#REGEX = '(0|1)1*(0|1)'
#REGEX = '(b|b)*abb(a|b)*'

## Syntax tree construction
# generate tree from regex
tree = SyntaxTree(OPERATORS, REGEX)


## Regex to NFA conversion (via Thompson)
# build NFA from generated tree
nfa = NFA(tree.symbols, tree)
nfa.thompson()

# graph resulting NFA
nfa.graph_automata()

time, result = nfa.simulate(STRING)

print("RESULTADO DE SIMULACION PARA NFA (Thompson)\n-> %s\n-> %.3f (ms)\n" % (result, time))


## NFA to DFA conversion (via Subset)
# instantiate DFA and call subset method 
dfa = DFA(nfa)
dfa.subset()

# graph resulting DFA
dfa.graph_automata(mapping=dfa.state_mapping)

time, result = dfa.simulate(STRING)

print("RESULTADO DE SIMULACION PARA DFA (Subconjuntos)\n-> %s\n-> %.3f (ms)\n" % (result, time))


## Regex to DFA using direct method
# tree for direct build
hash_tree = SyntaxTree(OPERATORS, REGEX + "#", direct=True)

# get nodes for computing nullable, firstpos, lastpos and followpos
print(hash_tree.traverse_postorder(hash_tree.root))
nodes = hash_tree.traverse_postorder(hash_tree.root, full=True)

# instantiate dfa object
direct_dfa = DFA(syntax_tree=hash_tree, direct=True, nodes=nodes)

# call direct method
direct_dfa.direct()

# graph resulting DFA
direct_dfa.graph_automata(mapping=direct_dfa.state_mapping)

time, result = direct_dfa.simulate(STRING)

print("RESULTADO DE SIMULACION PARA DFA (Directo)\n-> %s\n-> %.3f (ms)\n" % (result, time))