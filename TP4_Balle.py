# -*- coding: utf-8 -*-
"""
Date de creation : 7 octobre 2025
Auteurs: Marie Louise MILLIEN & Elouen WURMSER
Projet: TP4 - CasseBrique
Titre: Fichier de la Balle
"""
import TP4_Constantes as c
import random as rd
import math as m

class Balle:
    def __init__(self, canvas, x=None, y=None, rayon=c.RAYON_BALLE, vitesse=c.VITESSE_BALLE, color="white"):
        self.canvas = canvas
        self.rayon = rayon
        self.speed = vitesse
        # initial position
        self.x = x if x is not None else float(canvas.winfo_reqwidth())/2
        self.y = y if y is not None else float(canvas.winfo_reqheight()) - 120
        # direction initiale : vers le haut, angle aléatoire
        angle = rd.uniform(m.radians(25), m.radians(155))
        self.vx = self.speed * m.cos(angle)
        self.vy = -abs(self.speed * m.sin(angle))

        # dessin
        self.id = self.canvas.create_oval(self.x - rayon, self.y - rayon,
                                          self.x + rayon, self.y + rayon,
                                          fill=color, outline="black")

    # getters
    # [left, top, right, bottom]
    def coords(self):
        return self.canvas.coords(self.id)

    def center(self):
        l, t, r, b = self.coords()
        return ((l + r) / 2, (t + b) / 2)

    def set_position(self, x, y):
        self.x = x
        self.y = y
        self.canvas.coords(self.id, x - self.rayon, y - self.rayon, x + self.rayon, y + self.rayon)

    def rebond_x(self):
        self.vx = -self.vx

    def rebond_y(self):
        self.vy = -self.vy

    def aug_vitesse(self, factor=c.FACTOR):
        self.vx *= factor
        self.vy *= factor
        self.speed *= factor

    def reset(self, x=None, y=None):
        # replacer la balle (utilisé après perte de vie)
        canvas_w = int(self.canvas['width'])
        canvas_h = int(self.canvas['height'])
        x = x if x is not None else canvas_w / 2
        y = y if y is not None else canvas_h - 120
        angle = rd.uniform(m.radians(25), m.radians(155))
        self.vx = self.speed * m.cos(angle)
        self.vy = -abs(self.speed * m.sin(angle))
        self.set_position(x, y)

    def move(self):
        # déplacement par frame
        self.x += self.vx
        self.y += self.vy
        self.canvas.coords(self.id, self.x - self.rayon, self.y - self.rayon, self.x + self.rayon, self.y + self.rayon)

    def position(self):
        # renvoie le centre
        return self.center()
