#!/usr/bin/python3

# Par Julien BERENGUER - 04/05/17
# Dérivé de matrice_module_IHM.py


# Bibliothèques

import matrice_module_IHM as m
#import GetLogic as l
#import tkinter_logic_gates7_linked_5 as l

# Variables globales
defaut = 'NULL'
nbcases = 2
listeCaseDefaut = []
matriceCreated = 0

# Fonctions
# -------------------------------------------
def MatriceInitDefaultValue(value):
    global defaut
    global matriceCreated
    
    if matriceCreated == 1:
        print("Attention, matrice déjà crée, le changement de valeur par défaut va mener à des erreurs !")
    
    defaut = value
    
# -------------------------------------------
def MatriceInit():
    global defaut
    global nbcases
    global listeCaseDefaut
    global matriceCreated

    print("\n====> Début\n")
    m.CreerMatrice(3, 0, nbcases, defaut) # 3 lignes pour les connecteurs a, b et c. 1 seule colonne au départ
    m.AfficherMatrice()
    matriceCreated = 1
    
    listeCaseDefaut = []
    for nb in range(0, 2):  # ou nbcases):
        listeCaseDefaut.append(defaut)
    
# -------------------------------------------
def MatriceAddColumn():

    print("\n====> Ajout porte logique ou E/S\n")
    m.CreateColonneMatrice(defaut) # Ajout d'une porte logique
    m.AfficherMatrice()
    
# -------------------------------------------
def MatriceLinkTo(lin1, col1, lin2, col2):  
    global defaut
    #global nbcases
    
    # Ligne = connecteur, Colonne = objet

    print("\n====> Connection\n")
    
    listeCase1 = m.ExtractionMatriceCase(lin1, col1)
    listeCase2 = m.ExtractionMatriceCase(lin2, col2)
    print(listeCase1, "\n", listeCase2, "\n", listeCaseDefaut)
    
    listeCaseModif1 = [lin1, col1]
    listeCaseModif2 = [lin2, col2]
    
    # On gère les multiples liaisons
    if listeCase1 != listeCaseDefaut:
        print(listeCase1, " et ", listeCaseDefaut)
        listeCaseModif2[:] = listeCase1
        listeCaseModif2.append(lin2)
        listeCaseModif2.append(col2)
        print("!!!---l1---!!!")
    
    if listeCase2 != listeCaseDefaut:
        print(listeCase2, " et ", listeCaseDefaut)
        listeCaseModif1[:] = listeCase2
        listeCaseModif1.append(lin1)
        listeCaseModif1.append(col1)
        print("!!!---l2---!!!")
    
    m.ModifierMatriceListe(lin1, col1, listeCaseModif2)
    m.ModifierMatriceListe(lin2, col2, listeCaseModif1) 
    
    m.AfficherMatrice()

    
# -------------------------------------------
def ChercherResultats(valCapteurs):   
    # On passe les valeurs des capteurs pour pouvoir utiliser la matrice et afficher le résultat des moteurs
    global listeCaseDefaut
    
    valMoteurs = [0, 0, 0, 0]
    listeCapteur = []
    listeMoteur = []
    
    for i in range(0, 4):
        listeCapteur.append(m.ExtractionMatriceCase(0, i))
        listeMoteur.append(m.ExtractionMatriceCase(0, 4+i))
    
    print("Résultat des extractions des liens : ")
    print("-- Capteurs")
    for i in range(0, 4):
        print("-", listeCapteur[i])
    print("-- Moteurs")
    for i in range(0, 4):
        print("-", listeMoteur[i])
    
    for i in range(0, 4):
        if listeMoteur[i] != listeCaseDefaut:   # Si le moteur a une connexion
            valMoteurs[i] = ChercherResultatsRecursif(listeMoteur[i], valCapteurs, 0, 0)
        
    
    return valMoteurs

# -------------------------------------------
def ChercherResultatsRecursif(valCase, valCapteurs, compteur, limite): # Récursivité nécessaire

    val = 0
    limite = int(len(valCase)/2)
    
    for i in range(0, limite):    # Gestion de multiples liens sur la case étudiée
        lin = valCase[i]
        col = valCase[i+1]
        
        if col in range(0, 4): # Si l'objet est un connecteur (colonne 0 à 4 exclu)
            if valCapteurs[col] > 0:    # On évite d'effacer la valeur si la dernière itération est un 0
                val = 1
        elif col in range(4, 8): # Si l'objet est un moteur (colonne 4 à 8 exclu)
            val = "MOTEUR"
        else:       # Porte logique
            valCaseCible = m.ExtractionMatriceCase(lin, col)    # Extraction de la case cible
            print("c:", valCaseCible)
            #print(l.GetLogic(valCaseCible[1]))
            
            limite = int(len(valCaseCible)/2)
            valTemp = ChercherResultatsRecursif(valCaseCible, valCapteurs, 0, limite)
            print("r:", valTemp)
            if valTemp > 0:
                val = 1
        
    if compteur < limite-1:     # Si on a pas analysé toutes les liaisons de la case étudiée
        ChercherResultatsRecursif(valCase, valCapteurs, compteur+1, limite)
            
    return val
