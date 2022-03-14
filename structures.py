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
    def __init__(self, operators, regex):
        ## language stuff
        self.operators = operators
        self.symbols = [char for char in regex if char not in operators if char != '(' and char != ')']
        self.regex = regex
        self.postfix = ""
        
        ## structure stuff
        self.root = None
        
        ## transformations to regex
        self.explicit_concat()
        self.to_postfix()
        self.build_tree()
        
        
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
                if (self.regex[i] in self.symbols and self.regex[i + 1] in self.symbols) or (self.regex[i] not in ['|', '('] and self.regex[i + 1] in self.symbols + ['(']): #  or (self.regex[i] in ['*', ')'] and self.regex[i + 1] in self.symbols + ['('])
                    new_regex += '^'
            except:
                pass
    
        self.regex = new_regex
    
    
    def to_postfix(self):
        operator_stack = Stack()
        
        for char in self.regex:
            
            if char in self.symbols:
                self.postfix += char
                
            elif char == '(':
                operator_stack.push(char)
                
            elif char == ')':
                while operator_stack.top() != '(':
                    self.postfix += operator_stack.pop()
                    
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
                    
    
    def build_tree(self):
        tree_stack = Stack()
        stack = []
        
        for char in self.postfix:
            if char in self.symbols:
                tree_stack.push(Node(char))
                stack.append(Node(char))
            else:
                if char in ['*']:
                    right = tree_stack.pop()
                    stack.pop()
                    
                    new = Node(char, right=right)
                    
                    right.parent = new
                    
                    tree_stack.push(new)
                    stack.append(new)
                    
                else:
                    right = tree_stack.pop()
                    left = tree_stack.pop()
                    
                    stack.pop()
                    stack.pop()
                    
                    new = Node(char, right=right, left=left)
                    
                    right.parent = new
                    left.parent = new
                    
                    tree_stack.push(new)
                    stack.append(new)
        
        self.root = tree_stack.pop()
        
        
        
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