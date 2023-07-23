# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 22:51:51 2015

@author: Natanaël Carpentier
"""

from pylab import *
from tkinter import *

M=array([[5,3,0,0,7,0,0,0,0],[6,0,0,1,9,5,0,0,0],[0,9,8,0,0,0,0,6,0],[8,0,0,0,6,0,0,0,3],[4,0,0,8,0,3,0,0,1],[7,0,0,0,2,0,0,0,6],[0,6,0,0,0,0,2,8,0],[0,0,0,4,1,9,0,0,5],[0,0,0,0,8,0,0,7,9]])

## Tests de chiffre

def test_ligne (i,j,n,M) :
    """ Cette fonction renvoie False si la valeur n est présente dans la ligne i de la grille M, True sinon."""
    for x in M[i]:
        if x==n:
            return False
    return True



def test_colonne (i,j,n,M) :
    """ Cette fonction renvoie False si la valeur n est présente dans la colonne j de la grille M, True sinon."""
    for x in M[:,j]:
        if x==n:
            return False
    return True



def test_carre (i,j,n,M) :
    """ Cette fonction renvoie False si la valeur n est présente dans le carré de la grille M contenant la case (i, j), True sinon."""
    ci=i//3
    cj=j//3
    for x in (3*ci,3*ci+1,3*ci+2):
        for y in (3*cj,3*cj+1,3*cj+2):
            if M[x,y]==n:
                return False
    return True



def test (i,j,n,M) :
    """Cette fonction regroupe les tests de ligne, de colonne et de carré."""
    return test_ligne(i,j,n,M) and test_colonne(i,j,n,M) and test_carre(i,j,n,M)

## Enregistrement de la grille initiale

def protection (M) :
    """ Cette fonction enregistre les coordonnées des cases qui sont initialement renseignées.
    Ces cases resteront inchangées."""
    orig=[]
    for i in range(len(M)):
        for j in range(len(M[i])):
            if M[i,j]!=0:
                orig.append((i,j))
    return orig

## Parcours de la grille

def case_suivante (i,j,protect) :
    """ Cette fonction renvoie les coordonnées de la première case à remplir APRES la case de coordonnées (i, j).
    Renvoie (9, 0) si toutes les cases ont été remplies.
    Utilisé si la case (i, j) a été remplie correctement."""
    l=i
    c=j
    if c<8:
        c+=1
    else:
        c=0
        l+=1
    if l==9:
        return (l,c)
    while (l,c) in protect:
        if c<8:
            c+=1
        else:
            c=0
            l+=1
        if l==9:
            return (l,c)
    return (l,c)



def case_precedente (i,j,protect) :
    """ Cette fonction renvoie les coordonnées de la première case à remplir AVANT la case de coordonnées (i, j).
    Renvoie (-1, 8) si aucune case n'a pu être remplie.
    Utilisé si la case (i, j) n'a pas été remplie correctement."""
    l=i
    c=j
    if c>0:
        c-=1
    else:
        c=8
        l-=1
    if l==-1:
        return (l,c)
    while (l,c) in protect:
        if c>0:
            c-=1
        else:
            c=8
            l-=1
        if l==-1:
            return (l,c)
    return (l,c)

## Remplissage d'une case

def remplissage (i,j,M) :
    """ Cette fonction rempli la case de coordonnées i, j de la grille M.
    Elle incrémente pour cela la valeur de la case, et teste cette valeur.
    Si une valeur correspond, elle la place et renvoie True ;
    sinon elle place 0 et renvoie False.
    (à défaut d'incrémentation la case vaut 0)"""
    for n in range(M[i,j],10): # Pöur n=M[i,j], test renvoie False ...
        if test(i,j,n,M):
            M[i,j]=n
            return True
    M[i,j]=0
    return False

## Résolution de la grille

def choix_grille () :
    """ Cette fonction permet de remplir manuellement une grille de sudoku (en mode console)."""
    M = array([[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0]])
    for i in range(9) :
        for j in range(9) :
            a = input("Valeur en coordonnées ("+str(i)+", "+str(j)+") : ")
            try :
                M[i, j] = int(a)
            except :
                pass
    return M



def resolution (M=0) :
    """ Cette fonction tente de résoudre une grille de Sudoku.
    Si aucune grille n'est précisée, vous devrez la remplir manuellement.
    Elle parcourt les cases de gauche à droite dans chaque ligne, et les lignes de haut en bas.
    Elle tente de remplir une case (par incrémentation) puis passe à la suivante en cas de succès
    ou revient sur la valeur de la précédente en cas d'échéc.
    Les cases pré-remplies restent bien évidemment inchangées durant cette opération !!!
    Elle renvoie le nombre d'étape nécessaire pour résoudre la grille ou déterminer qu'elle est insoluble."""
    
    """ Si la gille est explicitement initialement insoluble, le programme prend beaucoup de temps pour trouver ce résultat
    car il teste toutes les combinaisons possible !!!"""
    if type(M)==int :
        M = choix_grille()
    #print(M, "\n")
    
    # enregistrement des cases "protégés"
    protect = protection(M)
    # indice de ligne
    ligne = 0
    # indice de colonne
    colonne = 0
    # compteur d'étape
    compte = 0
    
    if (ligne,colonne) not in protect:
        r = remplissage (ligne, colonne, M)
        compte += 1
        if r:
            (ligne, colonne) = case_suivante (ligne, colonne, protect)
        else:
            (ligne, colonne) = case_precedente (ligne, colonne, protect)
    else:
        (ligne, colonne) = case_suivante (ligne, colonne, protect)
    
    while (ligne, colonne)!=(-1, 8) and (ligne, colonne)!=(9, 0):
        r = remplissage (ligne, colonne, M)
        compte += 1
        if r:
            (ligne, colonne) = case_suivante (ligne, colonne, protect)
        else:
            (ligne, colonne) = case_precedente (ligne, colonne, protect)
    
    compte = str(compte)
    if (ligne, colonne)==(-1, 8):
        #print('La grille est insoluble (résultat déterminé en ' + compte + ' étapes).')
        return False, M, compte, protect
    if (ligne, colonne)==(9, 0):
        #print('La grille est résolvable en ' + compte + ' étapes : ')
        #print(M)
        return True, M, compte, protect















