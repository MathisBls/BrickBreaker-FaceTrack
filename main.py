import cv2

# allumer la caméra
cap = cv2.VideoCapture(0)

# initialiser le détecteur de visage
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# initialiser le tracker de visage
tracker = cv2.TrackerCSRT_create()

# variables de suivi de visage
face_tracked = False
face_bbox = None

while True:
    # capturer une image de la caméra
    ret, frame = cap.read()

    # convertir en niveaux de gris
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # si le visage n'est pas encore suivi, détecter le visage
    if not face_tracked:
        faces = face_cascade.detectMultiScale(gray, 1.3, 5) #1.3 = scale factor, 5 = min neighbors

        # si un visage est détecté, initialiser le tracker
        if len(faces) > 0:
            face_bbox = tuple(faces[0])
            face_tracked = tracker.init(frame, face_bbox)

    # si le visage est suivi, mettre à jour la position
    if face_tracked:
        success, bbox = tracker.update(frame)
        if success:
            face_bbox = tuple(map(int, bbox))
        else:
            face_tracked = False

    # dessiner le rectangle autour du visage
    if face_bbox is not None:
        cv2.rectangle(frame, face_bbox[:2], (face_bbox[0] + face_bbox[2], face_bbox[1] + face_bbox[3]), (255,0,0), 2)

    # afficher la vidéo
    cv2.imshow('frame',frame)

    # arrêter la boucle si la touche 'q' est pressée
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# fermer la fenêtre de la vidéo
cap.release()
cv2.destroyAllWindows()
