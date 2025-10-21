# -*- coding: utf-8 -*-
"""
Fichier principal pour lancer le Casse-Brique (version avec options modifiables).
Utilise : cstes.py, raquette.py, balle.py, briques.py
"""

import tkinter as tk
from tkinter import ttk, messagebox
import TP4_Constantes as c
from TP4_Raquette import Raquette
from TP4_Balle import Balle
from TP4_Briques import BriqueManager

APP_TITLE = "Casse Brique"

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.resizable(False, False)

        container = ttk.Frame(self)
        container.pack(fill="both", expand=True)

        self.frames = {}
        for F in (FenetreDemarrage, FenetreOption, FenetreJeu):
            frame = F(parent=container, app=self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("FenetreDemarrage")

    def show_frame(self, name: str):
        """Affiche la frame identifiée par son nom et gère on_hide/on_show."""
        prev = getattr(self, "_current_frame_name", None)
        # appeler on_hide sur la frame précédente si elle a la méthode
        if prev is not None and prev in self.frames:
            prev_frame = self.frames.get(prev)
            if hasattr(prev_frame, "on_hide") and callable(prev_frame.on_hide):
                try:
                    prev_frame.on_hide()
                except Exception as e:
                    print("Erreur on_hide:", e)

        frame = self.frames.get(name)
        if frame is None:
            return
        frame.tkraise()
        # store current
        self._current_frame_name = name

        # appeler on_show sur la frame affichée si définie
        if hasattr(frame, "on_show") and callable(frame.on_show):
            try:
                frame.on_show()
            except Exception as e:
                print("Erreur on_show:", e)
        frame = self.frames.get(name)
        if frame is None:
            return
        frame.tkraise()
        # si la frame a un hook on_show, l'appeler pour rafraîchir son état
        if hasattr(frame, "on_show") and callable(getattr(frame, "on_show")):
            try:
                frame.on_show()
            except Exception as e:
                # log simple (print) pour debug, mais on continue
                print("Erreur on_show:", e)


class FenetreDemarrage(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, padding=20)
        self.app = app

        ttk.Label(self, text=APP_TITLE, font=("Arial", 24, "bold")).pack(pady=20)
        ttk.Button(self, text="Jouer", command=lambda: app.show_frame("FenetreJeu")).pack(pady=10)
        ttk.Button(self, text="Options", command=lambda: app.show_frame("FenetreOption")).pack(pady=10)
        ttk.Button(self, text="Quitter", command=app.destroy).pack(pady=10)


class FenetreOption(ttk.Frame):
    """Fenêtre d'options: permet de modifier les constantes liées aux briques."""
    def __init__(self, parent, app):
        super().__init__(parent, padding=16)
        self.app = app

        ttk.Label(self, text="Options", font=("Arial", 20, "bold")).pack(pady=(0,12))

        # Frame pour les paramètres de briques
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
        self.sb_lignes = make_spin(frame_params, "Lignes (LIGNES)", c.LIGNES, 1, 30, 1)
        self.sb_colonnes = make_spin(frame_params, "Colonnes (COLONNES)", c.COLONNES, 1, 30, 1)
        self.sb_largeur = make_spin(frame_params, "Largeur brique (px)", c.LARGEUR_BRIQUE, 10, 300, 1)
        self.sb_hauteur = make_spin(frame_params, "Hauteur brique (px)", c.HAUTEUR_BRIQUE, 6, 120, 1)
        self.sb_vies_b = make_spin(frame_params, "Vies des briques", c.VIES, 1, 5, 1)
        self.sb_rayon_b = make_spin(frame_params, "Rayon de la balle", c.RAYON_BALLE, 5, 500, 1)
        self.sb_factor = make_spin(frame_params, "Accelerations",c.FACTOR,1,10,0.05)

        # Boutons appliquer / réinitialiser / retour
        btn_row = ttk.Frame(self)
        btn_row.pack(pady=12)

        ttk.Button(btn_row, text="Appliquer", command=self.apply_changes).pack(side="left", padx=6)
        ttk.Button(btn_row, text="Réinitialiser valeurs par défaut", command=self.reset_defaults).pack(side="left", padx=6)
        ttk.Button(btn_row, text="Retour", command=lambda: app.show_frame("FenetreDemarrage")).pack(side="left", padx=6)

        # Aide / remarque
        ttk.Label(self, text="Les modifications s'appliquent quand tu retournes à la fenêtre du jeu.", foreground="gray").pack(pady=(8,0))

    def apply_changes(self):
        """Applique les valeurs des spinboxes aux constantes dans cstes (module c)."""
        try:
            # lire et convertir
            lignes = int(self.sb_lignes.get())
            colonnes = int(self.sb_colonnes.get())
            largeur = int(self.sb_largeur.get())
            hauteur = int(self.sb_hauteur.get())
            vies = int(self.sb_vies_b.get())
            rayon_b = int(self.sb_rayon_b.get())
            factor = float(self.sb_factor.get())

            # validate basic constraints
            if lignes < 1 or colonnes < 1 or largeur < 4 or hauteur < 4:
                messagebox.showwarning("Valeurs invalides", "Certaines valeurs sont trop petites.")
                return

            # appliquer dans le module cstes (cela prendra effet pour les nouvelles génération de niveau)
            c.LIGNES = lignes
            c.COLONNES = colonnes
            c.LARGEUR_BRIQUE = largeur
            c.HAUTEUR_BRIQUE = hauteur
            c.VIES = vies
            c.RAYON_BALLE = rayon_b
            c.FACTOR = factor

            messagebox.showinfo("Appliqué", "Paramètres appliqués. Retourne au jeu pour voir les changements.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible d'appliquer les paramètres : {e}")

    def reset_defaults(self):
        """Réinitialise les spinboxes aux valeurs définies actuellement dans cstes (utile si on a fait des erreurs)."""
        self.sb_lignes.delete(0, "end"); self.sb_lignes.insert(0, str(c.LIGNES))
        self.sb_colonnes.delete(0, "end"); self.sb_colonnes.insert(0, str(c.COLONNES))
        self.sb_largeur.delete(0, "end"); self.sb_largeur.insert(0, str(c.LARGEUR_BRIQUE))
        self.sb_hauteur.delete(0, "end"); self.sb_hauteur.insert(0, str(c.HAUTEUR_BRIQUE))
        self.sb_vies_b.delete(0, "end"); self.sb_vies_b.insert(0, str(c.VIES))
        self.sb_rayon_b.delete(0, "end"); self.sb_rayon_b.insert(0, str(c.RAYON_BALLE))
        self.sb_factor.delete(0, "end"); self.sb_factor.insert(0, str(c.FACTOR))


class FenetreJeu(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        top_bar = ttk.Frame(self, padding=(8, 8))
        top_bar.pack(fill="x")

        self.score = 0
        self.score_var = tk.StringVar(value=f"Score : {self.score}")
        ttk.Label(top_bar, textvariable=self.score_var, font=("Arial", 12, "bold")).pack(side="left", padx=8)

        self.lives = c.NOMBRE_VIES
        self.lives_var = tk.StringVar(value=f"Vies : {self.lives}")
        ttk.Label(top_bar, textvariable=self.lives_var, font=("Arial", 12, "bold")).pack(side="left", padx=20)

        bottom_bar = ttk.Frame(self, padding=(8, 8))
        bottom_bar.pack(side="bottom", fill="x")

        ttk.Button(bottom_bar, text="Retour", command=lambda: app.show_frame("FenetreDemarrage")).pack(side="left", padx=6)
        ttk.Button(bottom_bar, text="Quitter", command=app.destroy).pack(side="left", padx=6)

        # Canvas
        self.canvas = tk.Canvas(self, width=c.LARGEUR_CANVA, height=c.HAUTEUR_CANVA, bg="black")
        self.canvas.pack(pady=6)
        self.canvas.focus_set()

        # raquette & input
        self.raquette = Raquette(c.LARGEUR_CANVA, c.HAUTEUR_CANVA)
        self.canvas.bind('<Key>', self.raquette.deplacement_barre)
        self.canvas.bind('<Motion>', self.souris_mouvement)

        # dessiner la raquette (graphique)
        x_center = self.raquette.get_x_center()
        half = self.raquette.largeur_raquette / 2
        y = self.raquette.y
        self.raillet = self.canvas.create_rectangle(
            x_center - half, y - self.raquette.hauteur_raquette/2,
            x_center + half, y + self.raquette.hauteur_raquette/2,
            fill="red"
        )

        # briques & balle — instanciation initiale (ne démarre pas la boucle)
        self.brique_manager = BriqueManager(self.canvas,
                                           lignes=c.LIGNES, colonnes=c.COLONNES,
                                           largeur_brique=c.LARGEUR_BRIQUE, hauteur_brique=c.HAUTEUR_BRIQUE,
                                           top_offset=c.TOP_OFFSET, padding=c.PADDING)
        self.balle = Balle(self.canvas, x=x_center, y=y - 30)

        # état jeu
        self.running = True         # indique que le jeu est actif (non game-over)
        self.paused = True          # << important : start en pause (car l'écran d'accueil est probablement visible)
        self.delay = c.FPS_DELAY_MS
        self._after_id = None       # stockage de l'ID retourné par after pour pouvoir annuler
        # NE PAS appeler self.after ici : on démarrera la boucle dans on_show()

    def on_show(self):
        """Appelé quand la fenêtre devient visible : on reprend le jeu (dépauser)."""
        # Recréer le niveau si les constantes ont changé (comme avant)
        try:
            try:
                self.brique_manager.clear_all()
            except Exception:
                pass

            self.brique_manager = BriqueManager(self.canvas,
                                               lignes=c.LIGNES, colonnes=c.COLONNES,
                                               largeur_brique=c.LARGEUR_BRIQUE, hauteur_brique=c.HAUTEUR_BRIQUE,
                                               top_offset=c.TOP_OFFSET, padding=c.PADDING)
            # repositionner la balle au-dessus de la raquette
            # remplacer l'ancienne balle par une nouvelle avec le rayon modifié
            try:
                self.canvas.delete(self.balle.id)
            except Exception:
                pass
            self.balle = Balle(self.canvas, x=self.raquette.get_x_center(), y=self.raquette.y - 30, rayon=c.RAYON_BALLE)

            self.update_raquette_graphics()
        except Exception as e:
            print("Erreur on_show FenetreJeu:", e)

        # reprendre le jeu : dépauser et lancer la boucle si nécessaire
        self.paused = False
        if self._after_id is None:
            self._schedule_next_frame()

    def on_hide(self):
        """Appelé quand on quitte la fenêtre : mettre le jeu en pause."""
        self.paused = True
        # annuler l'after en attente pour que rien ne tourne en arrière-plan
        if self._after_id is not None:
            try:
                self.after_cancel(self._after_id)
            except Exception:
                pass
            self._after_id = None

    def _schedule_next_frame(self):
        """Planifie la prochaine itération de la boucle et conserve l'id."""
        self._after_id = self.after(self.delay, self.game_loop)

    def souris_mouvement(self, event):
        self.raquette.set_x_center(event.x)

    def update_raquette_graphics(self):
        x_center = self.raquette.get_x_center()
        half = self.raquette.largeur_raquette / 2
        y = self.raquette.y
        self.canvas.coords(self.raillet,
                           x_center - half, y - self.raquette.hauteur_raquette/2,
                           x_center + half, y + self.raquette.hauteur_raquette/2)

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
        try:
            self.brique_manager.clear_all()
        except Exception:
            pass
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
            messagebox.showinfo("Victoire", f"Bravo ! Tu as détruit toutes les briques.\nScore: {self.score}")
            self.restart_game()
            return

        # replanifier prochain frame
        self._schedule_next_frame()


if __name__ == "__main__":
    app = App()
    app.mainloop()
