print("Welcome to my Shooting game!")

import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((800, 600))

# Game icon and caption
pygame.display.set_caption("Space Game")
icon = pygame.image.load('game_icon.png')
pygame.display.set_icon(icon)

# Background Image
background = pygame.image.load('background.jpg')

# Resize the image
new_width, new_height = 800, 600
resized_image = pygame.transform.scale(background, (new_width, new_height))

# Player image
player_image = pygame.image.load('spaceship.png')
player_width, player_height = 64, 64  # Adjust according to player image size
player_X = 370
player_Y = 480
p_x = 0

def player(X, Y):
    screen.blit(player_image, (X, Y))

# Enemy image
enemy_image = pygame.image.load('enemy.png')
enemy_X = [random.randint(0, 800) for _ in range(4)]
enemy_Y = [random.randint(50, 150) for _ in range(4)]
enemy_width, enemy_height = 64, 64  # Adjust according to enemy image size
enemy_x_change = [0.3, -0.2, 0.4, -0.3]
enemy_y_change = [0, 0.3, -0.3, 0.2]

def enemy(X, Y):
    for i in range(4):
        screen.blit(enemy_image, (X[i], Y[i]))

# Bullet image
bullet_image = pygame.image.load('bullet_icon.png')
bullet_Y = 480
bullet_x_change = 0
bullet_y_change = 5
bullets = []

def bullet_fire(X, Y):
    bullets.append([X, Y])

# Score
score = 0
font = pygame.font.Font(None, 36)

def display_score(score):
    score_display = font.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(score_display, (10, 10))

# Game over message
game_over_font = pygame.font.Font(None, 72)

def game_over_message():
    game_over_text = game_over_font.render("Game Over", True, (255, 0, 0))
    screen.blit(game_over_text, (250, 250))
    pygame.display.update()
    pygame.time.delay(2000)  # Display game over message for 2 seconds
    pygame.quit()
    sys.exit()

# Collision function
def is_collision(obj1_x, obj1_y, obj1_width, obj1_height, obj2_x, obj2_y, obj2_width, obj2_height):
    return (
        obj1_x < obj2_x + obj2_width and
        obj1_x + obj1_width > obj2_x and
        obj1_y < obj2_y + obj2_height and
        obj1_y + obj1_height > obj2_y
    )

# Game loop
run = True
while run:

    # Screen background colors
    screen.fill((250, 230, 230))

    # Background Image
    screen.blit(resized_image, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            print('Keystoke has been pressed.')

            # Player moving Left side
            if event.key == pygame.K_LEFT:
                p_x = -1
            # Player moving Right side
            if event.key == pygame.K_RIGHT:
                p_x = 1

            # Fire bullet when space key is pressed
            if event.key == pygame.K_SPACE:
                bullet_fire(player_X + 16, bullet_Y)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                p_x = 0

    # Adding value left or right
    player_X += p_x

    # Condition for stopping player within the screen
    if player_X <= 0:
        player_X = 0
    elif player_X >= 736:
        player_X = 736

    # Player function
    player(player_X, player_Y)

    # Adding value left or right so that enemies move
    for i in range(4):
        enemy_X[i] += enemy_x_change[i]
        enemy_Y[i] += enemy_y_change[i]

        # Reset enemy position if it goes out of bounds
        if enemy_X[i] <= 0 or enemy_X[i] >= 736 or enemy_Y[i] <= 0 or enemy_Y[i] >= 536:
            enemy_X[i] = random.randint(0, 800)
            enemy_Y[i] = random.randint(50, 150)

        # Check for collisions with the player
        if is_collision(player_X, player_Y, player_width, player_height, enemy_X[i], enemy_Y[i], enemy_width, enemy_height):
            game_over_message()

    # Enemy function
    enemy(enemy_X, enemy_Y)

    # Bullet logic
    for bullet in bullets:
        bullet[1] -= bullet_y_change
        screen.blit(bullet_image, (bullet[0], bullet[1]))

        # Check for collisions with the enemies
        for i in range(4):
            if is_collision(bullet[0], bullet[1], 32, 32, enemy_X[i], enemy_Y[i], enemy_width, enemy_height):
                bullets.remove(bullet)
                score += 10
                enemy_X[i] = random.randint(0, 800)
                enemy_Y[i] = random.randint(50, 150)

    # Remove bullets that reach the top of the screen
    bullets = [bullet for bullet in bullets if bullet[1] > 0]

    # Display the score
    display_score(score)

    pygame.display.update()

    # Introduce a slight delay for better visualization
    pygame.time.delay(2)
