# -*- coding: utf-8 -*-
"""
Date de creation : 7 octobre 2025
Auteurs: Marie Louise MILLIEN & Elouen WURMSER
Projet: TP4 - CasseBrique
Titre: Fichier principal du jeu (CONTROLEUR)
"""

#Description
"""
Description:
    Fichier 'CONTROLEUR' du jeu, gere la communication entre ce que demande le joueur,
    la 'VUE' graphique et les 'MODELE' logique
    Ce fichier gère donc les touches clavier, les collisions, la boucle de jeu et la 
    mise à jour de la vue (partie graphique) à partir du modèle (partie logique)
"""

#To do
"""
TO DO:
    - Gestion du score et des vies
    - Si le bouton 'Lancer' est cliquer on lance une partie {avec la fonction jeu ?}
    - Quand une brique est detruite j_score += 1
    - Conditions d'arret du jeu:
        -> Victoire : Plus aucunes briques existantes
        -> Defaite : Plus aucunes vie (j_vie = 0)
    - IL FAUT LANCEMENT CE QU'IL Y A DANS RQUETTE ICI
"""

#Importation des fichiers MODELES
import TP4_Balle as Bl
import TP4_Raquette as R
import TP4_Briques as Br

#Importation des fichiers VUE
import TP4_Gestion_graphique as Gg
import TP4_Fenetre as F
import TP4_FenetreOFF as FELN

#Importation des modules
import tkinter as tk

class Jeu:
    def __init__(self):
        #Creation des objets LOGIQUES
        self.j_balle = Bl.Balle()
        self.j_raquette = R.Raquette()

        #Creation des briques (en logique)
        """Realiser plusieurs briques; reflechir au nombre de lignes, chaque 
        ligne de brique est constituee de brique de meme couleur"""

        #Initialisation du score et des vies
        self.j_score = 0
        self.vies = 3

        #Creation de la communication CONTROLLEUR-VUE
        self.j_manager_vue = Gg.Manager_fenetre(self.j_balle,self.j_raquette,self.j_score)

    #Creation de la boucle de jeu
    def lancer_casse_brique():
        pass
        """
        C'est ici qu'on appelle mainloop()
        A chaque boucle WHILE:
            -> on deplace la balle logique
            -> on verifie les collision de la balle
            -> on appelle le deplacement de la raquette
            -> on verifie les collisions de la balle
            -> on verifie l'etat de CHAQUE briques de CHAQUE ligne
                -> SI la verification d'une brique renvoie FALSE on ajoute 1 au score
                    -> on met a jour l'affichage
            -> on verifie qu'il reste des briques a casser
                -> SI plus aucune brique FIN
            -> on verifie que la balle ne sort pas
                -> SI elle sort on perd 1 vie
                    -> on met a jour l'affichage
            -> on verifie qu'il reste des vies
                -> SI vie <= 0 FIN et GAME OVER
            -> Mise a jour graphique
        """