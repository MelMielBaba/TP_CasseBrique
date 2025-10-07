# -*- coding: utf-8 -*-
"""
Date de creation : 7 octobre 2025
Auteur: Marie Louise MILLIEN & Elouen WURMSER
Projet: TP4 - Casse-Brique
Fichier : Fenetre (interface graphique Tkinter)

Ce fichier implémente la classe principale App qui gère la navigation entre les 3 écrans:
- FenetreDemarrage : écran de démarrage avec les boutons Jouer, Option, Quitter
- FenetreOption : écran des options
- FenetreJeu : écran contenant le canvas de jeu et le score


Les transitions entre les fenetres sont réalisées en détruisant la frenetre courante
puis en créant la suivante.

"""

#Importation des modules
import tkinter as tk

class App:
    """Classe principale qui gère les fenêtres
Attributs :
root (tk.Tk) : la fenêtre principale Tkinter
start_frame correspond à la FenetreDemarrage : La fenetre de demarrage
second_menu_frame correspond à la FenetreOption : La fenetre des options
third_menu_frame correspond à la FenetreJeu : La fenetre de jeu)
"""

    def __init__(self, root):
        #Initialisation de l'application.
        self.root = root
        self.root.geometry("400x400")
        self.creation_fenetre_demarrage()
 
    def creation_fenetre_demarrage(self):
        """Crée et affiche l'écran de démarrage.


La méthode instancie FenetreDemarrage, lie les boutons aux méthodes de 
app pour naviguer vers les autres écrans, puis affiche la fenetre avec pack().
        """
        self.start_frame = FenetreDemarrage(self.root, self)
        self.start_frame.btn_option.bind('<Button-1>', self.creation_fenetre_option)
        self.start_frame.btn_jouer.bind('<Button-1>', self.creation_fenetre_jeu)
        self.start_frame.pack()
 
    def creation_fenetre_option(self, event=None):
        """Transition vers la fenetre des options.


Paramètre event : reçu quand la méthode est appelée via bind. Permet à la
meme fonction d'être utilisée comme retour d'appel.
        """
        self.start_frame.destroy()
        self.second_menu_frame = FenetreOption(self.root, self)
        self.second_menu_frame.pack()
    
    def creation_fenetre_jeu(self, event=None):
        """Transition vers la fenetre de jeu.


Paramètre event : reçu quand la méthode est appelée via bind. Permet à la
meme fonction d'être utilisée comme retour d'appel.
        """
        self.start_frame.destroy()       
        self.third_menu_frame = FenetreJeu(self.root, self)
        self.third_menu_frame.pack()
    
    def retour_demarrage_option(self):
        """Retour au menu de démarrage depuis la fenetre d'options.
        C'est la fonction d'appel du bouton retour de la fenetre d'options
        """
        self.second_menu_frame.destroy()
        self.creation_fenetre_demarrage()

    def retour_demarrage_jeu(self):
        """Retour au menu de démarrage depuis la fenetre de jeu.
        C'est la fonction d'appel du bouton retour de la fenetre de jeu
        """
        self.third_menu_frame.destroy()
        self.creation_fenetre_demarrage()
 
 
class FenetreDemarrage(tk.Frame):
    # La fenetre de demarrage, afficher en premier lors du lancement
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        
        # Affichage du nom de la fenetre
        tk.Label(self, 
                 text='Casse Brique', 
                 font=("Arial", 20, "bold")).pack(pady=20)

        # LES BOUTONS
        # Creation du bouton de jeu
        self.btn_jouer = tk.Button(self, text="Jouer")
        self.btn_jouer.pack(pady=10)

        # Creation du bouton des options
        self.btn_option = tk.Button(self, text="Option")
        self.btn_option.pack(pady=10)

        # Bouton pour quitter l'application
        self.btn_quitter = tk.Button(self, 
                                     text="Quitter", 
                                     command=app.root.destroy) # arrete le programme en cours
        self.btn_quitter.pack(pady=10)
 
 
class FenetreOption(tk.Frame):
    # La fenetre des options
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        # Nom de la fenetre 
        tk.Label(self, 
                 text='Options', 
                 font=("Arial", 20, "bold")).pack(pady=20)
        
        # Bouton des options
        # OPTION 1
        self.btn_option1 = tk.Button(self, text="WIP")
        self.btn_option1.pack(pady=10)

        # Bouton du retour au menu de demarrage
        self.btn_retour = tk.Button(self, text="Retour", 
                                    command=app.retour_demarrage_option) #Voir fonction dans app
        self.btn_retour.pack(pady=10)
 

class FenetreJeu(tk.Frame):
    # La fenetre de jeu ici, elle contient le jeu casse brique
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        
        # initialisation de la bare du haut
        self.top_bar = tk.Frame(self)
        self.top_bar.pack(fill="x", pady=5, padx=5)

        # Initialisation de la bare du bas
        self.bottom_bar= tk.Frame(self)
        self.bottom_bar.pack(side="bottom", fill="both", expand=True)

        # Bouton pour quitter l'application
        self.btn_quitter = tk.Button(self.bottom_bar, # Bouton retour est dans la bare du bas
                                     text="Quitter", #Texte
                                     command=app.root.destroy) # Voir fonction dans app
        self.btn_quitter.pack(side="left", padx=5, pady=5)

        # Bouton du retour au menu de démarrage
        self.btn_retour = tk.Button(self.bottom_bar, # Bouton retour est dans la bare du bas
                                    text="Retour", #Texte
                                    command=app.retour_demarrage_jeu) # Voir fonction dans app
        self.btn_retour.pack(side="left", 
                             padx=5, 
                             pady=5)

        # Affichage du canvas
        self.canvas = tk.Canvas(self, 
                                width=1000, #Largeur
                                height=500, #Hauteur
                                bg="black") #Couleur
        self.canvas.pack()

        #  Affichage du score
        self.score = 0
        self.score_var = tk.StringVar(value=f"Score : {self.score}")
        self.score_label = tk.Label(self.top_bar,  # SCORE est dans la bare du haut
                                    textvariable=self.score_var, # Affichage du texte variable
                                    font=("Arial", 12, "bold"))  # Personalisation
        
        self.score_label.pack(side="left", 
                              padx=10)


# Démarrage de l'application
if __name__ == "__main__":
    root = tk.Tk()
    main = App(root)
    root.mainloop()

