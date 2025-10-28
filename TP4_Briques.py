# -*- coding: utf-8 -*-

#►►EN-TÊTE◄◄
"""
=========================================================================================
Date de creation : 7 octobre 2025
Auteurs: Marie Louise MILLIEN & Elouen WURMSER
Projet: TP4 - CasseBrique
Titre: Fichier de la gestion des briques
=========================================================================================
Description :
    Dans ce fichier on créer la classe de l'objet brique et un manager pour gerer les 
    differentes briques.
=========================================================================================
"""

#►►IMPORTATIONS◄◄
import TP4_Constantes as c

#►►CREATION OBJET BRIQUE◄◄
class Brique:
    """
    Fonction : Gere l'objet Brique
    Attributs : > self.canvas : recupere le canvas
                > self.vies : recupere le nombre de pv de la brique en constantes
                > self.type : recupere le type de la brique (exemple: normale) en 
                constantes
                > self.couleur : recupere la couleur de la brique en constantes
                > self.id : créer le rectangle representant la brique sur le canvas
    Methodes : > toucher() : gere la vie et la couleur de la brique
               > destroy() : supprime la brique graphique
               > coords() : renvoie les coordonnées graphique de la brique
    """
    def __init__(self, canvas, x1, y1, x2, y2, couleur=c.COULEUR, vies=c.VIES, types=c.TYPE):
        #Recuperation des attributs
        self.canvas = canvas

        #Recuperation des constantes
        self.vies = vies
        self.types = types
        self.couleur = couleur

        #Creation du rectangle
        self.id = canvas.create_rectangle(x1, y1, x2, y2, fill=couleur, outline="black")
        
    def toucher(self):
        """
        Fonction : Retire une vie a la brique si celle-ci n'est pas indestructible et la 
        detruit si elle n'a plus de vies ou alors change sa couleur
        Entree : None
        Sortie : Un booléen (TRUE ou FALSE)
        """
        #Verification du type
        if self.types == "indestructible":
            return False

        #Enleve une vie a la brique
        self.vies -= 1

        #Si elle n'a plus de vie on la detruit
        if self.vies <= 0:
            self.destroy()
            return True
        
        #Sinon on change la couleur de la brique
        else:
            self.canvas.itemconfig(self.id, fill = "orange")
            return False

    def destroy(self):
        """
        Fonction : Detruit la brique graphique
        Entree : None
        Sortie : None
        """
        try:
            self.canvas.delete(self.id)
        except Exception:
            pass

    def coords(self):
        """
        Fonction : Renvoie les coordonnées graphique de la brique
        Entree : None
        Sortie : Les coordonnées graphique de la brique (INT)"""
        return self.canvas.coords(self.id)

#►►CREATION GESTIONNAIRE BRIQUES◄◄
class BriqueManager:
    """
    Fonction : Gere la creation et la gestion des briques presentes dans le jeu
    Attributs : > self.canvas : recupere le canvas
                > self.lignes : recupere le nombre de lignes en constantes
                > self.colonnes : recupere le nombre de colonnes en constantes
                > self.largeur_brique : recupere la largeur d'une brique en constantes
                > self.hauteur_brique : recupere la hauteur d'une brique en constantes
                > self.top_offset : recupere le top offset en constantes
                > self.padding : recupere le padding en constantes
                > self.briques : liste contenant les objets Brique
    Methodes : > creation_niveau() : gere la creation de la grille de briques
               > clear_all() : supprime chaque brique graphique et reinitialise la liste
               de briques
               > reste() : renvoie la longueur de la liste de briques
               > collision(balle) : gere les colision entre les briques et une balle
    """
    def __init__(self, canvas, lignes = c.LIGNES, colonnes = c.COLONNES, 
                 largeur_brique = c.LARGEUR_BRIQUE, hauteur_brique = c.HAUTEUR_BRIQUE,
                 top_offset = c.TOP_OFFSET, padding = c.PADDING):
        #Recuperation des attributs
        self.canvas = canvas

        #Recuperation des constantes
        self.lignes = lignes
        self.colonnes = colonnes
        self.largeur_brique = largeur_brique
        self.hauteur_brique = hauteur_brique
        self.top_offset = top_offset
        self.padding = padding

        #Creation d'une liste contenant les briques
        self.briques = []       #◊LISTE◊ [?]

        #Creation d'une grille de brique dès l'initialisation
        self.creation_niveau()

    def creation_niveau(self):
        """
        Fonction : Créer une grille de briques centrée en tenant compte des constantes;
        Utilise les attributs de l'instance (self.lignes, self.colonnes, etc.) et 
        retombe sur les constantes c.* si un attribut venait à manquer; Si la largeur 
        totale dépasse celle du canvas, on adapte la largeur des briques pour que la 
        grille tienne horizontalement
        Entree : None
        Sortie : 
        """
        #Vide l'ancien niveau
        self.clear_all()

        #Récupérer paramètres (fallback vers constantes)
        lignes = getattr(self, "lignes", c.LIGNES)
        colonnes = getattr(self, "colonnes", c.COLONNES)
        largeur_brique = getattr(self, "largeur_brique", c.LARGEUR_BRIQUE)
        hauteur_brique = getattr(self, "hauteur_brique", c.HAUTEUR_BRIQUE)
        top_offset = getattr(self, "top_offset", c.TOP_OFFSET)
        padding = getattr(self, "padding", c.PADDING)

        #Calcul de la largeur totale nécessaire
        total_width = colonnes * largeur_brique + (colonnes - 1) * padding
        canvas_w = int(self.canvas['width'])

        #Si ça déborde, on réduit la largeur des briques pour rentrer dans le canvas
        margin = 20  # marge minimale gauche/droite
        max_allowed = max(canvas_w - margin, 10)
        if total_width > max_allowed and colonnes > 0:
            #Garder le padding fixe, ajuster largeur_brique
            largeur_brique = int((max_allowed - (colonnes - 1) * padding) / colonnes)
            if largeur_brique < 4:
                largeur_brique = 4  #safeguard minimal
            total_width = colonnes * largeur_brique + (colonnes - 1) * padding

        #Calculer le point de départ pour centrer la grille
        start_x = max(int((canvas_w - total_width) / 2), 10)
        y = top_offset

        #Palette de couleurs (tu peux la modifier)
        colors = ["#5e3ce7"]

        #Création de la grille
        for row in range(lignes):
            x = start_x
            for col in range(colonnes):
                x1 = x
                y1 = y
                x2 = x + largeur_brique
                y2 = y + hauteur_brique
                couleur = colors[row % len(colors)]
                b = Brique(self.canvas, x1, y1, x2, y2, couleur=couleur, vies= c.VIES)
                self.briques.append(b)
                x += largeur_brique + padding
            y += hauteur_brique + padding

    def clear_all(self):
        """
        Fonction : Supprime chaque brique graphique de la liste de brique puis 
        réinitialise cette liste comme une liste vide
        Entree : None
        Sortie : None
        """
        for brique in self.briques:
            brique.destroy()
        self.briques = []

    def reste(self):
        """
        Fonction : Retourne la longeur de la liste de briques
        Entree : None
        Sortie : La longeur de la liste de briques (INT)"""
        return len(self.briques)

    def collision(self, balle:object):
        """
        Fonction : Gérer les collisions des briques de la grille avec une balle en parametre
        Entree : La balle (OBJ)
        Sortie : La variable hit_brick 
        """
        #Récupération des coordonnees graphique de la balle
        bx1, by1, bx2, by2 = balle.coords()

        #Initialisation de la variable
        hit_brick = None

        #On itére sur une copie car on peut supprimer
        """Pour chaque brique on recupere ses coordonnees graphiques"""
        for brique in list(self.briques):
            coords = brique.coords()
            if len(coords) != 4:
                continue

            #Separation des coordonnees en 4 variables pour faire les verifications
            x1, y1, x2, y2 = coords

            #On verifie la correspondance des coordonnees
            if not (bx2 < x1 or bx1 > x2 or by2 < y1 or by1 > y2):
                destroyed = brique.toucher()
                if destroyed:
                    try:
                        self.briques.remove(brique)
                    except ValueError:
                        pass
                hit_brick = brique
                #ne casse pas la boucle : gérer potentiellement plusieurs collisions (mais une suffit)
                break
        return hit_brick
