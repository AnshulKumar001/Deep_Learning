# -*- coding: utf-8 -*-
"""Untitled4.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1XfDrWhQyW9LWKsM94Jy492tuSPtTaEqG
"""

from google.colab import drive
drive.mount('/content/drive')

!mkdir -p /content/data/train
!mkdir -p /content/data/test

!unzip "/content/drive/MyDrive/train.zip" -d "/content/data/train"
!unzip "/content/drive/MyDrive/test.zip" -d "/content/data/test"

import tensorflow as tf
from tensorflow import keras
from keras import Sequential
from keras.layers import Dense, Conv2D, MaxPooling2D, Flatten

train_ds=keras.utils.image_dataset_from_directory(
    directory='/content/data/train',
    labels='inferred',
    label_mode='int',
    batch_size=32,
    image_size=(256,256)
)

validation_ds=keras.utils.image_dataset_from_directory(
    directory='/content/data/test',
    labels='inferred',
    label_mode='int',
    batch_size=32,
    image_size=(256,256)
)

# Normalize
def process(image,label):
  image=tf.cast(image/255. ,tf.float32)
  return image,label

train_ds=train_ds.map(process)
validation_ds=validation_ds.map(process)

#CNN
model=Sequential()
model.add(Conv2D(32,kernel_size=(3,3),padding='valid',activation='relu',input_shape=(256,256,3)))
model.add(MaxPooling2D(pool_size=(2,2),strides=2,padding='valid'))

model.add(Conv2D(64,kernel_size=(3,3),padding='valid',activation='relu'))
model.add(MaxPooling2D(pool_size=(2,2),strides=2,padding='valid'))

model.add(Conv2D(128,kernel_size=(3,3),padding='valid',activation='relu'))
model.add(MaxPooling2D(pool_size=(2,2),strides=2,padding='valid'))

model.add(Flatten())

#ANN
model.add(Dense(128,activation='relu'))
model.add(Dense(64,activation='relu'))
model.add(Dense(1,activation='sigmoid'))

model.compile(optimizer='adam',loss='binary_crossentropy',metrics=['accuracy'])

model.fit(train_ds,steps_per_epoch=200,epochs=5,validation_data=validation_ds)

import cv2
import numpy as np

test_img=cv2.imread("/content/23.jpg")

test_img.shape

test_img=resize(test_img,(256,256))

from skimage.transform import resize

test_img = resize(test_img, (256, 256), anti_aliasing=True)

test_input=test_img.reshape((1,256,256,3))

model.predict(test_input)