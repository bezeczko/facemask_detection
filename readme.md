# Facemask detection using OpenCV

Program containing user interface (web) and API which allow to process image, video or webcam feed in order to recognize faces on each frame and distinguish whether detected face is wearing facemask or not. 

User interface is built (being build) using simple JavaScript/jQuery. For API I'm using here FastAPI which helps me build API without wasting time. 

Processing of data will be done using OpenCV 2 in Python.

---

## Requirements
- fastapi
- cv2

---

## Using
Run below command in the ***/server*** folder:
```
uvicorn server:app --reload
```
User interface can be accessed by accessing ***localhost:8000***

---

## Dataset
Dataset used for training model was obtained from:
```
https://github.com/chandrikadeb7/Face-Mask-Detection/tree/master/dataset
```
based on MIT license.

---