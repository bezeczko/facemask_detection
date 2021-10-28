import cv2
import tensorflow as tf
from tensorflow import keras
import os

print(os.getcwd())

# Wczytanie wcześniej wyszkolonego modelu
model = keras.models.load_model('saved_model')

# Czcionka dla napisów w wideo
font = cv2.FONT_HERSHEY_COMPLEX_SMALL

# Wczytanie kaskady
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Przechwytywanie wideo
cap = cv2.VideoCapture('video.mp4')
print(type(cap))
# Parametry pliku wejściowego, które zostaną wykorzystane
# do stworzenia pliku wyjściowego
cap_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
cap_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
cap_fps = cap.get(cv2.CAP_PROP_FPS)
fourcc = cv2.VideoWriter_fourcc('m','p','4','v')

# Plik wyjściowy
out = cv2.VideoWriter('output.mp4', fourcc, cap_fps, (int(cap_width), int(cap_height)))

while (cap.isOpened()):

    ret, frame = cap.read()

    if ret == True:
        # Changing to grayscale so haarcascade can do its job
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detecting faces using haarcascade
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(60, 60), flags=cv2.CASCADE_SCALE_IMAGE)
        
        for (x, y, w, h) in faces:

            # Checking if values are not exceeding dimensions of the frame
            if (y-40) > 0:
                y0 = y-40    
            else:
                y0 = 0
            
            if (y+h+40) < frame.shape[0]:
                y1 = y+h+40  
            else:
                y1 = frame.shape[0]

            if (x-20) > 0:
                x0 = x-20
            else:
                x0 = 0

            if (x+w+20) < frame.shape[1]:
                x1 = x+w+20 
            else:
                x1 = frame.shape[1]

            # Preparing detected face to be predicted by the model:
            # - we're cutting face from the frame
            # - then we're changing color space from BGR to RGB
            # - and on the end we're resizing it to 140 x 140 (model is prepared for such data)
            img_array = keras.preprocessing.image.img_to_array(cv2.resize(cv2.cvtColor(frame[y0:y1, x0:x1], cv2.COLOR_BGR2RGB),(140,140)))
            img_array = tf.expand_dims(img_array, 0)

            print(type(img_array))
            print(img_array)
            
            # Checking the image
            predictions = model.predict(img_array)
            # Getting the score
            score = float(predictions[0])

            # Preparing text for the image
            predictions_text_1 = "{:.2f}% with mask".format(100 * (1 - score))
            predictions_text_2 = "{:.2f}% without mask".format(100 * score)

            # Checking if prediction for wearing a mask are more than 50%
            # If so green rectangle will be drawn and if not red one
            if score < 0.5:
                cv2.rectangle(frame, (x-20, y-40), (x+w+20, y+h+40), (0,255,0), 2)
            else:
                cv2.rectangle(frame, (x-20, y-40), (x+w+20, y+h+40), (0,0,255), 2)
            
            # Adding text with score of prediction
            cv2.putText(frame, predictions_text_1, (x, y+h+50), font, 1,(255,255,255),2,cv2.LINE_AA)
            cv2.putText(frame, predictions_text_2, (x, y+h+80), font, 1,(255,255,255),2,cv2.LINE_AA)

        out.write(frame)
    else:
        break

cap.release()
out.release()