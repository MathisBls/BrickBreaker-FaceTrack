import cv2

# allumer la caméra
cap = cv2.VideoCapture(0)
x = 0
w = 0

# charger le fichier XML contenant les informations sur les visages
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
while True:
    # capturer une image depuis la caméra
    ret, frame = cap.read()

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

    # si ma tete va à gauche alors ca affiche gauche sinon ça affiche droite
    if x + w/2 < frame.shape[1] / 2:
        print('droite')
    else:
        print('gauche')
    # afficher l'image avec les rectangles
    cv2.imshow('frame',frame)

    # attendre une touche pour quitter
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# libérer la caméra et fermer toutes les fenêtres
cap.release()
cv2.destroyAllWindows()
