# -*- coding: utf-8 -*-
"""
Date de creation : 7 octobre 2025
Auteurs: Marie Louise MILLIEN & Elouen WURMSER
Projet: TP4 - CasseBrique
Titre: Fichier principal du jeu
"""

"""
TO DO:
    - Gestion du score et des vies
    - Si le bouton 'Lancer' est cliquer on lance une partie {avec la fonction jeu ?}
    - Quand une brique est detruite j_score += 1
    - Conditions d'arret du jeu:
        -> Victoire : Plus aucunes briques existantes
        -> Defaite : Plus aucunes vie (j_vie = 0)
"""

#Importation des fichiers
import TP4_Fenetre as F
import TP4_Balle as Bl
import TP4_Raquette as R
import TP4_Briques as Br
import TP4_Fenetre_Elouen as FELN

j_manager_fenetre = F.Manager_fenetres()

#Creation des objets
j_balle = Bl.Balle()
j_raquette = R.Raquette()
j_briques = Br.Brique() #/!\ ici on a créer qu'UNE SEULE brique /!\

j_score = 0
j_vies = 3

def lancer_casse_brique():
    app = FELN.App()
    app.mainloop()

def lancer_partie():
    while j_vies > 0:
        #si balle tombe du canvas (pas de collision en bas pour rappel):
            #j_vies -= 1
            #detruire la balle actuelle et regenerer une nouvelle balle
        #si une brique est detruite:
            #j_score += 1
        #actualiser l'affichage
        pass
    print("Game over! Merci d'avoir jouer!")

    



#Creation du gestionnaire des fenetres
#J_Manager_fenetres = F.Manager_fenetres()

#Creation des objets
#J_Balle = B.Balle(J_Manager_fenetres)
#J_Raquette = R.Raquette(J_Manager_fenetres)

#Creation des objets fenetre
#J_Fenetre_principale = F.Fenetre_principale()
#J_Fenetre_jeu = F.Fenetre_jeu()
#J_Fenetre_option = F.Fenetre_option()

#J_Manager_fenetres.ajouter_nouvelle_fenetre("Fenetre principale")
#J_Manager_fenetres.ajouter_nouvelle_fenetre(J_Fenetre_option)
#J_Manager_fenetres.ajouter_nouvelle_fenetre(J_Fenetre_jeu)

#J_Manager_fenetres.lancer_fenetre_courante()

#print(J_Manager_fenetres.mf_stock_fenetre)
#print("baguette")
#print(J_Manager_fenetres.get_fenetre("Fenetre principale"))
#J_Fenetre_principale.f_afficher_fenetre()
#fenetre = F.Fenetre('nom')
#fenetre.f_afficher_fenetre()
#J_Fenetre_jeu.f_afficher_fenetre()
#J_Manager_fenetres.afficher_fenetre_actuelle("Fenetre principale")