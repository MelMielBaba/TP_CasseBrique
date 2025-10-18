# -*- coding: utf-8 -*-
"""
Date de creation : 7 octobre 2025
Auteurs: Marie Louise MILLIEN & Elouen WURMSER
Projet: TP4 - CasseBrique
Titre: Fichier de la classe de la raquette (MODELE)
"""

#Description
"""
Description:
    Ce fichier est le fichier 'MODELE' de la raquette, son but est de representer la 
    raquette comme un objet python uniquement, sans aspect graphique et sans visuel 
    Tkinter
    Ce fichier creer donc la classe Raquette qui possede des attributs positions, 
    taille, vitesse et des methodes comme se deplacer (logiquement), actions que 
    l'objet sait faire seul
    Cette classe ne sait pas qu’elle sera dessinée, elle ne connaît pas le canvas, ni 
    Tkinter, elle ne fait que gérer ses coordonnées et son comportement (puis le 
    fichier 'VUE' utilisera ensuite ses coordonnées pour afficher le rectangle à la 
    bonne position)
"""

#Importation du fichier des constantes
import TP4_Constantes as C

class Raquette():
    def __init__(self):
        #Recuperation des constantes
        self.__r_larg = C.C_LARGEUR_RAQUETTE
        self.__r_haut = C.C_HAUTEUR_RAQUETTE
        self.__r_vitesse = C.C_VITESSE_RAQUETTE

        #Position logique initiale de la balle (pas graphique)
        self.__r_posx = self.__r_larg/2
        self.__r_posy = self.__r_haut/2

    def get_position_raquette(self):
        """
        Fonction : Getter de position de la barre (a noter que la position y ne 
        change jamais)
        Entree : None
        Sortie : Couple posX,posY (TUPPLE)
        """
        return (self.__r_posx, self.__r_posy)
    
    def deplacement_barre(self,db_direction:str):
        """
        Fonction : Gere le deplacement logique de la barre en fonction d'une direction
        Entree : un evenement de tkinter
        Sortie : None
        """
        print(db_direction)

        #deplacement a gauche
        if db_direction == 'gauche':
            self.__r_posx -= self.__r_vitesse
            print("Deplacement gauche")

        #deplacement a droite
        elif db_direction == 'droite':
            self.__r_posx += self.__r_vitesse
            print("Deplacement droite")
        
        #on empeche la barre de quitter une position max et min
        self.__r_posx = max(self.__r_larg // 2, min(self.__r_posx, C.C_LARGEUR_CANVAS - self.__r_larg // 2))

