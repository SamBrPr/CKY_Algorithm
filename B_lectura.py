import os
from pytokr import pytokr
import json



def llegir_dades(nom_fitxer):
    nom_fitxer += '.txt'
    directori = os.path.dirname(os.path.abspath(__file__))
    loc = os.path.join(directori, 'fitxers')
    fitxer = os.path.join(loc, nom_fitxer)

    gramatica = {}

    with open(fitxer, 'r') as file:
        for linia in file:
            linia = linia.strip()
            if not linia or '->' not in linia:
                continue
            esquerra, dreta = linia.split('->')
            esquerra = esquerra.strip()
            produccions = dreta.strip().split('|')
            gramatica[esquerra] = [prod.strip() for prod in produccions]

    return gramatica




def llegir_dades_prob( nom):
    gramatica = {}
    nom += '.txt'
    directori = os.path.dirname(os.path.abspath(__file__))
    loc = os.path.join(directori,'fitxers')
    fitxer = os.path.join(loc, nom)
    with open(fitxer, 'r') as file:
        linees = file.readlines()
        k = 1
        for i in range(0,len(linees)):
            norma = linees[i][0]
            if norma not in gramatica:
                gramatica[norma] = [[],[]]
            frase = linees[i]
            paraula = ''
            n = 0
            while frase[n] != '>':
                n+=1
            for j in range(n+1,len(frase)):
                lletra = frase[j]
                if lletra == '|' or j == len(frase)-1:
                    if i == len(linees)-1 and j == len(frase)-1:
                        paraula += lletra
                    if  k%2 == 0:
                        gramatica[norma][1].append(float(paraula))
                        k+=1
                    else:
                        gramatica[norma][0].append(paraula)
                        k+=1
                    paraula = ''
                elif lletra != '':
                    paraula += lletra
    return(gramatica)



##########################################################################
#LLEGIR JOCS DE PROVES
##########################################################################

def llegir_joc_proves_json(json_path='fitxers/joc_proves.json'):
    item = pytokr()
    ordre = item()
    dic_joc_proves = {}

    while ordre != 'finalitzar':
        if ordre == 'new_gram':
            nom_fitxer = item()
            if nom_fitxer not in dic_joc_proves:
                dic_joc_proves[nom_fitxer] = {}
            next = item()
            while next != 'end':
                paraula = next.strip()
                #tractar cadena buida (ε --> llegida com  ??)
                if paraula in {'@empty', 'ε', '??'}or paraula.replace('"', '') == '':
                    paraula = ''
                bool_p = item()
                bool_p= True if bool_p == 'T' else False  # Convertir a booleà
                if paraula not in dic_joc_proves[nom_fitxer]:
                    dic_joc_proves[nom_fitxer][paraula] = bool_p
                else:
                    print(f'La paraula "{paraula}" ja existeix a la gramàtica "{nom_fitxer}".')
                next = item()
        ordre = item()
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(dic_joc_proves, f, ensure_ascii=False, indent=2)
    print(f'Joc de proves guardat a {json_path}')


def carregar_joc_proves_json(json_path='fitxers/joc_proves.json'):
    with open(json_path, 'r', encoding='utf-8') as f:
        dic_joc_proves = json.load(f)
    return dic_joc_proves




if __name__ == "__main__":
    print("Llegint dades de joc de proves...")
    llegir_joc_proves_json()  





