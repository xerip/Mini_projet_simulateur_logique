import tkinter as tk
import canvas_niveau as cn


def fen_taille(root): # creation de la fenetre de choix de la taille du niveau
    root.state('withdrawn') # on cache la fenetre principale
    # creation d'une Toplevel #
    tl=tk.Toplevel(root) 
    tl.title("Taille du niveau") # donne un titre a la Toplevel
    # creation d'un label #
    l1=tk.Label(tl, text="Définissez la taille du niveau (hors contours)",bg='white').pack(fill='x')
    # creation d'une frame
    f1=tk.Frame(tl)
    # label ancré a la frame f1
    l2=tk.Label(f1, text="Longueur (2-15 carrés) :  ").pack(side='left')
    longueur=tk.IntVar() # creation d'une variable Int
    longueur.set(2) # on l'initialise a 5
    # creation d'un spinbox avec minimum 2 et maximum 15 comme valeur possible
    spinlong= tk.Spinbox(f1,command=lambda:aug_long(longueur),from_=2,to=15,increment=1,width=5,state='readonly',textvariable=longueur).pack()
    def aug_long(longueur):
        if longueur.get()<=15:
            longueur.set(longueur.get()+1)
        else:
            return 0
    f2=tk.Frame(tl) # creation d'une nouvelle frame
    # label ancré a la frame f2
    l3=tk.Label(f2, text="Largeur (2-15 carrés) :    ").pack(side='left')
    largeur=tk.IntVar() # creation d'une variable IntVar
    largeur.set(2) # on l'initialise a 5
    # creation d'un spinbox avec minimum 2 et maximum 15 comme valeur possible
    spinlong= tk.Spinbox(f2,command=lambda:aug_larg(largeur),from_=2,to=15,increment=1,width=5,state='readonly',textvariable=largeur).pack()
    def aug_larg(largeur):
        if largeur.get()<=15:
            largeur.set(largeur.get()+1)
        else:
            return 0
    f3=tk.Frame(tl) # creation d'une nouvelle frame
    # creation d'un bouton
    # creation de deux boutons dont l'activation va appeler leur fonction predefinie
    b1=tk.Button(f3, text='Valider', command=lambda:val(root,tl,longueur,largeur)).pack(side='left')
    b2=tk.Button(f3, text='Retour', command=lambda:retour(root,tl)).pack(side='left')
    # on affiche les frames
    f1.pack()
    f2.pack()
    f3.pack(side='bottom')
    return tl


def retour(root,tl):
    tl.destroy() # detruit la fenetre tl
    root.state('normal') # fait reapparaitre la fenetre principale

    
def val(root,tl,longueur,largeur): # s'active apres avoir presse le bouton valider
            
    Long=int(longueur.get()) # transforme les valeurs longueur et largeur des spinboxs en entiers
    Larg=int(largeur.get())
    tl.state('withdrawn') # cache la fenetre tl

    # Creation de la Toplevel 2 #
    tl2=tk.Toplevel()
    tl2.title('Création du niveau') # donne un titre a tl2
    # creation d'une frame f4
    f4=tk.Frame(tl2)

    # radioboutons #

    rbvar=tk.StringVar() # creation d'une variable StringVar
    rbv=tk.IntVar() # creation d'une variable IntVar
    rbv2=tk.IntVar() # creation d'une variable IntVar
    rbv3=tk.IntVar() # creation d'une variable IntVar

    # execute la fonction frbdepart du module canvas_niveau quand presse
    bdepart=tk.Radiobutton(f4,text='Placer/Déplacer la case Départ',variable=rbvar,value=rbv,indicatoron=0,command=lambda:cn.frbdepart(canvas)).pack(side='left')
    # execute la fonction frbmur du module canvas_niveau quand presse
    bmur=tk.Radiobutton(f4,text='Construire/Détruire un mur',indicatoron=0,variable=rbvar,value=rbv2,command=lambda:cn.frbmur(canvas)).pack(side='left')
    # execute la fonction frbarrivee du module canvas_niveau quand presse
    barrivee=tk.Radiobutton(f4,text='Placer/Déplacer la case Arrivée',indicatoron=0,variable=rbvar,value=rbv3,command=lambda:cn.frbarrivee(canvas)).pack(side='left')

    # creation d'un canvas selon Long et Larg #
    
    canvas=tk.Canvas(tl2,width=32*(Long+2)+2,height=32*(Larg+2)+2) #adapte le canvas en fct de ce que veut l'utilisateur
    
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

    # creation d'une nouvelle frame ancre a tl2
    f5=tk.Frame(tl2)
    
    # boutons qui activent leur fonctions predefinies situees dans le module canvas_niveau
    
    bremove=tk.Button(f5,text='Tout effacer', command=lambda:cn.remove(canvas)).pack(side='left')
    bsave=tk.Button(f5,text='Enregistrer', command=lambda:cn.save(tl2, canvas, Long, Larg)).pack(side='left')
    bundo=tk.Button(f5,text='Redéfinir la taille du niveau', command=lambda:cn.undo(tl,tl2)).pack(side='left')
    bquit=tk.Button(f5,text='Retour au menu principal', command=lambda:cn.retour_menu(root, tl2)).pack(side='left')

    # on affiche les frames et le canvas
    f4.pack() 
    f5.pack(side='bottom')
    canvas.pack()
