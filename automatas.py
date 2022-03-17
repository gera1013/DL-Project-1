import uuid
import shortuuid

from structures import Stack, Colors


shortuuid.set_alphabet("0914856327")


class FA(object):
    """
    CLASS FA (Finite Automata)
    
    Clase para instanciar un objeto con las características de un automata finito.
    
    Params:
        ->
    """
    def __init__(self, symbols, states, tfunc, istate, tstate):
        self.states = states
        self.symbols = symbols
        self.transition_function = tfunc
        self.initial_state = istate
        self.terminal_states = tstate
        
    
    def print_automata(self, type, i_state, t_state, states, symbols, t_function):
        print(Colors.OKBLUE + "[INFO]" + Colors.ENDC + " NEW " + Colors.UNDERLINE + type + Colors.ENDC + " AUTOMATA CREATED WITH")
        print(Colors.OKCYAN + " INITIAL STATE" + Colors.ENDC)
        print(" °", i_state)
        print(Colors.OKCYAN + " TERMINAL STATES" + Colors.ENDC)
        print(" °", t_state)
        print(Colors.OKCYAN + " STATES" + Colors.ENDC)
        print(" °", states)
        print(Colors.OKCYAN + " SYMBOLS" + Colors.ENDC)
        print(" °", symbols)
        print(Colors.OKCYAN + " TRANSITIONS" + Colors.ENDC)
        print(" °")
        for key, value in t_function.items():
            print("     ", key, "->", value)
        print("")




class NFA(FA):
    def __init__(self, symbols=None, syntax_tree=None, states=[], tfunc={}, istate=None, tstate=[]):
        self.syntax_tree = syntax_tree
        
        if symbols:
            try:
                symbols.remove('ε')
            except:
                pass
        
        # instanciamos al objeto 
        FA.__init__(self, symbols, states=states, tfunc=tfunc, istate=istate, tstate=tstate)


    def thompson(self):
        sym = self.syntax_tree.traverse_postorder(self.syntax_tree.root)
        stack = Stack()
        self.a_stack = Stack()
        
        for i in range(len(sym) - 1, -1, -1):
            stack.push(sym[i])
            
        while not stack.is_empty():
            nxt = stack.pop()
            
            if nxt in self.symbols:
                new_automata = self.SYMBOL(nxt)
                self.a_stack.push(new_automata)
            else:
                if   nxt == '|':
                    a = self.a_stack.pop()
                    b = self.a_stack.pop()
                    
                    new_automata = self.OR(a, b)
                    self.a_stack.push(new_automata)
                    
                elif nxt == '+':
                    a = self.a_stack.pop()
                    b = self.KLEENE(a, new_names=True)
                    
                    new_automata = self.CONCAT(a, b)
                    self.a_stack.push(new_automata)
                
                elif nxt == '*':
                    a = self.a_stack.pop()
                    
                    new_automata = self.KLEENE(a)
                    self.a_stack.push(new_automata)
                
                elif nxt == '^':
                    b = self.a_stack.pop()
                    a = self.a_stack.pop()
                    
                    new_automata = self.CONCAT(a, b)
                    self.a_stack.push(new_automata)
                    
                elif nxt == '?':
                    a = self.a_stack.pop()
                    b = self.SYMBOL('ε')
                    
                    new_automata = self.OR(a, b)
                    self.a_stack.push(new_automata)
                    
                else:
                    pass
                
        final_automata = self.a_stack.pop()
        self.initial_state = final_automata.initial_state
        self.terminal_states = final_automata.terminal_states
        self.states = final_automata.states
        self.symbols = final_automata.symbols
        self.transition_function = final_automata.transition_function
                
    
    def SYMBOL(self, symbol):
        # generate id's for the initial and terminal states
        i_state = shortuuid.encode(uuid.uuid4())[:4]
        t_state = shortuuid.encode(uuid.uuid4())[:4]
        
        # states list
        states = [i_state, t_state]
        
        # transition_function
        t_function = {
            (i_state, symbol): [t_state]
        }
        
        #symbols
        symbols = list(symbol)
        
        self.print_automata("SYMBOL", i_state, t_state, states, symbols, t_function)
        
        return NFA(symbols, states=states, tfunc=t_function, istate=i_state, tstate=[t_state])
    
    
    def CONCAT(self, a, b):
        # generate id's for the initial and terminal states
        i_state = a.initial_state
        t_state = b.terminal_states
        
        # union of both a's and b's sets of symbols
        symbols = list(set(a.symbols + b.symbols))
        
        # create intermediate state for merging a's final and b's initial state
        intermediate_state = shortuuid.encode(uuid.uuid4())[:4]
        
        # transition function (a's final state and b's initial state become on)
        t_function = dict(list(a.transition_function.items()) + list(b.transition_function.items()))
        
        for key, value in list(t_function.items()):
            if key[0] == b.initial_state: 
                t_function[(intermediate_state, key[1])] = value
                del t_function[key]
            
            for fstate in a.terminal_states:
                if fstate in value:
                    t_function[key] = [intermediate_state if x == fstate else x for x in value]
        
        # new set of states with the merge done
        states = [x for x in b.states if x != b.initial_state] + [x for x in a.states if x not in a.terminal_states] + [intermediate_state]
    
        self.print_automata("CONCAT", i_state, t_state, states, symbols, t_function)    
    
        return NFA(symbols=symbols, states=states, tfunc=t_function, istate=i_state, tstate=t_state)
    
    def OR(self, a, b):
        # generate id's for the initial and terminal states
        i_state = shortuuid.encode(uuid.uuid4())[:4]
        t_state = shortuuid.encode(uuid.uuid4())[:4]
        
        # union of both a's and b's sets of symbols
        symbols = list(set(a.symbols + b.symbols))
        
        # transition function 
        t_function = dict(list(a.transition_function.items()) + list(b.transition_function.items()))
        
        # append a's states, b's states, and new initial and terminal state
        states = a.states + b.states + [i_state] + [t_state]
        
        # add new transition, create list if is the first one (a)
        try: 
            t_function[(i_state, 'ε')].append(a.initial_state)
        except: 
            t_function[(i_state, 'ε')] = [a.initial_state]
            
        # add new transition, create list if is the first one (b)
        try: 
            t_function[(i_state, 'ε')].append(b.initial_state)
        except: 
            t_function[(i_state, 'ε')] = [b.initial_state]
        
        # add new transition from (a) final states to new final state
        for fstate in a.terminal_states:
            try: 
                t_function[(fstate, 'ε')].append(t_state)
            except: 
                t_function[(fstate, 'ε')] = [t_state]
                
        # add new transition from (b) final states to new final state
        for fstate in b.terminal_states:
            try: 
                t_function[(fstate, 'ε')].append(t_state)
            except: 
                t_function[(fstate, 'ε')] = [t_state]
                
                
        self.print_automata("OR", i_state, t_state, states, symbols, t_function)
        
        return NFA(symbols=symbols, states=states, tfunc=t_function, istate=i_state, tstate=[t_state])
        
    
    def KLEENE(self, a, new_names=False):
        # generate id's for the initial and terminal states
        i_state = shortuuid.encode(uuid.uuid4())[:4]
        t_state = shortuuid.encode(uuid.uuid4())[:4]
        
        mirror_states = [shortuuid.encode(uuid.uuid4())[:4] for state in a.states] if new_names else a.states
        
        state_mapping = {}
        
        for i in range(len(mirror_states)):
            state_mapping[a.states[i]] = mirror_states[i]
        
        # states list
        states = [i_state, t_state] + mirror_states
        
        # copy symbols list
        symbols = a.symbols
        
        # copy transition function
        t_function = {}
        for key, value in list(a.transition_function.items()):
            t_function[(state_mapping[key[0]], key[1])] = [state_mapping[val] for val in value]
            
        # add transitions for: 
        # new initial state to new final state (accept ε cases) 
        try: 
            t_function[(i_state, 'ε')].append(t_state)
        except: 
            t_function[(i_state, 'ε')] = [t_state]
            
        # from new initial state to old initial state
        try: 
            t_function[(i_state, 'ε')].append(state_mapping[a.initial_state])
        except: 
            t_function[(i_state, 'ε')] = [state_mapping[a.initial_state]]
        
        # from old terminal states to new terminal state
        for fstate in a.terminal_states:
            try: 
                t_function[(state_mapping[fstate], 'ε')].append(t_state)
            except: 
                t_function[(state_mapping[fstate], 'ε')] = [t_state]
                
        # and the recursive transition from old terminal states to old initial state
        for fstate in a.terminal_states:
            try: 
                t_function[(state_mapping[fstate], 'ε')].append(state_mapping[a.initial_state])
            except: 
                t_function[(state_mapping[fstate], 'ε')] = [state_mapping[a.initial_state]]
        
        
        self.print_automata("KLEENE", i_state, t_state, states, symbols, t_function)
        
        return NFA(symbols=symbols, states=states, tfunc=t_function, istate=i_state, tstate=t_state)




class DFA(FA):
    def __init__(self, nfa=None, syntax_tree=None, symbols=None, states=[], tfunc={}, istate=None, tstate=[]):
        self.syntax_tree = syntax_tree
        self.nfa = nfa
        
        # remove 'ε' from symbols (affects construction)
        'ε' in nfa.symbols and nfa.symbols.remove('ε')
        
        # instanciamos al objeto 
        FA.__init__(
            self, 
            symbols= nfa.symbols,
            states=states, 
            tfunc=tfunc,
            istate=istate, 
            tstate=tstate
        )
        
    
    def subset(self):
        t_func = {}
        
        dstates_u = [self.e_closure_state(self.nfa.initial_state)]
        dstates_m = []
        
        while len(dstates_u) > 0:
            T = dstates_u.pop(0)
            dstates_m.append(T)
            
            for symbol in self.symbols:
                U = self.e_closure_set(self.move(T, symbol))
                
                if len(U) > 0:
                    if U not in dstates_u and U not in dstates_m:
                        dstates_u.append(U)
                
                    t_func[(tuple(T), symbol)] = [item for item in U]
                    
        
        for states in dstates_m:
            for state in states:
                if state in self.nfa.terminal_states:
                    self.terminal_states.append(state)
                
        self.initial_state = dstates_m[0]
        self.states = dstates_m 
        self.transition_function = t_func
    
    
    def e_closure_state(self, state):
        closure = [state]
        
        for key in self.nfa.transition_function.keys():
            if key[0] == state and key[1] == 'ε':
                for x in self.nfa.transition_function[key]:
                    closure.append(x)
            
            
        return closure
    
    
    def e_closure_set(self, T):
        t_func = self.nfa.transition_function
        stack = Stack()
        
        for t in T:
            stack.push(t)
            
        closure = T[:]
        
        while not stack.is_empty():
            top = stack.pop()
            
            for key, value in t_func.items():
                if key[0] == top and key[1] == 'ε':
                    for x in value:
                        if x not in closure:
                            closure.append(x)
                            stack.push(x)
                    
        return closure            
    
    
    def move(self, sset, symbol):
        move_set = []
        
        for key in self.nfa.transition_function.keys():
            if key[0] in sset and key[1] == symbol: 
                for x in self.nfa.transition_function[key]:
                    move_set.append(x)
            
        return move_set