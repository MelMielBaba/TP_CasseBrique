# -*- coding: utf-8 -*-
"""
Date de creation : 7 octobre 2025
Auteurs: Marie Louise MILLIEN & Elouen WURMSER
Projet: TP4 - CasseBrique
Titre: Fichier de la classe des briques (MODELE)
"""

#Description
"""
Description:
    Ce fichier est le fichier 'MODELE' des briques, son but est de representer une 
    brique comme un objet python uniquement, sans aspect graphique et sans visuel 
    Tkinter
    Ce fichier creer donc la classe Brique qui possede des attributs positions, taille,
    etat et des methodes comme détecter une collision avec une balle, actions que 
    l'objet sait faire seul
    Cette classe ne sait pas qu’elle sera dessinée, elle ne connaît pas le canvas, ni 
    Tkinter, elle ne fait que gérer ses coordonnées et son comportement (puis le 
    fichier 'VUE' utilisera ensuite ses coordonnées pour afficher le rectangle de 
    cette brique à la bonne position)
"""

#Importation du fichier des constantes
import TP4_Constantes as C

class Brique:
    def __init__(self,br_posx:int,br_posy:int,br_color:str):
        #Recuperation des attributs donnes en parametres
        self.__br_posx = br_posx
        self.__br_posy = br_posy
        self.__br_color = br_color

        #Recuperation des constantes
        self.__br_larg = C.C_LARGEUR_BRIQUE
        self.__br_haut = C.C_HAUTEUR_BRIQUE

        #Etat de la brique : si elle est 'en vie' c'est True
        self.__br_etat = True
    
    def get_etat_brique(self):
        """
        Fonction : Getter de l'etat de la brique
        Entree : None
        Sortie : Etat (BOOL)
        """
        return self.__br_etat

    def touchee_par_balle(self,tpb_balle:object):
        """
        Fonction : Passe l'etat a "detruite" = False quand la brique est touche par la balle
        Entree : Une balle (OBJ)
        Sortie : None
        """
        #Recuperation des positions de la balle
        tpb_b_posx,tpb_b_posy = tpb_balle.get_position_balle()

        #Cas ou la balle touche effectivement la brique
        if (self.__br_posx - self.__br_larg // 2) < tpb_b_posx < (self.__br_posx + self.__br_larg // 2):
            if (self.__br_posy - self.__br_haut // 2) < tpb_b_posy < (self.__br_posy - self.__br_haut // 2):
                self.__br_etat = False
                print("Brique detruite")