import copy

import numpy as np
from queue import LifoQueue


class SyntaxTree(object):
    """
    CLASS SYNTAX TREE
    
    Una instancia de esta clase es capaz de recibir una expresión regular,
    y a partir de ella generar un árbol sintáctico según los operadores definidos.
    
    Params:
        -> operators (list): lista de operadores reconocidos por el árbol
        -> regex (string): expresión regular que genera un lenguaje
        -> root (Node): nodo raíz del árbol
    """
    def __init__(self, operators, regex, direct=False):
        ## language stuff
        self.operators = operators
        self.symbols = list(set([char for char in regex if char not in operators if char != '(' and char != ')']))
        self.regex = regex
        self.postfix = ""
        
        ## options
        self.direct = direct
        
        ## structure stuff
        self.root = None
        
        ## transformations to regex
        self.explicit_concat()
        self.to_postfix()
        direct and self.clean_postfix()
        self.build_tree()
        
        self.pos = 1
        
        
    def get_precedence(self, c):
        try:
            precedence = self.operators[c]
        except:
            precedence = 0
            
        return precedence;
    
    
    def explicit_concat(self):
        new_regex = ""
        for i in range(len(self.regex)):
            new_regex += self.regex[i]
            try:
                if (self.regex[i] in self.symbols and self.regex[i + 1] in self.symbols) \
                    or (self.regex[i] not in ['|', '('] and self.regex[i + 1] in self.symbols + ['(']):
                        new_regex += '^'
            except:
                pass
    
        self.regex = new_regex
        
        
    def clean_postfix(self):
        print(Colors.OKBLUE + "[INFO] " + Colors.ENDC + "Cleaning and refactoring postfix")
        new_postfix = ""
        
        for char in self.postfix:
            if char == '?':
                new_postfix += 'ε|'
                self.symbols.append('ε')
            else:
                new_postfix += char
        
        self.postfix = new_postfix
            
    
    
    def to_postfix(self):
        operator_stack = Stack()
        
        print(Colors.OKBLUE + "[INFO] " + Colors.ENDC + "Transforming regex to postfix")
        for char in self.regex:
            if char in self.symbols:
                self.postfix += char
                
            elif char == '(':
                operator_stack.push(char)
                
            elif char == ')':
                while operator_stack.top() != '(':
                    self.postfix += operator_stack.pop()
                    
                    if operator_stack.is_empty():
                        print(Colors.FAIL + "[ERROR] " + Colors.ENDC + "Error sintáctico, falta un paréntesis en la expresión")
                        exit()
                    
                    
                operator_stack.pop()
    
            else:
                while not operator_stack.is_empty():
                    top = operator_stack.top()
                    
                    top_precedence = self.get_precedence(top)
                    char_precedence = self.get_precedence(char)
                    
                    if (top_precedence >= char_precedence):
                        self.postfix += operator_stack.pop()
                    else:
                        break
                        
                operator_stack.push(char)
                
        while not operator_stack.is_empty():
            self.postfix += operator_stack.pop()
            
        print(Colors.OKBLUE + "[INFO] " + Colors.ENDC + "Postfix obtained: " + self.postfix)
                    
    
    def build_tree(self):
        tree_stack = Stack()
        
        print(Colors.OKBLUE + "[INFO] " + Colors.ENDC + "Building tree")
        for char in self.postfix:
            if char in self.symbols:
                tree_stack.push(Node(char))
            else:
                if char in ['*', '?', '+']:
                    if tree_stack.get_size() > 0:
                        if self.direct and char == '+':
                                a = tree_stack.pop()
                                a_copy = copy.deepcopy(a)
                                
                                kleene = Node('*', right=a_copy)
                                
                                concat = Node('^', right=kleene, left=a)
                                
                                a_copy.parent = kleene
                                kleene.parent = concat
                                a.parent = concat
                                
                                tree_stack.push(concat)
                        else:
                            right = tree_stack.pop()
                        
                            new = Node(char, right=right)
                        
                            right.parent = new
                        
                            tree_stack.push(new)
                    else:
                        print(Colors.FAIL + "[ERROR] " + Colors.ENDC + "Operación " + char + " incompleta, insuficientes parámetros")
                        exit()
                else:
                    if tree_stack.get_size() > 1:
                        right = tree_stack.pop()
                        left = tree_stack.pop()
                    
                        new = Node(char, right=right, left=left)
                    
                        right.parent = new
                        left.parent = new
                    
                        tree_stack.push(new)
                    else:
                        print(Colors.FAIL + "[ERROR] " + Colors.ENDC + "Operación CONCAT u OR incompleta, falta un símbolo")
                        exit()
        
        self.root = tree_stack.pop()
        
    
    def _height(self, node):
        if node is None:
            return 0
        else:
            return 1 + max(self._height(node.left), self._height(node.right))    
    
    
    def height(self):
        return self._height(self.root)
    
    
    def traverse_postorder(self, node, reachable=None, nodes=None, full=False):
        if not node:
            return
        
        if reachable is None:
            reachable = []
            
        if nodes is None:
            nodes = []
            
        self.traverse_postorder(node.left, reachable, nodes)
        self.traverse_postorder(node.right, reachable, nodes)
        
        reachable.append(node.data)
        nodes.append(node)
        
        if node.data in self.symbols:
            # define pos
            node.pos = self.pos
            self.pos += 1
            
            # define nullable
            if node.data == 'ε':
                node.nullable = True
            else:
                node.nullable = False
                
            # define first and last pos
            node.firstpos = [node.pos]
            node.lastpos = [node.pos]
            
        else:
            if node.data == '|':
                node.nullable = node.right.nullable or node.left.nullable
                
                node.firstpos = list(set(node.right.firstpos + node.left.firstpos))
                node.lastpos = list(set(node.right.lastpos + node.left.lastpos))
                
            elif node.data == '^':
                node.nullable = node.right.nullable and node.left.nullable
                
                node.firstpos = list(set(node.right.firstpos + node.left.firstpos)) if node.left.nullable else node.left.firstpos
                node.lastpos = list(set(node.right.lastpos + node.left.lastpos)) if node.right.nullable else node.right.lastpos
                
            elif node.data == '*':
                node.nullable = True
                node.firstpos = node.right.firstpos
                node.lastpos = node.right.lastpos
            
            else:
                pass
        
        return nodes if full else reachable 
    
    
    def __str__(self):
        if self.root is not None:
            self.print_tree(self.root)
            
        return ("")
            
    
    def print_tree(self, node):
        if node is not None:
            print(node.data)
            self.print_tree(node.left)
            self.print_tree(node.right)




class Node(object):
    """
    CLASS NODE
    
    Una clase nodo, almacena información de un nodo en un árbol binario.
    
    Params:
        -> parent (Node): nodo padre (si no tiene es un nodo raíz)
        -> left (Node): nodo hijo del lado izquierdo
        -> right (Node): nodo hijo del lado derecho
        -> data (string): símbolo u operador que el nodo almacena
    """
    def __init__(self, data, parent=None, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right
        self.parent = parent
        
        self.lastpos = []
        self.firstpos = []
        self.followpos = []
        self.nullable = False
        self.pos = None




class Stack(object):
    """
    CLASS STACK
    
    Esta clase construye un stack utilizando la librería collections y LifoQueue
    e implementa las funcionalidades básicas de un stack (push, pop, get_size, is_empty)
    
    Params:
        None
    """
    def __init__(self):
        self.stack = LifoQueue()
       
        
    def push(self, item):
        self.stack.put(item)
        
    
    def pop(self):
        return self.stack.get()
    
    
    def top(self):
        top = self.pop()
        self.stack.put(top)
        
        return top
    
    
    def snoc(self):
        if self.get_size() == 1:
            return (self.pop(), None)
        
        return (self.pop(), self.top())
    
    
    def get_size(self):
        return self.stack.qsize()
    
    
    def is_empty(self):
        return self.stack.empty()




class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'