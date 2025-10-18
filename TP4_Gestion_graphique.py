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

#Importation des fichiers
import TP4_Constantes as C

#Importation des modules
import tkinter as tk

#Classe Manager_fenetre
class Manager_fenetre:
    """
    Classe de gestion des differentes fenetres. Fait le lien entre les 
    demandes du CONTROLLEUR et lui renvoie les resultats des VUE
    """
    def __init__(self,mf_balle:object,mf_raquette:object,score:int):
        #Recuperation des objets transmis par le CONTROLLEUR
        self.mf_balle = mf_balle
        self.mf_raquette = mf_raquette
        self.score = score
        #reflechir aux briques

        #Creation de la fenetre tkinter
        self.mf_fenetre_racine = tk.Tk()
        self.mf_fenetre_racine.title(C.C_TITRE_FENETRE)
        self.mf_fenetre_racine.resizable(False,False)

        #Creation du conteneur de Frame
        self.mf_conteneur = tk.ttk.Frame(self.mf_fenetre_racine)
        self.mf_conteneur.pack(fill="both", expand=True)

        #Creation d'un dico stockant les objets fenetres
        self.mf_dico_fenetre = {}

        #Creation des fenetres a l'initialisation
        for F in (Fenetre_demarage, Fenetre_option, Fenetre_jeu):
            frame = F(parent = self.mf_conteneur, manager = self)
            self.mf_dico_fenetre[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        #Affiche le premier ecran a l'initialisation
        self.afficher_fenetre("Fenetre demarage")

        #Recuperation de l'ecran de jeu pour les mise a jour
        self.mf_ecran_jeu = self.mf_dico_fenetre.get("Fenetre jeu")

    def afficher_fenetre(self,af_nom_fenetre:str):
        """
        Fonction : Affiche la fenetre dont le nom est donne en parametre
        Entree : Le nom de la fenetre (STR)
        Sortie : None
        """
        af_fenetre = self.mf_dico_fenetre.get(af_nom_fenetre)
        if af_fenetre:
            af_fenetre.tkraise()
    
    def demande_lancer_jeu(self):
        """
        Fonction : Renvoie au CONTROLLEUR la demande de l'utilisateur de lancer une partie
        Entree : None
        Sortie : True (BOOL)
        """
        pass

    def update_dessin_raquette(self):
        """
        Fonction : Actualiser le dessin de la raquette
        Entree : 
        Sortie : 
        """
        pass

    def update_dessin_balle(self):
        """
        Fonction : Actualiser le dessin de la 
        Entree : 
        Sortie : 
        """
        pass

    def update_canvas(self):
        """
        Fonction : 
        Entree : 
        Sortie : 
        """
        pass
    

#Classe Mere Fenetre
class Fenetre(tk.ttk.Frame):
    def __init__(self, f_parent:tk.Widget, f_manager:Manager_fenetre, f_nom_fenetre:str):
        super().__init__(f_parent, padding = 20)
        #self.f_manager = f_manager #(?)

        #Nom de cette fenetre
        self.__nom_fenetre = f_nom_fenetre

        #Titre de la fenetre
        self.__titre_fenetre = tk.ttk.Label(self, 
                                            text = f"{C.C_TITRE_FENETRE} - {self.__nom_fenetre}", 
                                            font = ("Arial", 24, "bold"))
        self.__titre_fenetre.pack(pady=20)

        #Barre des infos
        self.haut_barre = tk.ttk.Frame(self, padding = (8, 8))
        self.haut_barre.pack(fill = "x")

        #Barre de menus
        self.bas_barre = tk.ttk.Frame(self, padding = (8, 8))
        self.bas_barre.pack(side = "bottom",fill = "x")

        #Bouton QUITTER
        self.btn_quitter = tk.Button(self.bas_barre,
                                     text = 'QUITTER',
                                     command = f_manager.mf_fenetre_racine.destroy)
        self.btn_quitter.pack(pady = 10)

#Classe Fille Fenetre_demarage
class Fenetre_demarage(Fenetre):
    def __init__(self, f_parent, f_manager, f_nom_fenetre = "Fenetre demarage"):
        super().__init__(f_parent, f_manager,f_nom_fenetre)
        #Bouton OPTION
        self.btn_option = tk.Button(self.bas_barre,
                                     text = 'OPTION',
                                     command = lambda: f_manager.afficher_fenetre("Fenetre option"))
        self.btn_option.pack(pady = 10)

        #Bouton JOUER
        self.btn_jouer = tk.Button(self.bas_barre,
                                     text = 'JOUER',
                                     command = lambda: f_manager.afficher_fenetre("Fenetre jeu"))
        self.btn_jouer.pack(pady = 10)

#Classe Fille Fenetre_option
class Fenetre_option(Fenetre):
    def __init__(self, f_parent, f_manager, f_nom_fenetre = "Fenetre option"):
        super().__init__(f_parent, f_manager, f_nom_fenetre)
        #Bouton OPTION 1
        self.btn_option1 = tk.Button(f_manager.mf_fenetre_racine,
                                     text='OPTION 1')
        self.btn_option1.pack(pady = 10)

        #Bouton OPTION 2
        self.btn_option2 = tk.Button(f_manager.mf_fenetre_racine,
                                     text='OPTION 2')
        self.btn_option2.pack(pady = 10)

        #Bouton RETOUR
        self.btn_retour = tk.Button(self.bas_barre,
                                     text = 'RETOUR',
                                     command = lambda: f_manager.afficher_fenetre("Fenetre demarage"))
        self.btn_retour.pack(pady = 10)

#Classe fille Fenetre_jeu
class Fenetre_jeu(Fenetre):
    def __init__(self, f_parent, f_manager, f_nom_fenetre = "Fenetre jeu"):
        super().__init__(f_parent, f_manager, f_nom_fenetre)
        #Score affichable
        self.fj_score = tk.StringVar(value=f"Score : {f_manager.score}")

        #Creation du Canvas
        self.fj_canvas = tk.Canvas(self, 
                                   width = C.C_LARGEUR_FENETRE, 
                                   height = C.C_HAUTEUR_FENETRE, 
                                   bg = "black")
        self.fj_canvas.pack(pady = 6)

        #Bouton LANCER
        self.btn_lancer = tk.Button(self.bas_barre,
                                     text = 'LANCER',
                                     command = lambda: f_manager.demande_lancer_jeu)
        self.btn_lancer.pack(pady = 10)

        #Bouton RETOUR
        self.btn_retour = tk.Button(self.bas_barre,
                                     text = 'RETOUR',
                                     command = lambda: f_manager.afficher_fenetre("Fenetre demarage"))
        self.btn_retour.pack(pady = 10)

        #Creation graphique de la raquette
        self.fj_raquette = self.fj_canvas.create_rectangle(f_manager.mf_raquette.get_position_raquette[0] - C.C_LARGEUR_RAQUETTE / 2,
                                                           f_manager.mf_raquette.get_position_raquette[1] - C.C_HAUTEUR_RAQUETTE / 2,
                                                           f_manager.mf_raquette.get_position_raquette[0] + C.C_LARGEUR_RAQUETTE / 2,
                                                           f_manager.mf_raquette.get_position_raquette[1] + C.C_HAUTEUR_RAQUETTE / 2,
                                                           fill = 'blue')
        
        #Creation graphique de la balle
        self.fj_balle = self.fj_canvas.create_oval(f_manager.mf_balle.get_position_balle[0] - C.C_RAYON_BALLE,
                                                   f_manager.mf_balle.get_position_balle[1] - C.C_RAYON_BALLE,
                                                   f_manager.mf_balle.get_position_balle[0] + C.C_RAYON_BALLE,
                                                   f_manager.mf_balle.get_position_balle[1] - C.C_RAYON_BALLE,
                                                   fill = 'red')
        
        #Creation graphique des briques
        """a realiser sous forme de fonction afin dajouter des lignes de briques"""


""""""
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
#import tkinter as tk
#import typing as typ

# Titre de l'application
#APP_TITLE = "Casse Brique"

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