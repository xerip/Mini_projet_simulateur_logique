import tkinter as tk
from tkinter import messagebox as msgbox
from tkinter import filedialog
import taille_niveau as tn
import modif_niveau as mn
import canvas_niveau as cn
import jouer
import os


def niv(root): # s'active lorsque le bouton Creer est presse
    toptaille=tn.fen_taille(root) # execute la fonction fen_taille du module taille_niveau


def Open_lvl(root): # ouvre un niveau choisi dans l'arborescence
    root.state('withdrawn') # cache la fenetre root
    # ouvre une fenetre permettant de choisir un fichier dans l'arborescence, renvoie le chemin du fichier choisi
    chemin = tk.filedialog.askopenfilename(title = "Ouvrir un niveau", parent = root, defaultextension = ".lvl", \
                                                filetypes = [('levels', '.lvl'), ('all files', '.*')])
    if len(chemin) > 0: # si un fichier a bien ete choisi
        # variables #
        test=True
        list_items=[]

        # Toplevel 3 #
        tl3=tk.Toplevel()
        tl3.title(os.path.basename(chemin)) # le nom du fichier choisi en titre de la fenetre
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

        # on cree un canvas qui s'adapte en fonction de la longueur et largeur obtenue 
        canvas=tk.Canvas(tl3,width=32*(Long+2)+2,height=32*(Larg+2)+2)
        
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

        for item in list_items: # pour chaque item dans la liste, on change la couleur du carre d'id obtenu
            if item[1]=='blue':
                canvas.itemconfigure(item[0], fill=item[1], outline='black')
            else:
                canvas.itemconfigure(item[0], fill=item[1], outline='grey')

        canvas.pack() # on affiche le canvas

        # bouton permettant de retourner au menu principal
        bquit=tk.Button(tl3,text='Retour au menu principal', command=lambda:cn.retour_menu(root, tl3)).pack(side='bottom')

# programme principal #
root=tk.Tk() # fenetre principale
root.title('Simulateur logique') # donne un titre a la fenetre
root.geometry('250x78') # donne une taille predefini a la fenetre

# creation d'un bouton Jouer
tk.Button(root, text='Jouer',command=lambda:jouer.fenetre_jouer(root)).pack(fill='x') # s'il est presse, execute la fonction Open_lvl

# creation d'un menu deroulant en pressant le bouton Niveau
#mb=tk.Menubutton(root, text="Niveau", relief='raised')
#menu=tk.Menu(mb, tearoff=False)
#menu.add_command(label="Créer", command=lambda:niv(root))
#menu.add_command(label="Modifier", command=lambda:mn.Modif_lvl(root))
#mb["menu"]=menu
#mb.pack(fill='x') # on affiche le menu
tk.Button(root, text='Creer', command=lambda:niv(root)).pack(fill='x')

# creation d'un bouton pour fermer l'application
tk.Button(root, text='Fermer', command=exit).pack(fill='x')


tk.mainloop()
exit(0)
