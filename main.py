import pygame
import random
import cv2
import sys
from tkinter import *

# text
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 30)


# Initialisation de pygame
pygame.init()
controller = False

WIDTH = 800
HEIGHT = 600
BALL_RADIUS = 10
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 10
BLOCK_WIDTH = 70
BLOCK_HEIGHT = 20
BLOCK_MARGIN = 10
BLOCK_ROWS = 5
BLOCK_COLS = 10
BLOCK_COLORS = [(255, 0, 0), (255, 128, 0), (255, 255, 0), (128, 255, 0), (0, 255, 0)]

def yes_button():
    global controller
    controller = False
    fenetre.destroy()

def no_button():
    global controller
    controller = True
    fenetre.destroy()

fenetre = Tk()
fenetre.title("Menu Brick Breaker")
fenetre.geometry("800x600") # Définition des dimensions de la fenêtre

# Ajout d'une icône pour la fenêtre
fenetre.iconbitmap("images/games.png")

# Ajout d'un fond d'écran pour la fenêtre
bg_image = PhotoImage(file="images/background.png")
background_label = Label(fenetre, image=bg_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Titre de la fenêtre
title_label = Label(fenetre, text="Voulez-vous utiliser la reconnaissance faciale ?", font=("Helvetica", 18), fg="white", bg="#974590")
title_label.pack(pady=20)

# Boutons "Oui" et "Non"
button_frame = Frame(fenetre, bg="#974590")
button_frame.pack(side=BOTTOM, pady=20)
yes_button = Button(button_frame, text="Oui", width=10, font=("Helvetica", 14), bg="#8d99ae", fg="white", bd=0, command=yes_button)
yes_button.pack(side=LEFT, padx=30)
no_button = Button(button_frame, text="Non", width=10, font=("Helvetica", 14), bg="#8d99ae", fg="white", bd=0, command=no_button)
no_button.pack(side=RIGHT, padx=30)

# Lancement de la fenêtre
fenetre.mainloop()

# Création de la fenêtre de jeu
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Breakout")

# Définition des fonctions
def draw_ball(ball_x, ball_y):
    pygame.draw.circle(screen, (255, 255, 255), (int(ball_x), int(ball_y)), BALL_RADIUS)

def draw_paddle(paddle_x):
    pygame.draw.rect(screen, (255, 255, 255), (int(paddle_x), HEIGHT - PADDLE_HEIGHT, PADDLE_WIDTH, PADDLE_HEIGHT))

def draw_block(block_x, block_y, block_color):
    pygame.draw.rect(screen, block_color, (int(block_x), int(block_y), BLOCK_WIDTH, BLOCK_HEIGHT))

def collision(ball_x, ball_y, paddle_x, blocks, ball_speed_x, ball_speed_y):
    if ball_y + BALL_RADIUS >= HEIGHT - PADDLE_HEIGHT and ball_x >= paddle_x and ball_x <= paddle_x + PADDLE_WIDTH:
        ball_speed_y = -ball_speed_y
        ball_speed_x += random.uniform(-1, 1)
        ball_speed_y += random.uniform(-1, 1)
        return True, ball_speed_x, ball_speed_y
    for row in range(BLOCK_ROWS):
        for col in range(BLOCK_COLS):
            block = blocks[row][col]
            if block is not None:
                block_x, block_y, block_color = block
                if ball_x + BALL_RADIUS >= block_x and ball_x - BALL_RADIUS <= block_x + BLOCK_WIDTH and ball_y + BALL_RADIUS >= block_y and ball_y - BALL_RADIUS <= block_y + BLOCK_HEIGHT:
                    blocks[row][col] = None
                    ball_speed_y = -ball_speed_y
                    ball_speed_x += random.uniform(-1, 1)
                    ball_speed_y += random.uniform(-1, 1)
                    return True, ball_speed_x, ball_speed_y
    return False, ball_speed_x, ball_speed_y


# Création des blocs
blocks = []
for row in range(BLOCK_ROWS):
    blocks.append([])
    for col in range(BLOCK_COLS):
        block_x = col * (BLOCK_WIDTH + BLOCK_MARGIN) + BLOCK_MARGIN
        block_y = row * (BLOCK_HEIGHT + BLOCK_MARGIN) + BLOCK_MARGIN
        block_color = BLOCK_COLORS[row]
        blocks[row].append((block_x, block_y, block_color))

ball_x = WIDTH / 2
ball_y = HEIGHT / 2
ball_speed_x = random.choice([-5, 5])
ball_speed_y = 3
paddle_x = WIDTH / 2 - PADDLE_WIDTH / 2
paddle_speed = 0
cap = cv2.VideoCapture(0)
x = 0
w = 0


# charger le fichier XML contenant les informations sur les visages
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
running = True
# Boucle principale du jeu
while running:

    hit, ball_speed_x, ball_speed_y = collision(ball_x, ball_y, paddle_x, blocks, ball_speed_x, ball_speed_y)


    ret, frame = cap.read()

    resize_frame = cv2.resize(frame, (WIDTH//2, HEIGHT//2))

    # convertir l'image en noir et blanc
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # détecter les visages dans l'image
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)


    # dessiner un rectangle autour de chaque visage détecté
    for (x,y,w,h) in faces:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)

        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        for (ex,ey,ew,eh) in eyes:
            cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                paddle_speed = -10
            elif event.key == pygame.K_RIGHT:
                paddle_speed = 10

    if  controller == False:
        if x + w/2 < frame.shape[1]/2:
            paddle_speed = 8
        elif x + w/2 > frame.shape[1]/2:
            paddle_speed = -8


    cv2.imshow('frame',resize_frame)


    paddle_x += paddle_speed
    if paddle_x < 0:
        paddle_x = 0
    elif paddle_x > WIDTH - PADDLE_WIDTH:
        paddle_x = WIDTH - PADDLE_WIDTH

    # Mise à jour de la position de la balle
    ball_x += ball_speed_x
    ball_y += ball_speed_y
    if ball_x < BALL_RADIUS or ball_x > WIDTH - BALL_RADIUS:
        ball_speed_x *= -1
    if ball_y < BALL_RADIUS:
        ball_speed_y *= -1
    elif ball_y > HEIGHT - BALL_RADIUS:
        running = False

    if hit:
        ball_speed_x = max(min(ball_speed_x, 5), -5)  # limiter la vitesse de la balle
    ball_x += ball_speed_x
    ball_y += ball_speed_y

# place la camera en bas a gauche
    cv2.moveWindow('frame', 0, 0)

    # Affichage
    screen.fill((0, 0, 0))
    draw_ball(ball_x, ball_y)
    draw_paddle(paddle_x)
    for row in range(BLOCK_ROWS):
        for col in range(BLOCK_COLS):
            block = blocks[row][col]
            if block is not None:
                block_x, block_y, block_color = block
                draw_block(block_x, block_y, block_color)
    pygame.display.flip()

    if all(block is None for row in blocks for block in row):
        print("You win!")
        running = False

cap.release()
cv2.destroyAllWindows()
cv2.waitKey(0)
pygame.quit()
