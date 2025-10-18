import copy

class GramTrans_CFGtoCNF:
    def __init__(self, gram):
        self.original= copy.deepcopy(gram)
        self.grammar= copy.deepcopy(gram)
        self.new_var_count = 0 
        self.start_sym= next(iter(gram))


    def _nova_var(self):
        self.new_var_count += 1
        return f'X{self.new_var_count}'
    
    def es_cnf(self):
        for lhs, rhss in self.grammar.items():
            for rhs in rhss:
                if rhs ==[]:
                    if lhs != self.start_sym:
                        return False
                    continue
                if len(rhs) == 1:
                    if rhs[0].isupper():
                        return False 
                elif len(rhs) == 2:
                    if not all(sym.isupper() for sym in rhs):
                        return False 
                else:
                    return False
        return True

   
    def eliminar_epsilon(self):
        s= set()
        for lhs, rhss in self.grammar.items():
            for rhs in rhss:
                if rhs == ['ε'] or rhs == ['??'] or rhs == ['@empty'] or rhs == []:
                    s.add(lhs)
        changed = True
        while changed:
            changed = False
            for lhs, rhss in self.grammar.items():
                for rhs in rhss:
                    if any(sym in s for sym in rhs) and lhs not in s:
                        s.add(lhs)
                        changed = True
        new_grammar = {}
        for lhs, rhss in self.grammar.items():
            new_rhss = set()
            for rhs in rhss:
                new_rhss.add(tuple(rhs)) 
                n_pos= [i for i, sym in enumerate(rhs) if sym in s]
                
                from itertools import combinations,chain
                for r in range(1, len(n_pos) +1):
                    for to_remove in combinations(n_pos, r):
                        new_rhs=[sym for i, sym in enumerate(rhs) if i not in to_remove]
                        if new_rhs:
                            new_rhss.add(tuple(new_rhs))
            new_grammar[lhs]= [list(rhs) for rhs in new_rhss ]
        
        self.grammar = new_grammar

    def ajustar_inicial_epsilon(self):
        def pot_ind_fer_epsilon(nt,vist=set()):
            if nt in vist:
                return False
            vist.add(nt)
            for rhs in self.grammar.get(nt, []):
                if rhs == []:
                    return True
                if all(sym in self.grammar and pot_ind_fer_epsilon(sym, vist.copy()) for sym in rhs):
                    return True
            return False
        
        if pot_ind_fer_epsilon(self.start_sym):
            if [] not in self.grammar[self.start_sym]:
                self.grammar[self.start_sym].append([])

        no_term= list(self.grammar.keys())
        for nt in no_term:
            if nt !=self.start_sym: 
                self.grammar[nt] = [rhs for rhs in self.grammar[nt] if rhs != []]
                if not self.grammar[nt]:  
                    del self.grammar[nt]  

    
    def eliminar_unitaries(self):
        for lhs in self.grammar:
            self.grammar[lhs] = [
                rhs for rhs in self.grammar[lhs]
                if not (len(rhs) == 1 and rhs[0].isupper() and rhs[0] not in self.grammar)
            ]
                                
        unit_p=set()
        for A in self.grammar:
            for rhs in self.grammar[A]:
                if len(rhs) == 1 and rhs[0] in self.grammar:
                    unit_p.add((A, rhs[0])) 
        changed = True
        while changed:
            changed = False
            noves_p= set(unit_p)
            for (A,B) in unit_p:
                for (C,D) in unit_p:
                    if B == C and (A, D) not in unit_p:
                        noves_p.add((A, D))
                        changed = True
            unit_p = noves_p
        new_grammar = {}
        for A in self.grammar:
            new_grammar[A] = []
            for rhs in self.grammar[A]:
                if not (len(rhs) == 1 and rhs[0] in self.grammar):
                    new_grammar[A].append(rhs)
        for (A,B) in unit_p:
            for rhs in self.grammar[B]:
                if not (len(rhs)== 1 and rhs[0] in self.grammar):
                    if rhs not in new_grammar[A]:
                        new_grammar[A].append(rhs)

        self.grammar = new_grammar

    def convertir_mixtes(self):
        terminal_map = {} 
        new_rules = {}
        for lhs, rhss in self.grammar.items():
            new_rhss = []
            for rhs in rhss:
                if len(rhs) > 1:
                    new_rhs = []
                    for sym in rhs:
                        if sym not in self.grammar and not sym.isupper():
                            if sym not in terminal_map:
                                var = self._nova_var()
                                terminal_map[sym] = var
                                new_rules[var] = [[sym]]
                            new_rhs.append(terminal_map[sym])
                        else:
                            new_rhs.append(sym)
                    new_rhss.append(new_rhs)
                else:
                    new_rhss.append(rhs)
            self.grammar[lhs] = new_rhss

        self.grammar.update(new_rules)

    def trencar_regles_no_bi(self):
        new_rules = {}
        for lhs, rhss in self.grammar.items():
            new_rhss = []
            for rhs in rhss:
                while len(rhs) > 2: 
                    new_var = self._nova_var()
                    new_rules[new_var] = [[rhs[1], rhs[2]]]
                    rhs = [rhs[0], new_var] + rhs[3:] 
                new_rhss.append(rhs)
            self.grammar[lhs] = new_rhss 
        self.grammar.update(new_rules) 


    def to_cnf(self):
        if self.es_cnf():
            print("La gramàtica ja està en CNF.")
            return self.grammar
        print("Transformant la gramàtica a CNF...")       
        for lhs in self.grammar:
            noves_produccions = []
            for rhs in self.grammar[lhs]:
                if rhs == '@empty':
                    noves_produccions.append([]) 
                else:
                    noves_produccions.append(list(rhs))
            self.grammar[lhs] = noves_produccions   
        self.eliminar_epsilon()
        self.ajustar_inicial_epsilon()
        print("Produccions epsilon eliminades i ajustades.")
        print(self.grammar)

        self.eliminar_unitaries()
        print("Produccions unitàries eliminades.")
        print(self.grammar)

        self.convertir_mixtes()
        print("Produccions de terminals convertides.")
        print(self.grammar)

        self.trencar_regles_no_bi()
        print("Regles llargues trencades.")
        print(self.grammar)

        return self.grammar 