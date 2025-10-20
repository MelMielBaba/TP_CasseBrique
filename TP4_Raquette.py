# -*- coding: utf-8 -*-
"""
Date de creation : 7 octobre 2025
Auteurs: Marie Louise MILLIEN & Elouen WURMSER
Projet: TP4 - CasseBrique
Titre: Fichier de la classe Raquette
"""


# TP4_Raquette.py
import TP4_Constantes as c

class Raquette:
    def __init__(self, largeur_canva=c.LARGEUR_CANVA, hauteur_canva=c.HAUTEUR_CANVA):
        self.largeur_canva = largeur_canva
        self.hauteur_canva = hauteur_canva
        self.largeur_raquette = c.LARGEUR_RAQUETTE
        self.hauteur_raquette = c.HAUTEUR_RAQUETTE
        self.vitesse_raquette = c.VITESSE_RAQUETTE

        # position centre (x)
        self.x_center = self.largeur_canva / 2
        # y fixe (bas du canvas)
        self.y = self.hauteur_canva - 40

    def get_x_center(self):
        return self.x_center

    def set_x_center(self, x):
        half = self.largeur_raquette / 2
        if x - half < 0:
            x = half
        if x + half > self.largeur_canva:
            x = self.largeur_canva - half
        self.x_center = x

    def move_by(self, dx):
        self.set_x_center(self.x_center + dx)

    def deplacement_barre(self, event):
        # event.keysym fournit 'Left'/'Right' etc
        key = event.keysym
        if key in ('Left', 'q', 'a'):
            self.move_by(-self.vitesse_raquette)
        elif key in ('Right', 'd'):
            self.move_by(self.vitesse_raquette)
        # aussi souris: handled from fenetre (optionnel)
