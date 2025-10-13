# -*- coding: utf-8 -*-

#En-tete
"""
Date de creation : 7 octobre 2025
Auteurs: Marie Louise MILLIEN & Elouen WURMSER
Projet: TP4 - CasseBrique
Titre: Fichier des Fenetres
"""

#Description
"""
Description du fichier:
    Ce fichier implémente la classe principale App qui gère la navigation entre les 3 écrans:
    - Fenetre_principale : écran de démarrage avec les boutons Jouer, Option, Quitter
    - Fenetre_option : écran des options
    - Fenetre_jeu : écran contenant le canvas de jeu et le score
"""

#TO DO
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

"""
Nouvelle structure:
-Manager_fenetre -> herite de personne creer la fenetre et gere les ecran(frames)
-Fenetre -> herite de frame et implemente les methode commune au ecrans filles
-Les fenetre -> herite dde fenetre et definisse des methodes plus specifique
"""

#Importation des modules
import tkinter as tk

class Manager_fenetres:
    """
    Description : Gere les differentes fenetres
    Attributs :
        - mf_stock_fenetre : le dictionnaire qui stock les fenetres
        - mf_fenetre_courante : la fenetre actuellement affichee
        - 
    Methodes :
        - ajouter_nouvelle_fenetre()
        - afficher_fenetre_actuelle()
        -
    """
    def __init__(self):
        #Creation d'une fenetre tkinter dans laquelle evolue les ecrans
        self.mf_fenetre_racine = tk.Tk()
        self.mf_fenetre_racine.title("Casse Brique")

        #Creation d'un container de tkinter
        self.mf_container = tk.Frame(self.mf_fenetre_racine)
        self.mf_container.pack(fill = "both", expand = True)

        #Stockage des fentetres dans un dictionnaire
        self.mf_stock_fenetre = dict() 

        #Ajout des fenetres (ecrans) des l'initialisation
        self.ajouter_nouvelle_fenetre("Fenetre principale")
        self.ajouter_nouvelle_fenetre("Fenetre option")
        self.ajouter_nouvelle_fenetre("Fenetre jeu")

        #Afficher la premiere fenetre
        self.mf_fenetre_courante = "Fenetre principale"

    def ajouter_nouvelle_fenetre(self,anf_nom_fenetre:str):
        """
        Fonction : Permet d'ajouter une nouvelle fenetre grace a son nom dans 
        le dictionnaire qui stock toutes les fenetres
        Entree : self, le nom de la fenetre (STR)
        Sortie : None
        """
        if anf_nom_fenetre == "Fenetre principale":
            anf_fenetre_ajoute = Fenetre_principale(self.mf_container,self)
            self.mf_stock_fenetre[anf_nom_fenetre] = anf_fenetre_ajoute
        elif anf_nom_fenetre == "Fenetre options":
            anf_fenetre_ajoute = Fenetre_option(self.mf_container,self)
            self.mf_stock_fenetre[anf_nom_fenetre] = anf_fenetre_ajoute
        elif anf_nom_fenetre == "Fenetre jeu" :
            anf_fenetre_ajoute = Fenetre_jeu(self.mf_container,self)
            self.mf_stock_fenetre[anf_nom_fenetre] = anf_fenetre_ajoute

    def afficher_fenetre_actuelle(self,afa_nom_fenetre:str):
        """
        Fonction : Gere le changement de la fenetre actuellement affichee; 
        Masque d'abord toutes les autres fenetres puis affiche la fenetre courante
        Entree : self, le nom de la fenetre (STR)
        Sortie : None
        """
        if afa_nom_fenetre in self.mf_stock_fenetre:
            afa_fenetre_affichee = self.mf_stock_fenetre[afa_nom_fenetre]
            afa_fenetre_affichee.tkraise()
    
    """
    def lancer_fenetre_courante(self):
        self.mf_stock_fenetre[self.mf_fenetre_courante].mainloop()
    """

    def get_fenetre(self,gf_nom_fenetre):
        return self.mf_stock_fenetre[gf_nom_fenetre]

class Fenetre(tk.Frame):
    """
    Description : Classe Mere des fenetres du jeu
    Attributs :
        - fenetre_racine : creation d'une fenetre TKinter via tk.Tk()
    Methodes :
        -
    """
    def __init__(self,nom_fenetre):
        #Heritage
        super().__init__(self)

        # --- Constantes ---
        self.f_fenetre_width = 1000
        self.f_fenetre_height = 650
        self.fj_canvas_width = 900
        self.fj_canvas_height = 500
        self.f_titre = "Casse Brique"

        #Nom de la fenetre
        self.__f_nom_fenetre = nom_fenetre 
        
        #►LES BARRES DE MENU ET D'INFOS◄
        #Creation de la barre de menu du haut
        self.f_haut_barre = tk.Frame(self)
        self.f_haut_barre.pack(fill = "x", pady = 5, padx = 5)

        #Creation de la barre de menu du bas
        self.f_bas_barre = tk.Frame(self)
        self.f_bas_barre.pack(side = "bottom", fill = "both", expand = True)

        #Le Canevas
        self.f_canvas = tk.Canvas(self, 
                                width = self.f_canvas_width, #Largeur
                                height = self.f_canvas_height, #Hauteur
                                bg = "black") #Couleur
        self.f_canvas.pack()
    
    def get_f_nom_fenetre(self):
        return self.__f_nom_fenetre


class Fenetre_principale(Fenetre):
    """
    Description : Classe Fille Fenetre de demarrage, affichee en 
    premier lorsqu'on lance le jeu via TP4_Jeu.py
    Attributs :
        - super().__init__() : recuperation des attributs parents, cad de Fenetre()
        - fp_btn_jouer, fp_btn_option, fp_btn_quitter : implementation des boutons Jouer,
        Option et Quitter
    Methodes :
        -
    """
    def __init__(self,fp_parent,fp_manager):
        super().__init__()
        
        #Affichage du titre de la fenetre
        tk.Label(self.f_fenetre_racine, 
                 text='Casse Brique', 
                 font=("Arial", 20, "bold")).pack(pady=20)
        

        #►LES BOUTONS◄
        #Creation du bouton pour lancer la fenetre de jeu
        self.fp_btn_jouer = tk.Button(self, text = "Jouer",command = fp_manager.afficher_fenetre_actuelle("Fenetre jeu"))
        self.fp_btn_jouer.pack(pady = 10)

        #Creation du bouton pour lancer la fenetre des options
        self.fp_btn_option = tk.Button(self, text = "Option",command = fp_manager.afficher_fenetre_actuelle("Fenetre option"))
        self.fp_btn_option.pack(pady = 10)

        #Creation du bouton pour quitter definitivement la fenetre
        self.fp_btn_quitter = tk.Button(self.f_fenetre_racine, 
                                     text = "Quitter", 
                                     command = self.fermer_fenetre)
        self.fp_btn_quitter.pack(pady = 10)
 
 
class Fenetre_option(Fenetre):
    """
    Description : Classe Fille Fenetre du menu des options
    Attributs :
        - super().__init__() : recuperation des attributs parents, cad de Fenetre()
        - fo_btn_option1, fo_btn_retour, fo_btn_quitter : implementation des 
        boutons Option1 (a definir), Retour qui renvoie a la fenetre principal et Quitter
    Methodes :
        - Aucunes
    """
    def __init__(self,fo_parent,fo_manager):
        super().__init__("Fenetre options")

        #Affichage du titre de la fenetre
        tk.Label(self, 
                 text = 'Options', 
                 font = ("Arial", 20, "bold")).pack(pady=20)
        
        #►LES BOUTONS◄
        #Creation des boutons des options
        #►OPTION 1
        self.fo_btn_option1 = tk.Button(self, text = "WIP1")
        self.fo_btn_option1.pack(pady = 10)
        #►OPTION 2
        self.fo_btn_option2 = tk.Button(self, text="WIP2")
        self.fo_btn_option2.pack(pady = 10)

        #Creation du bouton pour revenir a la fenetre principale
        self.fo_btn_retour = tk.Button(self, text = "Retour", 
                                    command = self.afficher_fenetre_actuelle("Fenetre principale")) 
        self.fo_btn_retour.pack(pady = 10)

        #Creation du bouton pour quitter definitivement la fenetre
        self.fo_btn_quitter = tk.Button(self, 
                                     text = "Quitter", 
                                     command = self.f_fermer_fenetre())
        self.fo_btn_quitter.pack(pady = 10)
 

class Fenetre_jeu(Fenetre):
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
    def __init__(self):
        super().__init__(self)

        #►LES BOUTONS◄
        #Creation du bouton pour quitter definitivement la fenetre
        self.fj_btn_quitter = tk.Button(self.fj_bas_barre, #Emplacement du bouton (la barre du bas)
                                     text = "Quitter", 
                                     command = self.f_fermer_fenetre) 
        self.fj_btn_quitter.pack(side = "left", padx = 5, pady = 5)

        """
        #Creation du bouton pour revenir a la fenetre principale
        self.fj_btn_retour = tk.Button(self.fj_bas_barre, #Emplacement du bouton (la barre du bas)
                                    text = "Retour", 
                                    command = self.afficher_fenetre_actuelle("Fenetre principale")) 
        self.fj_btn_retour.pack(side = "left", 
                             padx = 5, 
                             pady = 5)
        

        #Creation du bouton pour lancer le jeu
        self.fj_btn_lancer = tk.Button(self.fj_bas_barre, #Emplacement du bouton (la barre du bas)
                                    text = "Lancer le jeu", 
                                    command = self.lancer_jeu) 
        self.fj_btn_lancer.pack(side = "left", 
                             padx = 5, 
                             pady = 5)
        """

        #Creation du canevas ou se deroule le jeu
        self.fj_canvas = tk.Canvas(self, 
                                width = self.fj_canevas_width, #Largeur
                                height = self.fj_canevas_height, #Hauteur
                                bg = "black") #Couleur
        self.fj_canvas.pack()

        #Affichage du score
        self.fj_score = 0
        self.fj_score_var = tk.StringVar(value = f"Score : {self.fj_score}")
        self.fj_score_label = tk.Label(self.fj_haut_barre,  # SCORE est dans la bare du haut
                                    textvariable = self.fj_score_var, # Affichage du texte variable
                                    font = ("Arial", 12, "bold"))  # Personalisation
        
        self.fj_score_label.pack(side = "left", 
                              padx = 10)

