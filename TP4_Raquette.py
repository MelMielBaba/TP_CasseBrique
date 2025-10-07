# -*- coding: utf-8 -*-
"""
Date de creation : 7 octobre 2025
Auteur: Marie Louise MILLIEN & Elouen WURMSER
Projet: TP4 - Casse-Brique
Titre: Fichier de la classe Raquette
"""

class Raquette():
    def __init__(self,largeur_canvas:int,hauteur_canvas:int):
        self.__long = 5 #Longueur initiale de la barre
        self.__haut = 2 #Heuteur FIXE de la barre
        #position initiale de la balle
        self.__xbarre = largeur_canvas/2
        self.__ybarre = hauteur_canvas/2
    
    def deplacement_barre(self,event):
        db_touche = event.keysym
        print(db_touche)

        #deplacement a gauche
        if db_touche == 'q':
            pass