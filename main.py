from automatas import NFA, DFA
from structures import SyntaxTree

OPERATORS = {
    '|': 1,
    '^': 2,
    '*': 3,
    '?': 3,
    '+': 3
}

#REGEX = '(a|b)*((a|(bb))*e)'
#REGEX = '(a|b)b'
REGEX = '(a|b)a?'
#REGEX = '(aa|b)+'


# generate tree from regex
tree = SyntaxTree(OPERATORS, REGEX)

# build NFA from generated tree (via Thompson)
nfa = NFA(tree.symbols, tree)
nfa.thompson()

# convert NFA to DFA (via Subset)
dfa = DFA(nfa)
dfa.subset()
