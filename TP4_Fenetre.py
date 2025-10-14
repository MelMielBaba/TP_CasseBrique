# -*- coding: utf-8 -*-
"""
Date de creation : 7 octobre 2025
Auteur: Marie Louise MILLIEN & Elouen WURMSER
Projet: TP4 - Casse-Brique
Fichier : Fenetre 

Ce fichier implémente la classe principale App qui gère la navigation entre les 3 fenetres:
- FenetreDemarrage : fenetre de démarrage avec les boutons Jouer, Option, Quitter
- FenetreOption : fenetre des options
- FenetreJeu : fentre contenant le canvas de jeu et le score

"""

import time
import tkinter as tk
import typing as typ
import TP4_Constantes as cste
from TP4_Raquette import Raquette
from tkinter import ttk
# on utilise ttk pour avoir une interface plus belle
APP_TITLE = "Casse Brique"

raquette = Raquette()

class App(tk.Tk):
    """Application principale

    Les fenetres sont créés en une seule fois et contenu dans un conteneur
    On affiche la fenetre désiré via la fonction show_frame(NomFenetre)
    """

    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.resizable(False, False)

        #self.raquette = Raquette(self)

        # Conteneur qui recoit toutes les fenetres
        container = ttk.Frame(self)
        container.pack(fill="both", expand=True)

        # Dictionnaire des fenetres 
        self.frames: typ.Dict[str, tk.Frame] = {}

        # création des fenetres
        for F in (FenetreDemarrage, FenetreOption, FenetreJeu):
            frame = F(parent=container, app=self)
            self.frames[F.__name__] = frame
            # on place toutes les fenetres au même endroit et on les affiche via tkraise
            frame.grid(row=0, column=0, sticky="nsew")

        # Affiche la fenetre de démarrage
        self.show_frame("FenetreDemarrage")

    def show_frame(self, name: str):
        """Affiche la frame identifiée par son nom cad la clé du dictionnaire frames"""
        frame = self.frames.get(name)
        frame.tkraise()
    


class FenetreDemarrage(ttk.Frame):
    """fenetre de démarrage avec boutons Jouer / Option / Quitter"""

    def __init__(self, parent: tk.Widget, app: App):
        super().__init__(parent, padding=20)
        self.app = app

        ttk.Label(self, 
                  text=APP_TITLE, 
                  font=("Arial", 24, "bold")).pack(pady=20)
        ttk.Button(self,
                   text="Jouer",
                   command=lambda: app.show_frame("FenetreJeu")).pack(pady=10)
        ttk.Button(self, 
                   text="Options", 
                   command=lambda: app.show_frame("FenetreOption")).pack(pady=10)
        ttk.Button(self, 
                   text="Quitter", 
                   command=app.destroy).pack(pady=10)


class FenetreOption(ttk.Frame):
    """fenetre des options"""

    def __init__(self, parent: tk.Widget, app: App):
        super().__init__(parent, padding=20)
        self.app = app

        ttk.Label(self, 
                  text="Options", 
                  font=("Arial", 20, "bold")).pack(pady=20)

        # Exemples d'options
        ttk.Button(self, 
                   text="Option 1 (WIP)").pack(pady=6)
        ttk.Button(self, 
                   text="Option 2 (WIP)").pack(pady=6)

        ttk.Button(self, 
                   text="Retour", 
                   command=lambda: app.show_frame("FenetreDemarrage")).pack(pady=12)


class FenetreJeu(ttk.Frame):
    """fenetre du jeu contenant le canvas et la barre de score"""

    def __init__(self, parent: tk.Widget, app: App):
        super().__init__(parent)
        self.app = app

        # Barre du haut (score)
        top_bar = ttk.Frame(self, padding=(8, 8))
        top_bar.pack(fill="x")

        # Variable de score
        self.score = 0
        self.score_var = tk.StringVar(value=f"Score : {self.score}")
        ttk.Label(top_bar, 
                  textvariable=self.score_var, 
                  font=("Arial", 12, "bold")).pack(side="left", padx=8)

        # Boutons basiques (Quitter / Retour)
        bottom_bar = ttk.Frame(self, padding=(8, 8))
        bottom_bar.pack(side="bottom", fill="x")

        ttk.Button(bottom_bar, 
                   text="Retour", 
                   command=lambda: app.show_frame("FenetreDemarrage")).pack(side="left", padx=6)
        ttk.Button(bottom_bar, 
                   text="Quitter", 
                   command=app.destroy).pack(side="left", padx=6)

        # Canvas de jeu
        self.canvas = tk.Canvas(self, 
                                width=cste.C_LARGEUR_FENETRE, 
                                height=cste.C_HAUTEUR_FENETRE, 
                                bg="black")
        self.canvas.pack(pady=6)

        # Création unique de la raquette
        x_center = raquette.get_r_xbarre()  # recup la position depuis l'autre fichier
        half_width = 30
        y_pos = 90
        self.raquette_id = self.canvas.create_line(
            x_center - half_width, y_pos,
            x_center + half_width, y_pos,
            width=8, fill='red')

        # Boucle d'update
        self.fps_delay = 16  # ~60 FPS
        self.update_raquette()


    def update_raquette(self):
        """Met à jour les coordonnées de la raquette sur le canvas"""
        x_center = raquette.get_r_xbarre()  # récupère la valeur de l'autre fichier
        half_width = 30
        y_pos = 90
        self.canvas.coords(
            self.raquette_id,
            x_center - half_width, y_pos,
            x_center + half_width, y_pos
        )
        self.after(self.fps_delay, self.update_raquette)






    # ##RAQUETTE
    #     self.pos_x=250
    #     self.afficher_raquette()
        
    # def afficher_raquette(self):
    #     """Affiche la raquette et met à jour sa position"""
    #     # Création de la raquette
    #     self.raquette = self.canvas.create_line(
    #         self.pos_x - 40,
    #         90,
    #         self.pos_x + 40,90,
    #         width=8,
    #         fill='red'
    #         )

    #     # Met à jour la raquette par FPS
    #     self.after(2, self.mettre_a_jour_raquette)

    # def mettre_a_jour_raquette(self):
    #     self.pos_x = get_r_xbarre() #250 #raq.pos_x  # pas de mouvement pour l'instant
    #     self.afficher_raquette()



if __name__ == "__main__":
    app = App()
    app.mainloop()
