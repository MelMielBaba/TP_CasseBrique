# -*- coding: utf-8 -*-
"""
Date de creation : 7 octobre 2025
Auteurs: Marie Louise MILLIEN & Elouen WURMSER
Projet: TP4 - CasseBrique
Titre: Fichier de la classe Raquette
"""

class Raquette():
    def __init__(self,r_manager):
        self.__long = 5 #Longueur initiale de la barre
        self.__haut = 2 #Heuteur FIXE de la barre
        #position initiale de la balle
        self.__xbarre = r_manager.get_largeur_canvas()/2
        self.__ybarre = r_manager.get_hauteur_canvas/2
    
    def deplacement_barre(self,event):
        db_touche = event.keysym
        print(db_touche)

        #deplacement a gauche
        if db_touche == 'q':
            pass