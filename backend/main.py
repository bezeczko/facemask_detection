from fastapi import FastAPI, File, UploadFile
import shutil
from fastapi.middleware.cors import CORSMiddleware
import os
import random
import string
from starlette.responses import StreamingResponse
import cv2
import numpy as np
import base64

app = FastAPI()

origins = [
    'http://localhost',
    'http://127.0.0.1'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = ['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/image/")
async def image(file: UploadFile = File(...)):

    with open(file.filename, "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)
    rnd_name = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(8)])
    file_suffix = file.filename.split(".")[1]
    os.rename(file.filename, "Images/"+rnd_name+"."+file_suffix)
    
    if file_suffix == ".jpg":
        img = cv2.imread("Images/"+rnd_name+"."+file_suffix)
        cv2.imshow("test", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    elif file_suffix == ".mp4":
        cap = cv2.VideoCapture("Images/"+rnd_name+"."+file_suffix)
        faceCascade = cv2.CascadeClassifier("haarcascade_frontalface.xml")

        while True:
            _, img = cap.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(gray, 1.1, 4)
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
            if img is None:
                break

        cap.release()

    
    return {
        "name": rnd_name,
        "suffix": file_suffix
        }

# @app.post("/movie/")
# async def movie(file: UploadFile = File(...)):
#     with open