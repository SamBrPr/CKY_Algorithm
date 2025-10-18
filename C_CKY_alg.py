import os

"""
Tot el programa serà bàsicament tota una classe ( per ara, si no va be doncs potser caldràn funcions fora de la classe, ns), 
ja veurem com farem la lectura de dades, pero per ara hem de programar l'algoritme en sí
"""
class CKY:
    def __init__(self,dades,nom_type):
        self.gramatica = dades
        self.metode = 'det'
        if 'prob' in nom_type:
            self.metode = 'prob'

    
    def crear_taula(self,n):
        if self.metode == 'prob':
            taula = [[[[],[]] for i in range(n-j)]for j in range(n)]
        else:
            taula = [[[] for i in range(n-j)]for j in range(n)]
        
        return(taula)
    
    def resol(self, paraula):
        n = len(paraula)
        if n == 0:
            return 'S' in self.gramatica and '' in self.gramatica['S']


        taula = self.crear_taula(n)
        taula = self.nivell1(taula,paraula)
        if self.metode == 'prob':
            return self.resol_prob(n,taula)
        else:
            return self.resol_det(n,taula)
        
    def combinacions(self, arg1, arg2):
        resultat = []
        if self.metode == 'prob':
            for idx1, nt1 in enumerate(arg1[0]):
                for idx2, nt2 in enumerate(arg2[0]):
                    element = nt1 + nt2
                    prob1 = arg1[1][idx1]
                    prob2 = arg2[1][idx2]
                    prob = prob1 * prob2
                    resultat.append((element, prob))
        else:
            if len(arg1) !=0 and len(arg2) != 0:
                for el1 in arg1:    
                    for el2 in arg2:
                        element = el1 + el2
                        resultat.append(element)
        return resultat
    
    def nivell1(self,taula,paraula):
        if self.metode == 'prob':
            for i in range(0,len(paraula)):
                for norma in self.gramatica:
                    for j, mot in enumerate(self.gramatica[norma][0]):
                        if paraula[i] == mot:
                            taula[0][i][0].append(norma)
                            taula[0][i][1].append(float(self.gramatica[norma][1][j])) 
        else:
            for i in range(0,len(paraula)):
                for norma in self.gramatica:
                    if paraula[i] in self.gramatica[norma]:
                        taula[0][i].append(norma) 
        return taula

    def resol_det(self,n,taula):
        for i in range(0,n):
            for j in range(0,n-i):
                for k in range(0,i):
                    elements = self.combinacions(taula[k][j], taula[i-k-1][j+k+1])
                    for valor in self.gramatica:
                        for element in elements:
                            if element in self.gramatica[valor]:
                                taula[i][j].append(valor)
        if 'S' in taula[n-1][0]:
            return True
        return False
    def resol_prob(self,n,taula):
        for i in range(0,n):
            for j in range(0,n-i):
                                
                for k in range(0,i):
                    elements = self.combinacions(taula[k][j], taula[i-k-1][j+k+1])
                    for valor in self.gramatica:
                        for element, prob in elements:
                            for idx, mot in enumerate(self.gramatica[valor][0]): 
                                if element == mot:
                                    prob = prob * self.gramatica[valor][1][idx]
                                    if valor in taula[i][j][0]: 
                                        idx = taula[i][j][0].index(valor)
                                        if prob > taula[i][j][1][idx]:
                                            taula[i][j][1][idx] = prob
                                    else:
                                        taula[i][j][0] += [valor]
                                        taula[i][j][1] += [prob]
        index = taula[n-1][0]                        
        if 'S' in index[0]:
            for count, lletra in enumerate(index[0]):
                if lletra == 'S':
                    probabilitat = index[1][count]
            return True,probabilitat
        return False,None
    
