import tkinter as tk
from tkinter import filedialog
import canvas_niveau as cn
import os


def Modif_lvl(root): # permet de modifier un niveau
    root.state('withdrawn') # cache la fenetre principale
    # ouvre une fenetre permettant de choisir un niveau dans l'arborescence de fichiers
    # qui renvoie le chemin du fichier choisi
    chemin = tk.filedialog.askopenfilename(title = "Ouvrir un niveau", parent = root, defaultextension = ".lvl", \
                                                filetypes = [('levels', '.lvl'), ('all files', '.*')])
    if len(chemin) > 0: # si un fichier a bien ete choisi
        # variables #
        test=True
        list_items=[]

        # Toplevel 4 #
        tl4=tk.Toplevel()
        tl4.title(os.path.basename(chemin)) #os.path.basename(chemin) est le nom du fichier choisi en titre
        fichier = open(os.path.basename(chemin),'r') # ouverture du fichier en mode lecture
        for line in fichier: # pour chaque ligne du fichier
            if test==True: # on lit la premiere ligne
                line=line.split()
                Long, Larg = int(line[0]), int(line[1]) # qui contient la longueur et la largeur du niveau
                test=False
            else: # puis les autres
                line=line.split() # qui contiennent l'id d'un carre et sa couleur
                if line[1]=='lime':
                    line[1]='lime green'
                list_items=list_items+[line] # on les ajoute a une liste

        # creation d'une frame
        f1=tk.Frame(tl4)
        
        rbvar=tk.StringVar() # creation d'une variable StringVar
        rbv=tk.IntVar() # creation d'une variable IntVar
        rbv2=tk.IntVar() # creation d'une variable IntVar
        rbv3=tk.IntVar() # creation d'une variable IntVar

        # execute la fonction frbdepart du module canvas_niveau quand presse
        bdepart=tk.Radiobutton(f1,text='Placer/Déplacer la case Départ',variable=rbvar,value=rbv,indicatoron=0,command=lambda:cn.frbdepart(canvas)).pack(side='left')
        # execute la fonction frbmur du module canvas_niveau quand presse
        bmur=tk.Radiobutton(f1,text='Construire/Détruire un mur',indicatoron=0,variable=rbvar,value=rbv2,command=lambda:cn.frbmur(canvas)).pack(side='left')
        # execute la fonction frbarrivee du module canvas_niveau quand presse
        barrivee=tk.Radiobutton(f1,text='Placer/Déplacer la case Arrivée',indicatoron=0,variable=rbvar,value=rbv3,command=lambda:cn.frbarrivee(canvas)).pack(side='left')

        f1.pack() # on affiche le canvas

        # creation d'un canvas selon Long et Larg #
        canvas=tk.Canvas(tl4,width=32*(Long+2)+2,height=32*(Larg+2)+2)

        # corps du niveau #
        
        for j in range(0,Larg+2): #on fabrique les carre selon le type de celui-ci (contour en bleu ou non contour en blanc)
            x0,x1,cpt=2,32,0
            if j==0:
                y0,y1=2,32
            else:
                y0=y0+32
                y1=y1+32
            for i in range(0,Long+2):
                cpt=cpt+1
                if j==0 or j==(Larg+2)-1 or (j!=0 and j!=Larg+2 and (cpt==1 or cpt==Long+2)):
                    canvas.create_rectangle(x0,y0,x1,y1,fill='blue')
                else:
                    canvas.create_rectangle(x0,y0,x1,y1, fill='white', outline='grey', tags=('cb',x0,y0,x1,y1))
                x0=x0+32
                x1=x1+32

        for item in list_items: # on change les couleurs de chaque carre pour que le niveau soit identique a celui du fichier choisi precedemment
            if item[1]=='blue':
                canvas.itemconfigure(item[0], fill=item[1], outline='black')
            else:
                canvas.itemconfigure(item[0], fill=item[1], outline='grey')

        canvas.pack() # on affiche le canvas

        # creation d'une nouvelle frame
        f2=tk.Frame(tl4)

        # boutons qui activent leur fonctions predefinies situees dans le module canvas_niveau
        
        bremove=tk.Button(f2,text='Tout effacer', command=lambda:cn.remove(canvas)).pack(side='left')
        bsave=tk.Button(f2,text='Enregistrer', command=lambda:cn.save(tl4, canvas, Long, Larg)).pack(side='left')
        bquit=tk.Button(f2,text='Retour au menu principal', command=lambda:cn.retour_menu(root, tl4)).pack(side='left')

        f2.pack(side='bottom') # on affiche la frame

    
