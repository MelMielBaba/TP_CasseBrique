# -*- coding: utf-8 -*-

#►►EN-TÊTE◄◄
"""
=========================================================================================
Date de creation : 7 octobre 2025
Auteurs: Marie Louise MILLIEN & Elouen WURMSER
Projet: TP4 - CasseBrique
Titre: Fichier de la raquette
=========================================================================================
Description :
    Dans ce fichier on créer la classe de l'objet raquette. Il s'agit d'une classe 
    uniquement logique n'utilisant aucunes spécificités de tkinter afin de pas mélanger 
    les deux.
=========================================================================================
"""

#►►IMPORTATIONS◄◄
import TP4_Constantes as c

#►►CREATION OBJET RAQUETTE◄◄
class Raquette:
    """
    Fonction : Gere l'objet logique Raquette
    Attributs : > self.largeur_canva : recupere la largeur du canvas
                > self.hauteur_canva : recupere la hauteur du canvas
                > self.largeur_raquette : recupere la largeur en constantes
                > self.hauteur_raquette : recupere la hauteur en constantes
                > self.vitesse_raquette : recupere la vitesse en constantes
                > self.x_center : position du centre de la raquette
                > self.y : position en y de la raquette sur le canvas
    Methodes : > get_x_center() : getter de la position centrale
               > set_x_center(x) : setter de la position centrale
               > move_by(dx) : ajoute un entier à la position centrale 
               > deplacement_barre(event) : gestion des deplacement de la raquette avec le 
               clavier
    """
    def __init__(self, largeur_canva=c.LARGEUR_CANVA, hauteur_canva=c.HAUTEUR_CANVA):
        #Attributs donnés à la création de l'objet
        self.largeur_canva = largeur_canva
        self.hauteur_canva = hauteur_canva

        #Recuperation des constantes
        self.largeur_raquette = c.LARGEUR_RAQUETTE
        self.hauteur_raquette = c.HAUTEUR_RAQUETTE
        self.vitesse_raquette = c.VITESSE_RAQUETTE

        #Position centre (x)
        self.x_center = self.largeur_canva / 2

        #y fixe (bas du canvas)
        self.y = self.hauteur_canva - 40

    def get_x_center(self):
        """
        Fonction : Getter de la position du centre
        Entree : None
        Sortie : Attribut self.x_center
        """
        return self.x_center

    def set_x_center(self, x:int):
        """
        Fonction : Setter de la position du centre en fonction d'un parametre x (INT)
        Entree : Un entier x (INT)
        Sortie : None
        """
        half = self.largeur_raquette / 2

        #Cas [?]
        if x - half < 0:
            x = half
        
        #Cas [?]
        elif x + half > self.largeur_canva:
            x = self.largeur_canva - half
        
        self.x_center = x

    def move_by(self, dx:int):
        """
        Fonction : Ajoute une valeur (negative ou positive) dx à l'attribut self.x_center
        Entree : Un entier dx (INT)
        Sortie : None
        """
        self.set_x_center(self.x_center + dx)

    def deplacement_barre(self, event):
        """
        Fonction : Deplace la raquette en fonction des touches clavier; Si 'LEFT'(<) ou 
        'q' la raquette est deplacer a gauche, a droite si 'RGIHT'(>) OU 'D'
        Entree : Un evenement
        Sortie : None
        """
        #event.keysym fournit 'Left'/'Right' etc
        key = event.keysym

        #Deplacement gauche
        if key in ('Left', 'q'):
            self.move_by(-self.vitesse_raquette)

        #Deplacement droite
        elif key in ('Right', 'd'):
            self.move_by(self.vitesse_raquette)
