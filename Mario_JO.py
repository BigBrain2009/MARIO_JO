import pygame
import random
import time
import os

# === Mode d'emploi des touches du jeu ===
# Flèche Haut    : Sauter
# Flèche Bas     : Se baisser
# Espace         : Mettre en pause / Reprendre
# Flèche Gauche  : Quitter le jeu
# Flèche Droite  : Redémarrer le jeu / Continuer après avoir gagné une médaille
# Entrée         : Commencer le jeu
# =========================================

# Initialiser Pygame
pygame.init()
pygame.mixer.init()  # Initialiser explicitement le module mixer

# Définir les couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 19, 255)

# Obtenir la résolution de l'écran
info = pygame.display.Info()
SCREEN_WIDTH = info.current_w
SCREEN_HEIGHT = info.current_h

# Paramètres de la fenêtre de jeu en plein écran
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Dino Game")

# Police pour le mode d'emploi
font = pygame.font.Font(None, 36)

# Variables pour la position et la taille de la mascotte
mascot_x = 600  # Position horizontale de la mascotte
mascot_y = SCREEN_HEIGHT - 400  # Position verticale de la mascotte
mascot_width = 150  # Largeur de la mascotte
mascot_height = 150  # Hauteur de la mascotte

# Fonction pour afficher un message à l'écran
def draw_message(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_obj, text_rect)

# Afficher le mode d'emploi à l'écran
def show_instructions():
    instructions = [
        "Mode d'emploi des touches du jeu :",
        "Flèche Haut   : Sauter",
        "Flèche Bas     : Se baisser",
        "Espace         : Mettre en pause / Reprendre",
        "Flèche Gauche  : Quitter le jeu",
        "Flèche Droite  : Redémarrer le jeu / Continuer",
        "Appuyez sur Entrée pour commencer..."
    ]
    screen.fill((0, 0, 0))  # Fond noir
    for i, line in enumerate(instructions):
        draw_message(line, font, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100 + i * 40)
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Attendre que la touche Entrée soit pressée
                    waiting = False

# Afficher les instructions
show_instructions()

# Charger la musique en fond
current_path = os.getcwd()
background_music_path = os.path.join(current_path, 'background_music 2.mp3')
pygame.mixer.music.load(background_music_path)
pygame.mixer.music.play(-1)  # -1 signifie que la musique sera jouée en boucle

# Charger le nouveau son de défaite
losing_sound_path = os.path.join(current_path, 'losing_sound.ogg')
losing_sound = pygame.mixer.Sound(losing_sound_path)

# Charger le nouveau son de victoire
victory_sound_path = os.path.join(current_path, 'Super Mario Bros. Music - Level Complete - BlittleMcNilsen.ogg')
victory_sound = pygame.mixer.Sound(victory_sound_path)

# Fonction pour jouer le son de défaite et mettre en pause la musique de fond
def play_losing_sound():
    pygame.mixer.music.pause()  # Mettre en pause la musique de fond
    pygame.mixer.Sound.play(losing_sound)

# Fonction pour jouer le son de victoire et mettre en pause la musique de fond
def play_victory_sound():
    pygame.mixer.music.pause()  # Mettre en pause la musique de fond
    pygame.mixer.Sound.play(victory_sound)

# Charger les images du jeu
background_image_path = os.path.join(current_path, 'Capture d’écran 2024-07-29 à 15.16.09.png')
background_image = pygame.image.load(background_image_path)
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

new_game_over_image_path = os.path.join(current_path, 'Capture d’écran 2024-07-31 à 19.15.00.png')
game_over_image = pygame.image.load(new_game_over_image_path)
game_over_image = pygame.transform.scale(game_over_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

dino_image_path = os.path.join(current_path, 'dino_transparent.png')
dino_image = pygame.image.load(dino_image_path)
dino_image = pygame.transform.scale(dino_image, (100, 100))  # Ajuster la taille de l'image si nécessaire

ground_image_path = os.path.join(current_path, 'terrain.png')
ground_image = pygame.image.load(ground_image_path)
ground_image = pygame.transform.scale(ground_image, (SCREEN_WIDTH, 20))

plante_image_path = os.path.join(current_path, 'plante.png')  # Nom de ton image de plante
plante_image = pygame.image.load(plante_image_path)
plante_image = pygame.transform.scale(plante_image, (40, 70))  # Ajuster la taille de l'image si nécessaire

obstacle_image_path = os.path.join(current_path, 'obstacle.png')  # Nom de ton image d'obstacle
obstacle_image = pygame.image.load(obstacle_image_path)
obstacle_image = pygame.transform.scale(obstacle_image, (90, 90))  # Ajuster la taille de l'image si nécessaire

medal_gold_path = os.path.join(current_path, 'medal_gold.png')
medal_silver_path = os.path.join(current_path, 'medal_silver.png')
medal_bronze_path = os.path.join(current_path, 'medal_bronze.png')

medal_gold = pygame.image.load(medal_gold_path).convert_alpha()
medal_silver = pygame.image.load(medal_silver_path).convert_alpha()
medal_bronze = pygame.image.load(medal_bronze_path).convert_alpha()

medal_size = (150, 150)  # Ajustez cette taille selon vos besoins
medal_gold = pygame.transform.scale(medal_gold, medal_size)
medal_silver = pygame.transform.scale(medal_silver, medal_size)
medal_bronze = pygame.transform.scale(medal_bronze, medal_size)

# Charger l'image de la mascotte avec la taille personnalisée
mascot_image_path = os.path.join(current_path, 'mascot.png')
mascot_image = pygame.image.load(mascot_image_path)
mascot_image = pygame.transform.scale(mascot_image, (mascot_width, mascot_height))

# Définir les variables pour le dinosaure
dino_width = dino_image.get_width()
dino_height = dino_image.get_height()
dino_x = 50
dino_y = SCREEN_HEIGHT - dino_height - 10
dino_vel_y = 0
gravity = 1.2
jump_power = -20
is_jumping = False
is_ducking = False
duck_height = 20

# Définir les variables pour les obstacles
obstacle_width = plante_image.get_width()
obstacle_height = plante_image.get_height()
obstacle_x = SCREEN_WIDTH
obstacle_y = SCREEN_HEIGHT - obstacle_height - 20
obstacle_vel_x = 10

# Définir les variables pour les oiseaux (obstacles remplacés)
bird_width = obstacle_image.get_width()
bird_height = obstacle_image.get_height()
bird_x = SCREEN_WIDTH + 400
bird_y = SCREEN_HEIGHT - dino_height - 10
bird_vel_x = 20

# Terrain en mouvement
ground_x = 0
ground_y = SCREEN_HEIGHT - 20
ground_vel_x = 10

# Fonction pour afficher le dinosaure
def draw_dino(x, y, ducking):
    if ducking:
        screen.blit(dino_image, (x, y + (dino_height - duck_height)))
    else:
        screen.blit(dino_image, (x, y))

# Fonction pour afficher les obstacles
def draw_obstacle(x, y):
    screen.blit(plante_image, (x, y))

# Fonction pour afficher les obstacles (oiseaux remplacés)
def draw_bird(x, y):
    screen.blit(obstacle_image, (x, y))

# Fonction pour afficher le terrain
def draw_ground(x, y):
    screen.blit(ground_image, (x, y))
    screen.blit(ground_image, (x + SCREEN_WIDTH, y))

# Fonction pour afficher un message de médaille avec l'image correspondante
def show_medal_message(medal):
    message = f"Bravo ! Vous avez gagné une {medal} !"
    draw_message(message, font, GREEN, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)
    
    # Afficher l'image de la médaille correspondante
    medal_image = None
    if medal == "médaille d'or":
        medal_image = medal_gold
    elif medal == "médaille d'argent":
        medal_image = medal_silver
    elif medal == "médaille de bronze":
        medal_image = medal_bronze
    
    if medal_image:
        medal_rect = medal_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        screen.blit(medal_image, medal_rect)
    
    pygame.display.flip()
    play_victory_sound()
    pygame.time.wait(2000)  # Attendre 2 secondes avant de continuer

# Fonction pour demander si le joueur veut continuer
def ask_continue():
    draw_message("Voulez-vous continuer ? (Flèche droite: Oui / Flèche gauche: Non)", font, GREEN, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100)
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:  # Remplacer pygame.K_o par pygame.K_RIGHT
                    pygame.mixer.music.unpause()  # Reprendre la musique de fond
                    return True
                if event.key == pygame.K_LEFT:  # Remplacer pygame.K_n par pygame.K_LEFT
                    pygame.quit()
                    return False

# Boucle principale du jeu
def main_game():
    global dino_y, dino_vel_y, is_jumping, is_ducking, obstacle_x, obstacle_y, obstacle_height, bird_x, bird_y, score, ground_x, obstacle_vel_x, ground_vel_x, bird_vel_x, start_time, accumulated_time
    
    running = True
    clock = pygame.time.Clock()
    score = 0
    start_time = time.time()
    accumulated_time = 0  # Variable pour garder une trace du temps accumulé
    pause_start_time = 0  # Temps où la pause a commencé
    level = 0
    level_time = start_time
    last_medal = ""
    continue_game = True
    paused = False  # Variable de pause

    while running and continue_game:
        current_time = time.time()  # Temps courant
        if not paused:
            # Mettre à jour la position du dinosaure
            dino_y += dino_vel_y
            if is_jumping:
                dino_vel_y += gravity
            if dino_y >= SCREEN_HEIGHT - dino_height - 20:
                dino_y = SCREEN_HEIGHT - dino_height - 20
                dino_vel_y = 0
                is_jumping = False

            # Mettre à jour la position de l'obstacle
            obstacle_x -= obstacle_vel_x
            if obstacle_x < -obstacle_width:
                obstacle_x = SCREEN_WIDTH + random.randint(0, 300)
                obstacle_height = random.randint(40, 80)
                obstacle_y = SCREEN_HEIGHT - obstacle_height - 20

            # Mettre à jour la position de l'obstacle (remplaçant les oiseaux)
            bird_x -= bird_vel_x
            if bird_x < -bird_width:
                bird_x = SCREEN_WIDTH + random.randint(0, 300)
                bird_y = SCREEN_HEIGHT - dino_height - 20

            # Mettre à jour la position du terrain
            ground_x -= ground_vel_x
            if ground_x <= -SCREEN_WIDTH:
                ground_x = 0

            # Calculer le score basé sur le temps écoulé sans compter le temps en pause
            score = int(current_time - start_time - accumulated_time)

            # Vérifier la collision avec les obstacles
            if (dino_x + dino_width > obstacle_x and dino_x < obstacle_x + obstacle_width and
                dino_y + dino_height > obstacle_y and not is_ducking):
                running = False
                if not last_medal:
                    play_losing_sound()  # Jouer le son de défaite uniquement si aucune médaille n'est gagnée

            # Vérifier la collision avec les obstacles (remplaçant les oiseaux)
            if (dino_x + dino_width > bird_x and dino_x < bird_x + bird_width):
                if not is_ducking and (dino_y + dino_height > bird_y):
                    running = False
                    if not last_medal:
                        play_losing_sound()  # Jouer le son de défaite uniquement si aucune médaille n'est gagnée

            # Mettre à jour le niveau toutes les minutes
            if current_time - level_time >= 30:
                level += 1
                level_time = current_time
                # Augmenter la difficulté
                obstacle_vel_x += 2
                ground_vel_x += 2
                bird_vel_x += 2

                # Mettre à jour la dernière médaille gagnée
                if level == 1:
                    last_medal = "médaille de bronze"
                elif level == 2:
                    last_medal = "médaille d'argent"
                elif level >= 3:
                    last_medal = "médaille d'or"

                # Arrêter d'augmenter la difficulté après trois niveaux (trois minutes)
                if level > 3:
                    level = 3

            # Dessiner le jeu
            screen.blit(background_image, [0, 0])  # Afficher l'image d'arrière-plan
            draw_ground(ground_x, ground_y)
            screen.blit(mascot_image, (mascot_x, mascot_y))  # Afficher la mascotte
            draw_dino(dino_x, dino_y, is_ducking)
            draw_obstacle(obstacle_x, obstacle_y)
            draw_bird(bird_x, bird_y)

            # Afficher le score
            score_text = font.render("Score: " + str(score), True, WHITE)
            screen.blit(score_text, [10, 10])

            # Afficher le niveau
            level_text = font.render("Level: " + str(level), True, WHITE)
            screen.blit(level_text, [SCREEN_WIDTH - 150, 10])

            pygame.mixer.music.unpause()  # Reprendre la musique lorsque le jeu reprend

        else:
            pygame.mixer.music.pause()  # Mettre la musique en pause
            # Afficher le message de pause
            draw_message("Pause - Appuyez sur Espace pour continuer", font, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

        # Gérer les événements (qu'ils soient en pause ou en cours)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and not is_jumping and not is_ducking and not paused:
                    dino_vel_y = jump_power
                    is_jumping = True
                if event.key == pygame.K_DOWN and not is_jumping and not paused:
                    is_ducking = True
                if event.key == pygame.K_SPACE:  # Appuyer sur 'Espace' pour mettre en pause/reprendre
                    if paused:
                        accumulated_time += current_time - pause_start_time  # Ajouter le temps passé en pause
                    else:
                        pause_start_time = time.time()  # Enregistrer l'heure de début de la pause
                    paused = not paused
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    is_ducking = False

        pygame.display.flip()
        
        # Limiter le taux de rafraîchissement à 60 FPS
        clock.tick(60)

    # Si le joueur perd après avoir gagné une médaille
    if last_medal:
        show_medal_message(last_medal)
        continue_game = ask_continue()
    else:
        game_over(last_medal)

    return last_medal, continue_game

# Fonction pour afficher l'écran de fin de partie
def game_over(last_medal):
    if not last_medal:
        play_losing_sound()  # Jouer le son de défaite uniquement si aucune médaille n'est gagnée
    screen.blit(game_over_image, [0, 0])  # Afficher la nouvelle image de Game Over
    draw_message("Score: " + str(score), font, GREEN, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    if last_medal:
        draw_message("Bravo ! Vous avez gagné une " + last_medal + " !", font, GREEN, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
    draw_message("Appuyez sur Flèche Droite pour Redémarrer ou Flèche Gauche pour Quitter", font, GREEN, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:  # Remplacer pygame.K_r par pygame.K_RIGHT
                    pygame.mixer.music.unpause()  # Reprendre la musique de fond
                    return True
                if event.key == pygame.K_LEFT:  # Remplacer pygame.K_q par pygame.K_LEFT
                    pygame.quit()
                    return False

# Boucle principale
try:
    while True:
        # Réinitialiser les variables de vitesse avant de démarrer une nouvelle partie
        obstacle_vel_x = 10
        ground_vel_x = 10
        bird_vel_x = 10
        dino_y = SCREEN_HEIGHT - dino_height - 20
        dino_vel_y = 0
        is_jumping = False
        is_ducking = False
        obstacle_x = SCREEN_WIDTH
        bird_x = SCREEN_WIDTH + 300
        bird_y = SCREEN_HEIGHT - dino_height - 50
        last_medal, continue_game = main_game()
        if not continue_game or not last_medal and not game_over(last_medal):
            break
except KeyboardInterrupt:
    pygame.quit()
    print("Game exited by user")
