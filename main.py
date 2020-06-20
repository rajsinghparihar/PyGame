import pygame
import random
import math
import os
import time

from pygame import mixer
# initialisation of pygame
pygame.init()

# screen creation
screen = pygame.display.set_mode((1050, 750))

# background
bg = pygame.image.load('Assets/Backgrounds/BG3.png')

# adding sounds
mixer.music.load('Assets/Sounds/bg_music.mp3')
mixer.music.play(-1)

# title and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('Assets/Sprites/Other/icon-small.png')
pygame.display.set_icon(icon)

# score counter
score = 0

# player
playerImg = pygame.image.load('Assets/Sprites/Players/player.png')
playerX = 500
playerY = 600
playerX_change = 0
playerY_change = 0

# enemies
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
visible = []
max_enemies = 21

# enemy count
count = max_enemies

for i in range(7):
    enemyImg.append(pygame.image.load('Assets/Sprites/Enemies/purple_enemy.png'))
    enemyImg.append(pygame.image.load('Assets/Sprites/Enemies/white_enemy.png'))
    enemyImg.append(pygame.image.load('Assets/Sprites/Enemies/cyanogen_enemy.png'))
for i in range(max_enemies):
    enemyX.append(random.randint(0, 985))
    enemyY.append(random.randint(50, 250))
    enemyX_change.append(5)
    enemyY_change.append(20)
    visible.append(True)

# bullet
bulletImg = pygame.image.load('Assets/Sprites/Other/beams.png')
bulletX = 0
bulletY = playerY
bulletX_change = 0
bulletY_change = 10
# ready state : you can't see the bullet, its not yet fired.
# fired state : the bullet is moving
bullet_state = "ready"

def create_font(text, size, color):
    font = pygame.font.Font('Assets/Fonts/mm.ttf', size)
    t = font.render(text, True, color)
    return t

def player(x, y):
    screen.blit(playerImg, (x, y))

def Collision(enemyX,enemyY,bulletX,bulletY):
    dist = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if(dist <= 50):
        return True
    else:
        return False

def enemy(i, x, y):
    screen.blit(enemyImg[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 3, y - 40))



# game loop
running = True
while running:

    # game over
    game_over_text = create_font("You Win! Well Played, Your Score : " + str(score), 62, (0, 255, 0))
    # rgb tuple to give bg-color, max is 255
    screen.fill((44, 44, 44))
    # bg img
    screen.blit(bg, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # input detection
        # horizontal movement
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE and bullet_state is "ready":
                bulletX = playerX
                bullet_sound = mixer.Sound('Assets/Sounds/shoot.wav')
                bullet_sound.play()
                fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

        # vertical movement
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                playerY_change = -5
            if event.key == pygame.K_DOWN:
                playerY_change = 5

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerY_change = 0
    # player movement
    playerX += playerX_change
    playerY += playerY_change

    # adding boundaries
    if playerX >= 985:
        playerX = 985
    if playerX <= 0:
        playerX = 0
    for i in range(max_enemies):
        enemyX[i] += enemyX_change[i]

        # adding boundaries
        if enemyX[i] >= 985:
            enemyX_change[i] = -enemyX_change[i]
            enemyY[i] += enemyY_change[i]

        elif enemyX[i] <= 0:
            enemyX_change[i] = 5
            enemyY[i] += enemyY_change[i]

    # multiple bullets
    if bulletY <= 0:
        bulletY = playerY;
        bullet_state = "ready"
    # bullet movement
    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change
    for i in range(max_enemies):
        #collision
        col = Collision(enemyX[i], enemyY[i], bulletX, bulletY)
        if col:
            col_sound = mixer.Sound('Assets/Sounds/invaderkilled.wav')
            col_sound.play()
            bulletY = playerY
            bullet_state = "ready"
            score += 100
            visible[i] = False
            enemyX[i] = 1100
            enemyY[i] = 1100
            count -= 1

    Scoreboard = create_font("Score : " + str(score), 40, (240, 188, 207))
    screen.blit(Scoreboard, (0, 0))

    player(playerX, playerY)
    for i in range(max_enemies):
        if visible[i]:
            enemy(i, enemyX[i], enemyY[i])
    if (count == 0):
        mixer.music.stop()
        win = mixer.Sound('Assets/Sounds/win.wav')
        win.play(1)
        screen.blit(game_over_text, (50, 380))

    pygame.display.update()
