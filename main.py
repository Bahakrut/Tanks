import math

import pygame
from pygame import mixer
import random
pygame.init()

screen = pygame.display.set_mode((800,600))

score = 0

# BACKGROUND MUSIC
mixer.music.load("ost/background.wav")
mixer.music.play(-1)

#CAPTION AND ICON
pygame.display.set_caption("WarTank")
icon = pygame.image.load('images/tank.png')
pygame.display.set_icon(icon)


#BACKGROUND IMAGE
background = pygame.image.load("images/background.png")


#PLAYER IMAGE

playerImg = pygame.image.load("images/tank.png")
playerX = 370
playerY = 500
playerX_change = 0
playerY_change = 0



# ENEMY IMAGE

enemyIMG = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
enemies_number = 5
for i in range(enemies_number):
    enemyIMG.append(pygame.image.load("images/enemy.png"))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(0.5)
    enemyY_change.append(40)




# BULLET IMAGE

bulletIMG = pygame.image.load("images/bullet.png")
bulletX = 0
bulletY = 480
bullet_state = "ready"
bulletX_change = 0
bulletY_change = 2

#Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

#GAME OVER

font_game_over = pygame.font.Font('freesansbold.ttf', 64)
def game_over():
    over_text = font_game_over.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))
def enemy(x, y, i):
    screen.blit(enemyIMG[i], (x, y))
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletIMG, (x+16, y+10))

#CHeck the Collisions
def isCollision(enemyX, enemyY, bulletX, bullety):
    return math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2)) < 27


# GAME LOOP
running = True
keys_pressed = {'left': False, 'right': False}

while running:
    screen.fill((191,227,180))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                keys_pressed['left'] = True
                keys_pressed['right'] = False  # Reset right key when left key is pressed
            elif event.key == pygame.K_RIGHT:
                keys_pressed['right'] = True
                keys_pressed['left'] = False  # Reset left key when right key is pressed
            elif event.key == pygame.K_SPACE and bullet_state == 'ready':
                bullet_sound = mixer.Sound("ost/fire.wav")
                bullet_sound.play()
                bulletX = playerX
                fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                keys_pressed['left'] = False
            elif event.key == pygame.K_RIGHT:
                keys_pressed['right'] = False

            # Update player position based on keys being pressed
        if keys_pressed['left']:
            playerX_change = -0.7
        elif keys_pressed['right']:
            playerX_change = 0.7
        else:
            playerX_change = 0



    playerX += playerX_change
    if(playerX >= 736):
        playerX = 736
    elif(playerX <= 0):
        playerX = 0

    for i in range(enemies_number):
        if(enemyY[i] > 440):
            for j in range(enemies_number):
                enemyY[j] = 2000;
            game_over()
            break


        enemyX[i] += enemyX_change[i]
        if (enemyX[i] >= 736):
            enemyX_change[i] = -0.5
            enemyY[i] += enemyY_change[i]
        elif (enemyX[i] <= 0):
            enemyX_change[i] = 0.5
            enemyY[i] += enemyY_change[i]

        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)

        if (collision):
            collision_sound = mixer.Sound("ost/explosion.wav")
            collision_sound.play()

            bullet_state = "ready"
            bulletY = 480
            score_value += 1
            print(score)
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)


        enemy(enemyX[i], enemyY[i], i)

    if(bulletY <= 0):
        bulletY = 480
        bullet_state = 'ready'
    if(bullet_state == "fire"):
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change


    show_score(textX, textY)
    player(playerX, playerY)

    pygame.display.update()