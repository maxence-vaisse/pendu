import random
import pygame
from pygame.locals import *

def afficher_menu():
    screen.fill((255, 165, 0))  # Fond orange

    menu_font = pygame.font.Font(None, 48)
    menu_texte1 = menu_font.render("1. Jouer avec les mots existants", True, (255, 255, 255))
    menu_texte2 = menu_font.render("2. Ajouter un mot", True, (255, 255, 255))

    menu_position1 = (screen.get_width() // 2 - menu_texte1.get_width() // 2, 200)
    menu_position2 = (screen.get_width() // 2 - menu_texte2.get_width() // 2, 300)

    screen.blit(menu_texte1, menu_position1)
    screen.blit(menu_texte2, menu_position2)
    pygame.display.flip()

def jouer_une_partie():
    with open("mots.txt") as fichier_de_lecture:
        listes_mots = [lettre.rstrip("\n") for lettre in fichier_de_lecture]

    mot_a_trouver = random.choice(listes_mots)

    lettres_trouves = []
    lettres_fausses = []
    faux = 0

    font = pygame.font.Font(None, 36)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                lettre_a_entrer = pygame.key.name(event.key).lower()

                if len(lettre_a_entrer) == 1 and lettre_a_entrer.isalpha():
                    if lettre_a_entrer not in lettres_trouves and lettre_a_entrer not in lettres_fausses:
                        if lettre_a_entrer not in mot_a_trouver:
                            lettres_fausses.append(lettre_a_entrer)
                            faux += 1
                        else:
                            lettres_trouves.append(lettre_a_entrer)

        screen.fill((255, 165, 0))

        if faux >= 1:
            pygame.draw.rect(screen, (255, 255, 255), (100, 350, 300, 2))  # sol
        if faux >= 2:
            pygame.draw.rect(screen, (255, 255, 255), (175, 50, 2, 300))  # verticale
        if faux >= 3:
            pygame.draw.rect(screen, (255, 255, 255), (175, 50, 200, 2))  # horizontale
        if faux >= 4:
            pygame.draw.line(screen, (255, 255, 255), (175, 100), (200, 50), 2)  # diagonale
        if faux >= 5:
            pygame.draw.rect(screen, (0, 0, 255), (375, 50, 2, 50))  # corde
        if faux >= 6:
            pygame.draw.ellipse(screen, (0, 0, 255), (350, 100, 50, 50), 1)  # tête
        if faux >= 7:
            pygame.draw.rect(screen, (0, 0, 255), (375, 150, 1, 100))  # corps
        if faux >= 8:
            pygame.draw.line(screen, (0, 0, 255), (375, 175), (360, 175), 1)  # avant-bras gauche
            pygame.draw.line(screen, (0, 0, 255), (375, 175), (390, 175), 1)  # avant-bras droit
        if faux >= 9:
            pygame.draw.line(screen, (0, 0, 255), (375, 250), (340, 275), 1)  # jambe gauche
            pygame.draw.line(screen, (0, 0, 255), (375, 250), (410, 275), 1)  # jambe droite

        texte_mot = font.render("Mot à trouver: {}".format(" ".join("_" if lettre not in lettres_trouves else lettre for lettre in mot_a_trouver)), True, (0, 0, 0))
        screen.blit(texte_mot, (400, 520))

        texte_fausses = font.render("Lettres fausses: {}".format(" | ".join(lettres_fausses)), True, (0, 0, 0))
        screen.blit(texte_fausses, (400, 560))

        if faux > 8 or all(lettre in lettres_trouves for lettre in mot_a_trouver):
            texte_resultat = font.render("Dommage tu as perdu !" if faux > 8 else "Bravo tu as gagné !", True, (255, 255, 255))
            screen.blit(texte_resultat, (400, 600))
            texte_mot_trouve = font.render("Le mot était: {}".format(mot_a_trouver), True, (0, 0, 0))
            screen.blit(texte_mot_trouve, (400, 640))

            texte_rejouer = font.render("Appuyez sur Entrée pour rejouer ou appuyez sur la croix pour quitter !", True, (0, 0, 0))
            screen.blit(texte_rejouer, (400, 680))
            pygame.display.flip()

            attente = True
            while attente:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        attente = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            attente = False
                            lettres_trouves = []
                            lettres_fausses = []
                            faux = 0
                            mot_a_trouver = random.choice(listes_mots)

                            screen.fill((255, 165, 0))
                            pygame.display.flip()

        pygame.display.flip()

def ajouter_mot():
    screen.fill((255, 165, 0))
    texte_instruction = font.render("Ajoutez un nouveau mot puis appuyez sur Entrée :", True, (255, 255, 255))
    screen.blit(texte_instruction, (200, 200))
    pygame.display.flip()

    nouveau_mot = ""
    ajout_en_cours = True
    while ajout_en_cours:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    ajout_en_cours = False
                elif event.key == pygame.K_BACKSPACE:
                    nouveau_mot = nouveau_mot[:-1]
                elif event.key in range(97, 123):  # ASCII codes for a to z
                    nouveau_mot += chr(event.key)

        screen.fill((255, 165, 0))
        texte_instruction = font.render("Ajoutez un nouveau mot puis appuyez sur Entrée :", True, (255, 255, 255))
        screen.blit(texte_instruction, (200, 200))
        texte_nouveau_mot = font.render(nouveau_mot, True, (255, 255, 255))
        screen.blit(texte_nouveau_mot, (500, 300))
        pygame.display.flip()

    with open("mots.txt", "a") as fichier_d_ecriture:
        fichier_d_ecriture.write("\n" + nouveau_mot)

# Initialisation de pygame
pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Jeu du pendu")

# Variables de couleurs
BLACK = (0, 0, 0)
GREY = (127, 127, 127)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Police pour le texte
font = pygame.font.Font(None, 36)

# Boucle principale
running = True
while running:
    afficher_menu()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                jouer_une_partie()
            elif event.key == pygame.K_2:
                ajouter_mot()

    pygame.display.flip()

pygame.quit()