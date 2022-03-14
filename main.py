from structures import SyntaxTree

OPERATORS = {
    '|': 1,
    '?': 1,
    '^': 2,
    '*': 3,
    '+': 3
}

# REGEX = '(a|b)*abb'
REGEX = '(a|b)*((a|(bb))*e)'


tree = SyntaxTree(OPERATORS, REGEX)

print(str(tree))