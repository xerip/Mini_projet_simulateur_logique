import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

# variables #

clic_depart=False
clic_arrivee=False

# fonctions pour la canvas du niveau #

def frbdepart(canvas): #binding du bouton depart
    canvas.tag_bind('cb', '<Button-1>', lambda event:clic_cb_depart(event,canvas))
def frbmur(canvas): #binding du bouton mur
    canvas.tag_bind('cb', '<Button-1>', lambda event:clic_cb_mur(event,canvas))
def frbarrivee(canvas): #binding du bouton arrivee
    canvas.tag_bind('cb', '<Button-1>', lambda event:clic_cb_arrivee(event,canvas))

            
def clic_cb_depart(event,canvas): # permet de placer une case depart dans le niveau
    global clic_depart # la variable clic_depart devient globale
    global oldcurrent_depart # de meme pour elle
    current=canvas.find_withtag("current") #current est la case ou l'on se trouve
    if (canvas.itemcget(current,'fill')=='blue') or (canvas.itemcget(current,'fill')=='red'):
        return 0 #si une couleur autre que blanc est sur la case alors on sort de la fonction
    if clic_depart==False: #s'il n'y a aucune case depart
        canvas.itemconfigure(current, fill='lime green', outline='grey')
        oldcurrent_depart=current
        clic_depart=True
    else: #s'il y a une case depart
        if oldcurrent_depart==current:
            pass #on ne fait rien si on clique au meme endroit
        else: #sinon on construit la nouvelle case et on enleve l'autre
            canvas.itemconfigure(current, fill='lime green', outline='grey')
            canvas.itemconfigure(oldcurrent_depart, fill='white', outline='grey')
            oldcurrent_depart=current


def clic_cb_mur(event,canvas): # permet de placer ou enlever un mur dans le niveau
    current=canvas.find_withtag("current") # current est la case ou l'on se trouve
    if (canvas.itemcget(current,'fill')=='lime green') or (canvas.itemcget(current,'fill')=='red'):
        return 0 #si une couleur autre que blanc est sur la case alors on sort de la fonction
    if (canvas.itemcget(current,'fill')=='blue'): # si la case est bleue donc si c'est un mur
        canvas.itemconfigure(current, fill='white', outline='grey') # on supprime le mur
    else: #sinon on colore la case en bleue (on en fait un mur)
        canvas.itemconfigure(current, fill='blue', outline='black')

            
def clic_cb_arrivee(event,canvas): # permet de placer une case arrivee dans le niveau
    global clic_arrivee # la variable clic_depart devient globale
    global oldcurrent_arrivee # de meme pour celle-ci
    current=canvas.find_withtag("current") # current est la case ou l'on se trouve
    if (canvas.itemcget(current,'fill')=='blue') or (canvas.itemcget(current,'fill')=='lime green'):
        return 0 #si une couleur autre que blanc est sur la case alors on sort de la fonction
    if clic_arrivee==False: #s'il n'y a aucune case arrivee
        canvas.itemconfigure(current, fill='red', outline='grey')
        oldcurrent_arrivee=current
        clic_arrivee=True
    else: #s'il y a une case arrivee
        if oldcurrent_arrivee==current:
            pass #on ne fait rien si on clique au meme endroit
        else: #sinon on construit la nouvelle case et on enleve l'autre
            canvas.itemconfigure(current, fill='red', outline='grey')
            canvas.itemconfigure(oldcurrent_arrivee, fill='white', outline='grey')
            oldcurrent_arrivee=current


def remove(canvas): # remet le canvas a zero
    global clic_depart # la variable clic_depart devient globale
    global clic_arrivee # de meme pour celle-ci
    for num_carre in canvas.find_withtag('cb'): # pour chaque carre du niveau avec le tag cb
        canvas.itemconfigure(num_carre, fill='white', outline='grey') # on met la couleur du carre en blanc
    clic_depart=False
    clic_arrivee=False

    
def undo(tl,tl2): #permet de retourner a la fenetre 'taille du niveau'
    tl2.destroy() # on detruit a fenetre du niveau
    tl.state('normal') # on fait reapparaitre la fenetre 'taille du niveau'


def retour_menu(root, tl2): # permet de retourner au menu principal
    tl2.destroy() # on detruit a fenetre du niveau
    root.state('normal') # on fait reapparaitre la fenetre principale

    
def save(tl2, canvas, Long, Larg): # permet de sauver un niveau

    # initialisation des variables #
    
    dep=False
    arr=False
    nbmur=0
    diff=""
    cbs=canvas.find_withtag('cb') # donne une liste de tous les id des carre de tag cb

    
    for item in cbs : # pour chaque item dans cbs
        if (canvas.itemcget(item,'fill')=='lime green'): # s'il y a une case depart
            dep=True
        elif (canvas.itemcget(item,'fill')=='red'): # s'il y a une case arrivee
            arr=True
        elif (canvas.itemcget(item,'fill')=='blue'): # s'il y a un mur
            nbmur=nbmur+1
    if (dep==True) and (arr==True): # s'il y a bien une case depart et une case arrivee
        if nbmur==0: # permet d'obtenir la difficulte du niveau
            diff="facile"
        elif nbmur>(Long*Larg/2):
            diff="difficile"
        else:
            diff="moyen"
        # ouvre une fenetre permettant de choisir un fichier dans l'arborescence, renvoie le chemin du fichier choisi
        chemin = tk.filedialog.asksaveasfilename(title = "Enregistrer sous", parent = tl2, defaultextension = ".lvl", \
                                                    filetypes = [('levels', '.lvl'), ('all files', '.*')], initialfile='level_1_'+diff)
        if len(chemin) > 0:    # ici le code pour enregistrer l'objet interne dans le fichier sélectionné self.repfic
            items = canvas.find_all()  # Recherche de toutes les objets créés
            fichier = open(chemin, "w")     # Création et ouverture du fichier
            fichier.write(str(Long)+' '+str(Larg)+'\n') # on ecrit la longueur et la largeur du niveau en premiere ligne
            for id in items: # pour chaque objet du canvas, on ecrit son id et sa couleur
                id_color = canvas.itemcget(id, 'fill')
                fichier.write(str(id)+' '+id_color)
                fichier.write('\n')
            fichier.close()
    else: # sinon on informe l'utilisateur sur la contenance de chaque niveau
        tk.messagebox.showinfo(parent=tl2,title='Information',message="Chaque niveau doit comporter :\n   - une case depart\n   - une case arrivée\n   - aucun, un ou plusieurs murs")
