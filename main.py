import pygame
import cv2

# Initialisation de Pygame
pygame.init()

# Taille de l'écran
screen_width = 800
screen_height = 600

# Initialisation de la fenêtre Pygame
screen = pygame.display.set_mode((screen_width, screen_height))

block_colors = [(69, 177, 232), (242, 85, 96), (86, 174, 87)]
block_size = 65
block_spacing = 5
blocks_per_row = screen_width // (block_size + block_spacing)

# Chargement de l'image de l'objet principal
platbb_img = pygame.image.load('images/platbb.png')

# Position initiale de l'objet principal
platbb_x = screen_width / 2
platbb_y = screen_height -80
platbb_img = pygame.transform.scale(platbb_img, (100, 50))

# Initialisation de la balle
ball_x = screen_width / 2
ball_y = screen_height / 2
ball_speed_x = 1
ball_speed_y = 1
ball_radius = 10

# Allumer la caméra
cap = cv2.VideoCapture(0)

# Charger le fichier XML contenant les informations sur les visages
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

# Boucle principale
while True:
    # Capturer une image depuis la caméra
    ret, frame = cap.read()

    # Redimensionner l'image de la caméra
    resized_frame = cv2.resize(frame, (screen_width // 4, screen_height // 4))

    # Convertir l'image en noir et blanc
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Détecter les visages dans l'image
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    screen.fill((255, 255, 255))
    
    # le joueur ne peut pas sortir de l'écran
    if platbb_x < 0:
        platbb_x = 0
    if platbb_x > screen_width - 100:
        platbb_x = screen_width - 100
    
    # Dessiner un rectangle autour de chaque visage détecté
    for (x,y,w,h) in faces:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)

        # Detecter si ma tete est vers la gauche ou vers la droite
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        for (ex,ey,ew,eh) in eyes:
            cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

        # Déplacer l'objet principal en fonction du mouvement de la tête
        if x + w/2 < frame.shape[1] / 2:
            platbb_x += 7
        else:
            platbb_x -= 7
            
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            platbb_x -= 7
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            platbb_x += 7
            

    for i in range(0, blocks_per_row):
        for j in range(0, len(block_colors)):
            x = i * (block_size + block_spacing)
            y = j * (block_size + block_spacing)
            pygame.draw.rect(screen, block_colors[j], (x, y, block_size, 20))
            
    ball_x += ball_speed_x
    ball_y += ball_speed_y
    # Rebondir sur les murs horizontaux
    if ball_y - ball_radius < 0 or ball_y + ball_radius > screen_height:
        ball_speed_y = -ball_speed_y

    # Rebondir sur les murs verticaux
    if ball_x - ball_radius < 0 or ball_x + ball_radius > screen_width:
        ball_speed_x = -ball_speed_x

    # Rebondir sur la plateforme
    if ball_y + ball_radius > platbb_y and ball_x + ball_radius > platbb_x and ball_x - ball_radius < platbb_x + 100:
        ball_speed_y = -ball_speed_y
        
    for i in range(0, blocks_per_row):
        for j in range(0, len(block_colors)):
            # supprime le seul block toucher et pas toute la rangée en sortant de la boucle
            if ball_y + ball_radius > j * (block_size + block_spacing) and ball_y + ball_radius < j * (block_size + block_spacing) + 20 and ball_x + ball_radius > i * (block_size + block_spacing) and ball_x - ball_radius < i * (block_size + block_spacing) + block_size:
                ball_speed_y = -ball_speed_y
                break
            x = i * (block_size + block_spacing)
            y = j * (block_size + block_spacing)
                

        
# si la ball touche le bas de l'écran
    if ball_y + ball_radius > screen_height:
            pygame.quit()        

    # Afficher la balle
    pygame.draw.circle(screen, (0, 0, 0), (int(ball_x), int(ball_y)), 5)


    screen.blit(platbb_img, (platbb_x, platbb_y))

    cv2.imshow('frame', resized_frame)

    cv2.moveWindow('frame', 0, 0)

    # Rafraîchir l'écran
    pygame.display.flip()

    # Attendre une touche pour quitter
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            cap.release()
            cv2.destroyAllWindows()
            exit()