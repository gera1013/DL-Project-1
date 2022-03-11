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
    """
    def __init__(self, operators, regex):
        self.operators = operators
        self.regular_expression = regex
        
    
    def toPosix(self):
        pass




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
    
    
    def get_size(self):
        return self.stack.qsize()
    
    
    def is_empty(self):
        return self.stack.empty()