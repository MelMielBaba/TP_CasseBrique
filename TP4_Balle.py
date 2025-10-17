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
        self.__bl_rayon = C.C_RAYON_BALLE

        #position initiale de la balle
        self.__bl_posx = C.C_LARGEUR_CANVAS // 2
        self.__bl_posy = C.C_HAUTEUR_CANVAS // 2

        #direction initiale de la balle
        self.__bl_vit = C.C_VITESSE_BALLE
        self.__bl_angle = rd.uniform(0,2*m.pi)

        #coordonnees vitesse initiales (angle = 0)
        self.__vxballe = self.__bl_vit*m.cos(self.__bl_angle)
        self.__vyballe = self.__bl_vit*m.sin(self.__bl_angle)

    def get_position_balle(self):
        """
        Fonction : Getter de position de la balle 
        Entree : None
        Sortie : Couple posX,posY (TUPPLE)
        """
        return (self.__bl_posx,self.__bl_posy)
    
    def get_vitesse_balle(self):
        """
        Fonction : Getter de vitesse de la balle 
        Entree : None
        Sortie : Couple vxballe,vyballe (TUPPLE)
        """
        return (self.__vxballe,self.__vyballe)
    
    def deplacement_balle(self):
        """
        Fonction : Gestion des deplacement de la balle
        Entree : None
        Sortie : None
        """
        #Deplacement regulier
        self.__bl_posx += self.__vxballe
        self.__bl_posy += self.__vyballe

    
    def rebond_sur_mur(self):
        """
        Fonction : Gestion des rebond de la balle avec les murs
        Entree : None
        Sortie : None
        """
        #Rebond vers la gauche
        if self.__bl_posx - self.__bl_rayon + self.__vxballe < 0 :
            self.__bl_posx = 2 * self.__bl_rayon - self.__bl_posx
            self.__vxballe = -self.__vxballe
        
        #Rebond vers la droite
        elif self.__bl_posx + self.__bl_rayon + self.__vxballe > C.C_LARGEUR_CANVAS :
            self.__bl_posx = 2 * (C.C_LARGEUR_CANVAS - self.__bl_rayon) - self.__bl_posx
            self.__vxballe = -self.__vxballe
        
        #Rebond vers le bas 
        elif self.__bl_posy + self.__bl_rayon + self.__vyballe > C.C_HAUTEUR_CANVAS :
            self.__bl_posy = 2 * (C.C_HAUTEUR_CANVAS - self.__bl_rayon) - self.__bl_posy
            self.__vyballe = -self.__vyballe

        #Rebond vers le haut (cas de collision avec la barre)
        elif self.__bl_posy - self.__bl_rayon + self.__vyballe < 0 :
            self.__bl_posy = 2 * self.__bl_rayon - self.__bl_posy
            self.__vyballe = -self.__vyballe
            print("Balle perdue !")
        
    def rebond_sur_raquette(self,rsr_raquette):
        """
        Fonction : Gestion des rebond de la balle avec la raquette
        Entree : None
        Sortie : None
        """
        #Recuperation des infos utiles de la raquette
        rsr_r_posx = rsr_raquette.__r_posx
        rsr_r_posy = rsr_raquette.__r_posy
        rsr_r_larg = C.C_LARGEUR_RAQUETTE
        rsr_r_haut = C.C_HAUTEUR_RAQUETTE
        
        #Calcul de la différence de position entre la balle et la brique
        rsb_deltax = self.__bl_posx - rsr_r_posx
        rsb_deltay = self.__bl_posy - rsr_r_posy

        #Calcul du chevauchement sur les axes de la balle et de la brique
        rsb_overaxe_x = (rsr_r_larg / 2 + self.__bl_rayon) - abs(rsb_deltax)
        rsb_overaxe_y = (rsr_r_haut / 2 + self.__bl_rayon) - abs(rsb_deltay)

        #Verification de la collision
        if rsb_overaxe_x > 0 and rsb_overaxe_y > 0:
            #Cas ou la colision verticale est prioritaire (arrive plus tot)
            if rsb_overaxe_y <= rsb_overaxe_x:

                #Calcul du decalage entre la balle et le centre de la raquette
                rsr_decalage = (self.__bl_posx - rsr_r_posx) / (rsr_r_larg / 2)

                #Modification de l'angle de rebond en fonction du point de contact
                self.__bl_angle = m.radians(90 - rsr_decalage * 60)

                #Modification des coordonnees vitesse
                self.__vxballe = self.__bl_vit * m.cos(self.__bl_angle)
                self.__vyballe = -abs(self.__bl_vit * m.cos(self.__bl_angle)) #on veut que la balle remonte, donc on doit diminuer sur y
            
            
        
    def rebond_sur_brique(self,rsb_brique):
        """
        Fonction : Gestion des rebond de la balle avec une brique
        Entree : None
        Sortie : None
        """
        #Recuperation des infos utiles de la brique
        rsb_br_posx = rsb_brique.__br_posx
        rsb_br_posy = rsb_brique.__br_posy
        rsb_br_larg = C.C_LARGEUR_BRIQUE
        rsb_br_haut = C.C_HAUTEUR_BRIQUE

        #Calcul de la différence de position entre la balle et la brique
        rsb_deltax = self.__bl_posx - rsb_br_posx
        rsb_deltay = self.__bl_posy - rsb_br_posy

        #Calcul du chevauchement sur les axes de la balle et de la brique
        rsb_overaxe_x = (rsb_br_larg / 2 + self.__bl_rayon) - abs(rsb_deltax)
        rsb_overaxe_y = (rsb_br_haut / 2 + self.__bl_rayon) - abs(rsb_deltay)

        #Verification de la collision
        if rsb_overaxe_x > 0 and rsb_overaxe_y > 0:
            #Cas ou la colision verticale est prioritaire (arrive plus tot)
            if rsb_overaxe_y <= rsb_overaxe_x:
                #Ici la balle vient soit du dessus ou du dessous donc le rebond est de type vertical
                
                #Calcul du decalage entre la balle et le centre de la raquette
                rsb_decalage = (self.__bl_posx - rsb_br_posx) / (rsb_br_larg / 2)

                #Modification de l'angle de rebond en fonction du point de contact
                self.__bl_angle = m.radians(90 - rsb_decalage * 60)

                #Modification des coordonnees vitesse
                self.__vxballe = self.__bl_vit * m.cos(self.__bl_angle)
                self.__vyballe = -self.__vyballe
            
            #Cas ou la colision horizontale est prioritaire (arrive plus tot)
            elif rsb_overaxe_y >= rsb_overaxe_x:

                #Calcul du decalage entre la balle et le centre de la raquette
                rsb_decalage = (self.__bl_posx - rsb_br_posx) / (rsb_br_larg / 2)

                #Modification de l'angle de rebond en fonction du point de contact
                self.__bl_angle = m.radians(90 - rsb_decalage * 60)

                #Modification des coordonnees vitesse
                self.__vxballe = -self.__vxballe
                self.__vyballe = self.__bl_vit * m.sin(self.__bl_angle)


