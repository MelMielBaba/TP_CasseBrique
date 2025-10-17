# -*- coding: utf-8 -*-
"""
Date de creation : 7 octobre 2025
Auteurs: Marie Louise MILLIEN & Elouen WURMSER
Projet: TP4 - CasseBrique
Titre: Fichier de la balle (MODELE)
"""

#Description
"""
Description:
    Ce fichier est le fichier 'MODELE' de la balle, son but est de representer la 
    balle comme un objet python uniquement, sans aspect graphique et sans visuel 
    Tkinter
    Ce fichier creer donc la classe Balle qui possede des attributs positions, taille,
    vitesse et des methodes se déplacer, rebondir, détecter une collision, des actions 
    que l'objet sait faire seul
    Cette classe ne sait pas qu’elle sera dessinée, elle ne connaît pas le canvas, ni 
    Tkinter, elle ne fait que gérer ses coordonnées et son comportement (puis le 
    fichier 'VUE' utilisera ensuite ses coordonnées pour afficher le cercle à la bonne 
    position)
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

        #position initiale de la balle
        self.__bl_posx = C.C_LARGEUR_CANVAS // 2
        self.__bl_posy = C.C_HAUTEUR_CANVAS // 2

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
    #►en x
    def get_xballe(self):
        return self.__xballe

    def set_xballe(self,sxb_coordx:int):
        self.__xballe += sxb_coordx

    #►en y
    def get_yballe(self):
        return self.__yballe

    def set_yballe(self,sxb_coordy:int):
        self.__yballe += sxb_coordy
    
    #Getter et Setter des coordonees de vitesse
    #►en dx
    def get_vxballe(self):
        return self.__vxballe

    def set_vxballe(self,svxb_coordvx:int):
        self.__vxballe += svxb_coordvx
    
    #►en dy
    def get_vyballe(self):
        return self.__vyballe

    def set_vyballe(self,svyb_coordvy:int):
        self.__vyballe += svyb_coordvy
    
    #Methodes de la balle
    def rebond_balle(self):
        """
        Fonction: Methode des rebonds de la balle
        Entree: None
        Sortie: None
        """
        #Rebond vers la gauche
        if self.__xballe - self.__rayon + self.__vxballe < 0 :
            self.set_xballe(2 * self.__rayon - self.__xballe)
            self.set_vxballe(-self.__vxballe)
        
        #Rebond vers la droite
        elif self.__xballe + self.__rayon + self.__vxballe > self.b_lclc :
            self.set_xballe(2 * (self.b_lc - self.__rayon) - self.__xballe)
            self.set_vxballe(-self.__vxballe)
        
        #Rebond vers le bas 
        elif self.__yballe + self.__rayon + self.__vyballe > self.b_hc :
            self.set_yballe(2 * (self.b_hc - self.__rayon) - self.__yballe)
            self.set_vyballe(-self.__vyballe)

        #Rebond vers le haut (cas de collision avec la barre)
        elif self.__yballe - self.__rayon + self.__vyballe < 0 :
            self.set_yballe(2 * self.__rayon - self.__yballe)
            self.set_vyballe(-self.__vyballe)
        
        else :
            self.set_xballe(self.__xballe + self.__vxballe)
            self.set_yballe(self.__yballe + self.__vyballe)