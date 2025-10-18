"""
Date de creation : 7 octobre 2025
Auteurs: Marie Louise MILLIEN & Elouen WURMSER
Projet: TP4 - CasseBrique
Titre: Fichier READ ME
"""

Description du fichier:
    -> Indication des règles du jeu
    -> Indication des spécificités de l'implémentation du projet
    -> Indication de l’adresse du répertoire GIT
    -> Indication d'où se trouvent les implémentations des structures de données demandées (la liste, la file et la pile)


►FONCTIONNENEMENT DU JEU◄
    >> Lancer le jeu : Ouvrir le fichier TP4_CasseBrique.py et l'exécuter
    >> Description de l'exécution générale:
        +-------------+  lance   +-----------------+
        |   Joueur    | -------> | TP4_CasseBrique |
        +-------------+          +-----------------+
                                          | appel
                                          ▼
                                     +---------+
        +----> +-------------------> | TP4_Jeu | -------------------+
        |      |                     +---------+                    |
        |      |                         | modifie les parametres   |  
        |      |                         ▼                          |
        |      | envoie ses infos   +---------+                     |
        |      +--------------------| MODELES |                     | envoie des 
        |                           +---------+                     |   instructions
        |                                                           |
        |                                                           |
        |                                                           ▼
        |            envoie le nouveau dessin           +----------------------+
        +-----------------------------------------------| TP4_GestionGraphique |
                                                        +----------------------+


►STRUCTURE DU PROJET◄
Fichier de lancement du jeu : TP4_CasseBrique.py
Fichier CONTROLEUR du jeu : TP4_Jeu.py
Fichier des constantes : TP4_Constantes.py
Fichier de la gestion graphique tkinter (VUE) : TP4_Fenetre.py/TP4_GestionGraphique.py
Fichier de la classe de la balle (MODELE) : TP4_Balle.py
Fichier de la classe de la barre (MODELE) : TP4_Raquette.py
Fichier de la classe des briques (MODELE) : TP4_Briques.py
Fichier ReadMe du projet : TP4_ReadMe.txt

►URL DU REPERTOIRE GIT◄
URL du git : https://github.com/MelMielBaba/TP_CasseBrique
/!\ Le depot est paramétré comme privé /!\


►CONTRAINTES DU PROJET◄
-> Le jeu est codé en POO
-> Le jeu doit présenter une implémentation d'une liste, d'une de file et d'une de pile
-> Le rendu se fera sous la forme d’une archive contenant l’ensemble des fichiers.
-> Dans l'archive du rendu doit se trouver ce fichier ReadMe.txt 
-> La notation prendra autant en compte le respect des consignes que le résultat final