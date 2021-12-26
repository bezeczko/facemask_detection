import cv2
import tensorflow as tf
from tensorflow import keras
import numpy as np
from PIL import Image

# Loading model trained earlier
model = keras.models.load_model('saved_model.h5')

# Font for text on video
font = cv2.FONT_HERSHEY_COMPLEX_SMALL

# Cascade for detecting faces
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Capturing external camera
video_capture = cv2.VideoCapture(1, cv2.CAP_DSHOW)

while True:
    
    # Getting frame from webcam
    ret, frame = video_capture.read()

    # Changing to grayscale so haarcascade can do its job
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Detecting faces using haarcascade
    faces = face_cascade.detectMultiScale(gray,
                                          scaleFactor=1.1,
                                          minNeighbors=5,
                                          minSize=(60, 60),
                                          flags=cv2.CASCADE_SCALE_IMAGE)
    
    # For every detected face predictions are made to determine if face
    # has facemask on it or not. If it has facemask on then green rectangle
    # is drawn and if not red one.
    for (x, y, w, h) in faces:

        # Checking if values are not exceeding dimensions of the frame
        if (y-40) > 0:
            y0 = y-40    
        else:
            y0 = 0
        
        if (y+h+60) < frame.shape[0]:
            y1 = y+h+60  
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

        # # Checking the image
        predictions = model.predict(img_array)
        
        # # Getting the score
        score = float(predictions[0])
        # print("{:.2f}%".format(100*score))

        # # Preparing text for the image
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

    # Displaying a frame
    cv2.imshow("Facemask detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()