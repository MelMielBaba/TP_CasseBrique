# -*- coding: utf-8 -*-

#►►EN-TÊTE◄◄
"""
=========================================================================================
Date de creation : 7 octobre 2025
Auteurs: Marie Louise MILLIEN & Elouen WURMSER
Projet: TP4 - CasseBrique
Titre: Fichier de la balle
=========================================================================================
Description :
    Dans ce fichier on créer la classe de l'objet balle.
=========================================================================================
"""

#►►IMPORTATIONS◄◄
"""Importation des fichiers"""
import TP4_Constantes as c

"""Importation des modules"""
import random as rd
import math as m

#►►CREATION OBJET BALLE◄◄
class Balle:
    """
    Fonction : Gere l'objet Balle
    Attributs : > self.canvas : recupere le canvas
                > self.rayon : recupere le rayon en constantes
                > self.speed : recupere la vitesse en constantes
                > self.x : position en x
                > self.y : position en y
                > self.dx : direction selon x
                > self.dy : direction selon y
                > self.id : créer l'oval' representant la balle sur le canvas
    Methodes : > coords() : renvoie les coordonnées graphique de la balle
               > center() : renvoie les coordonnées du centre de la balle
               > set_position(x,y) : modifie les positions logique et graphique de la 
               balle
               > rebond_x() : inverse la direction selon x
               > rebond_y() : inverse la direction selon y
               > aug_vitesse(factor) : modifie les directions et la vitesse en fonction 
               d'un facteur
               > reset(x,y) : reinitialise la balle
               > move() : deplacement de la balle
               > position() : renvoie les coordonnees du centre de la balle
    """
    def __init__(self, canvas, x=None, y=None, rayon=c.RAYON_BALLE, vitesse=c.VITESSE_BALLE, color="white"):
        #Recuperation des attributs
        self.canvas = canvas
        
        #Recuperation des constantes
        self.rayon = rayon
        self.speed = vitesse

        #Positions initiales
        self.x = x if x is not None else float(canvas.winfo_reqwidth())/2
        self.y = y if y is not None else float(canvas.winfo_reqheight()) - 120

        #Direction initiale 
        """Vers le haut, angle aléatoire"""
        angle = rd.uniform(m.radians(25), m.radians(155))
        self.vx = self.speed * m.cos(angle)
        self.vy = -abs(self.speed * m.sin(angle))

        #Dessin
        self.id = self.canvas.create_oval(self.x - rayon, self.y - rayon,
                                          self.x + rayon, self.y + rayon,
                                          fill=color, outline="black")

    def coords(self):
        """
        Fonction : Renvoie les coordonnees graphiques de la balle
        Entree : None
        Sortie : Les coordonnées graphique de la balle (INT)
        """
        return self.canvas.coords(self.id)

    def center(self):
        """
        Focntion : Renvoie les coordonnees du centre de la balle (graphiquement)
        Entree : None
        Sortie : Le couple des coordonnees du centre de la balle (TUPPLE)
        """
        l, t, r, b = self.coords()
        return ((l + r) / 2, (t + b) / 2)

    def set_position(self, x:int, y:int):
        """
        Fonction : Modifie la position (logique & graphique) de la balle en fonction de 
        deux entiers x et y
        Entrees : Deux entiers x et y (INT)
        Sortie : None
        """
        self.x = x
        self.y = y
        self.canvas.coords(self.id, 
                           x - self.rayon, 
                           y - self.rayon, 
                           x + self.rayon, 
                           y + self.rayon)

    def rebond_x(self):
        """
        Fonction : Inverse la direction selon x
        Entree : None
        Sortie : None
        """
        self.vx = -self.vx

    def rebond_y(self):
        """
        Fonction : Inverse la direction selon y
        Entree : None
        Sortie : None
        """
        self.vy = -self.vy

    def aug_vitesse(self, factor=c.FACTOR):
        """
        Fonction : Modifie les directions et la vitesse en fonction d'un facteur
        Entree : Un facteur d'accélération (FLOAT)
        Sortie : None
        """
        self.vx *= factor
        self.vy *= factor
        self.speed *= factor

    def reset(self, x=None, y=None):
        """
        Fonction : Réinitialise la balle à zero avec les parametres donnes au depart dans le __init__
        Entree : Deux entiers x et y 
        Sortie : None
        """
        #Recuperation des information du canvas
        canvas_w = int(self.canvas['width'])
        canvas_h = int(self.canvas['height'])

        #Repositionner la balle (utilisé après perte de vie)
        x = x if x is not None else canvas_w / 2
        y = y if y is not None else canvas_h - 120

        #Redéfinir l'angle et la direction
        angle = rd.uniform(m.radians(25), m.radians(155))
        self.vx = self.speed * m.cos(angle)
        self.vy = -abs(self.speed * m.sin(angle))

        #Modifier la position
        self.set_position(x, y)

    def move(self):
        """
        Fonction : Gestion des deplacements de la balle
        Entree : None
        Sortie : None
        """
        #Deplacement logique
        self.x += self.vx
        self.y += self.vy

        #Deplacement graphique
        self.canvas.coords(self.id, self.x - self.rayon, self.y - self.rayon, self.x + self.rayon, self.y + self.rayon)

    def position(self):
        """
        Fonction : Renvoie les coordonnees du centre de la balle
        Entree : None
        Sortie : Coordonnees du centre de la balle (TUPPLE)
        """
        return self.center()
