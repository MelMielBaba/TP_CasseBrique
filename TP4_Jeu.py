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
    - IL FAUT LANCEMENT CE QUIL Y A DANS RQUETTE ICI
"""

#Importation des fichiers
import TP4_FenetreOFF as F
import TP4_Balle as B
import TP4_Raquette as R
import TP4_Fenetre as FELN

# IL FAUT LANCEMENT CE QUIL Y A DANS RQUETTE ICI
if __name__ == "__main__":
    app = FELN.App()
    app.mainloop()



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