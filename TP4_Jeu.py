# -*- coding: utf-8 -*-
"""
Date de creation : 7 octobre 2025
Auteurs: Marie Louise MILLIEN & Elouen WURMSER
Projet: TP4 - CasseBrique
Titre: Fichier principal du jeu
"""

# Jeu.py
import tkinter as tk
from TP4_Constantes import C_LARGEUR_CANVAS, C_HAUTEUR_CANVAS, C_FPS
from TP4_Balle import Balle
from TP4_Briques import BrickManager
from TP4_Raquette import Raquette

class Jeu:
    def __init__(self, root):
        self.root = root
        self.width = C_LARGEUR_CANVAS
        self.height = C_HAUTEUR_CANVAS
        self.running = False
        self.lives = 3
        self.score = 0

        # UI
        self.setup_ui()

        # game objects
        self.raquette = Raquette(canvas_width=self.width, canvas_height=self.height)
        # create ball above paddle
        self.ball = Balle(self.canvas, x=self.width/2, y=self.height - 120)
        self.brick_manager = BrickManager(self.canvas, rows=5, cols=9, brick_w=80, brick_h=20, top_offset=30, padding=6)

        # draw paddle as a rectangle (for easier collision)
        half = self.raquette.width / 2
        y = self.raquette.y
        self.paddle_id = self.canvas.create_rectangle(self.raquette.x_center - half, y - 8,
                                                      self.raquette.x_center + half, y + 8,
                                                      fill="red")

        # key binding
        self.root.bind("<Left>", lambda e: self.key_move(-1))
        self.root.bind("<Right>", lambda e: self.key_move(1))
        self.root.bind("<space>", lambda e: self.toggle_running())

        # loop
        self.update_ui()
        self.redraw_paddle()
        self.fps_delay = C_FPS
        self.root.after(self.fps_delay, self.game_loop)

    def setup_ui(self):
        top_frame = tk.Frame(self.root)
        top_frame.pack(side=tk.TOP, fill=tk.X)
        self.score_var = tk.StringVar(value=f"Score: {self.score}")
        self.lives_var = tk.StringVar(value=f"Vies: {self.lives}")
        tk.Label(top_frame, textvariable=self.score_var).pack(side=tk.LEFT, padx=8)
        tk.Label(top_frame, textvariable=self.lives_var).pack(side=tk.LEFT, padx=8)

        btn_frame = tk.Frame(top_frame)
        btn_frame.pack(side=tk.RIGHT)
        tk.Button(btn_frame, text="Démarrer", command=self.start).pack(side=tk.LEFT, padx=4)
        tk.Button(btn_frame, text="Quitter", command=self.root.quit).pack(side=tk.LEFT, padx=4)

        # canvas
        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height, bg="black")
        self.canvas.pack()

    def start(self):
        if not self.running:
            self.running = True

    def toggle_running(self):
        self.running = not self.running

    def key_move(self, direction):
        # direction -1 left, +1 right -> move paddle by vitesse
        dx = direction * self.raquette.vitesse
        self.raquette.move_by(dx)
        self.redraw_paddle()

    def redraw_paddle(self):
        half = self.raquette.width / 2
        y = self.raquette.y
        self.canvas.coords(self.paddle_id,
                           self.raquette.x_center - half, y - 8,
                           self.raquette.x_center + half, y + 8)

    def update_ui(self):
        self.score_var.set(f"Score: {self.score}")
        self.lives_var.set(f"Vies: {self.lives}")

    def handle_collisions(self):
        # walls
        bx1, by1, bx2, by2 = self.ball.coords()
        # left/right
        if bx1 <= 0:
            self.ball.reflect_x()
            self.ball.set_position(self.ball.rayon, (by1+by2)/2)
        elif bx2 >= self.width:
            self.ball.reflect_x()
            self.ball.set_position(self.width - self.ball.rayon, (by1+by2)/2)
        # top
        if by1 <= 0:
            self.ball.reflect_y()
            self.ball.set_position((bx1+bx2)/2, self.ball.rayon)

        # bottom -> life lost
        if by2 >= self.height:
            self.lives -= 1
            self.update_ui()
            self.running = False
            if self.lives <= 0:
                print("Game Over")
            else:
                # reset ball above paddle
                self.ball.reset(x=self.raquette.x_center, y=self.raquette.y - 30)
            return

        # paddle collision (AABB)
        px1, py1, px2, py2 = self.canvas.coords(self.paddle_id)
        if not (bx2 < px1 or bx1 > px2 or by2 < py1 or by1 > py2):
            # compute relative hit [-1..1]
            paddle_center = (px1 + px2) / 2
            ball_center_x = (bx1 + bx2) / 2
            rel = (ball_center_x - paddle_center) / ( (px2 - px1) / 2 )
            rel = max(-1, min(1, rel))
            max_vx = 6
            self.ball.vx = rel * max_vx
            self.ball.vy = -abs(self.ball.vy)
            # nudge ball above paddle
            self.ball.set_position(ball_center_x, py1 - self.ball.rayon - 1)

        # brick collision
        hit = self.brick_manager.check_collision(self.ball)
        if hit:
            # reflect y and add score
            self.ball.reflect_y()
            self.score += 50
            self.update_ui()
            if self.brick_manager.remaining() == 0:
                self.running = False
                print("Victory!")

    def game_loop(self):
        if self.running:
            self.ball.move()
            self.handle_collisions()
        # redraw paddle position in any case (raquette peut avoir bougé)
        self.redraw_paddle()
        # schedule next frame
        self.root.after(self.fps_delay, self.game_loop)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Casse-brique - TP (module Jeu.py)")
    jeu = Jeu(root)
    root.mainloop()
