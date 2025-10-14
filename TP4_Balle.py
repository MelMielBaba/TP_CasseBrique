# -*- coding: utf-8 -*-
"""
Date de creation : 7 octobre 2025
Auteurs: Marie Louise MILLIEN & Elouen WURMSER
Projet: TP4 - CasseBrique
Titre: Fichier de la Balle
"""

#Importation du fichier des constantes
import TP4_Constantes as C

#Importation des modules
import random as rd
import math as m

class Balle:
    def __init__(self):
        #Recuperation des constantes
        self.__rayon = C.C_RAYON_BALLE

        #recuperation des infos du canevas
        self.b_lc = C.C_LARGEUR_CANVAS
        self.b_hc = C.C_HAUTEUR_CANVAS

        #position initiale de la balle
        self.__xballe = self.b_lc/2
        self.__yballe = self.b_hc/2

        #direction initiale de la balle
        self.__b_vit = C.C_VITESSE_BALLE
        self.__b_angle = rd.uniform(0,2*m.pi)

        #coordonnees vitesse initiales (angle = 0)
        self.__vxballe = self.__b_vit*m.cos(self.__b_angle)
        self.__vyballe = self.__b_vit*m.sin(self.__b_angle)
    
    #Getter et Setter de la vitesse (sera utile quand on voudra faire aller le jeu plus vite)
    def get_vitesse_balle(self):
        return self.__b_vit

    def set_vitesse_balle(self,svb_vitesse:int):
        self.__b_vit += svb_vitesse

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
        return self.__vxballe

    def set_vxballe(self,svxb_coordvx:int):
        self.__vxballe += svxb_coordvx
    
    def get_vyballe(self):
        return self.__vyballe

    def set_vyballe(self,svyb_coordvy:int):
        self.__vyballe += svyb_coordvy
    

    def rebond_balle(self):
        """
        Fonction: Methode des rebonds de la balle
        Entree: 
        Sortie: 
        """
        #Rebond a gauche
        if self.__xballe - self.__rayon + self.__vxballe < 0 :
            self.set_xballe(2 * self.__rayon - self.__xballe)
            self.set_vxballe(-self.__vxballe)
        
        #Rebond a droite
        elif self.__xballe + self.__rayon + self.__vxballe > self.b_lclc :
            self.set_xballe(2 * (self.b_lc - self.__rayon) - self.__xballe)
            self.set_vxballe(-self.__vxballe)
        
        #Rebond en bas 
        elif self.__yballe + self.__rayon + self.__vyballe > self.b_hc :
            self.set_yballe(2 * (self.b_hc - self.__rayon) - self.__yballe)
            self.set_vyballe(-self.__vyballe)

        #Rebond en haut (cas de collision avec la barre)
        elif self.__yballe - self.__rayon + self.__vyballe < 0 :
            self.set_yballe(2 * self.__rayon - self.__yballe)
            self.set_vyballe(-self.__vyballe)
        
        else :
            self.set_xballe(self.__xballe + self.__vxballe)
            self.set_yballe(self.__yballe + self.__vyballe)