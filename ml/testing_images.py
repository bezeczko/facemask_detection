import tensorflow as tf
from tensorflow import keras
import matplotlib.pyplot as plt

image_size = (140, 140)

model = keras.models.load_model('C:/Users/jakub/Desktop/GitHub/facemask_detection/ml/saved_model')

img = keras.preprocessing.image.load_img(
    "C:/Users/jakub/Desktop/GitHub/facemask_detection/ml/test_images/test.png", target_size=image_size
)
img_array = keras.preprocessing.image.img_to_array(img)
img_array = tf.expand_dims(img_array, 0)  # Create batch axis

predictions = model.predict(img_array)
score = predictions[0]

print("This image is %.2f with mask and %.2f percent without mask." % (100 * (1 - score), 100 * score))