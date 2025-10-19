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

#Importation du fichier des Constantes
import TP4_Constantes as C

#Importation des fichiers MODELES
import TP4_Balle as Bl
import TP4_Raquette as R
import TP4_Briques as Br

#Importation des fichiers VUE
import TP4_Gestion_graphique as Gg

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
        self.briques = []
        for i in range(C.C_LIGNES_BRIQUES):
            ligne = []
            for j in range(C.C_NB_BRIQUES_LIGNE):
                if i == 0 :
                    ligne.append(Br.Brique(C.C_BR_POX_INIT * (i+1),C.C_BR_POY_INIT * (j+1),'red'))
                elif i == 1 :
                    ligne.append(Br.Brique(C.C_BR_POX_INIT * (i+1),C.C_BR_POY_INIT * (j+1),'green'))
                elif i == 2 :
                    ligne.append(Br.Brique(C.C_BR_POX_INIT * (i+1),C.C_BR_POY_INIT * (j+1),'blue'))
            self.briques.append(ligne)

        #Initialisation du score et des vies
        self.j_score = 0
        self.j_vies = 3

        #Creation de la communication CONTROLLEUR-VUE
        self.j_manager_vue = Gg.Manager_fenetre(self.j_balle,self.j_raquette,self.briques,self.j_score,self.j_vies)

    #Creation de la boucle de jeu
    def lancer_casse_brique(self):
        """
        Fonction : 
        Entree : None
        Sortie : None
        """
        self.update_jeu()
        self.j_manager_vue.mainloop()
        
    def deplacement_touches(self,event):
        """
        Fonction : Gere le deplacement tkinter de la barre en fonction 
        d'un evenement tkinter et qui appel la methode logique en lui 
        donnant la direction
        Entree : Evenement tkinter
        Sortie : None
        """
        dt_touche = event.keysym
        print(dt_touche)

        #deplacement a gauche
        if dt_touche == 'q' or dt_touche == 'LEFT':
            self.j_raquette.deplacement_barre('gauche')

        #deplacement a droite
        elif dt_touche == 'd' or dt_touche == 'RIGHT':
            self.j_raquette.deplacement_barre('droite')

    #Creation d'une nouvelle balle si on perd la precedente
    def nouvelle_balle(self):
        """
        Fonction : 
        Entree : 
        Sortie : 
        """
        self.j_balle = Bl.Balle()

    #Verification de la sortie de la balle
    def verifier_sortie_balle(self):
        """
        Fonction : 
        Entree : 
        Sortie : 
        """
        if self.j_balle.get_position_balle()[1] > C.C_HAUTEUR_CANVAS:
            self.vies -= 1
            self.nouvelle_balle()
    
    def verifier_etat_briques(self):
        """
        Fonction : 
        Entree : 
        Sortie : 
        """
        for veb_ligne in self.briques:
            for veb_brique in veb_ligne:
                if veb_brique.touchee_par_balle(self.j_balle) :
                    self.j_balle.rebond_sur_brique(veb_brique)
                    veb_brique.detruire()
                    self.j_score += 1

    #Creation de la boucle de mise a jour
    def update_jeu(self):
        """
        Fonction : 
        Entree : 
        Sortie : 
        """
        # [1] Deplacer la balle (LOGIQUE)
        self.j_balle.deplacement_balle()

        # [2] Verification des colisions (LOGIQUE)
        self.j_balle.rebond_sur_mur()
        self.j_balle.rebond_sur_raquette(self.j_raquette)
        #self.j_balle.rebond_sur_brique() #Gestion des briques

        # [3] Verifier les mise a jour (LOGIQUE)
        #self.verifier_etat_briques()    #verifier etat des briques
        self.verifier_sortie_balle()

        # [4] Mise a jour graphique (VUE)
        self.j_manager_vue.update_dessin_balle()
        self.j_manager_vue.update_dessin_raquette()
        self.j_manager_vue.update_canvas()

        # [5] Relancer la mise à jour après un court délai
        self.j_manager_vue.mf_fenetre_racine.after(C.C_FPS, self.update_jeu)
        

        pass
        """
        A chaque boucle qui utilise after:
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