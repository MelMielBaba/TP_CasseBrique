# -*- coding: utf-8 -*-
"""
Date de creation : 7 octobre 2025
Auteurs: Marie Louise MILLIEN & Elouen WURMSER
Projet: TP4 - CasseBrique
Titre: Fichier des Fenetres
"""

"""
Description du fichier:
    Ce fichier implémente la classe principale App qui gère la navigation entre les 3 écrans:
    - FenetreDemarrage : écran de démarrage avec les boutons Jouer, Option, Quitter
    - FenetreOption : écran des options
    - FenetreJeu : écran contenant le canvas de jeu et le score

    Les transitions entre les fenetres sont réalisées en détruisant la frenetre courante
    puis en créant la suivante.
"""

"""
TO DO :
    - Redéfinir les methodes de Fenetre(), fonctionnement et description en commentaire
    - Dans la classe Fenetre_option rajouter le bouton QUITTER self.fo_btn_quitter
    - Trouver le moyen de recuperer la largeur et la hauteur du canevas (on en aurait 
    besoin pour le balle)
    - Réfléchir a la gestion du score {plutot l'implementer dans TP4_Jeu.py pour la 
    modifier là}
    - {Creer une classe Manager_fenetres() pour les gestions des fenetres, car c'est 
    bizarre que la mere appelle ses filles dans ses methodes}
    - Verifier que Fenetre_jeu() verifie les points suivant:
        • Un canevas (zone principale du jeu)
        • Une zone de texte affichant le score
        • Un bouton permettant de démarrer une partie
        • Un bouton permettant de quitter le jeu proprement
        • Un menu avec différentes options
"""

#Importation des modules
import tkinter as tk

class Fenetre:
    """
    Description : Classe Mere des fenetres du jeu
    Attributs :
        - fenetre_racine : creation d'une fenetre TKinter via tk.Tk()
    Methodes :
        -
    """
    def __init__(self):
        #creation de la fenetre graphique
        self.fenetre_racine = tk.Tk()
        #taille de la fenetre
        self.fenetre_racine.geometry("400x400")

        self.creation_fenetre_demarrage()
 
    def creation_fenetre_demarrage(self):
        """
        Fonction : Crée et affiche l'écran de démarrage. La méthode instancie 
        FenetreDemarrage, lie les boutons aux méthodes de app pour naviguer 
        vers les autres écrans, puis affiche la fenetre avec pack().
        Entree : self
        Sortie : 
        """
        self.start_frame = Fenetre_principale(self.root, self)
        self.start_frame.btn_option.bind('<Button-1>', self.creation_fenetre_option)
        self.start_frame.btn_jouer.bind('<Button-1>', self.creation_fenetre_jeu)
        self.start_frame.pack()
 
    def creation_fenetre_option(self, event=None):
        """
        Fonction : Transition vers la fenetre des options. Paramètre event : 
        reçu quand la méthode est appelée via bind. Permet à la meme 
        fonction d'être utilisée comme retour d'appel.
        Entree : self
        Sortie : 
        """
        self.start_frame.destroy()
        self.second_menu_frame = Fenetre_option(self.root, self)
        self.second_menu_frame.pack()
    
    def creation_fenetre_jeu(self, event=None):
        """
        Fonction : Transition vers la fenetre de jeu. Paramètre event : 
        reçu quand la méthode est appelée via bind. Permet à la meme 
        fonction d'être utilisée comme retour d'appel.
        Entree : self
        Sortie : 
        """
        self.start_frame.destroy()       
        self.third_menu_frame = Fenetre_jeu(self.root, self)
        self.third_menu_frame.pack()
    
    def retour_demarrage_option(self):
        """
        Fonction : Retour au menu de démarrage depuis la fenetre d'options.
        C'est la fonction d'appel du bouton retour de la fenetre d'options
        Entree : self
        Sortie : 
        """
        self.second_menu_frame.destroy()
        self.creation_fenetre_demarrage()

    def retour_demarrage_jeu(self):
        """
        Fonction : Retour au menu de démarrage depuis la fenetre de jeu.
        C'est la fonction d'appel du bouton retour de la fenetre de jeu
        Entree : self
        Sortie : 
        """
        self.third_menu_frame.destroy()
        self.creation_fenetre_demarrage()
 
 
class Fenetre_principale(tk.Frame):
    """
    Description : Classe Fille Fenetre de demarrage, affichee en 
    premier lorsqu'on lance le jeu via TP4_Jeu.py
    Attributs :
        - super().__init__(self) : recuperation des attributs parents, cad de Fenetre()
        - fp_btn_jouer, fp_btn_option, fp_btn_quitter : implementation des boutons Jouer,
        Option et Quitter
    Methodes :
        -
    """
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        
        #Affichage du titre de la fenetre
        tk.Label(self, 
                 text='Casse Brique', 
                 font=("Arial", 20, "bold")).pack(pady=20)

        #►LES BOUTONS◄
        #Creation du bouton pour lancer la fenetre de jeu
        self.fp_btn_jouer = tk.Button(self, text="Jouer")
        self.fp_btn_jouer.pack(pady=10)

        #Creation du bouton pour lancer la fenetre des options
        self.fp_btn_option = tk.Button(self, text="Option")
        self.fp_btn_option.pack(pady=10)

        #Creation du bouton pour quitter definitivement la fenetre
        self.fp_btn_quitter = tk.Button(self, 
                                     text="Quitter", 
                                     command=app.root.destroy) # arrete le programme en cours
        self.fp_btn_quitter.pack(pady=10)
 
 
class Fenetre_option(tk.Frame):
    """
    Description : Classe Fille Fenetre du menu des options
    Attributs :
        - super().__init__(self) : recuperation des attributs parents, cad de Fenetre()
        - fo_btn_option1, fo_btn_retour, fo_btn_quitter : implementation des 
        boutons Option1 (a definir), Retour qui renvoie a la fenetre principal et Quitter
    Methodes :
        - Aucunes
    """
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        #Affichage du titre de la fenetre
        tk.Label(self, 
                 text='Options', 
                 font=("Arial", 20, "bold")).pack(pady=20)
        
        #►LES BOUTONS◄
        #Creation des boutons des options
        #►OPTION 1
        self.fo_btn_option1 = tk.Button(self, text="WIP")
        self.fo_btn_option1.pack(pady=10)

        #Creation du bouton pour revenir a la fenetre principale
        self.fo_btn_retour = tk.Button(self, text="Retour", 
                                    command=app.retour_demarrage_option) #Voir fonction dans app
        self.fo_btn_retour.pack(pady=10)

        #Creation du bouton pour quitter definitivement la fenetre
        self.fo_btn_quitter = None
 

class Fenetre_jeu(tk.Frame):
    """
    Description : Classe Fille Fenetre du jeu, elle contient le canevas ou 
    se deroule le jeu casse brique
    Attributs :
        - super().__init__(self) : recuperation des attributs parents, cad de Fenetre()
        - fj_btn_option1, fj_btn_retour : implementation des boutons Option1 (a definir),
        et Retour qui renvoie a la fenetre principal
        - fj_haut_barre , fj_bas_barre : implementation des barres des boutons et du texte
        - fj_canvas : canevas ou se deroule le jeu
        - fj_score : score du joueur afficher
    Methodes :
        - Aucunes
    """
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        
        #►LES BARRES DE MENU ET D'INFOS◄
        #Creation de la barre de menu du haut
        self.fj_haut_barre = tk.Frame(self)
        self.fj_haut_barre.pack(fill="x", pady=5, padx=5)

        #Creation de la barre de menu du bas
        self.fj_bas_barre = tk.Frame(self)
        self.fj_bas_barre.pack(side="bottom", fill="both", expand=True)

        #►LES BOUTONS◄
        #Creation du bouton pour quitter definitivement la fenetre
        self.fj_btn_quitter = tk.Button(self.fj_bas_barre, #Emplacement du bouton (la barre du bas)
                                     text="Quitter", 
                                     command=app.root.destroy) 
        self.fj_btn_quitter.pack(side="left", padx=5, pady=5)

        #Creation du bouton pour revenir a la fenetre principale
        self.fj_btn_retour = tk.Button(self.fj_bas_barre, #Emplacement du bouton (la barre du bas)
                                    text="Retour", 
                                    command=app.retour_demarrage_jeu) 
        self.fj_btn_retour.pack(side="left", 
                             padx=5, 
                             pady=5)

        #Creation du canevas ou se deroule le jeu
        self.fj_canvas = tk.Canvas(self, 
                                width=1000, #Largeur
                                height=500, #Hauteur
                                bg="black") #Couleur
        self.fj_canvas.pack()

        #Affichage du score
        self.fj_score = 0
        self.fj_score_var = tk.StringVar(value=f"Score : {self.score}")
        self.fj_score_label = tk.Label(self.top_bar,  # SCORE est dans la bare du haut
                                    textvariable=self.score_var, # Affichage du texte variable
                                    font=("Arial", 12, "bold"))  # Personalisation
        
        self.fj_score_label.pack(side="left", 
                              padx=10)


class Manager_fenetres:
    """
    Description : Gere les differentes fenetres
    Attributs :
        - 
    Methodes :
        - changement_fenetre()
        - 
    """
    def __init__(self):
        pass