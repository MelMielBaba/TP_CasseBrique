"""
Date de creation : 7 octobre 2025
Auteurs: Marie Louise MILLIEN & Elouen WURMSER
Projet: TP4 - CasseBrique
Titre: Fichier de gestion des briques
"""

import TP4_Constantes as c

class Brique:
    """
    On initialise la Brique de longeur x2--x1 et de hauteur y2--y1
    avec un couleur non modifiable, un nombre de vie modifiable des les paramètres
    et le type de briques
    """
    def __init__(self, canvas, x1, y1, x2, y2, couleur=c.COULEUR, vies=c.VIES, types=c.TYPE):
        self.canvas = canvas
        # Creation de la brique
        self.id = canvas.create_rectangle(x1, y1, x2, y2, fill=couleur, outline="black")
        self.vies = vies
        self.types = types
        self.couleur = couleur
    """
    La fonction toucher est activé lorsque la balle touche une brique,
    si la brique est de type indéstructible alors elle ne perd aucun point de vie
    sinon elle perd un point de vie
    """
    def toucher(self):
        # Gère le type de brique
        if self.types == "indestructible":
            return False
        # Soustrait une vie
        self.vies -= 1
        # Si la vie atteint une valeur nulle alors elle est détruite
        if self.vies <= 0:
            self.destroy()
            return True
        # Sinon on change la couleur de la brique pour signaler qu'elle a été touchée
        else:
            self.canvas.itemconfig(self.id, fill="orange")
            return False
    """
    La fonction destroy permet de détruire la brique
    """
    def destroy(self):
        self.canvas.delete(self.id)

    """
    La fonction coords  permet de récupérer les coords de la brique
    """
    def coords(self):
        return self.canvas.coords(self.id)


class BriqueManager:
    """
    Gestionnaire du niveau, cette classe gère l'assemblement des briques entre-elles,
    elle prends en compte le nombre de lignes et de colonnes de briques que l'on veut,
    modifiable dans les paramètres, les largeurs et hauteurs des briques.
    le top offset correspond à l'espacement entre la 1er ligne du haut et la fin du canva
    le padding correspond à l'espacement entre chaque brique
    """
    def __init__(self, canvas,
                 lignes=c.LIGNES, colonnes=c.COLONNES,
                 largeur_brique=c.LARGEUR_BRIQUE, hauteur_brique=c.HAUTEUR_BRIQUE,
                 top_offset=c.TOP_OFFSET, padding=c.PADDING):
        self.canvas = canvas
        self.lignes = lignes
        self.colonnes = colonnes
        self.largeur_brique = largeur_brique
        self.hauteur_brique = hauteur_brique
        self.top_offset = top_offset
        self.padding = padding
        self.briques = []
        self.creation_niveau()

    def creation_niveau(self):
        """
        Creation d'une grille de briques centrée en tenant compte des constantes.
        Pour aller plus loin, on peut créer plusieurs creation de niveau.
        """
    # vide l'ancien niveau
        self.clear_all()

    # récupérer paramètres définies dans __init__ getattr(objet,attribut)
        lignes = getattr(self, "lignes")
        colonnes = getattr(self, "colonnes")
        largeur_brique = getattr(self, "largeur_brique")
        hauteur_brique = getattr(self, "hauteur_brique")
        top_offset = getattr(self, "top_offset")
        padding = getattr(self, "padding")

    # calcul de la largeur totale nécessaire
        total_width = colonnes * largeur_brique + (colonnes - 1) * padding
        canvas_w = int(self.canvas['width'])

    # si ça déborde, on réduit la largeur des briques pour rentrer dans le canvas
        margin = 20  # marge minimale gauche/droite
        max_allowed = max(canvas_w - margin, 10)
        if total_width > max_allowed and colonnes > 0:
        # garder le padding fixe, ajuster largeur_brique
            largeur_brique = int((max_allowed - (colonnes - 1) * padding) / colonnes)
            if largeur_brique < 4:
                largeur_brique = 4  # safeguard minimal
            total_width = colonnes * largeur_brique + (colonnes - 1) * padding

    # calculer le point de départ pour centrer la grille
        start_x = max(int((canvas_w - total_width) / 2), 10)
        y = top_offset

    # palette de couleurs
        colors = ["#5e3ce7"]

    # création de la grille
        for ligne in range(lignes):
            x = start_x
            for colonne in range(colonnes):
                # Emplacement de la brique
                x1 = x
                y1 = y
                x2 = x + largeur_brique
                y2 = y + hauteur_brique
                # Couleur de celle ci
                couleur = colors[ligne % len(colors)]
                # Création de la brique
                b = Brique(self.canvas, x1, y1, x2, y2, couleur=couleur, vies= c.VIES)
                # Ajoute a la file
                self.briques.append(b)
                x += largeur_brique + padding
            y += hauteur_brique + padding

    """
    la fonction clear_qll vide la file
    """
    def clear_all(self):
        for brique in self.briques:
            brique.destroy()
    """
    La fonction reste permet de savoir on a gagner, utile dans le fichier fenetre
    """
    def reste(self):
        return len(self.briques)

    """
    La fonction collision permet de détecter une collision entre une brique et la balle
    """
    def collision(self, balle):
        # On récupère les dimensions de la balle
        bx1, by1, bx2, by2 = balle.coords()
        hit_brick = None
        # Pour chaque brique dans la grille
        for brique in list(self.briques):
            # On récupère les coordonnées d'une vrique
            x1, y1, x2, y2 = brique.coords()
            # Si les coordonnées de la balle et de la brique se superpose
            if not (bx2 < x1 or bx1 > x2 or by2 < y1 or by1 > y2):
                destroyed = brique.toucher()
                if destroyed:
                    self.briques.remove(brique)
                hit_brick = brique
        return hit_brick
