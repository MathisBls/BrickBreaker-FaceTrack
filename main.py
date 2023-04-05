import pygame
import cv2

# Initialisation de Pygame
pygame.init()

# Taille de l'écran
screen_width = 800
screen_height = 600

# Chargement de l'image de l'objet principal
platbb_img = pygame.image.load('images/platbb.png')

# Position initiale de l'objet principal
platbb_x = screen_width / 2
platbb_y = screen_height / 2

# Allumer la caméra
cap = cv2.VideoCapture(0)

# Charger le fichier XML contenant les informations sur les visages
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

# Initialisation de la fenêtre Pygame
screen = pygame.display.set_mode((screen_width, screen_height))

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
            platbb_x += 5
        else:
            platbb_x -= 5

    # Afficher l'image de l'objet principal sur l'écran
    screen.blit(platbb_img, (platbb_x, platbb_y))

    # Afficher avec cv2 l'image redimensionnée de la caméra
    cv2.imshow('frame', resized_frame)

    # Mettre la caméra en petit en haut à gauche
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