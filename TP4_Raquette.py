# -*- coding: utf-8 -*-
"""
Date de creation : 7 octobre 2025
Auteurs: Marie Louise MILLIEN & Elouen WURMSER
Projet: TP4 - CasseBrique
Titre: Fichier de la classe Raquette
"""



#Importation du fichier des constantes
import TP4_Constantes as C

class Raquette():
    def __init__(self):
        #Recuperation des constantes
        self.__r_long = C.C_LARGEUR_RAQUETTE
        self.__r_haut = C.C_HAUTEUR_RAQUETTE
        self.__r_vitesse = C.C_VITESSE_RAQUETTE

        #recuperation des infos du canevas
        self.r_lc = C.C_LARGEUR_CANVAS
        self.r_hc = C.C_HAUTEUR_CANVAS

        #position initiale de la balle
        self.__r_xbarre = self.r_lc/2
        self.__r_ybarre = self.r_hc/2


    def get_r_xbarre(self):
        return self.__r_xbarre
    
    def set_r_xbarre(self,srxb_position:int):
        self.__r_xbarre = srxb_position
        
    def change_xbarre(self,cxb_valeur:int):
        """
        Fonction : modifie la valeur de la position en y en ajoutant 
        une valeur (exemple pour 5 y+5 ou y-5)
        Entree : la valeur a ajouter (INT)
        Sortie : None
        """
        self.__r_xbarre += cxb_valeur

    def deplacement_barre(self,event):
        """
        Fonction : Gere le deplacement de la barre en fonction des touches du clavier
        Entree : un evenement de tkinter
        Sortie : None
        """
        db_touche = event.keysym
        print(db_touche)

        #deplacement a gauche
        if db_touche == 'q' or db_touche == 'Left':
            self.change_xbarre(+self.__r_vitesse)
            print("Deplacement gauche")

        #deplacement a droite
        elif db_touche == 'd' or db_touche == 'Right':
            self.change_xbarre(-self.__r_vitesse)
            print("Deplacement droite")

