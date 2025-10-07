# -*- coding: utf-8 -*-
"""
Date de creation : 7 octobre 2025
Auteurs: Marie Louise MILLIEN & Elouen WURMSER
Projet: TP4 - CasseBrique
Titre: Fichier de la Balle
"""

#Importation des modules
import tkinter as tk
import random as rd
import math as m

class Balle:
    def __init__(self,rayon:int,largeur_canvas:int,hauteur_canvas:int):
        self.__ray = rayon
        #position initiale de la balle
        self.__xballe = largeur_canvas/2
        self.__yballe = hauteur_canvas/2
        #direction initiale de la balle
        self.__vit = 1
        self.__angle = rd.uniform(0,2*m.pi)
        #coordonnees vitesse initiales (angle = 0)
        self.__vx = self.__vit*m.cos(self.__angle)
        self.__vy = self.__vit*m.sin(self.__angle)
        #recuperation des infos du canevas
        self.lc = largeur_canvas
        self.hc = hauteur_canvas
    
    #Getter et Setter de la vitesse (sera utile quand on voudra faire aller le jeu plus vite)
    def get_vitesse(self):
        return self.__vit

    def set_vitesse(self,sv_vitesse:int):
        self.__vit += sv_vitesse

    #Getter et Setter des coordonees de position
    def get_xballe(self):
        return self.__xballe

    def set_xballe(self,sxb_coordx:int):
        self.__xballe += sxb_coordx

    def get_yballe(self):
        return self.__yballe

    def set_yballe(self,sxb_coordy:int):
        self.__yballe += sxb_coordy
    
    #Getter et Setter des coordonees de vitesse
    def get_vxballe(self):
        return self.__vx

    def set_vxballe(self,svxb_coordvx:int):
        self.__vx += svxb_coordvx
    
    def get_vyballe(self):
        return self.__vy

    def set_vyballe(self,svyb_coordvy:int):
        self.__vy += svyb_coordvy
    

    def rebond_balle(self):
        """
        Fonction: Methode des rebonds de la balle
        Entree: 
        Sortie: 
        """
        #Rebond a gauche
        if self.__xballe - self.__ray + self.__vx < 0 :
            self.set_xballe(2 * self.__ray - self.__xballe)
            self.set_vxballe(-self.__vx)
        
        #Rebond a droite
        elif self.__xballe + self.__ray + self.__vx > self.lc :
            self.set_xballe(2 * (self.lc - self.__ray) - self.__xballe)
            self.set_vxballe(-self.__vx)
        
        #Rebond en bas 
        elif self.__yballe + self.__ray + self.__vy > self.hc :
            self.set_yballe(2 * (self.hc - self.__ray) - self.__yballe)
            self.set_vyballe(-self.__vy)

        #Rebond en haut (cas de collision avec la barre)
        elif self.__yballe - self.__ray + self.__vy < 0 :
            self.set_yballe(2 * self.__ray - self.__yballe)
            self.set_vyballe(-self.__vy)
        
        else :
            self.set_xballe(self.__xballe + self.__vx)
            self.set_yballe(self.__yballe + self.__vy)