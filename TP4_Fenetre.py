# -*- coding: utf-8 -*-
"""
Date de creation : 7 octobre 2025
Auteurs: Marie Louise MILLIEN & Elouen WURMSER
Projet: TP4 - CasseBrique
Titre: Fichier principal de la gestion du jeu
"""

"""
Description :
    Fichier principal pour lancer le Casse-Brique (version avec options modifiables).
    Utilise : TP4_Constantes.py,
    Cree les instances issues des fichier: TP4_Raquette.py, TP4_Balle.py, TP4_Briques.py
"""

#Importation des fichiers
import TP4_Constantes as c
from TP4_Raquette import Raquette
from TP4_Balle import Balle
from TP4_Briques import BriqueManager

#Importation des modules
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
#from PIL import Image, ImageTk  # pour supporter JPEG

#Constante de type str
APP_TITLE = "Casse Brique"

#Creation de la classe qui gere les differentes fenetres
class App(tk.Tk):
    """
    Fonction : Herite de tk.Tk() et gere la creation de la fenetre tkinter dans 
    laquelle evolue les differents ecrans
    Attributs : self.frames le dictionnaire des objets des fenetres
    Methodes : show_frame(name) permet d'afficher la fenetre dont on donne le nom
    """
    def __init__(self):
        #Creation de la fenetre tkinter
        super().__init__()
        self.title(APP_TITLE)
        self.resizable(False, False)

        #Creation du conteneur des frames
        container = ttk.Frame(self)
        container.pack(fill="both", expand=True)

        #Creation d'un dictionnaire stockant les objets fenetres
        self.frames = {}
        for F in (FenetreDemarrage, FenetreOption, FenetreJeu):
            frame = F(parent=container, app=self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        #Affichage de la premiere fenetre
        self.show_frame("FenetreDemarrage")

    def show_frame(self, name: str):
        """
        Fonction : Affiche la frame identifiée par son nom et gère on_hide/on_show.
        Entree : Le nom de la fenetre a afficher
        Sortie : None
        """
        #Recuperation de la fenetre d'avant ?
        prev = getattr(self, "_current_frame_name", None)

        #Appeler on_hide sur la frame précédente si elle a la méthode
        if prev is not None and prev in self.frames:
            prev_frame = self.frames.get(prev)
            if hasattr(prev_frame, "on_hide") and callable(prev_frame.on_hide):
                try:
                    prev_frame.on_hide()
                except Exception as e:
                    print("Erreur on_hide:", e)

        #Recuperation de la fenetre a afficher maintenant
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

#Classe de la fenetre de demarrage
class FenetreDemarrage(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, padding=20)
        self.app = app

        #Titre du jeu
        ttk.Label(self, text=APP_TITLE, font=("Arial", 24, "bold")).pack(pady=20)

        #Barre des boutons
        bnt_barre = ttk.Frame(self)
        bnt_barre.pack(pady=12)

        #Boutons
        ttk.Button(bnt_barre, text="JOUER", command=lambda: app.show_frame("FenetreJeu")).pack(side="left",padx=10)
        ttk.Button(bnt_barre, text="OPTIONS", command=lambda: app.show_frame("FenetreOption")).pack(side="left",padx=10)
        ttk.Button(bnt_barre, text="QUITTER", command=app.destroy).pack(side="left",padx=10)

        self.photo = None #pour garder une reference
        self.img_dict = {}
        self.canvas = tk.Canvas(self, width=c.LARGEUR_CANVA, height=c.HAUTEUR_CANVA, bg="black")
        self.canvas.pack(pady=6)

        self.ouvrir_image()
    
    def ouvrir_image(self):
        #filename = filedialog.askopenfilename(title="Ouvrir l'image", filetypes=[("Images JPEG","*.jpeg"),("Tous types","*.*")])

        # Efface le canvas
        self.canvas.delete("all")

        # Demande un fichier image
        filename = filedialog.askopenfilename(title="Ouvrir l'image",
                                              filetypes=[("Images PNG", "*.png"), ("Tous types", "*.*")])

        if not filename:
            return  # annulation

        self.photo = tk.PhotoImage(file=filename)
    
        # Conserve une référence pour éviter le garbage collection
        self.img_dict[filename] = self.photo

        # Affiche l'image en haut à gauche
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)

        # Ajuste la taille du canvas
        self.canvas.config(width=self.photo.width(), height=self.photo.height())



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

        ttk.Button(btn_row, text="APPLIQUER", command=self.apply_changes).pack(side="left", padx=6)
        ttk.Button(btn_row, text="REINITIALISER", command=self.reset_defaults).pack(side="left", padx=6)
        ttk.Button(btn_row, text="RETOUR", command=lambda: app.show_frame("FenetreDemarrage")).pack(side="left", padx=6)
        ttk.Button(btn_row, text="JOUER", command=lambda: app.show_frame("FenetreJeu")).pack(side="left", padx=6)
        ttk.Button(btn_row, text="QUITTER", command=app.destroy).pack(side="left", padx=6)

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
        #Heritage de la fenetre tkinter
        super().__init__(parent)
        self.app = app

        #Barres d'affichage
        #►Haut - Score et vies
        top_bar = ttk.Frame(self, padding=(8, 8))
        top_bar.pack(fill="x")
        #►Bas - Boutons
        bottom_bar = ttk.Frame(self, padding=(8, 8))
        bottom_bar.pack(side="bottom", fill="x")

        #Initiation du score et affichage
        self.score = 0
        self.score_var = tk.StringVar(value=f"Score : {self.score}")
        ttk.Label(top_bar, textvariable=self.score_var, font=("Arial", 12, "bold")).pack(side="left", padx=8)

        #Initiation des vies et affichage
        self.lives = c.NOMBRE_VIES
        self.lives_var = tk.StringVar(value=f"Vies : {self.lives}")
        ttk.Label(top_bar, textvariable=self.lives_var, font=("Arial", 12, "bold")).pack(side="left", padx=20)

        #Creation des boutons
        ttk.Button(bottom_bar, text="RETOUR", command=lambda: app.show_frame("FenetreDemarrage")).pack(side="left", padx=6)
        ttk.Button(bottom_bar, text="LANCER",command=self.lancer_game).pack(side="left", padx=6)
        ttk.Button(bottom_bar, text="PAUSE",command=self.arreter_game).pack(side="left", padx=6)
        ttk.Button(bottom_bar, text="QUITTER", command=app.destroy).pack(side="left", padx=6)

        #Creation du canvas
        self.canvas = tk.Canvas(self, width=c.LARGEUR_CANVA, height=c.HAUTEUR_CANVA, bg="black")
        self.canvas.pack(pady=6)

        #Initiation de la raquette & gestion des inputs
        self.raquette = Raquette(c.LARGEUR_CANVA, c.HAUTEUR_CANVA)
        self.canvas.bind('<Key>', self.raquette.deplacement_barre) #controle clavier
        #self.canvas.bind('<Motion>', self.souris_mouvement) #controle souris

        #Dessin de la raquette (graphique)
        x_center = self.raquette.get_x_center()
        half = self.raquette.largeur_raquette / 2
        y = self.raquette.y
        self.raillet = self.canvas.create_rectangle(
            x_center - half, y - self.raquette.hauteur_raquette/2,
            x_center + half, y + self.raquette.hauteur_raquette/2,
            fill="red"
        )

        #Briques & balle — instanciation initiale (ne démarre pas la boucle)
        self.brique_manager = BriqueManager(self.canvas,
                                           lignes=c.LIGNES, colonnes=c.COLONNES,
                                           largeur_brique=c.LARGEUR_BRIQUE, hauteur_brique=c.HAUTEUR_BRIQUE,
                                           top_offset=c.TOP_OFFSET, padding=c.PADDING)
        self.balle = Balle(self.canvas, x=x_center, y=y - 30)

        #Etat jeu
        self.running = False         # indique que le jeu est actif (non game-over)
        self.paused = True          # << important : start en pause (car l'écran d'accueil est probablement visible)
        self.delay = c.FPS_DELAY_MS
        self._after_id = None       # stockage de l'ID retourné par after pour pouvoir annuler
        # NE PAS appeler self.after ici : on démarrera la boucle dans on_show()

    def on_show(self):
        """
        Fonction : Appelée quand la fenêtre devient visible : on reprend le jeu (dépauser)
        Entree : None
        Sortie : None
        """
        #On demarre le focus du canvas ici pour etre sur qu'il 'ecoute' bien les input clavier
        self.canvas.focus_set()
        #Recréer le niveau si les constantes ont changé (comme avant)
        try:
            try:
                self.brique_manager.clear_all()
            except Exception:
                pass

            #Réarranger les briques
            self.brique_manager = BriqueManager(self.canvas,
                                               lignes=c.LIGNES, colonnes=c.COLONNES,
                                               largeur_brique=c.LARGEUR_BRIQUE, hauteur_brique=c.HAUTEUR_BRIQUE,
                                               top_offset=c.TOP_OFFSET, padding=c.PADDING)
            
            try:
                self.canvas.delete(self.balle.id)
            except Exception:
                pass

            #Repositionne la balle au-dessus de la raquette en lui appliquant les nouveaux parametres
            self.balle = Balle(self.canvas, x=self.raquette.get_x_center(), y=self.raquette.y - 30, rayon=c.RAYON_BALLE)
            
            #Mise a jour du dessin
            self.update_raquette_graphics()

        except Exception as e:
            print("Erreur on_show FenetreJeu:", e)

        #Reprise du jeu : dépauser et lancer la boucle si nécessaire
        self.paused = False
        if self._after_id is None:
            self._schedule_next_frame()

    def on_hide(self):
        """
        Fonction : Appelée quand on quitte la fenêtre : mettre le jeu en pause
        Entree : None
        Sortie : None
        """
        self.paused = True
        # annuler l'after en attente pour que rien ne tourne en arrière-plan
        if self._after_id is not None:
            try:
                self.after_cancel(self._after_id)
            except Exception:
                pass
            self._after_id = None

    def _schedule_next_frame(self):
        """
        Fonction : Planifie la prochaine itération de la boucle et conserve l'id
        Entree : None
        Sortie : None
        """
        self._after_id = self.after(self.delay, self.game_loop)

    def souris_mouvement(self, event):
        """
        Fonction : Gestion du deplacement de la raquette avec les mouvement de la souris
        Entree : None
        Sortie : None
        """
        self.raquette.set_x_center(event.x)

    def update_raquette_graphics(self):
        """
        Fonction : Mise a jour du dessin de la raquette
        Entree : None
        Sortie : None
        """
        #Redefinition des nouveaux parametres
        x_center = self.raquette.get_x_center()
        half = self.raquette.largeur_raquette / 2
        y = self.raquette.y

        #Actualisation des parametre de l'affichage du dessin
        self.canvas.coords(self.raillet,
                           x_center - half, y - self.raquette.hauteur_raquette/2,
                           x_center + half, y + self.raquette.hauteur_raquette/2)

    def check_collisions(self):
        """
        Fonction : Verification des collisions de la balle avec les murs (haut, 
        gauche, droit), la raquette, les briques, et le cas de perte de balle 
        (mur bas)
        Entree : None
        Sortie : None
        """
        #Collisions des murs
        l, t, r, b = self.balle.coords()
        #rebond gauche
        if l <= 0:
            self.balle.rebond_x()
            self.balle.x = self.balle.rayon
        #rebond droite
        elif r >= c.LARGEUR_CANVA:
            self.balle.rebond_x()
            self.balle.x = c.LARGEUR_CANVA - self.balle.rayon
        #rebond haut
        elif t <= 0:
            self.balle.rebond_y()
            self.balle.y = self.balle.rayon

        #rebond bas -> perte de vie
        elif b >= c.HAUTEUR_CANVA:
            self.lives -= 1
            self.lives_var.set(f"Vies : {self.lives}")
            if self.lives <= 0:
                self.game_over()
                return
            else:
                self.balle.reset(x=self.raquette.get_x_center(), y=self.raquette.y - 30)
                return

        #Collisions avec la raquette
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

        #Collision avec les briques
        hit = self.brique_manager.collision(self.balle)
        if hit is not None:
            self.balle.rebond_y()
            self.score += 1
            self.score_var.set(f"Score : {self.score}")

    def game_over(self):
        """
        Fonction : Passe l'attribut running en False et affiche la messagebox 
        de fin de partie en cas de defaite
        Entree : None
        Sortie : None
        """
        self.arreter_game()
        messagebox.showinfo("Game Over", f"Game over!\nScore: {self.score}")
        # On recrée un niveau prêt à jouer, mais en pause
        self.restart_game()

    def restart_game(self):
        """
        Fonction : Reinitialise les parametre de score et de vie, recreer de 
        nouvelles briques
        Entree : None
        Sortie : None
        """
        #Reinitialisation des parametres
        self.score = 0
        self.score_var.set(f"Score : {self.score}")
        self.lives = c.NOMBRE_VIES
        self.lives_var.set(f"Vies : {self.lives}")

        #Effacer toutes les briques et en recréer de nouvelles
        try:
            self.brique_manager.clear_all()
        except Exception:
            pass

        self.brique_manager = BriqueManager(self.canvas,
                                           lignes=c.LIGNES, colonnes=c.COLONNES,
                                           largeur_brique=c.LARGEUR_BRIQUE, hauteur_brique=c.HAUTEUR_BRIQUE,
                                           top_offset=c.TOP_OFFSET, padding=c.PADDING)
        
        #Reinitialise la balle au-dessus de la raquette
        self.balle.reset(x=self.raquette.get_x_center(), y=self.raquette.y - 30)
        
        # Mise à jour graphique de la raquette (au cas où)
        self.update_raquette_graphics()

        # On stoppe la boucle (pas de mouvement)
        self.paused = True
        self.running = False

        # S'assurer qu'aucun after ne reste planifié
        if self._after_id is not None:
            try:
                self.after_cancel(self._after_id)
            except Exception:
                pass
        self._after_id = None

    def game_loop(self):
        """
        Fonction : Gestion de la boucle de jeu
        Entree : None
        Sortie : None
        """
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
            self.arreter_game()
            messagebox.showinfo("Victoire", f"Bravo ! Tu as détruit toutes les briques.\nScore: {self.score}")
            self.restart_game()  # Prépare le nouveau niveau (sans le lancer)
            return

        # replanifier prochain frame
        self._schedule_next_frame()

    def lancer_game(self):
        """
        Fonction : Active le jeu et s'assure qu'une itération est planifiée
        Entree : None
        Sortie : 
        """
        self.running = True
        # dépauser si besoin
        self.paused = False
        # Si aucune itération n'est planifiée, en créer une
        if self._after_id is None:
            self._schedule_next_frame()
        # donner le focus au canvas pour capter le clavier
        try:
            self.canvas.focus_set()
        except Exception:
            pass
    
    def arreter_game(self):
        """
        Fonction : Désactive le jeu et annule l'after en attente pour arrêter 
        proprement la boucle
        Entree : None
        Sortie : 
        """
        self.running = False
        # Optionnel : mettre en pause aussi
        self.paused = True
        # annuler l'after s'il existe
        if self._after_id is not None:
            try:
                self.after_cancel(self._after_id)
            except Exception:
                pass
            self._after_id = None