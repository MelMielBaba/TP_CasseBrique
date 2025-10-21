import TP4_Constantes as c

class Brique:
    def __init__(self, canvas, x1, y1, x2, y2, couleur=c.COULEUR, vies=c.VIES, types=c.TYPE):
        self.canvas = canvas
        self.id = canvas.create_rectangle(x1, y1, x2, y2, fill=couleur, outline="black")
        self.vies = vies
        self.types = types
        self.couleur = couleur

    def toucher(self):
        if self.types == "indestructible":
            return False

        self.vies -= 1

        if self.vies <= 0:
            self.destroy()
            return True
        else:
            self.canvas.itemconfig(self.id, fill="orange")
            return False

    def destroy(self):
        try:
            self.canvas.delete(self.id)
        except Exception:
            pass

    def coords(self):
        return self.canvas.coords(self.id)


class BriqueManager:
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
        """Creation d'une grille de briques centrée en tenant compte des constantes.

    Utilise les attributs de l'instance (self.lignes, self.colonnes, etc.)
    et retombe sur les constantes c.* si un attribut venait à manquer.
    Si la largeur totale dépasse celle du canvas, on adapte la largeur des briques
    pour que la grille tienne horizontalement.
        """
    # vide l'ancien niveau
        self.clear_all()

    # récupérer paramètres (fallback vers constantes)
        lignes = getattr(self, "lignes", c.LIGNES)
        colonnes = getattr(self, "colonnes", c.COLONNES)
        largeur_brique = getattr(self, "largeur_brique", c.LARGEUR_BRIQUE)
        hauteur_brique = getattr(self, "hauteur_brique", c.HAUTEUR_BRIQUE)
        top_offset = getattr(self, "top_offset", c.TOP_OFFSET)
        padding = getattr(self, "padding", c.PADDING)

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

    # palette de couleurs (tu peux la modifier)
        colors = ["#5e3ce7"]

    # création de la grille
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
        for brique in self.briques:
            brique.destroy()
        self.briques = []

    def reste(self):
        return len(self.briques)

    def collision(self, balle):
        bx1, by1, bx2, by2 = balle.coords()
        hit_brick = None
        # itérer sur copie car on peut supprimer
        for brique in list(self.briques):
            coords = brique.coords()
            if len(coords) != 4:
                continue
            x1, y1, x2, y2 = coords
            # test AABB overlap
            if not (bx2 < x1 or bx1 > x2 or by2 < y1 or by1 > y2):
                destroyed = brique.toucher()
                if destroyed:
                    try:
                        self.briques.remove(brique)
                    except ValueError:
                        pass
                hit_brick = brique
                # ne casse pas la boucle : gérer potentiellement plusieurs collisions (mais une suffit)
                break
        return hit_brick
