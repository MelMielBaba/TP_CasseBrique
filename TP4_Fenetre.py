# -*- coding: utf-8 -*-

#►►EN-TÊTE◄◄
"""
=========================================================================================
Date de creation : 7 octobre 2025
Auteurs: Marie Louise MILLIEN & Elouen WURMSER
Projet: TP4 - CasseBrique
Titre: Fichier principal de la gestion du jeu
=========================================================================================
Description :
    Fichier principal pour lancer le Casse-Brique (version avec options modifiables).
    Utilise : TP4_Constantes.py,
    Cree les instances issues des fichier: TP4_Raquette.py, TP4_Balle.py, TP4_Briques.py
=========================================================================================
"""

#►►IMPORTATIONS◄◄
"""Importation des fichiers"""
import TP4_Constantes as c
from TP4_Raquette import Raquette
from TP4_Balle import Balle
from TP4_Briques import BriqueManager

"""Importation des modules"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from collections import deque
import random as rd
#from PIL import Image, ImageTk  # pour supporter JPEG

#►►CONSTANTES STR◄◄
APP_TITLE = "Casse Brique"

#►►CREATION GESTIONNAIRE FENETRE TKINTER◄◄
class App(tk.Tk):
    """
    Fonction : Herite de tk.Tk() et gere la creation de la fenetre tkinter dans 
    laquelle evolue les differents ecrans
    Attributs : > self.frames : le dictionnaire des objets des fenetres
    Methodes : > show_frame(name) : permet d'afficher la fenetre dont on donne le nom
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

#►►CREATION FENETRE DE DEMARRAGE◄◄
class FenetreDemarrage(ttk.Frame):
    """
    Fonction : Herite de ttk.Frame, qui est un module de tkinter, et gere la creation de 
    l'ecran/la fenetre/le frame qui s'affiche au demarrage du jeu; Cette fentetre possede 
    un bouton QUITTER, un bouton OPTIONS pour acceder au menu des options, et un bouton 
    JOUER pour acceder a la fenetre de jeu; Les boutons sont placer sur une barre et une 
    image de fond est prevue pour s'afficher en-dessous grace a un canvas (cette idée 
    n'est pour le moment pas aboutie ni opérationnelle)
    Attributs : > self.app : reference a la fenetre tkinter de App() [?]
                > self.photo : la reference de l'image dans tkinter
                > self.img_dict : le dictionnaire pour referer l'image
                > self.canvas : le canvas pour placer l'image
    Methodes : > ouvrir_image() : permet d'afficher l'image dans le canvas
    """
    def __init__(self, parent, app):
        #Heritage du module et reference a la fenetre tkinter App()
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

        #Gestion de l'image de fond
        self.photo = None #pour garder une reference
        self.img_dict = {}
        self.canvas = tk.Canvas(self, width=c.LARGEUR_CANVA, height=c.HAUTEUR_CANVA, bg="black")
        self.canvas.pack(pady=6)

        #Affichage de l'image dès l'initialisation
        #self.ouvrir_image()
    
    def ouvrir_image(self):
        """
        Fonction : 
        Entree : None
        Sortie : None
        """
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

#►►CREATION FENETRE DU MENU DES OPTIONS◄◄
class FenetreOption(ttk.Frame):
    """
    Fonction : Herite de ttk.Frame, qui est un module de tkinter, et gere la creation de 
    l'ecran/la fenetre/le frame du menu des options; Cette fenetre permet 
    de modifier les constantes liées aux briques ou a la balle; Le jeu a des parametres 
    par defaut qui sont modifiables pour certains par ce menu comme par exemple le nombre 
    de lignes ou de collonne de briques ou le rayon de la balle; Elle possede plusieurs 
    bouton afin de soit APPLIQUER les parametres selectionnés, REINITIALISER les 
    parametres par defaut, pouvoir faire un RETOUR au menu de demarrage ou QUITTER le jeu
    Attributs : > self.app : reference a la fenetre tkinter de App() [?]
                > self.sb_lignes, self.sb_colonnes, self.sb_largeur, self.sb_hauteur, 
                self.sb_vies_b, self.sb_rayon_b, self.sb_factor: spinbox des parametre 
                modifiables (nb lignes de briques, nb de colonnes de briques, largeur 
                d'une brique, hauteur d'une brique, vie d'une brique, vitesse de la balle, 
                facteur d'acceleration)
    Methodes : > apply_changes() : permet de modifier les parametres lorqu'il est modifié
               > reset_defaults() : permet de remettre les parametre a leur valeur 
               d'origine
    """
    def __init__(self, parent, app):
        #Heritage du module et reference a la fenetre tkinter App()
        super().__init__(parent, padding=16)
        self.app = app

        #Titre du menu
        ttk.Label(self, text="Options", font=("Arial", 20, "bold")).pack(pady=(0,12))

        #Frame pour placer les paramètres modifiable
        frame_params = ttk.Frame(self)
        frame_params.pack(pady=6, padx=6, fill="x")

        #Fonction pour créer ligne label & spinbox
        def make_spin(parent, label_text, var_init, from_, to_, increment=1):
            """
            Fonction : Permettre d'eviter d'alourdir le code par la repetition des etapes 
            pour ajouter une nouvelle ligne de parametre modifiable
            Entrees : >Parent:La ou placer la ligne; >Label_text:texte a afficher; 
                      >Var_init:la valeur initiale du parametre; >from_:valeur minimale 
                      autorisée pour ce parametre; >to_:valeur maximale autorisée pour ce 
                      parametre
            Sortie : La variable sb, une Spinbox pour ce parametre
            """
            #on creer un frame pour placer la spinbox
            row = ttk.Frame(parent)
            row.pack(fill="x", pady=4)

            #on ajoute un titre a la ligne
            ttk.Label(row, text=label_text, width=20, anchor="w").pack(side="left")

            #on creer la spinbox
            sb = tk.Spinbox(row, from_=from_, to=to_, increment=increment, width=8)
            sb.pack(side="left")
            sb.delete(0, "end")
            sb.insert(0, str(var_init))

            return sb

        #Spinboxes pour les paramètres modifiable
        self.sb_lignes = make_spin(frame_params, "Lignes (LIGNES)", c.LIGNES, 1, 30, 1)
        self.sb_colonnes = make_spin(frame_params, "Colonnes (COLONNES)", c.COLONNES, 1, 30, 1)
        self.sb_largeur = make_spin(frame_params, "Largeur brique (px)", c.LARGEUR_BRIQUE, 10, 300, 1)
        self.sb_hauteur = make_spin(frame_params, "Hauteur brique (px)", c.HAUTEUR_BRIQUE, 6, 120, 1)
        self.sb_vies_b = make_spin(frame_params, "Vies des briques", c.VIES, 1, 5, 1)
        self.sb_rayon_b = make_spin(frame_params, "Rayon de la balle", c.RAYON_BALLE, 5, 500, 1)
        self.sb_factor = make_spin(frame_params, "Accelerations",c.FACTOR,1,10,0.05)

        #Barre où placer les boutons
        btn_row = ttk.Frame(self)
        btn_row.pack(pady=12)

        #Boutons
        ttk.Button(btn_row, text="APPLIQUER", command=self.apply_changes).pack(side="left", padx=6)
        ttk.Button(btn_row, text="REINITIALISER", command=self.reset_defaults).pack(side="left", padx=6)
        ttk.Button(btn_row, text="RETOUR", command=lambda: app.show_frame("FenetreDemarrage")).pack(side="left", padx=6)
        ttk.Button(btn_row, text="JOUER", command=lambda: app.show_frame("FenetreJeu")).pack(side="left", padx=6)
        ttk.Button(btn_row, text="QUITTER", command=app.destroy).pack(side="left", padx=6)

        #Affichage d'un texte donnant des indications en remarques
        ttk.Label(self, text="Les modifications s'appliquent quand on retourne à la fenêtre du jeu.", foreground="gray").pack(pady=(8,0))

    def apply_changes(self):
        """
        Fonction : Applique les valeurs des spinboxes aux constantes dans TP4_Constantes 
        (module c)
        Entree : None
        Sortie : None
        """
        try:
            #Lire et convertir
            lignes = int(self.sb_lignes.get())
            colonnes = int(self.sb_colonnes.get())
            largeur = int(self.sb_largeur.get())
            hauteur = int(self.sb_hauteur.get())
            vies = int(self.sb_vies_b.get())
            rayon_b = int(self.sb_rayon_b.get())
            factor = float(self.sb_factor.get())

            #Valider les contraintes basiques
            if lignes < 1 or colonnes < 1 or largeur < 4 or hauteur < 4:
                messagebox.showwarning("Valeurs invalides", "Certaines valeurs sont trop petites.")
                return

            #Appliquer dans le module TP4_Constantes 
            """(cela prendra effet pour les nouvelles génération de niveau)"""
            c.LIGNES = lignes
            c.COLONNES = colonnes
            c.LARGEUR_BRIQUE = largeur
            c.HAUTEUR_BRIQUE = hauteur
            c.VIES = vies
            c.RAYON_BALLE = rayon_b
            c.FACTOR = factor

            #Affichage d'un message de validation
            messagebox.showinfo("Appliqué", "Paramètres appliqués. Retourner au jeu pour voir les changements.")
        
        #En cas d'erreur affiche un message
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible d'appliquer les paramètres : {e}")

    def reset_defaults(self):
        """
        Fonction : Réinitialise les spinboxes aux valeurs définies initialement dans 
        TP4_Constantes (utile si on a fait des erreurs)
        Entree : None
        Sortie : None
        """
        self.sb_lignes.delete(0, "end"); self.sb_lignes.insert(0, str(c.LIGNES))
        self.sb_colonnes.delete(0, "end"); self.sb_colonnes.insert(0, str(c.COLONNES))
        self.sb_largeur.delete(0, "end"); self.sb_largeur.insert(0, str(c.LARGEUR_BRIQUE))
        self.sb_hauteur.delete(0, "end"); self.sb_hauteur.insert(0, str(c.HAUTEUR_BRIQUE))
        self.sb_vies_b.delete(0, "end"); self.sb_vies_b.insert(0, str(c.VIES))
        self.sb_rayon_b.delete(0, "end"); self.sb_rayon_b.insert(0, str(c.RAYON_BALLE))
        self.sb_factor.delete(0, "end"); self.sb_factor.insert(0, str(c.FACTOR))

#►►CREATION FENETRE DU MENU DU JEU◄◄
class FenetreJeu(ttk.Frame):
    """
    Fonction : Herite de ttk.Frame, qui est un module de tkinter, et gere la creation de 
    l'ecran/la fenetre/le frame qui gere le jeu; 
    Attributs : > self.app : reference a la fenetre tkinter de App() [?]
                > self.sb_lignes, self.sb_colonnes, self.sb_largeur, self.sb_hauteur, 
                self.sb_vies_b, self.sb_rayon_b, self.sb_factor: spinbox des parametre 
                modifiables (nb lignes de briques, nb de colonnes de briques, largeur 
                d'une brique, hauteur d'une brique, vie d'une brique, vitesse de la balle, 
                facteur d'acceleration)
    Methodes : > on_show() : passe la fenetre en visible et de (re)prendre le jeu
               > on_hide() : met le jeu en pause si on quitte la fenetre
               > _schedule_next_frame() : planifie la prochaine itération de boucle et 
               conserve l'id
               > souris_mouvement(event) : gestion des deplacement de la raquette avec la 
               souris
               > update_raquette_graphics() : mise a jour du dessin de la raquette
               > check_collisions() : Verification des collisions
               > game_over() : Gestion de fin de partie en cas de defaite
               > restart_game() : Recreer une nouvelle partie sans la lancer
               > game_loop() : Boucle principale de jeu
               > lancer_game() : Lancement du jeu via un bouton
               > arreter_game() : Met le jeu en pause
    """
    def __init__(self, parent, app):
        #Heritage du module et reference a la fenetre tkinter App()
        super().__init__(parent)
        self.app = app

        #►BARRES D'AFFICHAGE◄
        """Haut - Score et vies"""
        top_bar = ttk.Frame(self, padding=(8, 8))
        top_bar.pack(fill="x")
        """Bas - Boutons"""
        bottom_bar = ttk.Frame(self, padding=(8, 8))
        bottom_bar.pack(side="bottom", fill="x")

        #►PILE & FILE◄
        """Pile pour enregistrement des scores; File pour les bonus des briques"""
        self.historique_scores = []   # pile (LIFO)
        self.file_bonus = deque()     # file (FIFO)

        #►SCORE◄
        """Initialisation & affichage"""
        self.score = 0
        self.score_var = tk.StringVar(value=f"Score : {self.score}")
        ttk.Label(top_bar, textvariable=self.score_var, font=("Arial", 12, "bold")).pack(side="left", padx=8)

        #►VIES◄
        """Initialisation & affichage"""
        self.lives = c.NOMBRE_VIES
        self.lives_var = tk.StringVar(value=f"Vies : {self.lives}")
        ttk.Label(top_bar, textvariable=self.lives_var, font=("Arial", 12, "bold")).pack(side="left", padx=20)

        #►BOUTONS◄
        ttk.Button(bottom_bar, text="RETOUR", command=lambda: app.show_frame("FenetreDemarrage")).pack(side="left", padx=6)
        ttk.Button(bottom_bar, text="LANCER",command=self.lancer_game).pack(side="left", padx=6)
        ttk.Button(bottom_bar, text="PAUSE",command=self.arreter_game).pack(side="left", padx=6)
        ttk.Button(bottom_bar, text="Annuler Score", command=self.supprimer_dernier_score).pack(side="left", padx=6)
        ttk.Button(bottom_bar, text="QUITTER", command=app.destroy).pack(side="left", padx=6)

        #►CANVAS◄
        self.canvas = tk.Canvas(self, width=c.LARGEUR_CANVA, height=c.HAUTEUR_CANVA, bg="black")
        self.canvas.pack(pady=6)

        #►RAQUETTE◄
        """Initialisation de la raquette & gestion des inputs"""
        self.raquette = Raquette(c.LARGEUR_CANVA, c.HAUTEUR_CANVA)
        self.canvas.bind('<Key>', self.raquette.deplacement_barre) #controle clavier
        #self.canvas.bind('<Motion>', self.souris_mouvement) #controle souris

        """Dessin de la raquette (graphique)"""
        x_center = self.raquette.get_x_center()
        half = self.raquette.largeur_raquette / 2
        y = self.raquette.y
        self.raillet = self.canvas.create_rectangle(
            x_center - half, y - self.raquette.hauteur_raquette/2,
            x_center + half, y + self.raquette.hauteur_raquette/2,
            fill="red"
        )

        #►BRIQUES◄
        """Instanciation initiale (ne démarre pas la boucle)"""
        self.brique_manager = BriqueManager(self.canvas,
                                           lignes=c.LIGNES, colonnes=c.COLONNES,
                                           largeur_brique=c.LARGEUR_BRIQUE, hauteur_brique=c.HAUTEUR_BRIQUE,
                                           top_offset=c.TOP_OFFSET, padding=c.PADDING)
        
        #►BALLE◄
        """Instanciation initiale (ne démarre pas la boucle)"""
        self.balle = Balle(self.canvas, x=x_center, y=y - 30)

        #►ETAT DU JEU◄
        """Running & pause"""
        self.running = False    #Indication jeu actif (non game-over)
        self.paused = True      #Initialisation en pause (écran demarrage probablement visible)
        """Delai de mise a jour de la boucle"""
        self.delay = c.FPS_DELAY_MS
        self._after_id = None   #Stockage de l'ID retourné par after pour pouvoir annuler
        #/!\NE PAS appeler self.after ici : on démarrera la boucle dans on_show()/!\

    def on_show(self):
        """
        Fonction : Appelée quand la fenêtre devient visible : on reprend le jeu (dépauser)
        Entree : None
        Sortie : None
        """
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
        #Met le jeu en etat de pause
        self.paused = True

        #Annuler l'after en attente pour que rien ne tourne en arrière-plan
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
        #COLLISIONS DES MURS
        l, t, r, b = self.balle.coords()

        #◗rebond gauche◖
        if l <= 0:
            self.balle.rebond_x()
            self.balle.x = self.balle.rayon

        #◗rebond droite◖
        elif r >= c.LARGEUR_CANVA:
            self.balle.rebond_x()
            self.balle.x = c.LARGEUR_CANVA - self.balle.rayon

        #◗rebond haut◖
        elif t <= 0:
            self.balle.rebond_y()
            self.balle.y = self.balle.rayon

        #◗rebond bas : perte de vie◖
        elif b >= c.HAUTEUR_CANVA:
            self.lives -= 1
            self.lives_var.set(f"Vies : {self.lives}")
            if self.lives <= 0:
                self.game_over()
                return
            else:
                self.balle.reset(x=self.raquette.get_x_center(), y=self.raquette.y - 30)
                return

        #COLLISIONS AVEC LA RAQUETTE
        """Recuperation des coins des deux objets"""
        rx1, ry1, rx2, ry2 = self.canvas.coords(self.raillet)
        bx1, by1, bx2, by2 = self.balle.coords()

        """Verification de la collision"""
        if not (bx2 < rx1 or bx1 > rx2 or by2 < ry1 or by1 > ry2):
            self.balle.rebond_y()
            ball_cx = (bx1 + bx2) / 2
            paddle_cx = (rx1 + rx2) / 2
            delta = (ball_cx - paddle_cx) / ((rx2 - rx1) / 2)
            max_horizontal = 5.0
            self.balle.vx += delta * max_horizontal
            self.balle.y = ry1 - self.balle.rayon - 1

        #COLLISIONS AVEC LES BRIQUES
        """Verification via le manager des briques"""
        hit = self.brique_manager.collision(self.balle)

        """Si collision activer le rebond, verifier les bonus et mise a jour du score"""
        if hit is not None:
            #1 chance sur 3 par brique cassée d’ajouter un bonus
            if rd.randint(1,10) == 1:
                self.file_bonus.append(rd.choice(["+1 vie","Accélération","Score x2","Balle+"]))
            
            #Traitement d'un bonus si présent
            if self.file_bonus:
                #Selection d'un bonus
                bonus = self.file_bonus.popleft() # Fifo
                self.afficher_message_bonus(bonus)

                #◗Nouvelle vie◖
                if bonus == "+1 vie":
                    self.lives += 1
                    self.lives_var.set(f"Vies : {self.lives}")
                
                #◗Acceleration◖
                elif bonus == "Accélération":
                    self.balle.aug_vitesse(1.1)

                #◗Multiplication score◖
                elif bonus == "Score x2":
                    self.score *= 2
                    self.score_var.set(f"Score : {self.score}")
                
                #◗Balle plus grosse◖
                elif bonus == "Balle+":
                    self.grossir_balle()

            #Gestion du rebond et du score
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
        #On recrée un niveau prêt à jouer, mais en pause
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
        
        #Creation d'un nouveau gestionnaire de briques
        self.brique_manager = BriqueManager(self.canvas,
                                           lignes=c.LIGNES, colonnes=c.COLONNES,
                                           largeur_brique=c.LARGEUR_BRIQUE, hauteur_brique=c.HAUTEUR_BRIQUE,
                                           top_offset=c.TOP_OFFSET, padding=c.PADDING)
        
        #Reinitialise la balle au-dessus de la raquette
        self.balle.reset(x=self.raquette.get_x_center(), y=self.raquette.y - 30)
        
        #Mise à jour graphique de la raquette (au cas où)
        self.update_raquette_graphics()

        #On stoppe la boucle (pas de mouvement)
        self.paused = True
        self.running = False

        #S'assurer qu'aucun after ne reste planifié
        if self._after_id is not None:
            try:
                self.after_cancel(self._after_id)
            except Exception:
                pass
        
        #Passe l'after a None [?]
        self._after_id = None

    def game_loop(self):
        """
        Fonction : Gestion de la boucle de jeu
        Entree : None
        Sortie : None
        """
        #Clear after id (car on est dans l'itération déclenchée)
        self._after_id = None

        #Ne rien faire si en pause, mais ne pas boucler automatiquement
        if self.paused or not self.running:
            return

        #Déplacer la raquette graphique, la balle & verifier collisions
        self.update_raquette_graphics()
        self.balle.move()
        self.check_collisions()

        #Verification condition de victoire
        if self.brique_manager.reste() == 0:
            self.arreter_game()
            messagebox.showinfo("Victoire", f"Bravo ! Tu as détruit toutes les briques.\nScore: {self.score}")
            self.restart_game()  #Prépare le nouveau niveau (sans le lancer)
            return

        #Replanifier prochain frame
        self._schedule_next_frame()

    def lancer_game(self):
        """
        Fonction : Active le jeu et s'assure qu'une itération est planifiée
        Entree : None
        Sortie : None
        """
        #Passe le running est True
        self.running = True

        #Enlever la pause si besoin
        self.paused = False

        #Si aucune itération n'est planifiée, en créer une
        if self._after_id is None:
            self._schedule_next_frame()

        #Donner le focus au canvas pour capter le clavier
        try:
            self.canvas.focus_set()
        except Exception:
            pass
    
    def arreter_game(self):
        """
        Fonction : Désactive le jeu et annule l'after en attente pour arrêter 
        proprement la boucle
        Entree : None
        Sortie : None
        """
        #Passe le running en False
        self.running = False

        #Mettre en pause aussi (optionnel)
        self.paused = True

        #Annuler l'after s'il existe
        if self._after_id is not None:
            try:
                self.after_cancel(self._after_id)
            except Exception:
                pass
            self._after_id = None

    def supprimer_dernier_score(self):
        """
        Fonction : Retire le dernier score sauvegardé (pile LIFO)
        """
        if not self.historique_scores:
            messagebox.showinfo("Aucun score précédent à annuler.")
            return
        ancien_score = self.historique_scores.pop()
        self.score = ancien_score
        self.score_var.set(f"Score : {self.score}")
        messagebox.showinfo("Historique", f"Score précédent restauré : {ancien_score}")

    def afficher_message_bonus(self, texte):
        """
        Affiche un message temporaire au centre du canvas.
        """
        largeur = self.canvas.winfo_width()
        hauteur = self.canvas.winfo_height()
        message_id = self.canvas.create_text(
            largeur / 2,
            hauteur / 2,
            text=texte,
            font=("Arial", 18, "bold"),
            fill="yellow"
        )
        # Le message disparaît après 2 secondes
        self.after(2000, lambda: self.canvas.delete(message_id))

    def grossir_balle(self):
        """
        Bonus : fait grossir la balle temporairement (5 secondes)
        Utilise la même méthode que dans le menu Option.
        """
        #1.5x plus grand)
        nouveau_rayon = int(c.RAYON_BALLE * 1.5)
        c.RAYON_BALLE = nouveau_rayon 

        # Redessiner la balle avec le nouveau rayon
        x, y = self.balle.x, self.balle.y
        self.canvas.coords(
            self.balle.id,
            x - nouveau_rayon,
            y - nouveau_rayon,
            x + nouveau_rayon,
            y + nouveau_rayon
        )
        self.balle.rayon = nouveau_rayon
        # Rétablir après 5 secondes
        self.after(5000, self.reduire_balle)

    def reduire_balle(self):
        """
        Rétablit la taille normale de la balle après grossissement.
        """
        # Rayon normal depuis les constantes
        rayon_normal = int(c.RAYON_BALLE / 1.5)
        c.RAYON_BALLE = rayon_normal

        x, y = self.balle.x, self.balle.y
        self.canvas.coords(
            self.balle.id,
            x - rayon_normal,
            y - rayon_normal,
            x + rayon_normal,
            y + rayon_normal
        )
        self.balle.rayon = rayon_normal
