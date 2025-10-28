=========================================================================================
►►EN-TÊTE◄◄
Date de creation : 7 octobre 2025
Auteurs: Marie Louise MILLIEN & Elouen WURMSER
Projet: TP4 - CasseBrique
Titre: Fichier README
=========================================================================================
►►DESCRIPTION◄◄
    -> Indication des règles du jeu
    -> Indication des spécificités de l'implémentation du projet
        *Fonctionnement general
        *Structure
    -> Indication de l’adresse du répertoire GIT
    -> Indication d'où se trouvent les implémentations des structures de 
    données demandées (la liste, la file et la pile)
    -> Rappel des contraintes
=========================================================================================
►REGLES DU JEU◄
    -> Lancer le jeu
    -> Soit vous pouvez lancer le jeu avec les parametre par defaut en 
    cliquant sur JOUER
    -> Soit vous pouvez d'abord modifier les parametre en cliquant sur 
    OPTION
    -> Une fois le jeu lancé le but est de detruire toutes les briques 
    sans perdre la balle
    -> Le jeu est perdu si on perd totes ses vies, c'est a dire qu'on a perdu 
    la balle 3 fois; Le jeu est gagné lorsque toutes les briques sont detruites
    -> Une fois la partie finie, victoire ou defaite, une messagebox affiche le 
    score final
=========================================================================================
►FONCTIONNENEMENT DU JEU◄
    >> Lancer le jeu : Ouvrir le fichier TP4_Jeu.py et l'exécuter
    >> Fonctionnement general :
        * TP4_Jeu appelle TP4_Fenetre en creant une App et en la lancant
        * Cette App creer les differente fenetre comme etant des frames dans un conteneur
        * La classe FenetreJeu cree et gere le jeu ainsi que son affichage
        * Les objets balle, raquette et briques sont créés respectivement dans les fichiers 
        TP4_Balle, TP4_Raquette et TP4_Briques
=========================================================================================
►STRUCTURE DU PROJET◄
    >> Fichier de lancement du jeu : TP4_Jeu.py
    >> Fichier des constantes : TP4_Constantes.py
    >> Fichier de la gestion graphique tkinter : TP4_Fenetre.py
    >> Fichier de la classe de la balle : TP4_Balle.py
    >> Fichier de la classe de la barre : TP4_Raquette.py
    >> Fichier de la classe des briques : TP4_Briques.py
    >> Fichier ReadMe du projet : TP4_ReadMe.txt
=========================================================================================
►URL DU REPERTOIRE GIT◄
    URL du git : https://github.com/MelMielBaba/TP_CasseBrique
    /!\ Le depot est paramétré comme privé et est censé être passé en public pour /!\
        évaluation 
    /!\ Important l'archive du rendu correspond a la branche MelBr9 /!\
=========================================================================================
►EMPLACEMENT DE LA LISTE,DE LA FILE ET DE LA PILE◄
    >> Liste : Dans ◊TP4_Briques◊ ligne n° ◊121◊
    >> File : Dans ◊TP4_Fenetre◊ ligne n° ◊376◊
    >> Pile : Dans ◊TP4_Fenetre◊ ligne n° ◊377◊
=========================================================================================
►CONTRAINTES DU PROJET◄
    -> Le jeu est codé en POO
    -> Le jeu doit présenter une implémentation d'une liste, d'une de file et d'une de 
    pile
    -> Le rendu se fera sous la forme d’une archive contenant l’ensemble des fichiers.
    -> Dans l'archive du rendu doit se trouver ce fichier ReadMe.txt 
    -> La notation prendra autant en compte le respect des consignes que le résultat 
    final
=========================================================================================
