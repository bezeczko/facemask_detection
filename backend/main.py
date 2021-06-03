from fastapi import FastAPI, File, UploadFile
import shutil
from fastapi.middleware.cors import CORSMiddleware
import os
import random
import string

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
    return {
        "name": rnd_name,
        "suffix": file_suffix
        }

# @app.post("/movie/")
# async def movie(file: UploadFile = File(...)):
#     with open