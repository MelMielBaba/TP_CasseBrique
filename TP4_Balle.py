"""
Date de creation : 7 octobre 2025
Auteurs: Marie Louise MILLIEN & Elouen WURMSER
Projet: TP4 - CasseBrique
Titre: Fichier de gestion de la Balle
"""

import TP4_Constantes as c
import random as rd
import math as m

class Balle:
    """
    On initialise la balle, sur le canvas, avec une position x et y nulle
    Le rayon de la balle/Vitesse correspond à une constante modifiable dans les paramètres
    La couleur de la balle est blanche, elle n'est pas modifiable
    """
    def __init__(self, canvas, x=None, y=None, rayon=c.RAYON_BALLE, vitesse=c.VITESSE_BALLE, color="white"):
        self.canvas = canvas
        self.rayon = rayon
        self.speed = vitesse
        # Vecteur Position initiale de la balle
        self.x = x
        self.y = y
        # Direction initiale de la balle, vers le haut avec un angle aléatoire
        angle = rd.uniform(m.radians(25), m.radians(155))
        # Vecteur Vitesse initiale de la balle
        self.vx = self.speed * m.cos(angle)
        self.vy = -abs(self.speed * m.sin(angle))
        # Creation de la Balle 
        self.id = self.canvas.create_oval(self.x - rayon, self.y - rayon,
                                          self.x + rayon, self.y + rayon,
                                          fill=color, outline="black")

    """
    La fonction coords permet de récupérer les "cotées" de la Balle par rapport au canva
    elle renvoie:
    l=Left,t=Top,r=Right,b=Bottom
    """
    def coords(self):
        return self.canvas.coords(self.id)

    """
    La fonction center permet de trouver le centre de la Balle
    On réalise la moyenne en x et en y, et on retourne les coordonnées du centre de la balle
    (x_centre_balle,y_centre_balle)
    """
    def center(self):
        l, t, r, b = self.coords()
        return ((l + r) / 2, (t + b) / 2)

    """
    La fonction set_position permet de déplacer la balle au dessus de la raquette
    """
    def set_position(self, x, y):
        self.x = x
        self.y = y
        self.canvas.coords(self.id, x - self.rayon, y - self.rayon, x + self.rayon, y + self.rayon)

    """
    La fonction rebond_x change le sens du vecteur vitesse en x
    """
    def rebond_x(self):
        self.vx = -self.vx

    """
    La fonction rebond_y change le sens du vecteur vitesse en y
    """
    def rebond_y(self):
        self.vy = -self.vy

    """
    La fonction aug_vitesse prends en argument FACTOR qui correspond à l'acceleration,
    que la balle prends à chaque frame, le vecteur vitesse est multiplié par un coef
    modifiable dans les options
    """
    def aug_vitesse(self, factor=c.FACTOR):
        acc= (factor-1)/1000 + 1
        self.vx *= acc
        self.vy *= acc
        self.speed *= acc
    """
    La fonction reset permet de replacer la balle après une perte de vie
    """
    def reset(self, x=None, y=None):
        # Angle initiale aléatoire
        angle = rd.uniform(m.radians(25), m.radians(155))
        # Vecteur vitesse initiale
        self.vx = self.speed * m.cos(angle)
        self.vy = -abs(self.speed * m.sin(angle))
        # Déplacement de la balle
        self.set_position(x, y)

    """
    La fonction move permet de calculer le vecteur position de la balle donc mettre a jour
    sa position dans l'espace a chaque frame/image
    """
    def move(self):
        # On accélère la balle
        self.aug_vitesse()
        # Calul du vecteur position
        self.x += self.vx
        self.y += self.vy
        # Déplacement de la balle
        self.canvas.coords(self.id, self.x - self.rayon, self.y - self.rayon, self.x + self.rayon, self.y + self.rayon)
