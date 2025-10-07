# -*- coding: utf-8 -*-
"""
Date de creation : 7 octobre 2025
Auteur: Marie Louise MILLIEN & Elouen WURMSER
Projet: TP4 - Casse-Brique
Titre: Fichier de la Fenetre
"""

#Importation des modules
import tkinter as tk

#Creation de la classe Fenetre
class Fenetre:
    """
    La classe fenetre est parente de toutes les fenetres du jeu. 
    Elle a donc en attribut une fenetre et un bouton quitter
    """
    def __init__(self):
        pass

#Creation de la classe de la fenetre principale
class Fenetre_principale(Fenetre):
    """
    Cette classe 'creer' la fenetre qui se lance au debut du jeu.
    Elle possede comme toute fenetre un bouton quitter (heriter de Fenetre()),
    un bouton option et un bouton jouer
    """
    def __init__(self):
        pass

#Creation de la classe de la fenetre de jeu
class Fenetre_jeu(Fenetre):
    """
    Cette classe 'creer' la fenetre sur laquelle se deroule le jeu.
    Elle possede comme toute fenetre un bouton quitter (heriter de Fenetre()),
    un bouton menu un caneva
    """
    def __init__(self):
        pass

#Creation de la classe de la fenetre de jeu
class Fenetre_Option(Fenetre):
    """
    Cette classe 'creer' la fenetre du menu des options.
    Elle possede comme toute fenetre un bouton quitter (heriter de Fenetre()),
    un bouton retour
    """
    def __init__(self):
        pass