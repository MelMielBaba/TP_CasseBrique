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
from tkinter import ttk #sous-module de tkinter donc on doit l'importer a part

#Classe Manager_fenetre
class Manager_fenetre:
    """
    Classe de gestion des differentes fenetres. Fait le lien entre les 
    demandes du CONTROLLEUR et lui renvoie les resultats des VUE
    """
    def __init__(self,mf_balle:object,mf_raquette:object,mf_briques:dict,score:int,vies:int):
        #Recuperation des objets transmis par le CONTROLLEUR
        self.mf_balle = mf_balle
        self.mf_raquette = mf_raquette
        self.mf_briques = mf_briques
        self.score = score
        self.vies = vies

        #Creation de la fenetre tkinter
        self.mf_fenetre_racine = tk.Tk()
        self.mf_fenetre_racine.title(C.C_TITRE_FENETRE)
        self.mf_fenetre_racine.resizable(False,False)

        #Creation du conteneur de Frame
        self.mf_conteneur = ttk.Frame(self.mf_fenetre_racine)
        self.mf_conteneur.pack(fill="both", expand=True)

        #Creation d'un dico stockant les objets fenetres
        self.mf_dico_fenetre = {}

        #Creation des fenetres a l'initialisation
        for F in (Fenetre_demarage, Fenetre_option, Fenetre_jeu):
            frame = F(f_parent = self.mf_conteneur, f_manager = self)
            self.mf_dico_fenetre[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        #Affiche le premier ecran a l'initialisation
        self.afficher_fenetre("Fenetre_demarage")


    def mainloop(self):
        """
        Fonction : 
        Entree : 
        Sortie : 
        """
        self.mf_fenetre_racine.mainloop()

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
        if "Fenetre_jeu" in self.mf_conteneur:
            if self.mf_conteneur["Fenetre_jeu"].demande_jeu == True:
                self.mainloop()

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
class Fenetre(ttk.Frame):
    def __init__(self, f_parent:tk.Widget, f_manager:Manager_fenetre, f_nom_fenetre:str):
        super().__init__(f_parent, padding = 20)
        self.f_manager = f_manager #(?)

        #Nom de cette fenetre
        self.__nom_fenetre = f_nom_fenetre

        #Titre de la fenetre
        self.__titre_fenetre = ttk.Label(self, 
                                            text = f"{C.C_TITRE_FENETRE} - {self.__nom_fenetre}", 
                                            font = ("Arial", 24, "bold"))
        self.__titre_fenetre.pack(pady=20)

        #Barre des infos
        self.haut_barre = tk.Frame(self, height=40, bg="gray") 
        self.haut_barre.pack(side = 'top',fill = "x")

        #Barre de menus
        self.bas_barre = tk.Frame(self, height=60, bg = 'gray')
        self.bas_barre.pack(side = "bottom",fill = "x")

        #Bouton QUITTER
        self.btn_quitter = tk.Button(self.bas_barre,
                                     text = 'QUITTER',
                                     command = f_manager.mf_fenetre_racine.destroy)
        self.btn_quitter.pack(side = "left", padx = 5, pady = 5)

#Classe Fille Fenetre_demarage
class Fenetre_demarage(Fenetre):
    def __init__(self, f_parent, f_manager, f_nom_fenetre = "Fenetre_demarage"):
        super().__init__(f_parent, f_manager,f_nom_fenetre)
        
        #Bouton OPTION
        self.btn_option = tk.Button(self.bas_barre,
                                     text = 'OPTION',
                                     command = lambda: self.f_manager.afficher_fenetre("Fenetre_option"))
        self.btn_option.pack(side = "left", padx = 5, pady = 5)

        #Bouton JOUER
        self.btn_jouer = tk.Button(self.bas_barre,
                                     text = 'JOUER',
                                     command = lambda: self.f_manager.afficher_fenetre("Fenetre_jeu"))
        self.btn_jouer.pack(side = "left", padx = 5, pady = 5)

#Classe Fille Fenetre_option
class Fenetre_option(Fenetre):
    def __init__(self, f_parent, f_manager, f_nom_fenetre = "Fenetre_option"):
        super().__init__(f_parent, f_manager, f_nom_fenetre)
        #Bouton OPTION 1
        self.btn_option1 = tk.Button(self,
                                     text='OPTION 1')
        self.btn_option1.pack(pady = 10)

        #Bouton OPTION 2
        self.btn_option2 = tk.Button(self,
                                     text='OPTION 2')
        self.btn_option2.pack(pady = 10)

        #Bouton RETOUR
        self.btn_retour = tk.Button(self.bas_barre,
                                     text = 'RETOUR',
                                     command = lambda: f_manager.afficher_fenetre("Fenetre_demarage"))
        self.btn_retour.pack(side = "left", padx = 5, pady = 5)

#Classe fille Fenetre_jeu
class Fenetre_jeu(Fenetre):
    def __init__(self, f_parent, f_manager, f_nom_fenetre = "Fenetre_jeu"):
        super().__init__(f_parent, f_manager, f_nom_fenetre)
        #Demande de jeu
        self.demande_jeu = False

        #Score affichable
        self.fj_score = tk.StringVar(value=f"SCORE : {f_manager.score}")
        self.fj_score_affiche = ttk.Label(self.haut_barre,
                                          textvariable = self.fj_score,
                                          font = ("Arial", 12, "bold"),
                                          background = 'gray')
        self.fj_score_affiche.pack(side="left", padx=8)

        #Vies affichable
        self.fj_vies = tk.StringVar(value = f"VIES : {f_manager.vies}")
        self.fj_vies_affichees = ttk.Label(self.haut_barre,
                                          textvariable = self.fj_vies,
                                          font = ("Arial", 12, "bold"),
                                          background = 'gray')
        self.fj_vies_affichees.pack(side="right", padx=8)

        #Creation du Canvas
        self.fj_canvas = tk.Canvas(self, 
                                   width = C.C_LARGEUR_FENETRE, 
                                   height = C.C_HAUTEUR_FENETRE, 
                                   bg = "black")
        self.fj_canvas.pack(side = 'top',expand = True, fill = 'both', pady = 6)

        #Bouton LANCER
        self.btn_lancer = tk.Button(self.bas_barre,
                                     text = 'LANCER',
                                     command = lambda: self.activer_demande_jeu())
        self.btn_lancer.pack(side = "left", padx = 5, pady = 5)

        #Bouton RETOUR
        self.btn_retour = tk.Button(self.bas_barre,
                                     text = 'RETOUR',
                                     command = lambda: f_manager.afficher_fenetre("Fenetre_demarage"))
        self.btn_retour.pack(side = "left", padx = 5, pady = 5)

        #Creation graphique de la raquette
        self.fj_raquette = self.fj_canvas.create_rectangle(f_manager.mf_raquette.get_position_raquette()[0] - C.C_LARGEUR_RAQUETTE / 2,
                                                           f_manager.mf_raquette.get_position_raquette()[1] - C.C_HAUTEUR_RAQUETTE / 2,
                                                           f_manager.mf_raquette.get_position_raquette()[0] + C.C_LARGEUR_RAQUETTE / 2,
                                                           f_manager.mf_raquette.get_position_raquette()[1] + C.C_HAUTEUR_RAQUETTE / 2,
                                                           fill = 'blue')
        print(f_manager.mf_raquette.get_position_raquette())
        
        #Creation graphique de la balle
        self.fj_balle = self.fj_canvas.create_oval(f_manager.mf_balle.get_position_balle()[0] - C.C_RAYON_BALLE,
                                                   f_manager.mf_balle.get_position_balle()[1] - C.C_RAYON_BALLE,
                                                   f_manager.mf_balle.get_position_balle()[0] + C.C_RAYON_BALLE,
                                                   f_manager.mf_balle.get_position_balle()[1] + C.C_RAYON_BALLE,
                                                   fill = 'red')
        
        #Creation graphique des briques
        """a realiser sous forme de fonction afin dajouter des lignes de briques"""

    #Activer la demande de jeu
    def activer_demande_jeu(self):
        print("oui")
        self.demande_jeu = True




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

