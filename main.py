import pygame
import random
import cv2

# Initialisation de pygame
pygame.init()

# Définition des variables de jeu
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

def collision(ball_x, ball_y, paddle_x, blocks):
    # Vérification de la collision avec le paddle
    if ball_y + BALL_RADIUS >= HEIGHT - PADDLE_HEIGHT and ball_x >= paddle_x and ball_x <= paddle_x + PADDLE_WIDTH:
        return True
    # Vérification de la collision avec les blocs
    for row in range(BLOCK_ROWS):
        for col in range(BLOCK_COLS):
            block = blocks[row][col]
            if block is not None:
                block_x, block_y, block_color = block
                if ball_x + BALL_RADIUS >= block_x and ball_x - BALL_RADIUS <= block_x + BLOCK_WIDTH and ball_y + BALL_RADIUS >= block_y and ball_y - BALL_RADIUS <= block_y + BLOCK_HEIGHT:
                    # Disparition du block touché
                    blocks[row][col] = None
                    return True
    return False

# Création des blocs
blocks = []
for row in range(BLOCK_ROWS):
    blocks.append([])
    for col in range(BLOCK_COLS):
        block_x = col * (BLOCK_WIDTH + BLOCK_MARGIN) + BLOCK_MARGIN
        block_y = row * (BLOCK_HEIGHT + BLOCK_MARGIN) + BLOCK_MARGIN
        block_color = BLOCK_COLORS[row]
        blocks[row].append((block_x, block_y, block_color))

# Boucle principale du jeu
ball_x = WIDTH / 2
ball_y = HEIGHT / 2
ball_speed_x = random.choice([-2, 5])
ball_speed_y = 2
paddle_x = WIDTH / 2 - PADDLE_WIDTH / 2
paddle_speed = 0

cap = cv2.VideoCapture(0)
x = 0
w = 0

# charger le fichier XML contenant les informations sur les visages
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

running = True
while running:
    
    ret, frame = cap.read()
    resize_frame = cv2.resize(frame, (WIDTH//2, HEIGHT//2))

    # convertir l'image en noir et blanc
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # détecter les visages dans l'image
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)    

    # dessiner un rectangle autour de chaque visage détecté
    for (x,y,w,h) in faces:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
        
# detecte si ma tete est vers la gauche ou vers la droite
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        for (ex,ey,ew,eh) in eyes:
            cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
    
    
    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    if x + w/2 < frame.shape[1]/2:
        paddle_speed = 5
    elif x + w/2 > frame.shape[1]/2:
        paddle_speed = -5
                
    cv2.imshow('frame',resize_frame)


    # Mise à jour de la position du paddle
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

    # Vérification de la collision
    if collision(ball_x, ball_y, paddle_x, blocks):
        ball_speed_y *= -1
        
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
cap.release()
cv2.destroyAllWindows()
pygame.quit()
    