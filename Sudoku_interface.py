"""
Créé le Sa 12/8/2016 à 23:36
Auteur : Nate
"""

from sudoku import *


## Fonctions graphiques

def verif () :
    """ Cette fonction vérifie que les cases de la grille ont été remplies par des entiers
    de 0 à 9. Elle renvoie True le cas échéant, ou lève une exception sinon. """
    for k in range(81) :
        a = var[k].get()
        try :
            a = int(a)
        except :
            raise TypeError
        if a<0 or a>=10 :
            raise ValueError
    return True


def nettoyer (b, c) :
    """ Cette fonction supprime le cadre de la page 1 et modifie les éléments qui restent dans la page 2. """
    global fr
    fr[0].destroy()
    if b :
        lab1["text"]="Grille résolue (en "+str(c)+" étapes)"
    else :
        lab1["text"]="Grille insoluble (déterminé en "+str(c)+" étapes)"
    bou1["text"]="Quitter"
    bou1["command"]=fe.destroy
    bou1.grid(row=3)


def affiche_carres (fram) :
    """ Cette fonction affiche les carrés d'une grille de sudoku sous forme de cadres noirs."""
    fr=[]
    for k in range(9) :
        fr.append(Frame(fram, bg="black", bd=5, height=100, width=100))
        fr[k].grid(row=k//3, column=k%3)
    return fr


def affiche_cases (car1, car2, car3, ligne) :
    """ Cette fonction affiche les cases d'une grille de sudoku sur la ligne précisée et sur les carrés adéquats. """
    can = []
    for k in range(9) :
        if k//3==0 :
            can.append(Canvas(car1, bg="white", height=20, width=20))
        elif k//3==1 :
            can.append(Canvas(car2, bg="white", height=20, width=20))
        elif k//3==2 :
            can.append(Canvas(car3, bg="white", height=20, width=20))
        can[k].grid(row=ligne, column=k%3, padx=2, pady=2)
        #can[k].create_line(10, 0, 10, 20, fill="red")
        #can[k].create_line(0, 10, 20, 10, fill="red")
    return can


def affiche_chiffre (chiffre, case) :
    """ Cette fonction affiche le chiffre spécifié dans la case spécifiée. """
    case.create_text(11, 11, text=chiffre)


def deuxieme_page (b, c) :
    """ Cette fonction affiche la deuxième page.
    
    Elle supprime le cadre de la page 1 et modifie les éléments restants par l'appel à 'nettoyer'.
    Puis elle crée deux grilles vierge (avec 'affiche_carre' et 'affiche_case') """
    nettoyer(b, c)
    Label(fe, text="grille initiale :").grid(row=1,column=0)
    if b :
        Label(fe, text="grille résolue :").grid(row=1, column=1)
    else :
        Label(fe, text="grille finale :").grid(row=1, column=1)
    fr1.grid(row=2, column=0, sticky="w", padx=5)
    fr2.grid(row=2, column=1, sticky="e", padx=5)
    list_car1 = affiche_carres(fr1)
    list_car2 = affiche_carres(fr2)
    list_can1 = []
    list_can2 = []
    for i in range(9) :
        if i//3==0 :
            list_can1.append(affiche_cases(list_car1[0], list_car1[1], list_car1[2], i%3))
        elif i//3==1 :
            list_can1.append(affiche_cases(list_car1[3], list_car1[4], list_car1[5], i%3))
        elif i//3==2 :
            list_can1.append(affiche_cases(list_car1[6], list_car1[7], list_car1[8], i%3))
    for j in range(9) :
        if j//3==0 :
            list_can2.append(affiche_cases(list_car2[0], list_car2[1], list_car2[2], j%3))
        elif j//3==1 :
            list_can2.append(affiche_cases(list_car2[3], list_car2[4], list_car2[5], j%3))
        elif j//3==2 :
            list_can2.append(affiche_cases(list_car2[6], list_car2[7], list_car2[8], j%3))
    return list_can1, list_can2


def validation () :
    """ Cette fonction est appelée par le bouton de validation pour passer à la deuxième page.
    
    Elle vérifie que la grille de la page 1 a été correctement remplie, puis affiche la 
    deuxième page, et remplie les deux nouvelles grilles. """
    M = array([[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0]])
    if not verif() :
        return None
    for i in range(9) :
        for j in range(9) :
            a = var[i*9+j].get()
            M[i, j] = int(a)
    grille = M.copy()
    (reussi, grille, compte, cases_init) = resolution(grille)
    (cases1, cases2) = deuxieme_page(reussi, compte)
    for i in range(9) :
        for j in range(9) :
            if M[i, j]!=0 :
                affiche_chiffre(str(M[i, j]), cases1[i][j])
            if grille[i, j]==0 :
                raise ValueError
            affiche_chiffre(str(grille[i, j]), cases2[i][j])



## Fenêtre

fe = Tk()
fe.title("Résolution de Sudoku")

## Données

contour = 5
longent = 3

## Widgets

# page 1 et 2

lab1 = Label(fe, text="Remplissez la grille initiale :")
bou1 = Button(fe, text="Valider", command=validation)

# page 1

fr = []
ent = []
var = []

for k in range(10) :
    if k==0 :
        fr.append(Frame(fe, bd=contour, relief="ridge"))
    else :
        fr.append(Frame(fr[0], bd=contour, relief="groove"))


for k in range(81) :
    var.append(StringVar())
    var[k].set("0")


for i in range(9) :
    for j in range(9) :
        if i//3==0 :
            if j//3==0 :
                ent.append(Entry(fr[1], width=longent, textvariable=var[i*9+j]))
            elif j//3==1 :
                ent.append(Entry(fr[2], width=longent, textvariable=var[i*9+j]))
            elif j//3==2 :
                ent.append(Entry(fr[3], width=longent, textvariable=var[i*9+j]))
        elif i//3==1 :
            if j//3==0 :
                ent.append(Entry(fr[4], width=longent, textvariable=var[i*9+j]))
            elif j//3==1 :
                ent.append(Entry(fr[5], width=longent, textvariable=var[i*9+j]))
            elif j//3==2 :
                ent.append(Entry(fr[6], width=longent, textvariable=var[i*9+j]))
        elif i//3==2 :
            if j//3==0 :
                ent.append(Entry(fr[7], width=longent, textvariable=var[i*9+j]))
            elif j//3==1 :
                ent.append(Entry(fr[8], width=longent, textvariable=var[i*9+j]))
            elif j//3==2 :
                ent.append(Entry(fr[9], width=longent, textvariable=var[i*9+j]))

# page 2

fr1 = Frame(fe, bg="grey", height=300, width=300)
fr2 = Frame(fe, bg="grey", height=300, width=300)

## Localisation

lab1.grid(row=0, column=0, columnspan=2)

for k in range(10) :
    if k==0 :
        fr[k].grid(row=1, column=0)
    else :
        fr[k].grid(row=(k-1)//3, column=(k-1)%3)

for i in range(9) :
    for j in range(9)  :
        ent[i*9+j].grid(row=i%3, column=j%3)

bou1.grid(row=2, column=0, columnspan=2)


## Boucle

fe.mainloop()

