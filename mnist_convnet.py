# -*- coding: utf-8 -*-
"""mnist_convnet

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/gist/XavierT1/fb7db502551013f78cb1cb2ea3baaa1f/mnist_convnet.ipynb

# Simple MNIST convnet

**Author:** [fchollet](https://twitter.com/fchollet)<br>
**Date created:** 2015/06/19<br>
**Last modified:** 2020/04/21<br>
**Description:** A simple convnet that achieves ~99% test accuracy on MNIST.

## Setup
"""

import numpy as np
import keras
from keras import layers
from keras.callbacks import ModelCheckpoint

"""## Prepare the data"""

# Model / data parameters
num_classes = 10
input_shape = (28, 28, 1)

# Load the data and split it between train and test sets
(x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()

# Scale images to the [0, 1] range
x_train = x_train.astype("float32") / 255
x_test = x_test.astype("float32") / 255
# Make sure images have shape (28, 28, 1)
x_train = np.expand_dims(x_train, -1)
x_test = np.expand_dims(x_test, -1)
print("x_train shape:", x_train.shape)
print(x_train.shape[0], "train samples")
print(x_test.shape[0], "test samples")

# Convert class vectors to binary class matrices
y_train = keras.utils.to_categorical(y_train, num_classes)
y_test = keras.utils.to_categorical(y_test, num_classes)

"""## Build the model"""

model = keras.Sequential(
    [
        keras.Input(shape=input_shape),
        layers.Conv2D(32, kernel_size=(3, 3), activation="relu"),
        layers.MaxPooling2D(pool_size=(2, 2)),
        layers.Conv2D(64, kernel_size=(3, 3), activation="relu"),
        layers.MaxPooling2D(pool_size=(2, 2)),
        layers.Flatten(),
        layers.Dropout(0.5),
        layers.Dense(num_classes, activation="softmax"),
    ]
)

model.summary()

"""## Train the model"""

batch_size = 128
epochs = 15

checkpoint = ModelCheckpoint(
    filepath="model_checkpoint_{epoch:02d}.keras",  # Include epoch number in filename
    monitor="val_accuracy",
    save_best_only=False,             # Save model at each epoch, not just best
    mode="max",
    verbose=1
)

model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])

"""# Train the model with the checkpoint"""

import os
from tensorflow import keras

# Find latest checkpoint file
checkpoint_files = [f for f in os.listdir() if f.startswith("model_checkpoint_")]
if checkpoint_files:
    latest_checkpoint = max(checkpoint_files, key=os.path.getctime)
    initial_epoch = int(latest_checkpoint[17:19])  # Extract epoch number from filename
    model = keras.models.load_model(latest_checkpoint)  # Load the model
    print(f"Resuming training from epoch {initial_epoch}")
else:
    initial_epoch = 0  # Start from epoch 0 if no checkpoint found

# ... (rest of the code)

model.fit(
    x_train, y_train,
    batch_size=batch_size,
    epochs=epochs,
    initial_epoch=initial_epoch,  # Specify starting epoch for training
    validation_split=0.1,
    callbacks=[checkpoint]
)

"""## Evaluate the trained model"""

# Save the model with the correct file extension
model.save("model_checkpoint.h5")

# Evaluate the trained model
score = model.evaluate(x_test, y_test, verbose=0)
print("Test loss:", score[0])
print("Test accuracy:", score[1])

# (Optional) Download the saved model if using Colab
from google.colab import files
files.download("model_checkpoint.h5")

from tensorflow import keras

# Carga el modelo
modelo_cargado = keras.models.load_model("model_checkpoint.h5")

# Compila el modelo nuevamente
modelo_cargado.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])

# Ahora puedes evaluar el modelo sin la advertencia
score = modelo_cargado.evaluate(x_test, y_test, verbose=0)
print("Test loss:", score[0])
print("Test accuracy:", score[1])

"""#Montaje de unidad de disco de Google Drive"""

from google.colab import drive

# 1. Mount Google Drive
drive.mount('/content/drive')

# 2. Define paths (adapt to your specific folder structure)
ruta_raiz = '/content/drive/MyDrive/Colab Notebooks/CLASES/VisionComputacional/'  # Base path on your Drive

ruta_train_set = ruta_raiz + 'DATASETS/MNIST/trainingSet/trainingSet/2/*.jpg'
ruta_test_set = ruta_raiz + 'DATASETS/MNIST/testSet/testSet/*.jpg'
ruta_train_data = ruta_raiz + 'DATASETS/MNIST/trainingSet/trainingSet'
ruta_test_data = ruta_raiz + 'DATASETS/MNIST/Validation'
ruta_save_model = ruta_raiz + 'modelo/'  # Where to save the model
ruta_load_image = ruta_raiz + 'imagenes/'

# ... (your model training code) ...

# 3. Save the model to Google Drive
model.save(ruta_save_model + 'model_checkpoint.h5')
print(f"Modelo guardado en: {ruta_save_model + 'model_checkpoint.h5'}")

from google.colab import drive
from tensorflow import keras

# 1. Mount Google Drive (if not already mounted)
drive.mount('/content/drive')

# 2. Define the path to your saved model (using ruta_raiz or the full path)
ruta_raiz = '/content/drive/MyDrive/Colab Notebooks/CLASES/VisionComputacional/'  # Your base path
ruta_modelo = ruta_raiz + 'modelo/model_checkpoint.h5'  # Path to the saved model

modelo_cargado = keras.models.load_model(ruta_modelo)
modelo_cargado.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])
score = modelo_cargado.evaluate(x_test, y_test, verbose=0)
print("Test loss:", score[0])
print("Test accuracy:", score[1])

# Now you can use 'modelo_cargado' for further tasks