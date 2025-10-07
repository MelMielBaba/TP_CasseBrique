# -*- coding: utf-8 -*-
"""
Date de creation : 7 octobre 2025
Auteur: Marie Louise MILLIEN & Elouen WURMSER
Projet: TP4 - Casse-Brique
Titre: Fichier de la Fenetre
"""

#Importation des modules
import tkinter as tk

#Creation de la classe Fenetre
class Fenetre:
    """
    La classe fenetre est parente de toutes les fenetres du jeu. 
    Elle a donc en attribut une fenetre et un bouton quitter
    """
    def __init__(self):
        pass

#Creation de la classe de la fenetre principale
class Fenetre_principale(Fenetre):
    """
    Cette classe 'creer' la fenetre qui se lance au debut du jeu.
    Elle possede comme toute fenetre un bouton quitter (heriter de Fenetre()),
    un bouton option et un bouton jouer
    """
    def __init__(self):
        pass

#Creation de la classe de la fenetre de jeu
class Fenetre_jeu(Fenetre):
    """
    Cette classe 'creer' la fenetre sur laquelle se deroule le jeu.
    Elle possede comme toute fenetre un bouton quitter (heriter de Fenetre()),
    un bouton menu un caneva
    """
    def __init__(self):
        pass

#Creation de la classe de la fenetre de jeu
class Fenetre_Option(Fenetre):
    """
    Cette classe 'creer' la fenetre du menu des options.
    Elle possede comme toute fenetre un bouton quitter (heriter de Fenetre()),
    un bouton retour
    """
    def __init__(self):
        pass

 
class App:
    def __init__(self, root):
        self.root = root
        self.root.geometry("800x800")
        self.creation_fenetre_demarrage()
 
    def creation_fenetre_demarrage(self):
        self.start_frame = FenetreDemarrage(self.root, self)
        self.start_frame.btn_option.bind('<Button-1>', self.creation_fenetre_option)
        self.start_frame.pack()
 
    def creation_fenetre_option(self, event=None):
        self.start_frame.destroy()
        self.second_menu_frame = FenetreOption(self.root, self)
        self.second_menu_frame.pack()
    
    def retour_demarrage(self):
        self.second_menu_frame.destroy()
        self.creation_fenetre_demarrage()
 
 
class FenetreDemarrage(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        
        tk.Label(self, text='Casse Brique', font=("Arial", 20, "bold")).pack(pady=20)

        self.btn_jouer = tk.Button(self, text="Jouer")
        self.btn_jouer.pack(pady=10)

        self.btn_option = tk.Button(self, text="Option")
        self.btn_option.pack(pady=10)

        self.btn_quitter = tk.Button(self, text="Quitter", command=self.app.root.destroy)
        self.btn_quitter.pack(pady=10)
 
 
class FenetreOption(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        
        tk.Label(self, text='Options', font=("Arial", 20, "bold")).pack(pady=20)
        
        self.btn_option1 = tk.Button(self, text="WIP")
        self.btn_option1.pack(pady=10)

        self.btn_retour = tk.Button(self, text="Retour", command=self.app.retour_demarrage)
        self.btn_retour.pack(pady=10)
 
 
if __name__ == "__main__":
    root = tk.Tk()
    main = App(root)
    root.mainloop()

