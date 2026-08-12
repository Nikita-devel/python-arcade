# Import the libraries
import pygame
import sys
import time
import random
import os
import math

# Import the pygame mixer
import pygame.mixer

# Start up pygame
pygame.init()
pygame.mixer.init()

# Get the folder this script lives in
base_path = os.path.dirname(os.path.abspath(__file__))

# Load the sounds
die_sound = pygame.mixer.Sound(os.path.join(base_path, 'audio', 'die.wav'))
hit_sound = pygame.mixer.Sound(os.path.join(base_path, 'audio', 'hit.wav'))
point_sound = pygame.mixer.Sound(os.path.join(base_path, 'audio', 'point.wav'))
swoosh_sound = pygame.mixer.Sound(os.path.join(base_path, 'audio', 'swoosh.wav'))
wing_sound = pygame.mixer.Sound(os.path.join(base_path, 'audio', 'wing.wav'))

# Load the background music
pygame.mixer.music.load(os.path.join(base_path, 'audio', 'flappybg.mp3'))

# Game window
largeur, hauteur = 350, 622
horloge = pygame.time.Clock()
ecran = pygame.display.set_mode((largeur, hauteur))
pygame.display.set_caption("Flappy Bird")

# Set up the background and ground images
img_fond = pygame.image.load(os.path.join(base_path, 'assets', 'img_46.png'))
img_base = pygame.image.load(os.path.join(base_path, 'assets', 'img_50.png'))
x_base = 0

# The bird's animation frames
oiseau_haut = pygame.image.load(os.path.join(base_path, 'assets', 'img_47.png'))
oiseau_bas = pygame.image.load(os.path.join(base_path, 'assets', 'img_48.png'))
oiseau_milieu = pygame.image.load(os.path.join(base_path, 'assets', 'img_49.png'))
oiseaux = [oiseau_haut, oiseau_milieu, oiseau_bas]
index_oiseau = 0
evenement_battement = pygame.USEREVENT
pygame.time.set_timer(evenement_battement, 200)
img_oiseau = oiseaux[index_oiseau]
rect_oiseau = img_oiseau.get_rect(center=(67, 622 // 2))
mouvement_oiseau = 0
gravite = 0.17

# Load the pipe image
img_tuyau = pygame.image.load(os.path.join(base_path, 'assets', 'greenpipe.png'))
hauteur_tuyau = [400, 350, 533, 490]

# So the pipes appear
tuyaux = []
creer_tuyau = pygame.USEREVENT + 1
pygame.time.set_timer(creer_tuyau, 1200)

# Game-over image
game_over = False
# 'jeu_demarre' stays False until the player presses SPACE
# for the first time. While it's False, gravity is off and
# the bird floats in the center: no more instant fall at startup.
jeu_demarre = False
img_game_over = pygame.image.load(os.path.join(base_path, 'assets', 'img_45.png')).convert_alpha()
rect_game_over = img_game_over.get_rect(center=(largeur // 2, hauteur // 2))

# Set up the score variables and font
score = 0
chemin_fichier_score = os.path.join(base_path, 'highest_score.txt')
meilleur_score = 0

temps_score = True
police_score = pygame.font.Font(os.path.join(base_path, 'assets', 'font.ttf'), 20)

# Set up the exit button
rect_bouton_sortie = pygame.Rect(250, 10, 80, 40)  # Ajustez la position et la taille au besoin

# Start playing the background music
pygame.mixer.music.play(-1)


# Function that draws the ground
def dessiner_sol():
    ecran.blit(img_base, (x_base, 520))
    ecran.blit(img_base, (x_base + 448, 520))

# Function that creates pipes
def creer_tuyaux():
    y_tuyau = random.choice(hauteur_tuyau)
    tuyau_haut = img_tuyau.get_rect(midbottom=(467, y_tuyau - 200))
    tuyau_bas = img_tuyau.get_rect(midtop=(467, y_tuyau))
    return tuyau_haut, tuyau_bas

# Function that animates the pipes
def animation_tuyaux():
    global game_over, temps_score
    for tuyau in tuyaux:
        if tuyau.top < 0:
            tuyau_inverse = pygame.transform.flip(img_tuyau, False, True)
            ecran.blit(tuyau_inverse, tuyau)
        else:
            ecran.blit(img_tuyau, tuyau)

        tuyau.centerx -= 3
        if tuyau.right < 0:
            tuyaux.remove(tuyau)

        if rect_oiseau.colliderect(tuyau):
            hit_sound.play()  # Jouer le son de collision
            game_over = True

# Function that draws the score
def dessiner_score(etat_jeu):
    if etat_jeu == "game_on":
        texte_score = police_score.render(str(score), True, (255, 255, 255))
        rect_score = texte_score.get_rect(center=(largeur // 2, 66))
        ecran.blit(texte_score, rect_score)
    elif etat_jeu == "game_over":
        texte_score = police_score.render(f" Score: {score}", True, (255, 255, 255))
        rect_score = texte_score.get_rect(center=(largeur // 2, 66))
        ecran.blit(texte_score, rect_score)

        texte_meilleur_score = police_score.render(f"Best Score : {meilleur_score}", True, (255, 255, 255))
        rect_meilleur_score = texte_meilleur_score.get_rect(center=(largeur // 2, 506))
        ecran.blit(texte_meilleur_score, rect_meilleur_score)

# Load the best score
def charger_meilleur_score():
    global meilleur_score
    if os.path.exists(chemin_fichier_score):
        with open(chemin_fichier_score, 'r') as fichier:
            meilleur_score = int(fichier.read())

def sauvegarder_meilleur_score():
    with open(chemin_fichier_score, 'w') as fichier:
        fichier.write(str(meilleur_score))


charger_meilleur_score()

# Function that updates the score
def mise_a_jour_score():
    global score, temps_score, meilleur_score
    if tuyaux:
        for tuyau in tuyaux:
            if 65 < tuyau.centerx < 69 and temps_score:
                score += 1
                temps_score = False
                point_sound.play()  # Jouer le son de pointage
            if tuyau.left <= 0:
                temps_score = True

    if score > meilleur_score:
        meilleur_score = score
        sauvegarder_meilleur_score()

# Function that draws the exit button
def dessiner_bouton_sortie():
    surface_bouton_sortie = pygame.Surface((80, 40), pygame.SRCALPHA)
    pygame.draw.rect(surface_bouton_sortie, (0, 0, 0), (0, 0, 80, 40), border_radius=5)
    texte_sortie = police_score.render("Exit", True, (255, 255, 255))
    surface_bouton_sortie.blit(texte_sortie, ((80 - texte_sortie.get_width()) // 2, (40 - texte_sortie.get_height()) // 2))
    ecran.blit(surface_bouton_sortie, rect_bouton_sortie.topleft)


# Game loop
en_cours = True
while en_cours:
    horloge.tick(90)

    # Check events
    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:  # QUIT event
            en_cours = False
            pygame.quit()
            sys.exit()

        if evenement.type == pygame.KEYDOWN:  # Key-down event
            if evenement.key == pygame.K_SPACE and not game_over:  # If the SPACE key is pressed
                # The first SPACE press starts the game.
                jeu_demarre = True
                mouvement_oiseau = 0
                mouvement_oiseau = -5
                wing_sound.play()  # Jouer le son d'aile lorsque l'oiseau bat des ailes

            if evenement.key == pygame.K_SPACE and game_over:
                game_over = False
                jeu_demarre = False  # Back to the waiting state
                tuyaux = []
                rect_oiseau = img_oiseau.get_rect(center=(67, 622 // 2))
                mouvement_oiseau = 0
                temps_score = True
                score = 0

        # To load the different frames
        if evenement.type == evenement_battement:
            index_oiseau += 1

            if index_oiseau > 2:
                index_oiseau = 0

            img_oiseau = oiseaux[index_oiseau]
            rect_oiseau = oiseau_haut.get_rect(center=rect_oiseau.center)

        # To add pipes to the list
        if evenement.type == creer_tuyau:
            tuyaux.extend(creer_tuyaux())

        # Check whether the exit button was clicked
        if evenement.type == pygame.MOUSEBUTTONDOWN and evenement.button == 1:
            if rect_bouton_sortie.collidepoint(evenement.pos):
                en_cours = False 
                pygame.quit()
                sys.exit()

    ecran.blit(img_base, (x_base, 550))
    ecran.blit(img_fond, (0, 0))


        # Game-over conditions
    if not game_over and jeu_demarre:
        # The game has started: normal physics apply.
        mouvement_oiseau += gravite
        rect_oiseau.centery += mouvement_oiseau
        oiseau_rotatif = pygame.transform.rotozoom(img_oiseau, mouvement_oiseau * -6, 1)

        if rect_oiseau.top < 5 or rect_oiseau.bottom >= 550:
            hit_sound.play()  # Jouer le son de collision
            game_over = True

        ecran.blit(oiseau_rotatif, rect_oiseau)
        animation_tuyaux()
        mise_a_jour_score()
        dessiner_score("game_on")
    elif not game_over and not jeu_demarre:
        # Waiting state: the bird floats gently, no pipes, no
        # gravity. We wait for the first SPACE press.
        tuyaux.clear()
        flottement = math.sin(pygame.time.get_ticks() * 0.005) * 6
        rect_oiseau.centery = hauteur // 2 + int(flottement)
        ecran.blit(img_oiseau, rect_oiseau)
        texte_pret = police_score.render("Appuyez sur ESPACE", True, (255, 255, 255))
        ecran.blit(texte_pret, texte_pret.get_rect(center=(largeur // 2, hauteur // 2 - 80)))
    elif game_over:
        ecran.blit(img_game_over, rect_game_over)
        dessiner_score("game_over")
        
        # Draw the exit button after the game ends
        dessiner_bouton_sortie()

    # To move the ground
    x_base -= 1
    if x_base < -448:
        x_base = 0

    dessiner_sol()

    # Update the game window
    pygame.display.update()

# Stop the background music and quit pygame
sauvegarder_meilleur_score()
pygame.mixer.music.stop()
pygame.quit()
sys.exit()
