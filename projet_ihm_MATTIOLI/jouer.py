#!/usr/bin/python3

# Par Julien BERENGUER - 05/05/17

# Version rendue

import tkinter as tk
import math
import matrice_module_IHM as m_m
import use_matrice_module_IHM as useM
import canvas_niveau as cn

root2=tk.Tk()
root2.state('withdrawn')
fenetre = tk.Toplevel(root2)         # Fenêtre qu'on manipule
fenetre.title('fenetre')
fenetre.state('withdrawn')
w = 500     # Largeur du canvas (width)
h = 500     # Hauteur du canvas (height)
can = tk.Canvas(fenetre, width = w, height = h, bg = 'white') # creation du canvas

# Variable de longueur
e = 25   # Ou ecart

# Rayon du cercle (link)
r = e/3
    
ident = 0           # Identifiant de l'objet traité
unique_item = ()    # Identifiant de l'objet traité
mouse_x = 0         # Coordonnées x de la souris
mouse_y = 0         # Coordonnées y de la souris

listItem = []       # Tous les items d'un objet
identObject = 0     # Numéro commun à tous les tracés communs à un objet

ecart_ligne_souris = 5 # Ecart entre la ligne en cours et le curseur => /!\ ne pas mettre à 0, sinon le curseur renverra à chaque fois la ligne
ESw = 0 # E/S with
ESh = 0 # E/S height

# Variables globales du link
link = 0            # Si on est en train de tracer une liaison
id_link = ()        # Identifiant de la ligne traitée
old_connect = ()    # Connecteur sélectionné en premier, pour éviter de lier un connecteur à lui-même
first_connect = 0   # Numéro du premier connecteur lors d'un lien entre deux connecteurs

# -------------------------------------------
def WhatText(nb): # Nord, Sud, Est ou Ouest pour les E/S
    
    text = ""
    
    if nb == 1:
        text = "Nord"
    if nb == 2:
        text = "Ouest"
    if nb == 3:
        text = "Est"
    if nb == 4:
        text = "Sud"
    
    return text
# -------------------------------------------
def InitESCanvas(): # Ajoute sur le canvas les Entrées/Sorties (capteurs et moteurs)
    global listItem
    global ESw
    global ESh
    
    ES = r   # écart entre les E/S par rapport à la taille de la fenêtre
    nb_mod = 4  # Nombre de modules => /!\, le programme n'est pas prévu pour en supporter plus ou moins de 4
    ESw = w/nb_mod  # Longueur de chaque module
    ESh = h/(nb_mod*2)   # Hauteur de chaque module
    
    # Capteurs
    listItem = []
    x0 = 0
    x1 = 0
    
    for i in range(1, nb_mod+1):
        x1 = i * ESw
        listItem.append(can.create_rectangle(x0+ES, 0, x1-ES, ESh, fill="yellow", outline="yellow"))
        can.addtag_withtag("Connect_0", listItem[-1])
        theText = WhatText(i)
        AjoutTags("Capteur")
        listItem = []
        can.create_text(x0+ES+ESw/2, ESh/2, text=theText, tags=(theText, "no", "Text"), font=('Times', 16, 'bold'), anchor="e")
        x0 = x1
    
    # Moteurs
    listItem = []
    x0 = 0
    x1 = 0
    
    for i in range(1, nb_mod+1):
        x1 = i * w/nb_mod
        listItem.append(can.create_rectangle(x0+ES, h, x1-ES, h-ESh, fill="red", outline="red"))
        can.addtag_withtag("Connect_0", listItem[-1])
        theText = WhatText(i)
        AjoutTags("Moteur")
        listItem = []
        can.create_text(x0+ES+ESw/2, h-ESh/2, text=theText, tags=(theText, "no", "Text"), font=('Times', 16, 'bold'), anchor="e")
        x0 = x1
    
    
# -------------------------------------------
def AjoutTags(typeObjet): # Ajout des tags pour les objets nouvellement créés, dernière étape de création
    global listItem
    global identObject
    
    useM.MatriceAddColumn()
    
    for item in listItem:
        can.addtag_withtag("Object Number " + str(identObject), item)
        can.addtag_withtag(str(typeObjet), item)

    identObject = identObject + 1
    
    for item in listItem:
        tags=can.gettags(item)
        print(tags)
# -------------------------------------------
def And(): # AND
    global listItem
    
    # Coordonées du Centre
    cx = w/2   # Ou centerX
    cy = h/2   # Ou centerY

    # Coordonnées du Rectangle
    x0 = cx-e
    y0 = cy-e
    x1 = cx+e
    y1 = cy+e

    listItem = []
    listItem.append(can.create_rectangle(x0, y0, x1, y1, fill="green", outline="green"))
    can.addtag_withtag("Center", listItem[-1])
    listItem.append(can.create_oval(x0+e, y0, x1+e, y1, fill="green", outline="green"))
    can.addtag_withtag("Oval", listItem[-1])
    listItem.append(can.create_line(x0, y0+(e/2), x0-2*e, y0+(e/2), fill="yellow", width=5))
    can.addtag_withtag("Line_1", listItem[-1])
    listItem.append(can.create_line(x0, y1-(e/2), x0-2*e, y1-(e/2), fill="red", width=5))
    can.addtag_withtag("Line_2", listItem[-1])
    listItem.append(can.create_line(x1+e, y0+e, x1+3*e, y0+e, fill="blue", width=5))
    can.addtag_withtag("Line_3", listItem[-1])
    listItem.append(can.create_oval(x0-2*e-r, y0+(e/2)+r, x0-2*e+r, y0+(e/2)-r, fill="yellow", outline="green"))
    can.addtag_withtag("Connect_0", listItem[-1])
    listItem.append(can.create_oval(x0-2*e-r, y1-(e/2)+r, x0-2*e+r, y1-(e/2)-r, fill="red", outline="green"))
    can.addtag_withtag("Connect_1", listItem[-1])
    listItem.append(can.create_oval(x1+3*e-r, y0+e+r, x1+3*e+r, y0+e-r, fill="blue", outline="green"))
    can.addtag_withtag("Connect_2", listItem[-1])
    print(listItem)
    AjoutTags("AND")
# -------------------------------------------
def OnItem(event):      # On est positionné sur un item (prend en compte chaque déplacement de la souris)
    global unique_item
    global ecart_ligne_souris
    #(link)
    global id_link
    global link
    
    item=can.find_withtag("current")    # Objet actuel
    if item != ():                  # Si l'on est bien sur un objet
        unique_item = item              # On associe l'objet à une variable globale pour pouvoir le sauvegarder
        #can.itemconfig(unique_item, fill="red")     # On le met en rouge
    else:                           # Si l'on est pas sur un objet
        #can.itemconfig(unique_item, fill="green")   # On le met en noir (item toujours connu grâce à la variable globale)
        unique_item = ()
    
    #(link)
    # Si on a créé un lien
    if link == 1:
        coord = can.coords(id_link)
        xy = 0          # Permet de savoir si on traite sur l'axe des abscisses ou l'axe des ordonnées
        pos = 0     # Position actuelle du curseur
        
        if ecart_ligne_souris <= 0:
            nb = 5
            ecart_ligne_souris = nb
            print("Attention : la variable 'ecart_ligne_souris' a été mise à zéro ou en négatif, valeur mise à", nb)
            
        coord[2] = event.x - ecart_ligne_souris # moins un nombre pour éviter de pointer uniquement sur la ligne
        coord[3] = event.y - ecart_ligne_souris
        #print(coord)
        can.coords(id_link, tk._flatten(coord))
# -------------------------------------------
def SelectItem(event):    # Première saisie de l'objet avant déplacement
    global unique_item
    global mouse_x
    global mouse_y
    global ESw
    global ESh
    
    #(link)
    global id_link
    global link
    global old_connect
    global first_connect

    # Première saisie, anciennes coordonées x et y
    mouse_x = event.x   
    mouse_y = event.y
    
    item=can.find_withtag("current")    # Objet actuel => /!\ n'est pas nécessaire, déjà effectué par OnItem
    if item != ():                  # Si l'on est bien sur un objet
        unique_item = item              # On associe l'objet à une variable globale pour pouvoir le sauvegarder
        
        #(link)
        tags = can.gettags(item)
        print("Item choisi : ", item, " tags = ", tags)
        #print(tags)
        #print('tags[0] =', tags[0])
        
        if tags[0].split('_')[0] == "Connect":  # Si on clique sur un connecteur
            print("Lien initié !")
            if link == 0:   # Si la ligne n'était pas crée => on la créé
                link = 1
                old_connect = item
                coord_connect = can.coords(old_connect) # Coordonées du connecteur pour placer le point de la ligne au centre
                # Fixe le début du lien sur le centre du connecteur
                if tags[2] == "Capteur" or tags[2] == "Moteur":
                    cx = ESw/2
                    cy = ESh/2
                else:
                    cx = r
                    cy = r
                linkLine = can.create_line(coord_connect[0]+cx, coord_connect[1]+cy, event.x, event.y, fill="black", width=5) 
                #print(">Centre connect : [", coord_connect[0]+r, ",", coord_connect[1]+r, "]")
                can.addtag_withtag("Link", linkLine)
                can.addtag_withtag(tags[1], linkLine)    # tag du numéro du premier objet
                id_link = linkLine
                #print("Id du lien : ", id_link)
                first_connect = int(tags[0].split('_')[1])
                print("first_connect =", first_connect)
                
            else:           # Si on avait déjà une ligne => on la lie au connecteur sélectionné si s'en est un, sinon suppression
                link = 0
                print("Item n°", item, " et ", old_connect)
                if item != old_connect: # S'il est différent du précédent
                    
                    coord_connect = can.coords(item)
                    coord_link = can.coords(id_link)
                    #print(">Link :", coord_link, "\n>Connect :", coord_connect)
                    if tags[2] == "Capteur" or tags[2] == "Moteur":
                        cx = ESw/2
                        cy = ESh/2
                    else:
                        cx = r
                        cy = r
                    coord_link[2] = coord_connect[0]+cx
                    coord_link[3] = coord_connect[1]+cy
                    
                    can.coords(id_link, tk._flatten(coord_link))
                    
                    #print("Id du lien : ", id_link)
                    can.addtag_withtag(tags[1], id_link)    # tag du numéro du second objet (sauf si c'est le même objet, pas deux tags identiques)
                    
                    # Gestion de la matrice
                    obj2 = 0
                    obj1 = 0
                    
                    tags_of_link = can.gettags(id_link)
                    print("Tags du link tout juste créé :", tags_of_link)
                    
                    obj1 = int(tags_of_link[1].split(' ')[2])
                    second_connect = int(tags[0].split('_')[1])
                    
                    if len(tags_of_link) > 2: # Connecté à deux objets
                        obj2 = int(tags_of_link[2].split(' ')[2])
                    else:
                        obj2 = obj1
                    
                    useM.MatriceLinkTo(first_connect, obj1, second_connect, obj2)
                    print("\n\n=> Connecteur 1 :", first_connect, ", Objet 1 :", obj1, ", Connecteur 2 :", second_connect, ", Objet 2 :", obj2)
                    
                    print("connecte")
                else:
                    can.delete(id_tag)
                    print("connecte pas")
    
# -------------------------------------------
def ObjectMove(event):    # Déplacement de tous les tracés communs à un objet en fluidité
    global unique_item
    global mouse_x
    global mouse_y
    
    item = can.find_withtag("current")
    tags = can.gettags(item)
    
    links_item = can.find_withtag("Link") # On recherche l'id de toutes les lignes
    
    # Si on ne sélectionne aucun item ou une ligne (lien) ou un objet qui ne doit pas bouger
    if len(item) == 0 or item in (links_item) or tags[2] in ("Text", "Capteur", "Moteur"):
        print("out")    # On évite l'erreur "tuple index out of range" lors du find_withtag
        return
    
    items_of_object = can.find_withtag(tags[1]) # Deuxième position => /!\ faire une recherche par tag, sinon peut causer bugs si on ne place pas bien les tags
    
    dif_x = event.x - mouse_x
    dif_y = event.y - mouse_y
    
    print("-------------------")
    for item in items_of_object:
        print("Déplacement : L'item : ", item)
        tags_of_item = can.gettags(item)
        # Si l'item traité est un lien entre deux objets
        if item in (links_item) and len(tags_of_item) > 2 : 
            print("L'item links est le n°", item, " avec les tags : ", tags_of_item)
            coord_link = can.coords(item)
            if tags_of_item[1] == tags[1]:  # Si le premier objet sélectionné pour créer le lien est celui qu'on bouge
                coord_link[0] += dif_x
                coord_link[1] += dif_y
            else:                           # Si le second objet sélectionné pour créer le lien est celui qu'on bouge (if tags_of_item[2] == tags[1]:)
                coord_link[2] += dif_x
                coord_link[3] += dif_y
            can.coords(item, tk._flatten(coord_link))
        # Si l'item traité n'est pas un lien ou un lien entre deux connecteurs d'un même objet
        else:
            can.move(item, dif_x, dif_y)
    print("-------------------")  
    
    mouse_x = event.x   # Actuelles coordonnées x => futures anciennes coordonnées x
    mouse_y = event.y   # Actuelles coordonnées y => futures anciennes coordonnées y

    
# -------------------------------------------
def ItemStopMove(event):    # Arrêt de déplacement (relâchement du clic souris gauche)
    global unique_item
    global mouse_x
    global mouse_y
    
    unique_item = ()
    mouse_x = 0
    mouse_y = 0
    
# -------------------------------------------
def RotationItem(event):    # Rotation d'un item
    global unique_item
    global mouse_x
    global mouse_y
    
    unique_item = ()
    mouse_x = 0
    mouse_y = 0
    
# -------------------------------------------
def RotationObject(event):    # Rotation d'un objet
    global unique_item
    global mouse_x
    global mouse_y
    
    a = math.pi / 2  # Rotation par défaut (90°), math travaille avec les radians
    #print("Angle de rotation en radian : ", a)
    
    item=can.find_withtag("current")    # Objet actuel => /!\ n'est pas nécessaire, déjà effectué par OnItem
    tags = can.gettags(item)    # Liste des tags de l'item sélectionné
    
    links_item = can.find_withtag("Link") # On recherche l'id de toutes les lignes
    
    # Si on ne sélectionne aucun item ou une ligne (lien) ou un objet qui ne doit pas bouger
    if len(item) == 0 or item in (links_item) or tags[2] in ("Text", "Capteur", "Moteur"):
        print("out")    # On évite l'erreur "tuple index out of range" lors du find_withtag
        return
    
    unique_item = item              # On associe l'objet à une variable globale pour pouvoir le sauvegarder
    
    unique_tag_of_object = tags[1]
    items_of_object = can.find_withtag(unique_tag_of_object)     # Liste des items appartenant à celui sélectionné
    #print(items_of_object)
    all_center_item  = can.find_withtag("Center")   # Liste de tous les items avec le tag Center
    #print(all_center_item)
    
    center_item = "None"
    
    # Intersection entre ceux avec le tag Center et ceux avec concernant l'objet pour retrouver le centre de celui-ci
    for item in all_center_item:
    
        tags_of_item = can.gettags(item)
        object_tag = tags_of_item[1]
        
        if object_tag == unique_tag_of_object:
            center_item = item
        
    if center_item == "None":
        print("L'objet ne comprend aucun item avec le tag 'center_item', rotation impossible.")
        return
    
    # Opérations de rotation :
    #
    # point central = t (tx, ty)
    # à faire : translation, rotation, translation^-1
    # rotation : 90° (= a)
    
    # T : x' = x-tx
    #     y' = y-ty
    
    # R : x' = xcos(a)-ysin(a)
    #     y' = xsin(a)+ycos(a)
    
    # T^-1 : x' = x+tx
    #        y' = y+ty
    
    
    
    # Centre de l'objet (point central T(tx, ty))
    coord_center = can.coords(center_item)
    #print(coord_center)
    
    x0_and_y0 = 0   # On fait un for uniquement sur x0 et y0 pour trouver le centre du cube Center
    
    for x_y in coord_center:   # Trouver les coordonées du centre du cube Center, donc de la porte logique
        if x0_and_y0 == 0:
            tx = x_y + e    # Coordonée X du centre du cube Center  (voir construction des portes logiques)
        if x0_and_y0 == 1:
            ty = x_y + e    # Coordonée Y du centre du cube Center  (voir construction des portes logiques)
        x0_and_y0 = x0_and_y0 + 1
    
    # >> Rotation de chaque objet
    for item in items_of_object:
        
        coord_item = can.coords(item)
        #print(coord_item)
        
        tags_of_item = can.gettags(item)
        
        link_orientation = 0
        # Si l'item traité est un lien entre deux objets (ici, gestion des bugs où le link prend le tag 'current', faussant ainsi le 'len(tags_of_item) > 2')
        if item in (links_item) and ((len(tags_of_item) > 2 and item not in can.find_withtag("current")) or (len(tags_of_item) > 3 and item in can.find_withtag("current"))):
            #print("1) L'item links est le n°", item, " avec les tags : ", tags_of_item)
            if tags_of_item[1] == tags[1]:  # Si le premier objet sélectionné pour créer le lien est celui qu'on bouge
                link_orientation = 1
            else:                           # Si le second objet sélectionné pour créer le lien est celui qu'on bouge (if tags_of_item[2] == tags[1]:)
                link_orientation = 2
        #print("2) Liste de tous les links items : ", links_item, ", item en cours : ", item)
        #if item in (links_item):
            #print("3) Link repéré, item n°", item, ", avec les tags : ", can.find_withtag(item))
        
        # >> Translation
        x_y = 0     # Variable pour savoir si on traite un x ou un y
        pos = 0     # Position actuelle du curseur
        for coord in coord_item:
            if x_y == 0:    # On traite une abscisse (x)
                if link_orientation == 0 or (link_orientation == 1 and pos == 0) or (link_orientation == 2 and pos == 2):
                    coord_item[pos] = coord - tx
                pos = pos + 1
                x_y = 1
            else:           # On traite une ordonnée (y)
                if link_orientation == 0 or (link_orientation == 1 and pos == 1) or (link_orientation == 2 and pos == 3):
                    coord_item[pos] = coord - ty
                pos = pos + 1
                x_y = 0
        #print("Coord 1 : ", coord_item)
        
        # >> Rotation
        x_y = 0     # Variable pour savoir si on traite un x ou un y
        old_x = 0   # Sauvegarde de la coordonée x avant modification (voir calcul)
        old_y = 0   # Sauvegarde de la coordonée y avant modification (voir calcul, non nécessaire ici)
        pos = 0     # Position actuelle du curseur
        for coord in coord_item:
            if x_y == 0:    # On traite une abscisse (x)
                if link_orientation == 0 or (link_orientation == 1 and pos == 0) or (link_orientation == 2 and pos == 2):
                    old_x = coord
                #print("x : ", old_x)
                #print("pos x : ", pos)
                pos = pos + 1
                x_y = 1
            else:           # On traite une ordonnée (y)
                #print("pos y : ", pos)
                if link_orientation == 0 or (link_orientation == 1 and pos == 1) or (link_orientation == 2 and pos == 3):
                    old_y = coord
                    coord_item[pos-1] = old_x * math.cos(a) - old_y * math.sin(a)       # Modification de x
                    coord_item[pos] = old_x * math.sin(a) + old_y * math.cos(a)         # Modification de y
                pos = pos + 1
                x_y = 0
        #print("Coord 2 : ", coord_item)
        
        # >> Translation ^-1
        x_y = 0     # Variable pour savoir si on traite un x ou un y
        pos = 0     # Position actuelle du curseur
        for coord in coord_item:
            if x_y == 0:    # On traite une abscisse (x)
                if link_orientation == 0 or (link_orientation == 1 and pos == 0) or (link_orientation == 2 and pos == 2):
                    coord_item[pos] = coord + tx
                pos = pos + 1
                x_y = 1
            else:           # On traite une ordonnée (y)
                if link_orientation == 0 or (link_orientation == 1 and pos == 1) or (link_orientation == 2 and pos == 3):
                    coord_item[pos] = coord + ty
                pos = pos + 1
                x_y = 0
        #print("Coord 3 : ", coord_item)
        can.coords(item, tk._flatten(coord_item))
# -------------------------------------------
def Launch(): 
    global nb_mod
    valCapteurs = [1, 1, 1, 1]
    # Affichage
    print("\nVoici les valeurs des capteurs :")
    for i in range(1, 4+1):#nb_mod+1):
        theText = WhatText(i)
        print("-", theText, "=", valCapteurs[i-1])
    
    # On passe les valeurs des capteurs
    valMoteurs = useM.ChercherResultats(valCapteurs)
    
    # Affichage
    print("\nVoici les résultats des moteurs :")
    for i in range(1, 4+1):#nb_mod+1):
        theText = WhatText(i)
        print("-", theText, "=", valMoteurs[i-1])
# -------------------------------------------
def GetLogic(objectNumber): # NON UTILISE, devait servir à la matrice, autre solution non trouvée
    
    objectItems = can.find_withtag("Object Number " + str(objectNumber))
    all_center_item  = can.find_withtag("Center")
    
    for item in objectItems:    # On cherche un unique item pour touver le tag de la porte logique
        if item in all_center_item:
            tags = can.gettags(item)
            return tags[2]
    
    return "ERROR, NOT FOUND"
# -------------------------------------------

def fenetre_jouer(root) :
    root.state('withdrawn') # cache root
    fenetre.state('normal')
    fenetre.title("Simulateur logique")        # Son nom
    fenetre.focus_set()                 # Premier plan par rapport aux autres fenêtres

    
    # Boutons
    frame = tk.Frame(fenetre)
    frame.pack(side = tk.TOP)

    button_and = tk.Button(frame, text = "AND", command = And)
    button_and.pack(side = tk.LEFT, expand = tk.YES)

    button_and = tk.Button(frame, text = "Launch", command = Launch)
    button_and.pack(side = tk.LEFT, expand = tk.YES)

    button_destroy = tk.Button(frame, text = "Quit", command = lambda:cn.retour_menu(root, fenetre))
    button_destroy.pack(side = tk.RIGHT, expand = tk.YES)


    can.pack(fill = tk.BOTH, expand = tk.YES)

    can.bind("<Motion>", OnItem)
    can.bind("<Button-1>", SelectItem)
    can.bind("<Button1-Motion>", ObjectMove)
    can.bind("<Button1-ButtonRelease>", ItemStopMove)

    can.bind("<Button-3>", RotationObject)

    useM.MatriceInitDefaultValue('N')
    useM.MatriceInit()

    InitESCanvas()

