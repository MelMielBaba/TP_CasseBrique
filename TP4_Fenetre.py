# -*- coding: utf-8 -*-
"""
Date de creation : 7 octobre 2025
Auteurs: Marie Louise MILLIEN & Elouen WURMSER
Projet: TP4 - CasseBrique
Titre: Fichier pour lancer le Casse-Brique.
Utilise les fichiers: cstes.py, raquette.py, balle.py, briques.py
"""

### IMPORTATION DES LIBRAIRIES
import tkinter as tk
from tkinter import ttk, messagebox
import TP4_Constantes as c
from TP4_Raquette import Raquette
from TP4_Balle import Balle
from TP4_Briques import BriqueManager

APP_TITLE = "Casse Brique"

### CREATION DE L'APP

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        # on empêche ici de modifier la taille de la fenetre
        self.resizable(False, False)
        # on créer un cadre pour mettre tous les widgets
        container = ttk.Frame(self)
        container.pack(fill="both")

        # dictionnaires des fenetres, ici on prévoit 3fenetres.
        self.frames = {}
        for F in (FenetreDemarrage, FenetreOption, FenetreJeu):
            frame = F(parent=container, app=self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # lancement de l'app sur la fenetre de demarrage
        self.show_frame("FenetreDemarrage")

    def show_frame(self, name: str):
        """Affiche la frame identifiée par son nom."""
        prev = getattr(self,'',None)
        if prev is not None and prev in self.frames:
            prev_frame = self.frames.get(prev)
            if hasattr(prev_frame, "on_hide") and callable(prev_frame.on_hide):
                prev_frame.on_hide()

        frame = self.frames.get(name)
        frame.tkraise()
        # store current
        self._current_frame_name = name

        # appeler on_show sur la frame affichée si définie
        if hasattr(frame, "on_show") and callable(frame.on_show):
            frame.on_show()

        frame = self.frames.get(name)
        frame.tkraise()
        # si la frame a un hook on_show, l'appeler pour rafraîchir son état
        if hasattr(frame, "on_show") and callable(getattr(frame, "on_show")):
            frame.on_show()

### CREATION DE L'ECRAN DE DEMARRAGE/ACCUEIL

class FenetreDemarrage(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, padding=20)
        self.app = app
        #Titre
        ttk.Label(self, text=APP_TITLE, font=("Arial", 24, "bold")).pack(pady=20)
        #Boutons
        ttk.Button(self, text="Jouer", command=lambda: app.show_frame("FenetreJeu")).pack(pady=10)
        ttk.Button(self, text="Options", command=lambda: app.show_frame("FenetreOption")).pack(pady=10)
        ttk.Button(self, text="Quitter", command=app.destroy).pack(pady=10)

### CREATION DE L'ECRAN DES OPTIONS

class FenetreOption(ttk.Frame):
    """Fenêtre d'options: permet de modifier les constantes liées aux briques et à la balle"""
    def __init__(self, parent, app):
        super().__init__(parent, padding=16)
        self.app = app

        ttk.Label(self, text="Options", font=("Arial", 20, "bold")).pack(pady=(0,12))

        # Initialisation de l'écran pour mettre les widgets dessus
        frame_params = ttk.Frame(self)
        frame_params.pack(pady=6, padx=6, fill="x")

        # utilitaire pour créer ligne label + spinbox
        def make_spin(parent, label_text, var_init, from_, to_, increment=1):
            row = ttk.Frame(parent)
            row.pack(fill="x", pady=4)
            ttk.Label(row, text=label_text, width=20, anchor="w").pack(side="left")
            sb = tk.Spinbox(row, from_=from_, to=to_, increment=increment, width=8)
            sb.pack(side="left")
            sb.delete(0, "end")
            sb.insert(0, str(var_init))
            return sb

        # Spinboxes pour les constantes briques
        self.sb_lignes = make_spin(frame_params, "Nombre de Lignes", c.LIGNES, 1, 30, 1)
        self.sb_colonnes = make_spin(frame_params, "Nombre de Colonnes", c.COLONNES, 1, 30, 1)
        self.sb_largeur = make_spin(frame_params, "Largeur des briques (px)", c.LARGEUR_BRIQUE, 10, 300, 1)
        self.sb_hauteur = make_spin(frame_params, "Hauteur des briques (px)", c.HAUTEUR_BRIQUE, 6, 120, 1)
        self.sb_vies_b = make_spin(frame_params, "Vies des briques", c.VIES, 1, 5, 1)
        self.sb_rayon_b = make_spin(frame_params, "Rayon de la balle", c.RAYON_BALLE, 5, 150, 1)
        self.sb_factor = make_spin(frame_params, "%Accelerations/sec",c.FACTOR,1,10,0.05)

        # Boutons appliquer / retour
        btn_row = ttk.Frame(self)
        btn_row.pack(pady=12)

        ttk.Button(btn_row, text="Appliquer", command=self.apply_changes).pack(side="left", padx=6)
        ttk.Button(btn_row, text="Retour", command=lambda: app.show_frame("FenetreDemarrage")).pack(side="left", padx=6)

    def apply_changes(self):
        """Applique les valeurs des spinboxes aux csts)."""
        # lire et convertir
        lignes = int(self.sb_lignes.get())
        colonnes = int(self.sb_colonnes.get())
        largeur = int(self.sb_largeur.get())
        hauteur = int(self.sb_hauteur.get())
        vies = int(self.sb_vies_b.get())
        rayon_b = int(self.sb_rayon_b.get())
        factor = float(self.sb_factor.get())

            # appliquer dans le module cstes (cela prendra effet pour les nouvelles génération de niveau)
        c.LIGNES = lignes
        c.COLONNES = colonnes
        c.LARGEUR_BRIQUE = largeur
        c.HAUTEUR_BRIQUE = hauteur
        c.VIES = vies
        c.RAYON_BALLE = rayon_b
        c.FACTOR = factor

### CREATION DE L'ECRAN DE JEU

class FenetreJeu(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        # Creation d'une barre en haut pour accueilir les widgets tq: le score et la vie
        top_bar = ttk.Frame(self, padding=(8, 8))
        top_bar.pack(fill="x")

        # Affichage du score
        self.score = 0
        self.score_var = tk.StringVar(value=f"Score : {self.score}")
        ttk.Label(top_bar, textvariable=self.score_var, font=("Arial", 12, "bold")).pack(side="left", padx=8)

        # Affichage de la vie
        self.lives = c.NOMBRE_VIES
        self.lives_var = tk.StringVar(value=f"Vies : {self.lives}")
        ttk.Label(top_bar, textvariable=self.lives_var, font=("Arial", 12, "bold")).pack(side="left", padx=20)

        # Creation d'une barre en bas pour accueilir les widgets tq: le bouton retour au menu principale et quitter
        bottom_bar = ttk.Frame(self, padding=(8, 8))
        bottom_bar.pack(side="bottom", fill="x")

        ttk.Button(bottom_bar, text="Retour", command=lambda: app.show_frame("FenetreDemarrage")).pack(side="left", padx=6)
        ttk.Button(bottom_bar, text="Quitter", command=app.destroy).pack(side="left", padx=6)

        # Creation du Canvas
        self.canvas = tk.Canvas(self, width=c.LARGEUR_CANVA, height=c.HAUTEUR_CANVA, bg="black")
        self.canvas.pack(pady=6)
        self.canvas.focus_set()


        # Creation de la raquette
        self.raquette = Raquette(c.LARGEUR_CANVA, c.HAUTEUR_CANVA)
        # Gestion du mouvement de la raquette par le clavier
        self.canvas.bind('<KeyPress>', self.clavier_mouvement)
        # Gestion du mouvement de la raquette par le clavier
        self.canvas.bind('<Motion>', self.souris_mouvement)

        # Affichage de la raquette
        # on l'affiche au centre du canva
        x_center = self.raquette.get_x_center()
        half = self.raquette.largeur_raquette / 2
        y = self.raquette.y
        # creation d'un rectangle: la raquete
        self.raillet = self.canvas.create_rectangle(
            x_center - half, y - self.raquette.hauteur_raquette/2,
            x_center + half, y + self.raquette.hauteur_raquette/2,
            fill="red"
        )

        ### GESTIONNNAIRES DES BRIQUES
        self.brique_manager = BriqueManager(self.canvas,
                                           lignes=c.LIGNES, 
                                           colonnes=c.COLONNES,
                                           largeur_brique=c.LARGEUR_BRIQUE, 
                                           hauteur_brique=c.HAUTEUR_BRIQUE,
                                           top_offset=c.TOP_OFFSET, 
                                           padding=c.PADDING)
        
        ### GESTIONNAIRE DE LA BALLE
        self.balle = Balle(self.canvas, x=x_center, y=y - 30)

        # Les états du jeu
        self.running = True         #  Le jeu tourne
        self.paused = True          #  Le jeu est en pause ( activité de base )
        self.delay = c.FPS_DELAY_MS #  Nombre de FPS
        self._after_id = None       # stockage de l'ID retourné par after pour pouvoir annuler

    def on_show(self):
        """Appelé quand la fenêtre devient visible : on reprend le jeu (dépauser)."""
        # Recréer le niveau si les constantes ont changé (comme avant)
        self.brique_manager.clear_all()

        self.brique_manager = BriqueManager(self.canvas,
                                               lignes=c.LIGNES, colonnes=c.COLONNES,
                                               largeur_brique=c.LARGEUR_BRIQUE, hauteur_brique=c.HAUTEUR_BRIQUE,
                                               top_offset=c.TOP_OFFSET, padding=c.PADDING)
        # repositionner la balle au-dessus de la raquette
        # remplacer l'ancienne balle par une nouvelle avec le rayon modifié
        self.canvas.delete(self.balle.id)
        self.balle = Balle(self.canvas, x=self.raquette.get_x_center(), y=self.raquette.y - 30, rayon=c.RAYON_BALLE)

        self.update_raquette_graphics()

        # reprendre le jeu : dépauser et lancer la boucle si nécessaire
        self.paused = False
        if self._after_id is None:
            self._schedule_next_frame()

    def on_hide(self):
        """Appelé quand on quitte la fenêtre : mettre le jeu en pause."""
        self.paused = True
        # annuler l'after en attente pour que rien ne tourne en arrière-plan
        if self._after_id is not None:
            self.after_cancel(self._after_id)
            self._after_id = None

    def _schedule_next_frame(self):
        """Planifie la prochaine itération de la boucle et conserve l'id."""
        self._after_id = self.after(self.delay, self.game_loop)

    def souris_mouvement(self, event):
        self.raquette.set_x_center(event.x)

    # NE FONCTIONNE PAS
    def clavier_mouvement(self,event):
        self.raquette.deplacement_barre(event.x)

    def update_raquette_graphics(self):
        x_center = self.raquette.get_x_center()
        half = self.raquette.largeur_raquette / 2
        y = self.raquette.y
        self.canvas.coords(self.raillet,
                           x_center - half, y - self.raquette.hauteur_raquette/2,
                           x_center + half, y + self.raquette.hauteur_raquette/2)

    # FONCTION COLLISIONS BALLES-BRIQUES-CANVA

    def check_collisions(self):
        # collision murs
        l, t, r, b = self.balle.coords()
        if l <= 0:
            self.balle.rebond_x()
            self.balle.x = self.balle.rayon
        if r >= c.LARGEUR_CANVA:
            self.balle.rebond_x()
            self.balle.x = c.LARGEUR_CANVA - self.balle.rayon
        if t <= 0:
            self.balle.rebond_y()
            self.balle.y = self.balle.rayon

        # bas -> perte de vie
        if b >= c.HAUTEUR_CANVA:
            self.lives -= 1
            self.lives_var.set(f"Vies : {self.lives}")
            if self.lives <= 0:
                self.game_over()
                return
            else:
                self.balle.reset(x=self.raquette.get_x_center(), y=self.raquette.y - 30)
                return

        # collision raquette
        rx1, ry1, rx2, ry2 = self.canvas.coords(self.raillet)
        bx1, by1, bx2, by2 = self.balle.coords()
        if not (bx2 < rx1 or bx1 > rx2 or by2 < ry1 or by1 > ry2):
            self.balle.rebond_y()
            ball_cx = (bx1 + bx2) / 2
            paddle_cx = (rx1 + rx2) / 2
            delta = (ball_cx - paddle_cx) / ((rx2 - rx1) / 2)
            max_horizontal = 5.0
            self.balle.vx += delta * max_horizontal
            self.balle.y = ry1 - self.balle.rayon - 1

        # collision briques
        hit = self.brique_manager.collision(self.balle)
        if hit is not None:
            self.balle.rebond_y()
            self.score += 10
            self.score_var.set(f"Score : {self.score}")

    def game_over(self):
        self.running = False
        messagebox.showinfo("Game Over", f"Game over!\nScore: {self.score}")
        self.restart_game()

    def restart_game(self):
        self.score = 0
        self.score_var.set(f"Score : {self.score}")
        self.lives = c.NOMBRE_VIES
        self.lives_var.set(f"Vies : {self.lives}")
        self.brique_manager.clear_all()
        self.brique_manager = BriqueManager(self.canvas,
                                           lignes=c.LIGNES, colonnes=c.COLONNES,
                                           largeur_brique=c.LARGEUR_BRIQUE, hauteur_brique=c.HAUTEUR_BRIQUE,
                                           top_offset=c.TOP_OFFSET, padding=c.PADDING)
        self.balle.reset(x=self.raquette.get_x_center(), y=self.raquette.y - 30)
        self.running = True
        # si on est visible (pas en pause) relancer la boucle
        if not self.paused and self._after_id is None:
            self._schedule_next_frame()

    def game_loop(self):
        # clear after id (car on est dans l'itération déclenchée)
        self._after_id = None

        if self.paused or not self.running:
            # ne rien faire si en pause ; mais ne pas boucler automatiquement
            return

        # logique cadre: déplacer la raquette graphique et la balle, collision, etc.
        self.update_raquette_graphics()
        self.balle.move()
        self.check_collisions()

        if self.brique_manager.reste() == 0:
            messagebox.showinfo("Victoire", f"Bravo ! Ton score:\nScore: {self.score}")
            self.restart_game()
            return

        # replanifier prochain frame
        self._schedule_next_frame()

