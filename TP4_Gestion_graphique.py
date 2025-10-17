# -*- coding: utf-8 -*-
"""
Date de creation : 17 octobre 2025
Auteurs: Marie Louise MILLIEN & Elouen WURMSER
Projet: TP4 - CasseBrique
Titre: Fichier de la partie graphique Tkinter (VUE)
"""

#Description
"""
Description:
    Fichier 'VUE' du jeu, cree et gere tous les aspects UNIQUEMENT graphique 
    (affichage et interaction visuelles)
    Ce fichier ne contient aucune logique de jeu : il ne deplace pas (modifie pas
    les positions) des objets, ne gere pas les colission entre le bords du canvas
    et la balle par ex, ne connait pas les regle de jeu et ne peut donc pas gerer 
    les scores juste les afficher
    Ce fichier ne fait que dessiner ce que le 'CONTROLEUR' lui demande, mettre a 
    jour l'ecran quand les objet changent, transmettre les evenement clavier au 
    'CONTROLEUR'
"""

#Schema de l'architecture du fichier envisagee
"""
=========================================
Architecture du projet Casse Brique
=========================================

          Manager_fenetre
          (hérite de tk.Tk)
-----------------------------------------
- frames: dict[str, tk.Frame]
- show_frame(name)
- Conteneur pour toutes les fenêtres
                │
                │
     ┌──────────┴─────────────┐
     │                        │
Fenetre_demarage           Fenetre_option
(tk.ttk.Frame)             (tk.ttk.Frame)
- Boutons: Jouer            - Boutons: Option 1, 2
           Option            - Retour / Quit
           Quitter
                │
                │
         ┌──────────────┐
         │Fenetre_jeu   │
         │(tk.ttk.Frame)│
         │--------------│
         │ Canvas       │
         │ Score        │
         │ Raquette     │  <-- Objet logique: R.Raquette
         │ Balle        │  <-- Objet logique: Bl.Balle
         │ Briques      │  <-- Objet logique: Br.Brique
         │--------------│
         │ update_canvas()   <- Boucle principale
         │ update_raquette() <- Boucle de mise à jour raquette
         └──────────────┘

=========================================
Objets logiques (sans Tkinter)
=========================================
- Raquette (TP4_Raquette)
  - posX, largeur, vitesse
  - deplacement_barre(event)

- Balle (TP4_Balle)
  - posX, posY, rayon, vitesse, angle
  - deplacement_balle()
  - rebond_sur_mur()
  - rebond_sur_raquette(raquette)
  - rebond_sur_brique(brique)

- Brique (TP4_Brique)
  - posX, posY, largeur, hauteur
  - état (visible/cassée)

=========================================
Flux général
=========================================
Manager_fenetre
    ├─ Fenetre_demarage
    ├─ Fenetre_option
    └─ Fenetre_jeu
         ├─ Canvas (affiche balle, raquette, briques)
         ├─ update_canvas() → déplace balle, gère collisions
         └─ update_raquette() → met à jour position raquette

Interaction clavier
→ Captée par Canvas → appelle R.Raquette.deplacement_barre()

"""

#Brouillon du fichier
"""
# Importation des modules nécessaires
# tkinter pour l'interface graphique
# typing pour la gestion des types
# TP4_Constantes pour les constantes du jeu
# TP4_Raquette, TP4_Balle, TP4_Briques pour la logique du jeu
#import tkinter as tk
#import typing as typ
#import TP4_Constantes as C
#import TP4_Raquette as R
#import TP4_Balle as Bl
#import TP4_Briques as Br

# Titre de l'application
#APP_TITLE = "Casse Brique"

# Classe principale qui gère toutes les fenêtres
#class Manager_fenetre(tk.Tk):
#    #Classe qui gère toutes les fenêtres de l'application

#    def __init__(self):
#        super().__init__()
#        self.title(APP_TITLE)
#        self.resizable(False, False)

#        # Conteneur pour toutes les fenêtres
#        container = tk.ttk.Frame(self)
#        container.pack(fill="both", expand=True)

#        # Dictionnaire des fenêtres
#        self.frames: typ.Dict[str, tk.Frame] = {}

#        # Création des fenêtres et ajout au dictionnaire
#        for F in (Fenetre_demarage, Fenetre_option, Fenetre_jeu):
#            frame = F(parent=container, manager=self)
#            self.frames[F.__name__] = frame
#            frame.grid(row=0, column=0, sticky="nsew")

#        # Affiche la fenêtre de démarrage
#        self.show_frame("Fenetre_demarage")

#    def show_frame(self, name: str):
#        #Affiche la fenêtre identifiée par son nom
#        frame = self.frames.get(name)
#        if frame:
#            frame.tkraise()


# Classe représentant la fenêtre de démarrage
#class Fenetre_demarage(tk.ttk.Frame):
#    #Fenêtre de démarrage avec boutons Jouer / Option / Quitter

#    def __init__(self, parent: tk.Widget, manager: Manager_fenetre):
#        super().__init__(parent, padding=20)
#        self.manager = manager

#        # Titre de la fenêtre
#        tk.ttk.Label(self, text=APP_TITLE, font=("Arial", 24, "bold")).pack(pady=20)

#        # Boutons Jouer, Options et Quitter
#        tk.ttk.Button(self, text="Jouer", command=lambda: manager.show_frame("Fenetre_jeu")).pack(pady=10)
#        tk.ttk.Button(self, text="Options", command=lambda: manager.show_frame("Fenetre_option")).pack(pady=10)
#        tk.ttk.Button(self, text="Quitter", command=manager.destroy).pack(pady=10)


# Classe représentant la fenêtre des options
#class Fenetre_option(tk.ttk.Frame):
#    #Fenêtre des options

#    def __init__(self, parent: tk.Widget, manager: Manager_fenetre):
#        super().__init__(parent, padding=20)
#        self.manager = manager

#        # Titre Options
#        tk.ttk.Label(self, text="Options", font=("Arial", 20, "bold")).pack(pady=20)

#        # Boutons Option 1 et 2 (WIP)
#        tk.ttk.Button(self, text="Option 1 (WIP)").pack(pady=6)
#        tk.ttk.Button(self, text="Option 2 (WIP)").pack(pady=6)

#        # Bouton Retour vers la fenêtre de démarrage
#        tk.ttk.Button(self, text="Retour", command=lambda: manager.show_frame("Fenetre_demarage")).pack(pady=12)


# Classe représentant la fenêtre du jeu
#class Fenetre_jeu(tk.ttk.Frame):
#    #Fenêtre du jeu avec canvas et barre de score

#    def __init__(self, parent: tk.Widget, manager: Manager_fenetre):
#        super().__init__(parent)
#        self.manager = manager

#        # Score initial
#        self.score = 0
#        self.score_var = tk.StringVar(value=f"Score : {self.score}")

#        # Barre du haut pour afficher le score
#        top_bar = tk.ttk.Frame(self, padding=(8, 8))
#        top_bar.pack(fill="x")
#        tk.ttk.Label(top_bar, textvariable=self.score_var, font=("Arial", 12, "bold")).pack(side="left", padx=8)

#        # Barre du bas pour les boutons Retour et Quitter
#        bottom_bar = tk.ttk.Frame(self, padding=(8, 8))
#        bottom_bar.pack(side="bottom", fill="x")
#        tk.ttk.Button(bottom_bar, text="Retour", command=lambda: manager.show_frame("Fenetre_demarage")).pack(side="left", padx=6)
#        tk.ttk.Button(bottom_bar, text="Quitter", command=manager.destroy).pack(side="left", padx=6)

#        # Canvas de jeu
#        self.canvas = tk.Canvas(self, width=C.C_LARGEUR_FENETRE, height=C.C_HAUTEUR_FENETRE, bg="black")
#        self.canvas.pack(pady=6)
#        self.canvas.focus_set()  # pour capter les événements clavier

#        # Création des objets logiques
#        self.raquette = R.Raquette()
#        self.balle = Bl.Balle()

#        # Création graphique de la raquette
#        self.raquette_id = self.canvas.create_line(0, 0, 0, 0, width=8, fill="red")
#        self.update_raquette()
#        self.canvas.bind("<Key>", self.raquette.deplacement_barre)

#        # Boucle de mise à jour du canvas
#        self.fps_delay = 50  # ms
#        self.update_canvas()

#    def update_raquette(self):
#        #Met à jour la position de la raquette sur le canvas
#        x_center = self.raquette.get_r_xbarre()
#        y_pos = C.C_Y_RAQUETTE
#        half_width = C.C_LARGEUR_RAQUETTE / 2
#        self.canvas.coords(
#            self.raquette_id,
#            x_center - half_width, y_pos,
#            x_center + half_width, y_pos
#        )
#        self.after(self.fps_delay, self.update_raquette)

#    def update_canvas(self):
#        #Boucle principale de mise à jour du canvas
#        # Déplacer la balle
#        self.balle.deplacement_balle()
#        # Ici on pourra ajouter rebonds et collisions
#        x, y = self.balle.get_position_balle()
#        r = self.balle.get_rayon()
#        self.canvas.delete("balle")
#        self.canvas.create_oval(x - r, y - r, x + r, y + r, fill="blue", tags="balle")

#        # Rappel de la boucle toutes les fps_delay ms
#        self.after(self.fps_delay, self.update_canvas)
"""