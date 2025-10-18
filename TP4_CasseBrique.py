# -*- coding: utf-8 -*-
"""
Date de creation : 14 octobre 2025
Auteurs: Marie Louise MILLIEN & Elouen WURMSER
Projet: TP4 - CasseBrique
Titre: Fichier de lancement du jeu (MAIN)
"""

"""
Description:
    Fichier 'MAIN' du jeu, sert uniquement a lancer un jeu Casse-brique
"""

#Importation du fichier CONTROLLEUR
import TP4_Jeu as J

#Creation d'un objet Jeu
casse_brique = J.Jeu()

#Appel de la fonction lancant le jeu
casse_brique.lancer_casse_brique()