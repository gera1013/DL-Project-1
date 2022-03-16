from automatas import NFA
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
#REGEX = '(a|b)a?'
REGEX = '(aa|b)+'


tree = SyntaxTree(OPERATORS, REGEX)
nfa = NFA(tree.symbols, tree)

nfa.thompson()