#!/usr/bin/python3

# Par Julien BERENGUER - 04/05/17
# Dérivé de matrice3.py + ajouts pour l'IHM (notamment pour le print)


# Bibliothèques

import time     # Pour mettre un laps de temps lors d'un dépassement => gestion des erreurs


# Variables globales

matrice = []    # Notre matrice
modif = []      # Simple liste pour les modifications avec le nombre de cases adéquat
nbcol = 0       # Nombre de colonnes, pour le print 2 de l'affichage
nbvarparcases = 0    # Nombre de variables par cases


# Définitions/Fonctions


# -------------------------------------------
#                INITIALISATION
# -------------------------------------------
def CreerMatrice(lin, col, nbcases, var):    # Création de la matrice
    global matrice
    global modif
    global nbcol
    global nbvarparcases
    
    nbcol = col
    nbvarparcases = nbcases
    
    # Initialisation de la matrice
    for i in range(lin):            # n lignes
        ligne = []
        for j in range(col):        # n colonnes
            ligne.append([var]* nbcases)    # n données par cases
            #print(ligne)
        matrice.append(ligne)
    
    # Initialisation de la modif
    for i in range(nbcases):
        modif.append(var)

# -------------------------------------------
#                MODIFICATIONS
# -------------------------------------------
def ModifierMatriceValeur(lin, col, nocase, var):    # Modification d'une valeur d'une case de la matrice
    global matrice
    global modif
    global nbvarparcases
    
    VerifTailleLigneMatrice(lin)
    VerifTailleColonneMatrice(col)
    VerifTailleCaseMatrice(nocase)
    
    saveModif=[]
    saveModif[:] = modif    # /!\ 'saveModif[:] = modif' => par copie et 'saveModif = modif' => par adresse /!\
    
    modif[nocase] = var
    matrice[lin][col] = modif[:]
    
    modif[:] = saveModif
# -------------------------------------------
def ModifierMatriceListe(lin, col, liste):    # Modification de toute une case de la matrice
    global matrice
    global modif
    
    VerifTailleLigneMatrice(lin)
    VerifTailleColonneMatrice(col)
    
    matrice[lin][col] = liste[:]

# -------------------------------------------
#                EXTRACTIONS
# -------------------------------------------
def ExtractionMatrice(lin, col, nocase):    # Affichage d'un membre d'une case
    global matrice
    
    result = matrice[lin][col]
    #print("\n>> Extraction aux coordonées [", lin, "], [", col, "] à la case n°", nocase,", résultat :", result[nocase])
# -------------------------------------------
def ExtractionMatriceCase(lin, col):    # Affichage d'une case complète (résultat sous forme de liste)
    global matrice
    
    result = matrice[lin][col]
    #print("\n>> Extraction de la case aux coordonées [", lin, "], [", col, "], résultat :", result)
    return result

# -------------------------------------------
#                CREATION
# -------------------------------------------
def CreateLigneMatrice(var):    # Ajoute une ligne à la fin de la matrice
    global matrice
    global nbcol
    global nbvarparcases
    
    ligne = []                  # 1 ligne
    for j in range(0, nbcol):        # toutes les colonnes déjà créées
        ligne.append([var]* nbvarparcases)    # n données par cases
    matrice.append(ligne)
    
    #print("\n>> Ajout d'une ligne")
# -------------------------------------------
def CreateColonneMatrice(var):    # Ajoute une colonne à la fin de la matrice
    global matrice
    global nbvarparcases
    global nbcol
    
    colonne = []
    for i in range(0, nbvarparcases):   # génération d'une liste pour chaque lignes
        colonne.append(var)
            
    for i in range(0, len(matrice)):    # toutes les lignes déjà créées
        #print(">",colonne)
        matrice[i].append(colonne)
    
    nbcol = nbcol + 1
    
    #print("\n>> Ajout d'une colonne")
    
# -------------------------------------------
#                DESTRUCTION
# -------------------------------------------
def DeleteLigneMatrice(lin):    # Enlève une ligne de la matrice
    global matrice
    
    VerifTailleLigneMatrice(lin)
    
    del matrice[lin]
    
    #print("\n>> Suppression de la ligne :", lin)
# -------------------------------------------
def DeleteColonneMatrice(col):    # Enlève une colonne de la matrice
    global matrice
    global nbcol
    
    VerifTailleColonneMatrice(col)
    
    for i in range(0, len(matrice) ):
        for j in range(0, len(matrice[i]) ):
            if j == col:
                del matrice[i][col]
    
    nbcol = nbcol - 1
    
    #print("\n>> Suppression de la colonne :", col)

# -------------------------------------------
#                REMPLACEMENT
# -------------------------------------------
def ReplaceLigneMatrice(lin, var):    # Modifie les valeurs de toute une ligne de la matrice
    global matrice
    
    VerifTailleLigneMatrice(lin)
    
    liste = []
    for nocase in range(0, nbvarparcases):
        liste.append(var)
    
    for i in range(0, len(matrice) ):
        for col in range(0, len(matrice[i]) ):
            ModifierMatriceListe(lin, col, liste)
    
    #print("\n>> Modification de la ligne :", lin, "avec la valeur :", var)
# -------------------------------------------
def ReplaceColonneMatrice(col, var):    # Modifie les valeurs de toute une colonne de la matrice
    global matrice
    global nbvarparcases
    
    VerifTailleColonneMatrice(col)
    
    liste = []
    for nocase in range(0, nbvarparcases):
        liste.append(var)
    
    for lin in range(0, len(matrice) ):
        ModifierMatriceListe(lin, col, liste)
    
    #print("\nModification de la colonne :", col, "avec la valeur :", var)

# -------------------------------------------
#                AFFICHAGE
# -------------------------------------------
def AfficherMatrice():    # Affichage de la matrice
    global matrice
    global nbcol
    
    print("\n\n>> Affichage de la matrice : ")   # => préférable d'utiliser (print 2 de la première version)
    print("Nombre de lignes (connecteurs) :", len(matrice), ", nombre de colonnes (objets) :", nbcol)
    string = ''
    for i in range(0, len(matrice) ):
        string = string + "\nConnecteur " + str(i) + " : "
        for j in range(0, len(matrice[i]) ):
            string = string + str(matrice[i][j]) + " "
    print(string)

# -------------------------------------------
#                VERIFICATION
# -------------------------------------------
def VerifTailleLigneMatrice(lin):    # Vérifie la taille d'une ligne passée en paramètre de la matrice
    global matrice
    
    if lin >= len(matrice):
        print("\n\n /!\ Dépassement ligne /!\ \n\n")
        time.sleep(2)
# -------------------------------------------
def VerifTailleColonneMatrice(col):    # Vérifie la taille d'une colonne passée en paramètre de la matrice
    global matrice
    global nbcol
    
    if col >= nbcol:
        print("\n\n /!\ Dépassement colonne /!\ \n\n")
        time.sleep(2)
# -------------------------------------------
def VerifTailleCaseMatrice(nocase):    # Vérifie la taille d'une case passée en paramètre de la matrice
    global matrice
    global nbvarparcases
    
    if nocase >= nbvarparcases:
        print("\n\n /!\ Dépassement case /!\ \n\n")
        time.sleep(2)
# -------------------------------------------

